import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, Dialog


class ErrorBox(Dialog):
    """ 自定义报错消息框 """

    def __init__(self,title,msg, parent=None):
        super().__init__(title,msg, parent)
        self.cancelButton.close()
        self.yesButton.setText("确定")
        self.titleLabel.setStyleSheet("color: red;")
        self.contentLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setTitleBarVisible(True)
