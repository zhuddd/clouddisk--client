from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QCompleter
from qfluentwidgets import PushButton, PasswordLineEdit, LineEdit
from requests.utils import dict_from_cookiejar

from Common.DataSaver import dataSaver
from Common.StyleSheet import StyleSheet
from Common.Tost import *
from Common.config import LOGIN_URL
import hashlib

from Common.MyRequests import MyRequestThread



class LoginPage(QtWidgets.QWidget):
    signal = QtCore.pyqtSignal()
    forget = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("loginPage")
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.pushbutton = PushButton("登录",self)
        self.gridLayout.addWidget(self.pushbutton, 2, 1, 1, 1)
        self.email = LineEdit(self)
        self.email.setPlaceholderText("邮箱")
        self.gridLayout.addWidget(self.email, 0, 0, 1, 2)
        self.password = PasswordLineEdit(self)
        self.password.setPlaceholderText("密码")
        self.gridLayout.addWidget(self.password, 1, 0, 1, 2)
        self.fogetPassword = PushButton("忘记密码", self)
        self.gridLayout.addWidget(self.fogetPassword, 2, 0, 1, 1)

        StyleSheet.LOGIN.apply(self)
        self.time = None
        accounts = dataSaver.get("accounts", [])
        self.completer = QCompleter(accounts, self.email)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setMaxVisibleItems(10)
        self.email.setCompleter(self.completer)

        self.pushbutton.clicked.connect(self.login)
        self.fogetPassword.clicked.connect(self.forget.emit)
        self.request = None
        self.loginBySession()

    def loginBySession(self):
        try:
            cookie = dataSaver.get("cookies")
            session = dict_from_cookiejar(cookie).get("session")
            if session is None or session == {}:
                return
            success(self, "正在登录")

            def s():
                if not self.request or not self.request.isRunning() and session:
                    self.request = MyRequestThread()
                    self.request.get(LOGIN_URL,
                                     params={"type": "SESSION", "session": session}
                                     )
                    self.request.response.connect(self.responseData)
                    self.request.error.connect(self.onError)
                    self.request.start()
                else:
                    print("请求已在运行")

            self.time = QtCore.QTimer()
            self.time.timeout.connect(s)
            self.time.setSingleShot(True)
            self.time.start(1000)
        except Exception as e:
            print(f"loginBySession: {e}")

    def login(self):
        email = self.email.text()
        password = self.password.text()
        if email == "" or password == "":
            error(self, "邮箱或密码为空")
            return
        password = hashlib.md5(password.encode()).hexdigest()
        if not self.request or not self.request.isRunning():
            self.pushbutton.setDisabled(True)
            self.request = MyRequestThread()
            self.request.get(LOGIN_URL,
                             params={"email": email,
                                     "password": password,
                                     "type": "PWD"}
                             )
            self.request.response.connect(self.responseData)
            self.request.error.connect(self.onError)
            self.request.start()
        else:
            print("login:请求已在运行")

    def onError(self, s: dict):
        self.pushbutton.setDisabled(False)
        error(self, s.get("message"))

    def responseData(self, response):
        try:
            self.pushbutton.setDisabled(False)
            response = response.json()
            if response["status"]:
                success(self, "登录成功")
                email = response["data"]["email"]
                dataSaver.update("accounts", email)
                dataSaver.set("user", email)

                self.signal.emit()
            else:
                dataSaver.set("cookies", None)
                error(self, response["data"]["error"])
        except Exception as e:
            print("responseData", response, e)
            error(self, "网络异常")


