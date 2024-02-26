import os
import pathlib
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from qfluentwidgets import FluentIcon

from Common.MyFile import convert_size
from Common.config import FILE_DOWNLOAD
from Ui.UpDownItem import UpDownItem
from Common.MyRequests import ResumableDownloader


class DownloadItem(QtWidgets.QWidget, UpDownItem):
    success = pyqtSignal(dict)
    delete = pyqtSignal(dict)

    def __init__(self, path, f_id, uid, success=False, parent=None):
        """
        :param path: 保存路径,包含文件名
        :param f_id: 文件id
        state -1:下载错误 0:未开始 1:下载中 2:暂停 3:下载完成 4:等待中
        """
        super().__init__(parent)
        self.req = None
        self.setupUi(self)
        self.path = pathlib.Path(path)
        self.f_id = f_id
        self.uid = uid
        self.is_success = False

        self.state = 0

        self.size_now = 0
        self.size_last = 0
        self.time_last = time.time()

        self.init_slot()
        self.init_btn()
        self.set_file_name()
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
        self.start_btn.clicked.connect(self.click_start)
        self.stop_btn.clicked.connect(self.click_stop)
        self.re_btn.clicked.connect(self.re)
        self.close_btn.clicked.connect(self.click_close)

    def start(self):
        if self.state == 1:
            return
        self.init_request()

    def stop(self):
        self.click_stop()

    def setWait(self):
        self.state = 4
        self.info.setText("等待中...")
        self.start_btn.hide()
        self.stop_btn.show()
        self.stop_btn.setEnabled(True)
        self.re_btn.hide()
        self.progress.setValue(0)
        self.progres_text.setText("0.0%")

    def click_start(self):
        if self.is_success:
            os.system(f"explorer /select , {self.path}")
        else:
            self.init_request()

    def click_stop(self):
        if self.req is not None:
            self.req.set_stop()
        else:
            self.on_stop()

    def re(self):
        self.init_request()

    def click_close(self):
        self.click_stop()
        self.delete.emit({"uid": self.uid, "path": str(self.path), "f_id": self.f_id})
        super().close()

    def on_finish(self):
        self.info.setText("下载成功")
        self.set_progress((100, 100))
        self.is_success = True
        self.start_btn.setIcon(FluentIcon.FOLDER)
        if not self.path.exists():
            self.start_btn.hide()
        else:
            self.start_btn.show()
        self.stop_btn.hide()
        self.re_btn.hide()
        self.success.emit({"uid": self.uid, "path": str(self.path), "f_id": self.f_id})
        if self.state != 0:
            self.close()
        self.state = 3

    def set_file_name(self, name=None):
        if name is None:
            self.name.setText(self.path.name)
        else:
            self.name.setText(name)
            self.path = self.path.parent / name

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
        if t == 0:
            return
        speed = convert_size(s / t)
        self.info.setText(f"{speed[0]} {speed[1]}/S")

    def on_stop(self):
        self.info.setText("已暂停")
        self.start_btn.show()
        self.stop_btn.hide()
        self.re_btn.hide()
        self.state = 2

    def on_error(self, data):
        self.info.setText(data)
        self.start_btn.hide()
        self.stop_btn.hide()
        self.re_btn.show()
        self.state = -1

    def on_start(self):
        self.info.setText("下载中")
        self.start_btn.hide()
        self.stop_btn.show()
        self.re_btn.hide()
        self.state = 1

    def init_request(self):
        self.req = ResumableDownloader(FILE_DOWNLOAD, self.path.parent, f_id=self.f_id, uid=self.uid)
        self.req.set_file_name.connect(self.set_file_name)
        self.req.progress.connect(self.set_progress)
        self.req.finish.connect(self.on_finish)
        self.req.error.connect(self.on_error)
        self.req.stop.connect(self.on_stop)
        self.req.start()
        self.on_start()
        self.state = 1
