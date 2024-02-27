import os
import pathlib

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QUrl, QTimer
from PyQt5.QtNetwork import QNetworkRequest
from qfluentwidgets import FluentIcon

from app.Common import config
from app.Common.DataSaver import dataSaver
from app.Common.MyFile import convert_size, CheckFile
from app.Common.Status import Status
from app.Ui.UpDownItem import UpDownItem


class DownloadItem(QtWidgets.QWidget, UpDownItem):
    success = pyqtSignal(dict)
    delete = pyqtSignal(dict)

    def __init__(self, path, f_id, uid, success=False, parent=None):
        """
        :param path: 保存路径,包含文件名
        :param f_id: 文件id
        """
        super().__init__(parent)
        self.setupUi(self)

        self.save_path = pathlib.Path(path).parent
        if not self.save_path.exists():
            self.save_path.mkdir(parents=True)
        self.file_path = pathlib.Path(path)
        self.f_id = f_id
        self.uid = uid
        self.check = None
        self.reply = None
        self.file = None
        self.md5 = None
        self.total_size = 0
        self.downloaded_size = 0
        self.download_speed = 0

        if success:
            self.setSuccess()
            return
        self.file_name = self.file_name_replace(pathlib.Path(path).name)
        self.tmp_file = pathlib.Path(f"{path}{uid}.tmp")
        self.statu = Status.NOT_STARTED
        self.name.setText(self.file_name)
        self.initBtn()

        self.url = QUrl(config.FILE_DOWNLOAD + f"?file_id={f_id}&Only_header={False}")
        self.manager = dataSaver.QNetworkAccessManager_cookies()
        self.manager.finished.connect(self.on_finished)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_download_speed)

    def initBtn(self):
        self.start_btn.clicked.connect(self.start_download)
        self.start_btn.setIcon(FluentIcon.PLAY_SOLID)
        self.stop_btn.clicked.connect(self.pause_download)
        self.stop_btn.setIcon(FluentIcon.PAUSE_BOLD)
        self.re_btn.setIcon(FluentIcon.SYNC)
        self.re_btn.clicked.connect(self.start_download)
        self.close_btn.setIcon(FluentIcon.CLOSE)
        self.close_btn.clicked.connect(self.close_download)
        self.stop_btn.hide()
        self.re_btn.hide()

    def setSuccess(self):
        self.file_name = pathlib.Path(self.file_path).name
        self.name.setText(self.file_name)
        self.statu = Status.SUCCESS
        self.info.setText("下载完成")
        self.progress.setValue(self.progress.maximum())
        if self.file_path.exists():
            self.start_btn.clicked.connect(lambda: os.system(f"explorer /select , {self.file_path}"))
            self.start_btn.setIcon(FluentIcon.FOLDER)
        else:
            self.start_btn.hide()
        self.stop_btn.hide()
        self.re_btn.hide()
        self.close_btn.setIcon(FluentIcon.CLOSE)
        self.close_btn.clicked.connect(self.close_download)

    def newQNetworkRequest(self):
        r = QNetworkRequest(self.url)
        r.setRawHeader(b"Range", f"bytes={self.downloaded_size}-".encode())
        return r

    def start_download(self, btn=True):
        self.stop_btn.show()
        self.start_btn.hide()
        self.re_btn.hide()
        if self.statu == Status.SUCCESS and btn:
            os.system(f"explorer /select , {self.file_path}")
        if self.statu == Status.DOWNLOADING:
            return
        if self.tmp_file.exists():
            self.file = open(self.tmp_file, "ab")
            self.downloaded_size = self.tmp_file.stat().st_size
        else:
            self.file = open(self.tmp_file, "wb")
        self.reply = self.manager.get(self.newQNetworkRequest())
        self.reply.readyRead.connect(self.on_ready_read)
        self.reply.downloadProgress.connect(self.on_download_progress)
        self.timer.start(500)
        self.statu = Status.DOWNLOADING

    def pause_download(self):
        if self.statu != Status.DOWNLOADING:
            return
        if self.reply:
            self.statu = Status.PAUSED
            self.reply.abort()
            self.reply = None
            self.file.close()
            self.timer.stop()

    def wait_download(self):
        self.statu = Status.WAITING
        self.stop_btn.hide()
        self.start_btn.show()
        self.re_btn.hide()
        self.info.setText("等待下载")

    def close_download(self):
        if self.reply:
            self.reply.abort()
            self.reply = None
        self.delete.emit({"uid": self.uid, "path": str(self.file_path), "f_id": self.f_id})
        self.close()

    def on_ready_read(self):
        if self.reply.attribute(QNetworkRequest.HttpStatusCodeAttribute) in [200, 206]:
            if not self.md5:
                self.md5 = self.reply.rawHeader(b"Hash").data().decode()
            data = self.reply.readAll()
            self.file.write(data)
            self.download_speed += len(data)

    def on_download_progress(self, bytesReceived, bytesTotal):
        if bytesTotal <= 0:
            return
        self.total_size = bytesTotal
        self.progress.setMaximum(self.downloaded_size + bytesTotal)
        self.progress.setValue(self.downloaded_size + bytesReceived)
        self.progres_text.setText(
            f"已下载: {(self.downloaded_size + bytesReceived) / (self.downloaded_size + bytesTotal) * 100:.2f}%")

    def update_download_speed(self):
        speed = convert_size(self.download_speed)
        self.info.setText(f"{speed[0]} {speed[1]}/S")
        self.download_speed = 0

    def file_name_replace(self, file_name):
        name = file_name
        t = 0
        while True:
            t += 1
            if self.save_path.joinpath(file_name).exists():
                if '.' in name:
                    a = len(name.split(".")[-1])
                    file_name = f"{name[:-a - 1]} ({t}).{name[-a:]}"
                else:
                    file_name = f"{name} ({t})"
            else:
                break
        return file_name

    def on_finished(self, repy):
        self.file.close()
        self.timer.stop()
        if self.statu == Status.PAUSED:
            self.info.setText("已暂停")
            self.start_btn.show()
            self.stop_btn.hide()
        elif self.statu == Status.DOWNLOADING:
            if repy.error() != 0:
                self.checkError()
                return
            self.check = CheckFile(self.tmp_file)
            self.check.hashes.connect(self.Check)
            self.check.start()

    def Check(self, hash):
        if hash[0] == self.md5:
            self.checkSuccess()
        else:
            self.checkError()

    def checkError(self):
        self.info.setText("下载失败")
        self.re_btn.show()
        self.stop_btn.hide()
        self.statu = Status.NOT_STARTED

    def checkSuccess(self):
        self.info.setText("下载完成")
        self.progress.setValue(self.progress.maximum())
        self.file_path = self.save_path / self.file_name_replace(self.file_name)
        self.name.setText(self.file_path.name)
        self.tmp_file.rename(self.file_path)
        self.statu = Status.SUCCESS
        self.success.emit({"uid": self.uid, "path": str(self.file_path), "f_id": self.f_id})
        self.close()
