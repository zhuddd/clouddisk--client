import requests
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QDesktopServices, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from qfluentwidgets import PushButton, TeachingTip, TeachingTipTailPosition, TeachingTipView, Theme
from requests.utils import dict_from_cookiejar

from Common.DataSaver import dataSaver
from Common.File import File
from Common.StyleSheet import StyleSheet
from Common.config import FILE_PREVIEW,FILE_GET_KEY, cfg


class FilePreview(QWebEngineView):
    download = pyqtSignal(File)
    full = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.path = None
        self.parent = parent
        self.file = None
        self.setObjectName("fileInfo")
        self.setSlot()
        self.setContextMenuPolicy(Qt.NoContextMenu)
        StyleSheet.FILEINFO.apply(self)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        self.page().profile().downloadRequested.connect(self._downloadRequested)

    def _downloadRequested(self, e):
        self.download.emit(self.file)

    def setSlot(self):
        self.page().fullScreenRequested.connect(self._fullScreenRequested)

    def _fullScreenRequested(self, request):
        request.accept()
        if self.parent.isFullScreen():
            self.showNormal()
            self.full.emit(False)
        else:
            self.showFullScreen()
            self.full.emit(True)

    def setFile(self, file: File):
        isDark = cfg.get(cfg.themeMode) == Theme.DARK
        self.file = file
        res= requests.get(FILE_GET_KEY, params={"file_id":file.id}, cookies=dataSaver.get('cookie'))
        if res.status_code !=200:
            self.setHtml("<h1>文件预览失败</h1>")
        k=res.json()["data"]
        self.path=f'{FILE_PREVIEW}/{k}'
        self.setUrl(QUrl(self.path))
        self.showBottomTip()
        self.showFullScreen()
        if isDark:
            self.page().setBackgroundColor(QColor(21, 28, 33))
        else:
            self.page().setBackgroundColor(QColor(255, 255, 255))

    def openBrowser(self):
        QDesktopServices.openUrl(QUrl(self.path))

    def showBottomTip(self):
        position = TeachingTipTailPosition.BOTTOM
        view = TeachingTipView(
            icon=None,
            title='提示',
            content="如果遇到页面错误，请使用浏览器打开",
            isClosable=True,
            tailPosition=position,
        )

        # add widget to view
        button = PushButton('浏览器打开')
        button.setFixedWidth(120)
        view.addWidget(button, align=Qt.AlignRight)

        w = TeachingTip.make(
            target=self,
            view=view,
            duration=5000,
            tailPosition=position,
            parent=self
        )
        view.closed.connect(w.close)
        button.clicked.connect(self.openBrowser)
