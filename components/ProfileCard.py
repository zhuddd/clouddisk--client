from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import AvatarWidget, HyperlinkButton, BodyLabel, setFont, isDarkTheme, PushButton, ProgressBar

from Common.DataSaver import DataSaver
from Common.MyFile import convert_size
from Common.UserInfo import getStorageSpace


class ProfileCard(QWidget):
    """ Profile card """
    logout = pyqtSignal()
    def __init__(self,   parent=None):
        super().__init__(parent=parent)
        avatarPath = 'resource/shoko.png'
        name = DataSaver.get('user', 'name')
        # name = "01234567890123456789"
        name_show= name if len(name)<12 else name[:12]+"..."
        self.avatar = AvatarWidget(avatarPath, self)
        self.nameLabel = BodyLabel(name_show, self)
        self.nameLabel.setToolTip(name)
        self.logoutButton = PushButton("退出登录",self)
        self.storage = ProgressBar(self)
        self.storageText = BodyLabel("0/0", self)

        self.logoutButton.clicked.connect(self.logout.emit)
        color = QColor(255, 255, 255) if isDarkTheme() else QColor(0, 0, 0)
        self.nameLabel.setStyleSheet('QLabel{color: '+color.name()+'}')
        self.storageText.setStyleSheet('QLabel{color: '+color.name()+'}')
        setFont(self.logoutButton, 13)
        setFont(self.storageText, 13)

        self.setFixedSize(200, 100)
        self.avatar.setRadius(24)
        self.avatar.move(2, 6)
        self.nameLabel.move(64, 5)
        self.logoutButton.move(90, 25)
        self.storage.setFixedSize(165, 10)
        self.storage.move(0, 65)
        self.storageText.move(0, 80)

        self.getUsedSize()

    def getUsedSize(self):
        used,total=getStorageSpace()
        used_=convert_size(used)
        total_=convert_size(total)
        self.storage.setMaximum(100)
        self.storage.setValue(min(int(used/total*100),100))
        self.storage.setToolTip(f"{used_[0]}{used_[1]}/{total_[0]}{total_[1]}")
        self.storageText.setText(f"{used_[0]}{used_[1]}/{total_[0]}{total_[1]}")
        if used/total>0.9:
            self.storage.setCustomBarColor(QColor(255,0,0),QColor(255,255,0))