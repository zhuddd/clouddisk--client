from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget

from app.Common.File import File
from app.Common.StyleSheet import StyleSheet
from app.Common.Tost import error
from app.components import Media


class FilePreview(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.media = None  # type: Media.MediaBase
        self.file = None
        self.vBoxLayout = QVBoxLayout(self)
        self.setObjectName("fileInfo")
        StyleSheet.FILEINFO.apply(self)

    def setFile(self, file: File):
        if file.type == "file_music":
            media = Media.Music(file, self)
        elif file.type == "file_img":
            media = Media.Picture(file, self)
        elif file.type == "file_video":
            media = Media.Video(file, self.parent())
            media.openBrowser()
            return False
        elif file.type == "file_pdf":
            media = Media.Pdf(file, self.parent())
            media.openBrowser()
            return False
        else:
            error(self.parent(), "文件预览失败,不支持的文件类型")
            return False
        if self.media is not None:
            self.media.close()
            self.media.deleteLater()
        self.media = media
        self.vBoxLayout.addWidget(self.media)
        return True
