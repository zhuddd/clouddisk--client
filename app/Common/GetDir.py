from typing import Union

import requests
from PyQt5.QtCore import QThread, pyqtSignal

from app.Common.DataSaver import dataSaver
from app.Common.MyIcon import MyIcon
from app.Common.File import File
from app.Common.config import FILE_DIR


class GetDir(QThread):
    """
    获取文件夹内文件列表
    """
    update = pyqtSignal(File)
    err = pyqtSignal(str)

    def __init__(self):
        super(GetDir, self).__init__()
        self.sortBy = 0
        self.msg = None
        self.find_type = None
        self.request = None
        self.path = FILE_DIR
        self.set_icon = None

    def get_dir(self, msg: Union[str, int], find_type=False, sortBy=0):
        '''
        获取文件列表
        :param msg: 文件夹id或者文件名(查找模式)
        :param find_type:  查找模式
        :param sortBy: 排序方式 0:默认 1:名称升序 2:名称降序 3:类型升序 4:类型降序 5:时间升序 6:时间降序
        :return:
        '''
        self.msg = msg
        self.find_type = find_type
        self.sortBy = sortBy
        self.start()

    def run(self):
        req = requests.get(f"{self.path}/{1 if self.find_type else 0}/{self.msg}", cookies=dataSaver.get("cookies"))
        if req.status_code != 200:
            self.err.emit("网络错误")
            return None
        data = req.json()
        if not data["status"]:
            self.err.emit(data["data"])
            return None
        file_list = [File(i) for i in data["data"]]

        if self.sortBy == 1:
            # 按名称升序排列
            file_list.sort(key=lambda x: x.name)
        elif self.sortBy == 2:
            # 按名称降序排列
            file_list.sort(key=lambda x: x.name, reverse=True)
        elif self.sortBy == 3:
            # 按类型升序排列
            file_list.sort(key=lambda x: x.type)
        elif self.sortBy == 4:
            # 按类型降序排列
            file_list.sort(key=lambda x: x.type, reverse=True)
        elif self.sortBy == 5:
            # 按时间升序排列
            file_list.sort(key=lambda x: x.time)
        elif self.sortBy == 6:
            # 按时间降序排列
            file_list.sort(key=lambda x: x.time, reverse=True)
        else:
            # 按类型降序排列
            file_list.sort(key=lambda x: x.type, reverse=True)

        # Emit the sorted files
        for f in file_list:
            f.icon = MyIcon(f.type)
            self.update.emit(f)

