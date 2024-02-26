from pathlib import Path
from uuid import uuid1

import requests
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTimer, QThread
from qfluentwidgets import FluentIcon


from app.Common.DataSaver import dataSaver
from app.Common.StyleSheet import StyleSheet
from app.Common.Tost import error
from app.Common.config import cfg, FILE_DOWNLOAD_TREE
from app.Ui.UpDown import UpDown
from app.components.DownloadItem import DownloadItem


class DownloadPage(QtWidgets.QWidget, UpDown):
    taskNum = QtCore.pyqtSignal(int)

    def __init__(self, text, *args, **kwargs):
        super(DownloadPage, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))
        StyleSheet.DOWNLOAD.apply(self)
        self.task_wait = []
        self.task_success = []
        self.controller = DownLoad(self)
        self.controller.creatItem.connect(self.create_download_item)
        self.controller.taskNum.connect(self.taskNum.emit)

        self.max_thread.setValue(dataSaver.get("download_max_thread", 5))
        self.toolBox.addItem(routeKey="Play", onClick=self.controkkerRun, icon=FluentIcon.PLAY_SOLID)
        self.toolBox.addItem(routeKey="Stop", onClick=self.controllerStop, icon=FluentIcon.PAUSE_BOLD)

        self.circulate = QTimer()
        self.circulate.timeout.connect(lambda: self.controller.setMax(self.max_thread.value()))
        self.circulate.timeout.connect(self.controller.start)
        self.circulate.start(1000)
        self.get_history()

    def controkkerRun(self):
        self.controller.setRun(True)

    def controllerStop(self):
        self.controller.setRun(False)

    def addTask(self, f_id):
        self.controller.new_task(f_id)

    def create_download_item(self, data: dict, success=False):
        """
        创建上传item,并添加到布局中,未完成的添加到上传控制器中
        :param data:  {"uid": uid, "path": path, "id": id}
        :param success:  是否上传成功
        :return:
        """
        item = DownloadItem(path=data["path"], f_id=data["f_id"], uid=data["uid"], success=success, parent=self)
        item.delete.connect(self.delete_history)
        if success:
            self.success_item_box.insertWidget(0, item)
            self.task_success.append(data.copy())
        else:
            item.success.connect(self.set_success)
            self.items_box.addWidget(item)
            self.task_wait.append(data.copy())
            data["item"] = item
            self.controller.addDownloadItem(data)
        self.save_history()

    def save_history(self):
        dataSaver.set(f"download_task_wait{dataSaver.get('user')}", self.task_wait)
        dataSaver.set(f"download_task_success{dataSaver.get('user')}", self.task_success)

    def get_history(self):
        task_wait = dataSaver.get(f"download_task_wait{dataSaver.get('user')}", [])
        task_success = dataSaver.get(f"download_task_success{dataSaver.get('user')}", [])
        for i in task_wait:
            self.create_download_item(i)
        for i in task_success:
            self.create_download_item(i, True)

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
        self.create_download_item(data, True)


class DownLoad(QThread):
    """
    下载控制器
    """
    creatItem = QtCore.pyqtSignal(dict)
    taskNum = QtCore.pyqtSignal(int)

    def __init__(self, parent: DownloadPage):
        super().__init__()
        self.p = parent
        self._run = False
        self._max = 5
        self.wait_list = []
        self.item_list = []

    def setMax(self, num: int):
        self._max = num
        dataSaver.set("download_max_thread", num)

    def setRun(self, run: bool):
        self._run = run
        for i in self.item_list:
            if not run:
                i["item"].stop()
            elif run and i["item"].state in (-1, 0, 2):
                i["item"].setWait()

    def new_task(self, f_id):
        self.get_tree(f_id)

    def get_tree(self, f_id):
        try:
            url = FILE_DOWNLOAD_TREE
            req = requests.post(url,
                                data={"file_id": f_id},
                                cookies=dataSaver.get("cookie")
                                )
            new_list = req.json()
            if new_list["status"]:
                tree = new_list["data"]
                file_list = self.init_task_list(tree)
                self.wait_list.extend(file_list)
            else:
                error(self.p.parent().parent(), new_list["data"])
        except:
            error(self.p.parent().parent(), "任务创建失败")

    def init_task_list(self, tree: dict, download_dir: Path = None):
        file_list = []
        if download_dir is None:
            download_dir = Path(cfg.get(cfg.downloadFolder))
        if tree["is_folder"]:
            children = tree.get("children")
            if children is not None:
                for i in children:
                    l = self.init_task_list(i, download_dir / tree["file_name"])
                    file_list.extend(l)
        else:
            file_list.append({"uid": uuid1().hex, "f_id": tree["Id"], "path": str(download_dir / tree["file_name"])})

        return file_list

    def creat_item(self):
        while len(self.wait_list) > 0:
            item = self.wait_list.pop(0)
            self.creatItem.emit(item)

    def addDownloadItem(self, item: dict):
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
