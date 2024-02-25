import json

import requests
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTimer
from qfluentwidgets import FluentIcon as FIF

from Common.DataSaver import dataSaver
from Common.MyFile import *
from Common.StyleSheet import StyleSheet
from Common.Tost import error
from Common.config import FILE_UPLOAD_DIR
from Ui.UpDown import UpDown
from components.UploadItem import UploadItem


class UploadPage(QtWidgets.QWidget, UpDown):
    taskNum = QtCore.pyqtSignal(int)
    update = QtCore.pyqtSignal()

    def __init__(self, text, *args, **kwargs):
        super(UploadPage, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))
        StyleSheet.UPLOAD.apply(self)
        self.task_wait = []
        self.task_success = []
        self.controller = UpLoad(self)
        self.controller.creatItem.connect(self.create_upload_item)
        self.controller.update.connect(lambda: self.update.emit())
        self.controller.taskNum.connect(self.taskNum.emit)

        self.max_thread.setValue(dataSaver.get("upload_max_thread", 5))
        self.toolBox.addItem(routeKey="Play", onClick=self.controkkerRun, icon=FIF.PLAY_SOLID)
        self.toolBox.addItem(routeKey="Stop", onClick=self.controllerStop, icon=FIF.PAUSE_BOLD)

        self.circulate = QTimer()
        self.circulate.timeout.connect(lambda: self.controller.setMax(self.max_thread.value()))
        self.circulate.timeout.connect(self.controller.start)
        self.circulate.start(1000)
        self.get_history()

    def controkkerRun(self):
        self.controller.setRun(True)

    def controllerStop(self):
        self.controller.setRun(False)

    def addTask(self, path):
        self.controller.new_task(path[0], path[1])

    def create_upload_item(self, data: dict, success=False):
        """
        创建上传item,并添加到布局中,未完成的添加到上传控制器中
        :param data:  {"uid": uid, "path": path, "id": id}
        :param success:  是否上传成功
        :return:
        """
        item = UploadItem(path=data["path"], f_id=data["id"], uid=data["uid"], success=success, parent=self)
        item.delete.connect(self.delete_history)
        if success:
            self.success_item_box.insertWidget(0, item)
            self.task_success.append(data.copy())
        else:
            item.success.connect(self.set_success)
            self.items_box.addWidget(item)
            self.task_wait.append(data.copy())
            data["item"] = item
            self.controller.addUploadItem(data)
        self.save_history()

    def save_history(self):
        dataSaver.set(f"upload_task_wait{dataSaver.get('user')}", self.task_wait)
        dataSaver.set(f"upload_task_success{dataSaver.get('user')}", self.task_success)

    def get_history(self):
        task_wait = dataSaver.get(f"upload_task_wait{dataSaver.get('user')}", [])
        task_success = dataSaver.get(f"upload_task_success{dataSaver.get('user')}", [])
        for i in task_wait:
            self.create_upload_item(i)
        for i in task_success:
            self.create_upload_item(i, True)

    def delete_history(self, data: dict, all=False):
        if all:
            self.task_wait = []
            self.task_success = []
        else:
            uid = data["uid"]
            for i in range(len(self.task_wait)):
                if self.task_wait[i]["uid"] == uid:
                    self.task_wait.pop(i)
                    break
            for i in range(len(self.task_success)):
                if self.task_success[i]["uid"] == uid:
                    self.task_success.pop(i)
                    break
        self.save_history()

    def set_success(self, data: dict):
        for i in range(len(self.task_wait)):
            if self.task_wait[i]["uid"] == data["uid"]:
                self.task_wait.pop(i)
                break
        self.create_upload_item(data, True)


class UpLoad(QThread):
    """
    文件上传控制器
    """
    creatItem = QtCore.pyqtSignal(dict)
    update = QtCore.pyqtSignal()
    taskNum = QtCore.pyqtSignal(int)

    def __init__(self, parent: UploadPage):
        super().__init__()
        self.p = parent
        self._run = False
        self._max = 5
        self.wait_list = []
        self.item_list = []

    def setMax(self, num: int):
        self._max = num
        dataSaver.set("upload_max_thread", num)

    def setRun(self, run: bool):
        self._run = run
        for i in self.item_list:
            if not run:
                i["item"].stop()
            elif run and i["item"].state in (-1, 0, 2):
                i["item"].setWait()

    def new_task(self, path, p):
        tree, path_list = create_tree(path)
        if len(path_list) >= 200:
            error(self.p.parent().parent(), "文件数量过多")
            return
        self.upload_tree(tree, path_list, p)

    def upload_tree(self, tree, path_list: dict, p):
        try:
            new_list = requests.post(FILE_UPLOAD_DIR,
                                     data={"p": p, "tree": json.dumps(tree)},
                                     cookies=dataSaver.get("cookie")
                                     ).json()
            if new_list["status"]:
                id_kv = new_list["data"]
                for i in path_list.keys():
                    path = path_list.get(i)
                    fid = id_kv.get(i)
                    if fid is None or path is None:
                        continue
                    self.wait_list.append({"uid": i, "path": path_list[i], "id": id_kv[i]})
            else:
                error(self.p.parent().parent(), new_list["data"])
            self.update.emit()
        except:
            error(self.p.parent().parent(), "上传失败")

    def creat_item(self):
        while len(self.wait_list) > 0:
            item = self.wait_list.pop(0)
            self.creatItem.emit(item)

    def addUploadItem(self, item: dict):
        self.item_list.append(item)
        item["item"].delete.connect(self.remove)
        item["item"].success.connect(self.remove)
        self.setRun(self._run)

    def remove(self, item: dict):
        for i in range(len(self.item_list)):
            if self.item_list[i]["uid"] == item["uid"]:
                self.item_list.pop(i)
                break

    def run(self):
        self.creat_item()
        num = self._max
        self.taskNum.emit(len(self.item_list))
        for i in self.item_list:
            if num <= 0 and self._run:
                break
            if i["item"].state == 1:
                num -= 1
                i["item"].set_speed()
                continue
            if i["item"].state == 4:
                if self._run:
                    i["item"].start()
                    num -= 1
