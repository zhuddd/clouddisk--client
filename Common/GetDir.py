from typing import Union

from PyQt5.QtCore import QThread, pyqtSignal
from requests import Response

from Common.MyIcon import MyIcon
from Common.File import File
from Common.MyRequests import MyRequestThread
from Common.config import FILE_DIR


class SetIcon(QThread):
    signal = pyqtSignal(File)

    def __init__(self, data):
        super(SetIcon, self).__init__()
        self.data = data

    def run(self):
        """
        在发出信号之前遍历数据并修复与图标相关的信息。
        """
        try:
            # TODO:文件类型排序
            for i in self.data:
                f = File(i)
                f.icon = MyIcon(i["file_type"])
                self.signal.emit(f)
        except Exception as e:
            print(e)


class GetDir:
    def __init__(self, errFunc, updateFunc):
        self.request = None
        self.path = FILE_DIR
        self.set_icon = None
        self.errFunc = errFunc
        self.updateFunc = updateFunc

    def get_dir(self, msg: Union[str, int], find_type=False):
        '''
        获取文件列表
        :param msg: 文件夹id或者文件名(查找模式)
        :param find_type:  查找模式
        :return:
        '''
        try:
            if self.request is None or not self.request.isRunning():
                self.request = MyRequestThread()
                self.request.get(f"{self.path}/{1 if find_type else 0}/{msg}")
                self.request.response.connect(self.update_page_data)
                self.request.error.connect(self.errFunc)
                self.request.start()
        except Exception as e:
            print(e)

    def update_page_data(self, data: Response):
        """
        使用检索到的信息更新页面数据。
        """
        if data.status_code != 200:
            self.errFunc("Network Error")
            return None
        data = data.json()
        if not data["status"]:
            self.errFunc(data["data"])
            return None
        if self.set_icon is None or not self.set_icon.isRunning():
            self.set_icon = SetIcon(data["data"])
            self.set_icon.signal.connect(self.updateFunc)
            self.set_icon.start()
