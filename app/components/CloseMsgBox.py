from qfluentwidgets import MessageBoxBase, SubtitleLabel, RadioButton


class CloseMsgBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel("您点击了关闭按钮", self)
        self.button1 = RadioButton('最小化到托盘', self)
        self.button2 = RadioButton('退出程序', self)
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.button1)
        self.viewLayout.addWidget(self.button2)
        self.button1.setChecked(True)

        self.yesButton.setText('确认')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(350)

    def isquit(self):
        if self.button1.isChecked():
            return False
        else:
            return True


