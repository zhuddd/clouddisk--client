# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from app.Common.commandbarR import CommandBarR


class UpDown(object):
    def setupUi(self, Ui):
        self.verticalLayout = QtWidgets.QVBoxLayout(Ui)
        self.widget = QtWidgets.QWidget(Ui)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        # spacerItem = QtWidgets.QSpacerItem(666666666, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.horizontalLayout.addItem(spacerItem)
        self.commandBar = CommandBarR(self.widget)
        self.horizontalLayout.addWidget(self.commandBar)

        self.verticalLayout.addWidget(self.widget)
        self.SmoothScrollArea = SmoothScrollArea(Ui)
        self.SmoothScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SmoothScrollArea.setWidgetResizable(True)
        self.SmoothScrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

        self.box = QtWidgets.QWidget()
        self.box.setGeometry(QtCore.QRect(0, 0, 477, 380))
        self.box_layout = QtWidgets.QVBoxLayout(self.box)
        self.box_layout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.box_layout.setContentsMargins(0, 0, 0, 0)
        self.box_layout.setSpacing(0)
        self.items_box = QtWidgets.QVBoxLayout()
        self.items_box.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.items_box.setSpacing(0)
        self.box_layout.addLayout(self.items_box)
        self.success_item_box = QtWidgets.QVBoxLayout()
        self.success_item_box.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.success_item_box.setSpacing(0)
        self.box_layout.addLayout(self.success_item_box)
        self.SmoothScrollArea.setWidget(self.box)
        self.verticalLayout.addWidget(self.SmoothScrollArea)

        self.retranslateUi(Ui)
        QtCore.QMetaObject.connectSlotsByName(Ui)

    def retranslateUi(self, Ui):
        _translate = QtCore.QCoreApplication.translate
        Ui.setWindowTitle(_translate("Ui", "Form"))
from qfluentwidgets import SmoothScrollArea
