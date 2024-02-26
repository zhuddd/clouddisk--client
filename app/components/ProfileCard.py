from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import BodyLabel, setFont, isDarkTheme, PushButton, ProgressBar

from app.Common.DataSaver import dataSaver
from app.Common.MyFile import convert_size
from app.Common.UserInfo import getStorageSpace


class ProfileCard(QWidget):
    """
    个人信息卡
    """
    logout = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        name = dataSaver.get('user', 'name')
        # name = "01234567890123456789"
        name_show = name if len(name) < 20 else name[:20] + "..."
        self.nameLabel = BodyLabel(name_show, self)
        self.nameLabel.setToolTip(name)
        self.logoutButton = PushButton("退出登录", self)
        self.storage = ProgressBar(self)
        self.storageText = BodyLabel("0/0", self)

        self.logoutButton.clicked.connect(self.logout.emit)
        color = QColor(255, 255, 255) if isDarkTheme() else QColor(0, 0, 0)
        self.nameLabel.setStyleSheet('QLabel{color: ' + color.name() + '}')
        self.storageText.setStyleSheet('QLabel{color: ' + color.name() + '}')
        setFont(self.logoutButton, 13)
        setFont(self.storageText, 13)

        self.setFixedSize(200, 100)
        self.nameLabel.move(0, 5)
        self.storage.setFixedSize(165, 10)
        self.storage.move(0, 30)
        self.storageText.move(0, 45)
        self.logoutButton.move(90, 65)

        self.getUsedSize()

    def getUsedSize(self):
        used, total = getStorageSpace()
        used_ = convert_size(used)
        total_ = convert_size(total)
        self.storage.setMaximum(100)
        self.storage.setValue(min(int(used / total * 100), 100))
        self.storage.setToolTip(f"{used_[0]}{used_[1]}/{total_[0]}{total_[1]}")
        self.storageText.setText(f"{used_[0]}{used_[1]}/{total_[0]}{total_[1]}")
        if used / total > 0.9 or used > total:
            self.storage.setCustomBarColor(QColor(255, 0, 0), QColor(255, 0, 0))
