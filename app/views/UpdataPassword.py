import hashlib

import requests
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QGridLayout, QWidget
from qfluentwidgets import LineEdit, PasswordLineEdit, PushButton

from app.Common import config
from app.Common.Tost import success, warning, error


class UpdatePassword(QWidget):
    back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("updatePassword")
        self.dtimer = None
        self.dtime = None
        self.initWindow()
        self.setSlot()

    def initWindow(self):
        self.email_edit = LineEdit(self)
        self.password_edit = PasswordLineEdit(self)
        self.password_edit2 = PasswordLineEdit(self)
        self.captcha_edit = LineEdit(self)
        self.get_capcha = PushButton("获取验证码", self)
        self.backbtn = PushButton("返回", self)
        self.send = PushButton("确认", self)

        self.email_edit.setPlaceholderText("邮箱")
        self.password_edit.setPlaceholderText("密码")
        self.password_edit2.setPlaceholderText("确认密码")
        self.captcha_edit.setPlaceholderText("验证码")
        self.captcha_edit.setMaxLength(6)

        self.box = QGridLayout(self)
        self.box.addWidget(self.email_edit, 1, 0, 1, 2)
        self.box.addWidget(self.password_edit, 2, 0, 1, 2)
        self.box.addWidget(self.password_edit2, 3, 0, 1, 2)
        self.box.addWidget(self.captcha_edit, 4, 0, 1, 1)
        self.box.addWidget(self.get_capcha, 4, 1, 1, 1)
        self.box.addWidget(self.backbtn, 5, 0, 1, 2)
        self.box.addWidget(self.send, 6, 0, 1, 2)

        self.setLayout(self.box)

        self.setWindowTitle("修改密码")

    def setSlot(self):
        self.backbtn.clicked.connect(self.back.emit)
        self.get_capcha.clicked.connect(self.get_capcha_clicked)
        self.send.clicked.connect(self.send_clicked)

    def disabled_get_capcha(self):
        self.get_capcha.setEnabled(False)
        self.dtime = 60
        self.dtimer = QTimer()
        self.dtimer.timeout.connect(self.set_get_capcha)
        self.dtimer.start(1000)

    def set_get_capcha(self):
        self.dtime -= 1
        if self.dtime == 0:
            self.get_capcha.setEnabled(True)
            self.get_capcha.setText("获取验证码")
            self.dtimer.stop()
            return
        self.get_capcha.setText(f"{self.dtime}秒后重新获取")

    def get_capcha_clicked(self):
        if self.email_edit.text() == "":
            warning(self, "邮箱不能为空")
            return
        req = requests.post(config.CAPTCHA_URL, data={"email": self.email_edit.text()})
        if req.status_code == 200:
            success(self, "验证码已发送")
            self.disabled_get_capcha()
        elif req.status_code == 400:
            warning(self, req.json()['data'])
        else:
            error(self, "未知错误")

    def send_clicked(self):
        if (self.email_edit.text() == ""
                or self.password_edit.text() == ""
                or self.password_edit2.text() == ""
                or self.captcha_edit.text() == ""):
            warning(self, "请填写完整")
            return
        if self.password_edit.text() != self.password_edit2.text():
            warning(self, "两次密码不一致")
            return
        password = hashlib.md5(self.password_edit.text().encode()).hexdigest()
        req = requests.post(config.UPDATE_PASSWORD_URL,
                            data={"email": self.email_edit.text(),
                                  "password": password,
                                  "captcha": self.captcha_edit.text()
                                  }
                            )
        if req.status_code == 200:
            self.back.emit()
            success(self, "修改成功")
        elif req.status_code == 400:
            warning(self, req.json()['data'])
        else:
            error(self, "未知错误")
