# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class UpDownItem(object):
    def setupUi(self, Ui):
        Ui.setObjectName("Ui")
        Ui.resize(556, 68)
        Ui.setMinimumSize(QtCore.QSize(0, 68))
        Ui.setMaximumSize(QtCore.QSize(16777215, 68))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Ui)
        self.gridLayout = QtWidgets.QGridLayout()
        self.info = QtWidgets.QLabel(Ui)
        self.gridLayout.addWidget(self.info, 2, 0, 1, 1)
        self.name = QtWidgets.QLabel(Ui)
        self.gridLayout.addWidget(self.name, 0, 0, 1, 1)
        self.progres_text = QtWidgets.QLabel(Ui)
        self.progres_text.setText("")
        self.progres_text.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.progres_text, 2, 1, 1, 1)
        self.progress = ProgressBar(Ui)
        self.gridLayout.addWidget(self.progress, 1, 0, 1, 2)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.start_btn = ToolButton(Ui)
        self.horizontalLayout_2.addWidget(self.start_btn)
        self.stop_btn = ToolButton(Ui)
        self.horizontalLayout_2.addWidget(self.stop_btn)
        self.re_btn = ToolButton(Ui)
        self.horizontalLayout_2.addWidget(self.re_btn)
        self.close_btn = TransparentToolButton(Ui)
        self.horizontalLayout_2.addWidget(self.close_btn)

from qfluentwidgets import ProgressBar, ToolButton, TransparentToolButton
