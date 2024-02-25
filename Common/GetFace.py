import requests
from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from Common.DataSaver import dataSaver
from Common.config import FILE_FACE


class FaceTmp:
    """
    封面缓存
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.data = {}
        return cls._instance

    def setface(self, key, value):
        self.data[key] = value

    def getface(self, key):
        return self.data.get(key, None)


class GetFace(QThread):
    signal = QtCore.pyqtSignal(bytes)

    def __init__(self, face_id):
        super(GetFace, self).__init__()
        self.face_id = face_id
        self.req = None

    def run(self):
        try:
            if FaceTmp().getface(self.face_id):
                self.signal.emit(FaceTmp().getface(self.face_id))
                return
            self.req = requests.get(
                FILE_FACE + "/" + str(self.face_id) + "/icon",
                cookies=dataSaver.get("cookies", None),
            )
            self.success(self.req)
        except Exception as e:
            print("getFace", e)

    def success(self, d):
        if d.status_code == 200:
            FaceTmp().setface(self.face_id, d.content)
            self.signal.emit(d.content)
        else:
            FaceTmp().setface(self.face_id, None)
