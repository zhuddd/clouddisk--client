from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QSizePolicy, QLabel

from qfluentwidgets import (MSFluentWindow, NavigationItemPosition, InfoBadge, InfoBadgePosition,
                            NavigationAvatarWidget, RoundMenu, SearchLineEdit, FluentTitleBar, FluentStyleSheet)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import StandardTitleBar, TitleBarBase, TitleBar

from Common.DataSaver import dataSaver
from Common.HomeTitleBar import HomeTitleBar
from Common.StyleSheet import StyleSheet
from Common.pipe_msg import PipeMsg
from components.ProfileCard import ProfileCard

from Common.File import File
from views.DownloadPage import DownloadPage
from views.FilePreview import FilePreview
from views.FilePage import FilePage
from views.PayPage import PayPage
from views.SaveShare import SaveShare
from views.Setting import Setting
from views.ShareListPage import ShareListPage
from views.UploadPage import UploadPage


class Home(MSFluentWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.save_share = None
        self.pipe = None
        self.setObjectName("mainWindow")
        self.PreviewPage = None
        self.verify = None
        self.download_num = None
        self.upload_num = None
        self.fileInterface = FilePage(self)
        self.ShareListInterface = ShareListPage("shareList",self)
        self.upLoadInterface = UploadPage("upLoad", self)
        self.downLoadInterface = DownloadPage("downLoad", self)
        self.payInterface = PayPage("pay", self)
        self.settingInterface = Setting(self)
        self.userInterface = NavigationAvatarWidget(
            dataSaver.get('user', 'name'),
            FIF.ROBOT.path()
        )

        self.initWindow()
        self.initNavigation()
        self.setSlot()
        self.init_pipe()
        StyleSheet.HOME.apply(self)

    def init_pipe(self):
        self.pipe = PipeMsg(self)
        self.pipe.msg.connect(self.saveShare)
        self.pipe.start()

    def setSlot(self):
        self.fileInterface.filePath.connect(self.upLoadInterface.addTask)
        self.fileInterface.preview.connect(self.setFilePreviewPage)
        self.fileInterface.fileDownload.connect(self.downloadFile)
        self.upLoadInterface.update.connect(self.fileInterface.updatePage)
        self.newTitleBar.searchSignal.connect(self.findFile)
        self.downLoadInterface.taskNum.connect(self.setDownloadTaskNum)
        self.upLoadInterface.taskNum.connect(self.setUploadTaskNum)

    def findFile(self, fileName):
        self.fileInterface.addInterface(f"搜索:{fileName}", fileName)
        self.navigationInterface.setCurrentItem(self.fileInterface.objectName())
        self.stackedWidget.setCurrentWidget(self.fileInterface)

    def downloadFile(self, file: File):
        self.downLoadInterface.addTask(file.id)

    def saveShare(self,msg):
        if self.save_share is not None:
            self.save_share.close()
            self.save_share = None
        self.save_share=SaveShare(msg)
        self.save_share.show()

    def initNavigation(self):
        self.addSubInterface(self.fileInterface, FIF.HOME, 'Home', FIF.HOME_FILL)
        self.addSubInterface(self.ShareListInterface, FIF.SHARE, '分享列表', FIF.SHARE)
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

    def setFilePreviewPage(self, file: File):
        if self.PreviewPage is None:
            self.PreviewPage = FilePreview(self)
            self.addSubInterface(self.PreviewPage, FIF.VIEW, '文件预览')
            self.PreviewPage.full.connect(self.full)
            self.PreviewPage.download.connect(self.downloadFile)
        self.PreviewPage.setFile(file)
        self.stackedWidget.setCurrentWidget(self.PreviewPage)

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
        self.newTitleBar = HomeTitleBar(self)
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
        dataSaver.set("cookies", None)
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
