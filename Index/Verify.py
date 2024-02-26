from PyQt5 import QtCore
from PyQt5.QtGui import QIcon

from qfluentwidgets import FluentIcon
from qfluentwidgets.window.fluent_window import MSFluentWindow

from Common import config
from Index import Home
from views.LoginPage import LoginPage
from views.RegisterPage import RegisterPage
from views.UpdataPassword import UpdatePassword


class Verify(MSFluentWindow):

    def __init__(self):
        super().__init__()
        self.update_password = None
        self.setWindowTitle("Cloud")
        self.setWindowIcon(QIcon(str(config.LOGO)))
        self.home = None
        self.resize(400, 400)

        self.login = LoginPage(self)
        self.register = RegisterPage(self)
        self.update_password = UpdatePassword(self)

        self.addSubInterface(self.login, FluentIcon.HOME, '登录')
        self.addSubInterface(self.register, FluentIcon.FINGERPRINT, '注册')
        self.addSubInterface(self.update_password, FluentIcon.MAIL, '修改密码')

        self.navigationInterface.setCurrentItem(self.login.objectName())

        self.login.signal.connect(self.start)
        self.login.forget.connect(self.password)
        self.register.back.connect(self.goLogin)
        self.update_password.back.connect(self.goLogin)

    def password(self):
        self.stackedWidget.setCurrentWidget(self.update_password)

    def goLogin(self):
        self.navigationInterface.setCurrentItem(self.login.objectName())
        self.stackedWidget.setCurrentWidget(self.login)

    def start(self):
        self.time = QtCore.QTimer()
        self.time.timeout.connect(self.move_to_home)
        self.time.setSingleShot(True)
        self.time.start(1000)

    def move_to_home(self):
        if self.home is None:
            self.home = Home.Home()
        else:
            self.home.close()
        self.home.show()
        self.hide()
