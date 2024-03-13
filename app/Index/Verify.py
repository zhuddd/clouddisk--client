from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QEventLoop, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon

from qfluentwidgets import FluentIcon, SplashScreen
from qfluentwidgets.window.fluent_window import MSFluentWindow

from app.Common import config
from app.views.LoginPage import LoginPage
from app.views.RegisterPage import RegisterPage
from app.views.UpdataPassword import UpdatePassword


class Verify(MSFluentWindow):
    to_init = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.home = None
        self.update_password = None
        self.setWindowTitle("Cloud")
        self.setWindowIcon(QIcon(str(config.LOGO)))
        self.resize(400, 400)
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.show()
        self.createSubInterface()
        self.splashScreen.finish()
        self.login.loginBySession()

    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(1000, loop.quit)
        QTimer.singleShot(0,self.initWindow)
        loop.exec()

    def initWindow(self):
        from app.Index.Home import Home
        if self.home is not None:
            self.home.close()
            self.home = None
        self.home = Home()
        self.login = LoginPage(self)
        self.register = RegisterPage(self)
        self.update_password = UpdatePassword(self)
        self.addSubInterface(self.login, FluentIcon.HOME, '登录')
        self.addSubInterface(self.register, FluentIcon.FINGERPRINT, '注册')
        self.addSubInterface(self.update_password, FluentIcon.MAIL, '修改密码')
        self.navigationInterface.setCurrentItem(self.login.objectName())
        self.login.signal.connect(self.start)
        self.login.forget.connect(self.re_password)
        self.register.back.connect(self.goLogin)
        self.update_password.back.connect(self.goLogin)

    def re_password(self):
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
        self.home.show()
        self.home.init_page()
        self.close()
