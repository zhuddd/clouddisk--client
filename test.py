import json
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QUrl, QFile, QTimer
from PyQt5.QtNetwork import QNetworkRequest, QNetworkReply
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentIcon

from app.Common import config
from app.Common.DataSaver import dataSaver
from app.Common.MyFile import CheckFile, get_file_hash_file, convert_size
from app.Common.Status import Status
from app.Ui.UpDownItem import UpDownItem


class UploadItem(QtWidgets.QWidget, UpDownItem):
    success = pyqtSignal(dict)
    delete = pyqtSignal(dict)

    def __init__(self, path, f_id, uid, success=False, parent=None):
        """
        :param path: 文件路径
        :param f_id: 文件id
        :param uid: 上传组件id
        """
        super().__init__(parent)
        self.check = None
        self.setupUi(self)
        self.file_path = Path(path)
        self.file_name = self.file_path.name
        self.f_id = f_id
        self.uid = uid
        self.reply = None
        self.hash = None
        self.checkhash = None
        self.start_byte = None
        self.uploaded = 0
        self.size_last = 0
        self.total_size = 0
        self.chunk_size = 1024 * 1024*100
        self.chunk_hash = None
        self.statu=Status.NOT_STARTED
        self.manager = dataSaver.QNetworkAccessManager_cookies()
        self.manager.finished.connect(self.onfinish)
        self.file=QFile(str(self.file_path))
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_upload_speed)
        self.init_btn()
        self.checkFile()
    def init_btn(self):
        self.progress.setMaximum(1000)
        self.name.setText(self.file_name)
        self.stop_btn.setIcon(FluentIcon.PAUSE_BOLD)
        self.stop_btn.clicked.connect(self.pause)
        self.start_btn.setIcon(FluentIcon.PLAY_SOLID)
        self.start_btn.clicked.connect(self.start)
        self.re_btn.setIcon(FluentIcon.SYNC)
        self.re_btn.clicked.connect(self.start)
        self.close_btn.setIcon(FluentIcon.CLOSE)
        self.close_btn.clicked.connect(self.close_upload)

        self.stop_btn.hide()
        self.re_btn.hide()

    def checkFile(self):
        if self.check is not None and self.check.isRunning():
            return
        self.stop_btn.setEnabled(False)
        self.check = CheckFile(self.file_path)
        self.check.hashes.connect(self.checkSuccess)
        self.check.start()
        self.info.setText("正在检查文件")

    def checkSuccess(self, hashes):
        self.hash = hashes[0]
        self.checkhash = hashes[1]
        self.total_size = self.file_path.stat().st_size
        self.stop_btn.setEnabled(True)
        self.info.setText("文件检查完成")
        if self.statu == Status.RUNNING:
            self.start()

    def newQNetworkRequest(self):
        r = QNetworkRequest(QUrl(str(config.FILE_UPLOAD)))
        r.setHeader(QNetworkRequest.ContentTypeHeader, "application/octet-stream")
        r.setRawHeader(b"size", f"{self.total_size}".encode())
        r.setRawHeader(b"hash", f"{self.hash}".encode())
        r.setRawHeader(b"checkhash", f"{self.checkhash}".encode())
        r.setRawHeader(b"fid", f"{self.f_id}".encode())
        r.setRawHeader(b"startbyte", f"{self.start_byte}".encode())
        r.setRawHeader(b"chunkhash", f"{self.chunk_hash}".encode())
        return r

    def start(self):
        self.statu = Status.RUNNING
        self.stop_btn.show()
        self.start_btn.hide()
        self.re_btn.hide()
        if self.hash is None or self.checkhash is None:
            self.checkFile()
            return
        if self.start_byte is None:
            self.info.setText("正在查找断点")
            self.reply=self.manager.post(self.newQNetworkRequest(), None)
            self.reply.uploadProgress.connect(self.uploadProgress)
        else:
            self.file.open(QFile.ReadOnly)
            self.file.seek(self.start_byte)
            chunk=self.file.read(self.chunk_size)
            self.file.close()
            self.chunk_hash=get_file_hash_file(chunk)
            self.reply=self.manager.post(self.newQNetworkRequest(), chunk)
            self.reply.uploadProgress.connect(self.uploadProgress)
            if not self.timer.isActive():
                self.timer.start(1000)

    def pause(self):
        if self.statu != Status.RUNNING:
            return
        if self.reply:
            self.statu = Status.PAUSED
            self.reply.abort()
            self.reply = None
            self.timer.stop()

    def close_upload(self):
        if self.reply:
            self.reply.abort()
            self.reply = None
        self.delete.emit({"uid": self.uid, "path": str(self.file_path), "id": self.f_id})
        self.close()

    def update_upload_speed(self):
        speed = convert_size(self.uploaded - self.size_last)
        self.size_last = self.uploaded
        self.info.setText(f"{speed[0]} {speed[1]}/S")

    def uploadProgress(self, bytesSent, bytesTotal):
        if self.total_size <=0:
            return
        self.uploaded = self.start_byte + bytesSent
        self.progress.setValue(int(self.uploaded / self.total_size * 1000))
        self.progres_text.setText(f"{self.uploaded / self.total_size:.2%}")

    def onfinish(self, reply:QNetworkReply):
        self.timer.stop()
        if self.statu == Status.PAUSED:
            self.info.setText("已暂停")
            self.start_btn.show()
            self.stop_btn.hide()
            return
        data=reply.readAll().data()
        if reply.error() == QNetworkReply.NoError:
            data=json.loads(data)['data']
            self.start_byte=data["upload_size"]
            self.info.setText(data["message"])
            if data["next"]:
                self.start()
            else:
                self.timer.stop()
                self.statu=Status.SUCCESS
                self.success.emit({"uid": self.uid, "path": str(self.file_path), "id": self.f_id})
                self.close()
        else:
            try:
                data=json.loads(data)
                self.info.setText(data["data"])
            except:
                self.info.setText("上传失败")
            self.hash = None
            self.checkhash = None
            self.start_byte = None
            self.re_btn.show()
            self.stop_btn.hide()
            self.start_btn.hide()
            self.statu = Status.ERROR



if __name__ == "__main__":
    app = QApplication([])
    uploader = UploadItem("D:\Desktop\工具\win.iso", 782, "123")
    uploader.show()
    app.exec_()
