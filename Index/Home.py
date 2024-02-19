from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QSizePolicy, QLabel

from qfluentwidgets import (MSFluentWindow, NavigationItemPosition, InfoBadge, InfoBadgePosition,
                            NavigationAvatarWidget, RoundMenu, SearchLineEdit, FluentTitleBar, FluentStyleSheet)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import StandardTitleBar, TitleBarBase, TitleBar

from Common.DataSaver import DataSaver
from Common.HomeTitleBar import HomeTitleBar
from Common.StyleSheet import StyleSheet
from components.ProfileCard import ProfileCard

from Common.File import File
from views.DownloadPage import DownloadPage
from views.FileInfo import FileInfo
from views.FilePage import FilePage
from views.PayPage import PayPage
from views.Setting import Setting
from views.UploadPage import UploadPage



class Home(MSFluentWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("mainWindow")
        self.InfoPage = None
        self.verify = None
        self.download_num = None
        self.upload_num = None
        self.fileInterface = FilePage(self)
        self.upLoadInterface = UploadPage("upLoad", self)
        self.downLoadInterface = DownloadPage("downLoad", self)
        self.payInterface = PayPage("pay", self)
        self.settingInterface = Setting(self)
        self.userInterface = NavigationAvatarWidget(
            DataSaver.get('user', 'name'),
            FIF.ROBOT.path()
        )

        self.initWindow()
        self.initNavigation()
        self.setSlot()
        StyleSheet.HOME.apply(self)

    def setSlot(self):
        self.fileInterface.filePath.connect(self.upLoadInterface.addTask)
        self.fileInterface.fileInfo.connect(self.setFileInfoPage)
        self.fileInterface.fileDownload.connect(self.downloadFile)
        self.upLoadInterface.update.connect(self.fileInterface.updatePage)
        self.newTitleBar.searchSignal.connect(self.findFile)
        self.downLoadInterface.taskNum.connect(self.setDownloadTaskNum)
        self.upLoadInterface.taskNum.connect(self.setUploadTaskNum)

    def findFile(self, fileName):
        self.fileInterface.addInterface(fileName,fileName)
    def downloadFile(self, file: File):
        self.downLoadInterface.addTask(file.id)

    def initNavigation(self):
        self.addSubInterface(self.fileInterface, FIF.HOME, 'Home', FIF.HOME_FILL)
        self.addSubInterface(self.upLoadInterface, FIF.SEND, '上传')
        self.addSubInterface(self.downLoadInterface, FIF.DOWNLOAD, '下载')
        self.addSubInterface(self.payInterface, FIF.SHOPPING_CART, '充值')
        self.navigationInterface.addWidget(
            routeKey='user',
            widget=self.userInterface,
            onClick=self.userInfo,
            position=NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', position=NavigationItemPosition.BOTTOM)
        self.navigationInterface.setCurrentItem(self.fileInterface.objectName())

    def setFileInfoPage(self, file: File):
        if self.InfoPage is None:
            self.InfoPage = FileInfo(self)
            self.addSubInterface(self.InfoPage, FIF.DOCUMENT, '文件预览')
            self.InfoPage.full.connect(self.full)
            self.InfoPage.download.connect(self.downloadFile)
        self.InfoPage.setFile(file)
        self.stackedWidget.setCurrentWidget(self.InfoPage)

    def setUploadTaskNum(self, num: int):
        if self.upload_num is None:
            item = self.navigationInterface.widget(self.upLoadInterface.objectName())
            self.upload_num = InfoBadge.attension(
                text=num,
                parent=item.parent(),
                target=item,
                position=InfoBadgePosition.NAVIGATION_ITEM
            )
            return
        if num <= 0:
            self.upload_num.hide()
        else:
            self.upload_num.show()
            self.upload_num.setNum(num)
            self.upload_num.adjustSize()

    def setDownloadTaskNum(self, num: int):
        if self.download_num is None:
            item = self.navigationInterface.widget(self.downLoadInterface.objectName())
            self.download_num = InfoBadge.attension(
                text=num,
                parent=item.parent(),
                target=item,
                position=InfoBadgePosition.NAVIGATION_ITEM
            )
            return
        if num <= 0:
            self.download_num.hide()
        else:
            self.download_num.show()
            self.download_num.setNum(num)
            self.download_num.adjustSize()

    def initWindow(self):
        self.resize(900, 700)
        self.newTitleBar=HomeTitleBar(self)
        self.setTitleBar(self.newTitleBar)
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        self.setWindowIcon(FIF.CLOUD.icon())
        self.setWindowTitle("网盘")
        # self.updateFrameless()
        self.setMicaEffectEnabled(True)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
    def userInfo(self):
        menu = RoundMenu(parent=self)
        card = ProfileCard(menu)
        card.logout.connect(self.logout)
        menu.addWidget(card)
        menu.exec(self.userInterface.pos() + self.pos())

    def logout(self):
        from Index import Verify
        DataSaver.set("cookies", None)
        self.verify = Verify()
        self.verify.show()
        self.close()

    def full(self, e):
        if e:
            self.showFullScreen()
            self.navigationInterface.hide()
            self.titleBar.hide()
            self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        else:
            self.showNormal()
            self.navigationInterface.show()
            self.titleBar.show()
            self.hBoxLayout.setContentsMargins(0, 48, 0, 0)
