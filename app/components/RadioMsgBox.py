from qfluentwidgets import MessageBoxBase, SubtitleLabel, RadioButton


class RadioMsgBox(MessageBoxBase):
    def __init__(self, title="", radios=None, yes_btn_text='确定', no_btn_text='取消', parent=None):
        super().__init__(parent)
        if radios is None:
            radios = ['']
        self.titleLabel = SubtitleLabel(title, self)
        self.viewLayout.addWidget(self.titleLabel)
        self.buttons = []
        for i in range(len(radios)):
            btn = RadioButton(radios[i], self)
            self.viewLayout.addWidget(btn)
            self.buttons.append(btn)
        self.buttons[0].setChecked(True)

        self.yesButton.setText(yes_btn_text)
        self.cancelButton.setText(no_btn_text)

        self.widget.setMinimumWidth(350)

    def isquit(self):
        for i in range(len(self.buttons)):
            if self.buttons[i].isChecked():
                return i
        return -1
