import json
from pathlib import Path
from uuid import uuid1

from PyQt5 import QtCore, QtWidgets, QtNetwork
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtNetwork import QNetworkRequest
from qfluentwidgets import FluentIcon

from app.Common.DataSaver import dataSaver
from app.Common.Status import Status
from app.Common.StyleSheet import StyleSheet
from app.Common.Tost import error
from app.Common.config import cfg, FILE_DOWNLOAD_TREE
from app.Ui.UpDown import UpDown
from app.components.DownloadItem import DownloadItem


class DownloadPage(QtWidgets.QWidget, UpDown):
    taskNum = QtCore.pyqtSignal(int)

    def __init__(self, text, *args, **kwargs):
        super(DownloadPage, self).__init__(*args, **kwargs)
        self._run = True
        self.reply = None
        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))
        StyleSheet.DOWNLOAD.apply(self)
        self.task_wait = []
        self.task_success = []
        self.downloadItems = {}  # type:dict[str,DownloadItem]

        self.max_thread.setValue(dataSaver.get("download_max_thread", 5))
        self.max_thread.valueChanged.connect(lambda x: dataSaver.set("download_max_thread", x))
        self.toolBox.addItem(routeKey="Play", onClick=self.allRun, icon=FluentIcon.PLAY_SOLID)
        self.toolBox.addItem(routeKey="Stop", onClick=self.allStop, icon=FluentIcon.PAUSE_BOLD)
        self.toolBox.setCurrentItem("Play")

        self.manager = dataSaver.QNetworkAccessManager_cookies()
        self.manager.finished.connect(self.getTreefinlish)
        self.circulate = QTimer()
        self.circulate.timeout.connect(self.start)
        self.get_history()
        self.allRun()

    def allRun(self):
        self._run = True
        for i in self.task_wait:
            uid = i["uid"]
            if self.downloadItems[uid].statu in (Status.WAITING, Status.NOT_STARTED, Status.PAUSED, Status.ERROR):
                self.downloadItems[uid].wait_download()
        self.circulate.start(1000)

    def allStop(self):
        for i in self.task_wait:
            uid = i["uid"]
            if self.downloadItems[uid].statu in (Status.DOWNLOADING, Status.WAITING):
                self.downloadItems[uid].pause_download()
        self._run = False
        self.circulate.stop()

    def start(self):
        n = self.max_thread.value()
        if len(self.task_wait) > 0:
            for i in self.task_wait:
                if n <= 0:
                    return
                uid = i["uid"]
                if self.downloadItems[uid].statu in (Status.NOT_STARTED,Status.WAITING):
                    self.downloadItems[uid].start_download()
                    n -= 1
                elif self.downloadItems[uid].statu == Status.DOWNLOADING:
                    n -= 1

    def addTask(self, fid):
        data = QtCore.QByteArray()
        data.append(f"file_id={fid}")
        self.reply = self.manager.post(QNetworkRequest(QUrl(FILE_DOWNLOAD_TREE)), data)

    def getTreefinlish(self, req):
        er = req.error()
        if er == QtNetwork.QNetworkReply.NoError:
            data = req.readAll().data()
            tree = json.loads(data)
            file_list = self.init_task_list(tree["data"])
            for i in file_list:
                self.create_download_item(i)
        else:
            error(self.parent(), "任务创建失败")

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
            file_list.append(
                {"uid": uuid1().hex, "f_id": tree["Id"], "path": str(download_dir / tree["file_name"])})

        return file_list

    def create_download_item(self, data: dict, success=False):
        """
        创建上传item,并添加到布局中,未完成的添加到上传控制器中
        :param data:  {"uid": uid, "path": path, "id": id}
        :param success:  是否上传成功
        :return:
        """
        item = DownloadItem(path=data["path"], f_id=data["f_id"], uid=data["uid"], success=success, parent=self)
        item.delete.connect(self.delete_history)
        self.downloadItems[data["uid"]] = item
        if success:
            self.success_item_box.insertWidget(0, item)
            self.task_success.append(data.copy())
        else:
            item.success.connect(self.set_success)
            self.items_box.addWidget(item)
            self.task_wait.append(data.copy())
        self.save_history()

    def save_history(self):
        dataSaver.set(f"download_task_wait{dataSaver.get('user')}", self.task_wait)
        dataSaver.set(f"download_task_success{dataSaver.get('user')}", self.task_success)
        self.taskNum.emit(len(self.task_wait))

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
