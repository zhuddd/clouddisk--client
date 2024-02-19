# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class RegisterUi(object):
    def setupUi(self, Ui):
        Ui.setObjectName("Ui")
        Ui.resize(310, 311)
        self.gridLayout = QtWidgets.QGridLayout(Ui)
        self.gridLayout.setObjectName("gridLayout")
        self.password = PasswordLineEdit(Ui)
        self.password.setInputMask("")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 1, 0, 1, 1)
        self.email = LineEdit(Ui)
        self.email.setInputMask("")
        self.email.setText("")
        self.email.setMaxLength(32767)
        self.email.setFrame(False)
        self.email.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.email.setObjectName("email")
        self.gridLayout.addWidget(self.email, 0, 0, 1, 1)
        self.pushbutton = PushButton(Ui)
        self.pushbutton.setObjectName("pushbutton")
        self.gridLayout.addWidget(self.pushbutton, 3, 0, 1, 1)
        self.password_2 = PasswordLineEdit(Ui)
        self.password_2.setObjectName("password_2")
        self.gridLayout.addWidget(self.password_2, 2, 0, 1, 1)

        self.retranslateUi(Ui)
        QtCore.QMetaObject.connectSlotsByName(Ui)

    def retranslateUi(self, Ui):
        _translate = QtCore.QCoreApplication.translate
        Ui.setWindowTitle(_translate("Ui", "Ui"))
        self.password.setPlaceholderText(_translate("Ui", "密码"))
        self.email.setPlaceholderText(_translate("Ui", "邮箱"))
        self.pushbutton.setText(_translate("Ui", "注册"))
        self.password_2.setPlaceholderText(_translate("Ui", "确认密码"))
from qfluentwidgets import LineEdit, PasswordLineEdit, PushButton
