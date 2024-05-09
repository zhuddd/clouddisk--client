import re

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from qfluentwidgets import PasswordLineEdit, PushButton, LineEdit

from app.Common.StyleSheet import StyleSheet
from app.Common.Tost import warning, success, error
from app.Common.config import REGISTER_URL
import hashlib

from app.Common.MyRequests import MyRequestThread


def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))


class RegisterPage(QtWidgets.QWidget):
    back = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("registerPage")
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.email = LineEdit(self)
        self.email.setPlaceholderText("邮箱")
        self.gridLayout.addWidget(self.email, 0, 0, 1, 1)
        self.password = PasswordLineEdit(self)
        self.password.setPlaceholderText("密码")
        self.gridLayout.addWidget(self.password, 1, 0, 1, 1)
        self.password_2 = PasswordLineEdit(self)
        self.password_2.setPlaceholderText("确认密码")
        self.gridLayout.addWidget(self.password_2, 2, 0, 1, 1)
        self.pushbutton = PushButton("注册", self)
        self.gridLayout.addWidget(self.pushbutton, 3, 0, 1, 1)

        StyleSheet.LOGIN.apply(self)
        self.pushbutton.clicked.connect(self.signup)
        self.request = None
        self.time = None

    def signup(self):
        email = self.email.text()
        password = self.password.text()
        password2 = self.password_2.text()
        if email == "":
            warning(self, "邮箱为空")
            return
        if not validate_email(email):
            warning(self, "邮箱格式错误")
            return
        if password != password2 or password == "":
            warning(self, "密码不一致或为空")
            return
        if len(password) < 7:
            warning(self, "密码长度不能小于7位")
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
            success(self, "注册成功")
        else:
            warning(self, data["data"]["error"])

    def onError(self, s: dict):
        self.pushbutton.setDisabled(False)
        error(self, s.get("message"))
