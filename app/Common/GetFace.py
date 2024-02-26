import requests
from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from app.Common.DataSaver import dataSaver
from app.Common.config import FILE_FACE


class FaceTmp:
    """
    封面缓存
    """

    data = {}

    def setface(self, key, value):
        self.data[key] = value

    def getface(self, key):
        return self.data.get(key, None)


faceTmp = FaceTmp()


class GetFace(QThread):
    """
    获取封面
    """
    signal = QtCore.pyqtSignal(bytes)

    def __init__(self, face_id, fid):
        super(GetFace, self).__init__()
        self.face_id = face_id
        self.fid = fid
        self.req = None

    def run(self):
        try:
            if faceTmp.getface(self.fid):
                self.signal.emit(faceTmp.getface(self.fid))
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
            faceTmp.setface(self.fid, d.content)
            self.signal.emit(d.content)
        else:
            faceTmp.setface(self.fid, None)
