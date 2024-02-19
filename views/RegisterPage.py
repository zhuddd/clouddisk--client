from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

from Common.StyleSheet import StyleSheet
from Common.Tost import warning, success, error
from Common.config import REGISTER_URL
from Ui.RegisterUi import RegisterUi
import hashlib

from Common.MyRequests import MyRequestThread


class RegisterPage(QtWidgets.QWidget, RegisterUi):
    back = pyqtSignal()
    def __init__(self,*args,**kwargs):
        super(RegisterPage, self).__init__(*args, **kwargs)
        self.setupUi(self)
        StyleSheet.LOGIN.apply(self)
        self.pushbutton.clicked.connect(self.signup)
        self.request = None
        self.time = None

    def signup(self):
        email = self.email.text()
        password = self.password.text()
        password2 = self.password_2.text()
        if email == "":
            warning(self.parent(), "邮箱为空")
            return
        if password != password2 or password == "":
            warning(self.parent(), "密码不一致或为空")
            return
        password = hashlib.md5(password.encode()).hexdigest()
        if not self.request or not self.request.isRunning():
            self.pushbutton.setDisabled(True)
            self.request = MyRequestThread()
            self.request.post(REGISTER_URL,
                              data={"email": email,
                                    "password": password,
                                    }
                              )
            self.request.response.connect(self.responseData)
            self.request.error.connect(self.onError)
            self.request.start()
        else:
            print("signup:请求已在运行")

    def responseData(self, s):
        self.pushbutton.setDisabled(False)
        data = s.json()
        if data["status"]:
            self.back.emit()
            success(self.parent(), "注册成功")
        else:
            warning(self.parent(), data["data"]["error"])

    def onError(self, s: dict):
        self.pushbutton.setDisabled(False)
        error(self.parent(), s.get("message"))



