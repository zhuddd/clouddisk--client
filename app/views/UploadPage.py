import json

from PyQt5 import QtCore, QtWidgets, QtNetwork
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtNetwork import QNetworkRequest
from qfluentwidgets import FluentIcon

from app.Common.DataSaver import dataSaver
from app.Common.MyFile import create_tree
from app.Common.Status import Status
from app.Common.StyleSheet import StyleSheet
from app.Common.Tost import error
from app.Common.config import FILE_UPLOAD_DIR
from app.Ui.UpDown import UpDown
from app.components.UploadItem import UploadItem


class UploadPage(QtWidgets.QWidget, UpDown):
    taskNum = QtCore.pyqtSignal(int)
    update = QtCore.pyqtSignal()

    def __init__(self, text, *args, **kwargs):
        super(UploadPage, self).__init__(*args, **kwargs)
        self.path_list = {}
        self._run = True
        self.reply = None
        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))
        StyleSheet.UPLOAD.apply(self)
        self.task_wait = []
        self.task_success = []
        self.uploadItems = {}  # type:dict[str,UploadItem]

        self.max_thread.setValue(dataSaver.get("upload_max_thread", 5))
        self.max_thread.valueChanged.connect(lambda x: dataSaver.set("upload_max_thread", x))
        self.toolBox.addItem(routeKey="Play", onClick=self.allRun, icon=FluentIcon.PLAY_SOLID)
        self.toolBox.addItem(routeKey="Stop", onClick=self.allStop, icon=FluentIcon.PAUSE_BOLD)
        self.toolBox.setCurrentItem("Play")

        self.manager = dataSaver.QNetworkAccessManager_cookies()
        self.manager.finished.connect(self.setTreefinlish)
        self.circulate = QTimer()
        self.circulate.timeout.connect(self.start)
        self.get_history()
        self.allRun()

    def allRun(self):
        self._run = True
        for i in self.task_wait:
            uid = i["uid"]
            if self.uploadItems[uid].statu in (Status.WAITING, Status.NOT_STARTED, Status.PAUSED, Status.ERROR):
                self.uploadItems[uid].waitUpload()
        self.circulate.start(1000)

    def allStop(self):
        for i in self.task_wait:
            uid = i["uid"]
            if self.uploadItems[uid].statu in (Status.RUNNING, Status.WAITING):
                self.uploadItems[uid].pause()
        self._run = False
        self.circulate.stop()

    def start(self):
        n = self.max_thread.value()
        if len(self.task_wait) > 0:
            for i in self.task_wait:
                if n <= 0:
                    return
                uid = i["uid"]
                if self.uploadItems[uid].statu in (Status.NOT_STARTED, Status.WAITING):
                    self.uploadItems[uid].start()
                    n -= 1
                elif self.uploadItems[uid].statu == Status.RUNNING:
                    n -= 1

    def addTask(self, path):
        tree, path_list = create_tree(path[0])
        self.path_list.update(path_list)
        if len(self.path_list) >= 200:
            error(self.parent(), "文件数量过多")
            return
        data = QtCore.QByteArray()
        data.append(f"tree={json.dumps(tree)}&p={path[1]}")
        self.reply = self.manager.post(QNetworkRequest(QUrl(FILE_UPLOAD_DIR)), data)

    def setTreefinlish(self, req):
        er = req.error()
        if er == QtNetwork.QNetworkReply.NoError:
            self.update.emit()
            data = req.readAll().data()
            new_list = json.loads(data)['data']
            file_list = self.init_task_list(new_list)
            for i in file_list:
                self.create_upload_item(i)
        else:
            error(self.parent(), "任务创建失败")

    def init_task_list(self, new_list):
        r = []
        for i in new_list.keys():
            path=self.path_list.pop(i,None)
            if path is None:
                continue
            fid=new_list.get(i)
            r.append({"uid": i, "path": path, "f_id": fid})
        return r

    def create_upload_item(self, data: dict, success=False):
        """
        创建上传item,并添加到布局中,未完成的添加到上传控制器中
        :param data:  {"uid": uid, "path": path, "f_id": f_id}
        :param success:  是否上传成功
        :return:
        """
        item = UploadItem(path=data["path"], f_id=data["f_id"], uid=data["uid"], success=success, parent=self)
        item.delete.connect(self.delete_history)
        self.uploadItems[data["uid"]] = item
        if success:
            self.success_item_box.insertWidget(0, item)
            self.task_success.append(data.copy())
        else:
            item.success.connect(self.set_success)
            self.items_box.addWidget(item)
            self.task_wait.append(data.copy())
        self.save_history()

    def save_history(self):
        dataSaver.set(f"upload_task_wait{dataSaver.get('user')}", self.task_wait)
        dataSaver.set(f"upload_task_success{dataSaver.get('user')}", self.task_success)
        self.taskNum.emit(len(self.task_wait))

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
