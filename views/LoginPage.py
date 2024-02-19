from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QCompleter
from requests.utils import dict_from_cookiejar

from Common.DataSaver import DataSaver
from Common.StyleSheet import StyleSheet
from Common.Tost import *
from Common.config import LOGIN_URL
from Ui.LoginUi import LoginUi
import hashlib

from Common.MyRequests import MyRequestThread



class LoginPage(QtWidgets.QWidget, LoginUi):
    signal = QtCore.pyqtSignal()
    forget = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(LoginPage, self).__init__(*args, **kwargs)
        self.setupUi(self)
        StyleSheet.LOGIN.apply(self)
        self.time = None
        accounts = DataSaver.get("accounts", [])
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
            cookie = DataSaver.get("cookies")
            session = dict_from_cookiejar(cookie).get("session")
            if session is None or session == {}:
                return
            success(self.parent(), "正在登录")

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
            error(self.parent(), "邮箱或密码为空")
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
        error(self.parent(), s.get("message"))

    def responseData(self, response):
        try:
            self.pushbutton.setDisabled(False)
            response = response.json()
            if response["status"]:
                success(self.parent(), "登录成功")
                email = response["data"]["email"]
                DataSaver.update("accounts", email)
                DataSaver.set("user", email)

                self.signal.emit()
            else:
                DataSaver.set("cookies", None)
                error(self.parent(), response["data"]["error"])
        except Exception as e:
            print("responseData", response, e)
            error(self.parent(), "网络异常")

# if __name__ == '__main__':
#     import sys
#     from PyQt5.QtWidgets import QApplication
#     # enable dpi scale
#     QApplication.setHighDpiScaleFactorRoundingPolicy(
#         Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
#     QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
#     QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
#
#     app = QApplication(sys.argv)
#     w = View()
#     w.show()
#     app.exec_()
