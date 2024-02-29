
import requests
from requests import Response

from app.Common.DataSaver import dataSaver
from app.Common.MyFile import *


class MyRequestThread(requests.Session, QThread):
    response = pyqtSignal(Response)
    error = pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        requests.Session.__init__(self)
        QThread.__init__(self, *args, **kwargs)
        self.method = None
        self.url = None
        self.request_args = None
        try:
            if dataSaver.get("cookies") is not None:
                self.cookies = dataSaver.get("cookies")
            else:
                dataSaver.set("cookies", self.cookies)
        except Exception as e:
            print("MyRequestThread init", e)
            self.error.emit({"message": "初始化失败"})

    def request(self, method, url, *args, **kwargs):
        self.method = method
        self.url = url
        self.request_args = (args, kwargs)

    def run(self):
        try:
            if not self.method or not self.url or not self.request_args:
                raise Exception("No request data set")
            args, kwargs = self.request_args
            response = super(MyRequestThread, self).request(self.method, self.url, *args, **kwargs)
            dataSaver.update("cookie", response.cookies)
            self.response.emit(response)
            response.close()
        except requests.exceptions.RequestException as e:
            print("MyRequestThread run", e)
            self.error.emit({"message": str(e).split(":")[-1]})



