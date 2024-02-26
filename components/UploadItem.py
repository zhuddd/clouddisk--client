import time
from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from qfluentwidgets import FluentIcon

from Common.DataSaver import dataSaver
from Common.MyFile import CheckFile, convert_size
from Common.config import FILE_UPLOAD_CHECK, FILE_UPLOAD
from Ui.UpDownItem import UpDownItem
from Common.MyRequests import MyRequestThread, ResumableUploader


class UploadItem(QtWidgets.QWidget, UpDownItem):
    success = pyqtSignal(dict)
    delete = pyqtSignal(dict)

    def __init__(self, path, f_id, uid, success=False, parent=None):
        """
        :param path: 文件路径
        :param f_id: 父文件夹id
        :param uid: 上传组件id
        """

        self.check_request = None
        self.state = 0
        '''state -1:上传错误 0:未开始 1:上传中 2:暂停 3:上传完成 4:等待中'''
        super().__init__(parent)
        self.request = None
        self.setupUi(self)
        self.path = Path(path)
        self.check_hash = None
        self.file_hash = None
        self.f_id = f_id
        self.uid = uid

        self.size_now = 0
        self.size_last = 0
        self.time_last = time.time()

        self.check = CheckFile(path)

        self.init_btn()
        self.init_slot()
        self.name.setText(self.path.name)
        if success:
            self.on_finish()

    def init_btn(self):
        self.progress.setMinimum(0)
        self.progress.setMaximum(10000)
        self.progress.setValue(0)
        self.stop_btn.setIcon(FluentIcon.PAUSE_BOLD)
        self.start_btn.setIcon(FluentIcon.PLAY_SOLID)
        self.re_btn.setIcon(FluentIcon.SYNC)
        self.close_btn.setIcon(FluentIcon.CLOSE)

        self.stop_btn.hide()
        self.re_btn.hide()

    def init_slot(self):
        self.check.hashes.connect(self.prepare_hash)
        self.start_btn.clicked.connect(self.start_btn_clicked)
        self.re_btn.clicked.connect(self.start_btn_clicked)
        self.close_btn.clicked.connect(self.click_close)
        self.stop_btn.clicked.connect(self.stop_btn_clicked)

    def start(self):
        self.start_btn_clicked()

    def stop(self):
        self.stop_btn_clicked()

    def setWait(self):
        self.state = 4
        self.info.setText("等待中...")
        self.start_btn.hide()
        self.stop_btn.show()
        self.stop_btn.setEnabled(True)
        self.re_btn.hide()
        self.progress.setValue(0)
        self.progres_text.setText("0.0%")

    def start_btn_clicked(self):
        if not self.path.exists():
            self.on_error("文件不存在")
            return
        self.check.start()
        self.on_start()

    def stop_btn_clicked(self):
        if self.state == 4:
            self.on_error("已取消")
            return
        else:
            self.stop_btn.setEnabled(False)
            if self.request is not None:
                self.request.set_stop()

    def on_start(self):
        self.info.setText("检查文件中...")
        self.start_btn.hide()
        self.stop_btn.show()
        self.stop_btn.setEnabled(False)
        self.re_btn.hide()
        self.progress.setValue(0)
        self.progres_text.setText("0.0%")
        self.state = 4

    def on_upload(self):
        self.info.setText("上传中...")
        self.start_btn.hide()
        self.stop_btn.show()
        self.stop_btn.setEnabled(True)
        self.re_btn.hide()
        self.state = 1

    def on_finish(self, msg=None):
        if msg is not None:
            self.info.setText(msg)
        self.start_btn.hide()
        self.stop_btn.hide()
        self.re_btn.hide()
        self.progress.setValue(10000)
        self.progres_text.setText("100%")
        self.info.setText("上传完成")
        self.success.emit({"uid": self.uid, "path": str(self.path), "id": self.f_id})
        if self.state != 0:
            self.close()
        self.state = 3

    def on_error(self, msg):
        self.info.setText(msg)
        self.start_btn.hide()
        self.stop_btn.hide()
        self.re_btn.show()
        self.re_btn.setEnabled(True)
        self.state = -1

    def on_stop(self):
        self.info.setText("上传暂停")
        self.start_btn.show()
        self.start_btn.setEnabled(True)
        self.stop_btn.hide()
        self.re_btn.hide()
        self.state = 2

    def prepare_hash(self, hashes):
        self.file_hash, self.check_hash = hashes
        self.upload_check()

    def click_close(self):
        self.delete.emit({"uid": self.uid, "path": str(self.path), "id": self.f_id})
        self.close()

    def set_progress(self, progress):
        self.size_now = progress[0]
        p = int(progress[0] / progress[1] * 10000)
        self.progress.setValue(max(p, 0))
        self.progres_text.setText(f"{p / 100:.2f}%")

    def set_speed(self):
        if self.state != 1:
            return
        s = self.size_now - self.size_last
        t = time.time() - self.time_last
        self.size_last = self.size_now
        self.time_last = time.time()
        speed = convert_size(s / t)
        self.info.setText(f"{speed[0]} {speed[1]}/S")

    def upload_check(self):
        self.check_request = MyRequestThread()
        self.check_request.post(
            url=FILE_UPLOAD_CHECK,
            data={"hash": self.file_hash,
                  "check_hash": self.check_hash,
                  "size": self.path.stat().st_size,
                  "f_id": self.f_id},
        )
        self.check_request.response.connect(self.check_response)
        self.check_request.start()

    def check_response(self, response):
        try:
            response = response.json()
            data = response["data"]
            if not response["status"]:
                self.on_error(data)
                return
            if data.get("state") == 1:
                self.on_finish("上传完成")
            elif data.get("state") in (2, 3):
                self.init_upload_request(data.get("start_byte", 0))
                self.on_upload()
            else:
                self.on_error("文件检查失败")
        except:
            self.on_error("文件检查失败")

    def init_upload_request(self, start_byte=0):
        auto_size = dataSaver.get("auto_size", True)
        self.request = ResumableUploader(
            url=FILE_UPLOAD,
            filepath=self.path,
            file_hash=self.file_hash,
            check_hash=self.check_hash,
            start_byte=start_byte,
            auto_size=auto_size,
        )
        self.request.progress.connect(self.set_progress)
        self.request.error.connect(self.on_error)
        self.request.finish.connect(self.upload_check)
        self.request.stop.connect(self.on_stop)
        self.state = 1
        self.request.start()
