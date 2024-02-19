import time

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStackedWidget, QVBoxLayout

from qfluentwidgets import Pivot
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow
from qframelesswindow import StandardTitleBar
from qfluentwidgets import FluentIcon as FIF

from Common.StyleSheet import StyleSheet
from Index import Home
from views.LoginPage import LoginPage
from views.RegisterPage import RegisterPage
from views.UpdataPassword import UpdatePassword


class Verify(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.update_password = None
        StyleSheet.VERIFY.apply(self)
        # self.setTitleBar(StandardTitleBar(self))
        self.titleBar.setAttribute(Qt.WA_StyledBackground)
        self.setWindowTitle("网盘")
        self.setWindowIcon(FIF.CLOUD.icon())
        self.home = None
        self.resize(400, 400)
        self.pivot = Pivot(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)


        self.login = LoginPage(self)
        self.register = RegisterPage(self)


        self.addSubInterface(self.login, '登录', '登录')
        self.addSubInterface(self.register, '注册', '注册')

        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, self.titleBar.height(), 30, 30)

        self.pivot.setCurrentItem(self.login.objectName())

        self.login.signal.connect(self.start)
        self.login.forget.connect(self.password)
        self.register.back.connect(self.goLogin)

    def addSubInterface(self, widget, objectName, text):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def password(self):
        if self.update_password is None:
            self.update_password = UpdatePassword(self)
            self.update_password.back.connect(self.goLogin)
            self.stackedWidget.addWidget(self.update_password)

        self.stackedWidget.setCurrentWidget(self.update_password)

    def goLogin(self):
        self.pivot.setCurrentItem(self.login.objectName())
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


