import sys

from PyQt5.QtCore import QUrl, Qt, QByteArray
from PyQt5.QtGui import QDesktopServices, QIcon, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QWidget, QFrame, QLabel
from qfluentwidgets import HyperlinkButton, IconWidget, PixmapLabel, SmoothScrollArea
from qfluentwidgets.components.widgets.acrylic_label import AcrylicLabel
from qfluentwidgets.multimedia import StandardMediaPlayBar

from app.Common.File import File
from app.Common.GetFace import GetFace
from app.Common.PreviewBase import PreviewBase
from app.Common.Tost import error, success
from app.components.IconCard import IconCard


class MediaBase(QWidget, PreviewBase):

    def __init__(self, file: File, parent=None):
        super().__init__(parent=parent)
        self.file = file
        self.set_file(file)
        self.vBoxLayout = QVBoxLayout(self)
        self.hyperlinkButton = HyperlinkButton(
            url=self.preview_path,
            text='浏览器打开',
            parent=self
        )
        self.vBoxLayout.addWidget(self.hyperlinkButton, alignment=Qt.AlignRight)

    def set_file(self, file: File):
        if not super().set_file(file):
            error(self, "文件预览失败")

    def openBrowser(self):
        success(self.parent(), "已使用浏览器打开")
        QDesktopServices.openUrl(QUrl(self.preview_path))


class Music(MediaBase):

    def __init__(self, file: File, parent=None):
        super().__init__(file, parent)
        self.icon = IconCard(self, file)
        self.icon.setFixedSize(500, 500)
        self.standardPlayBar = StandardMediaPlayBar(self)
        self.standardPlayBar.skipBackButton.hide()
        self.standardPlayBar.skipForwardButton.hide()

        self.vBoxLayout.addWidget(self.icon, alignment=Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.standardPlayBar)
        self.vBoxLayout.setAlignment(self.standardPlayBar, Qt.AlignBottom)

        self.setSource(self.data_path)

    def setSource(self, url):
        url = QUrl(url)
        self.standardPlayBar.player.setSource(url)


class Picture(MediaBase):
    def __init__(self, file: File, parent=None):
        super().__init__(file, parent)
        self.vBoxLayout.setSpacing(0)
        self.picture = IconWidget(self)

        self.vBoxLayout.addWidget(self.picture, alignment=Qt.AlignCenter)

        self.get_face = GetFace(self.file.id, self.file.fid, True)
        self.get_face.signal.connect(self.setIcon)
        self.get_face.start()

    def setIcon(self, icon: bytes):
        byte_array = QByteArray(icon)
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array)
        if pixmap.isNull():
            error(self, "文件预览失败")
            return
        img=QIcon(pixmap)
        self.picture.setIcon(img)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        size = self.size()
        self.picture.setFixedSize(size.width() - 60, size.height() - 60)




class Video(MediaBase):
    def __init__(self, file: File, parent=None):
        super().__init__(file, parent)

class Pdf(MediaBase):
    def __init__(self, file: File, parent=None):
        super().__init__(file, parent)

# if __name__ == '__main__':
#     QApplication.setHighDpiScaleFactorRoundingPolicy(
#         Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
#     QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
#     QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
#
#     app = QApplication([])
#     music = Music(File({"Id": 1096}))
#     music.show()
#     sys.exit(app.exec())
