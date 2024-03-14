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

    def __init__(self, face_id, fid, preview=False):
        super(GetFace, self).__init__()
        self.face_id = face_id
        self.fid = fid
        self.req = None
        self.preview = preview
        self.tmp_id=str(fid)+("icon" if not self.preview else "preview")

    def run(self):
        try:
            if faceTmp.getface(self.tmp_id):
                self.signal.emit(faceTmp.getface(self.tmp_id))
                return
            url = FILE_FACE + "/" + str(self.face_id) + ("/icon" if not self.preview else "/preview")
            self.req = requests.get(url,cookies=dataSaver.get("cookies", None))
            self.success(self.req)
        except Exception as e:
            print("getFace", e)

    def success(self, d):
        if d.status_code == 200:
            faceTmp.setface(self.tmp_id, d.content)
            self.signal.emit(d.content)
        else:
            faceTmp.setface(self.tmp_id, None)
