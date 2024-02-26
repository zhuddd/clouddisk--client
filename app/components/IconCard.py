from typing import Union

from PyQt5.QtCore import QTimer, pyqtSignal, Qt, QByteArray
from PyQt5.QtGui import QIcon, QPixmap, QContextMenuEvent
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QFrame
from qfluentwidgets import IconWidget,  FluentIconBase

from app.Common.File import File
from app.Common.GetFace import GetFace
from app.Common.MyFile import convert_size


class IconCard(QFrame):
    """ Icon card """

    left_clicked = pyqtSignal(File)
    left_clicked_double = pyqtSignal(File)
    right_clicked = pyqtSignal(QContextMenuEvent, File)

    def __init__(self, parent, file: File):
        super().__init__(parent=parent)
        self.icon = file.icon
        self.name = file.name
        self.Id = file.id
        self.face = file.face
        self.file = file
        self.fid = file.fid

        self.iconWidget = IconWidget(self.icon, self)
        self.nameLabel = QLabel(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.setFixedSize(100, 100)
        self.vBoxLayout.setContentsMargins(5, 5, 5, 5)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.iconWidget.setFixedSize(70, 70)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.nameLabel, 0, Qt.AlignHCenter)

        self.setText()
        self.setTip()

        self.singleClick = False
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.checkClick)

        if self.face is None or self.face is True:
            self.get_face = GetFace(self.Id,self.fid)
            self.get_face.signal.connect(self.setIcon)
            self.get_face.start()

    def setIcon(self, icon: Union[QIcon, str, FluentIconBase, bytes]):
        if isinstance(icon, bytes):
            if len(icon) <= 10:
                return
            byte_array = QByteArray(icon)
            pixmap = QPixmap()
            pixmap.loadFromData(byte_array)
            icon = QIcon(pixmap)
        self.iconWidget.setIcon(icon)

    def setText(self):
        self.nameLabel.setText(self.file.name if len(self.file.name) < 7 else self.file.name[:7] + "...")

    def setTip(self):
        size = convert_size(self.file.size)
        tip = f"{self.file.name}\n上传时间：{self.file.time}"
        if size[0] != 0:
            tip += f"\n文件大小：{size[0]}{size[1]}"
        self.setToolTip(tip)

    def setToolTip(self, a0):
        super().setToolTip(str(a0))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.singleClick = True
            self.timer.start(200)

    def contextMenuEvent(self, event):
        self.right_clicked.emit(event, self.file)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton and self.singleClick == True:
            self.left_clicked_double.emit(self.file)
            self.singleClick = False

    def checkClick(self):
        if self.singleClick:
            self.left_clicked.emit(self.file)
            self.singleClick = False

