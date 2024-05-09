from typing import Union

from PyQt5.QtCore import pyqtSignal, Qt, QByteArray, QPropertyAnimation, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QContextMenuEvent, QColor
from PyQt5.QtWidgets import QVBoxLayout
from qfluentwidgets import IconWidget, FluentIconBase, CaptionLabel, SimpleCardWidget, isDarkTheme, ToolTipFilter, \
    ToolTipPosition
from qfluentwidgets.common.animation import DropShadowAnimation

from app.Common.File import File
from app.Common.GetFace import GetFace
from app.Common.MyFile import convert_size


class IconCard(SimpleCardWidget):
    """ Emoji card """
    left_clicked = pyqtSignal(File)
    left_clicked_double = pyqtSignal(File)
    right_clicked = pyqtSignal(QContextMenuEvent, File)

    def __init__(self, parent=None, file: File = None):
        super().__init__(parent)
        self.get_face = None
        self.shadowAni = DropShadowAnimation(self, hoverColor=QColor(0, 0, 0, 20))
        self.shadowAni.setOffset(0, 5)
        self.shadowAni.setBlurRadius(38)

        self.elevatedAni = QPropertyAnimation(self, b'pos', self)
        self.elevatedAni.setDuration(100)

        self._originalPos = self.pos()
        self.setBorderRadius(8)
        self.file = file
        self.iconWidget = IconWidget(self.file.icon, self)
        self.label = CaptionLabel(self.file.name if len(self.file.name) <= 10 else self.file.name[:10] + "...", self)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.label, 0, Qt.AlignHCenter | Qt.AlignBottom)

        self.setFixedSize(120, 120)
        self.setTip()

    def setIcon(self, icon: Union[QIcon, str, FluentIconBase, bytes]):
        if isinstance(icon, bytes):
            if len(icon) <= 10:
                return
            byte_array = QByteArray(icon)
            pixmap = QPixmap()
            pixmap.loadFromData(byte_array)
            icon = QIcon(pixmap)
        self.iconWidget.setIcon(icon)

    def setTip(self):
        size = convert_size(self.file.size)
        tip = f"{self.file.name}\n创建时间：{self.file.time}"
        if size[0] != 0:
            tip += f"\n文件大小：{size[0]}{size[1]}"
        self.setToolTip(tip)
        self.installEventFilter(ToolTipFilter(self, 800, ToolTipPosition.TOP))

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.left_clicked_double.emit(self.file)

    def contextMenuEvent(self, event):
        self.right_clicked.emit(event, self.file)

    def enterEvent(self, e):
        super().enterEvent(e)

        # if self.elevatedAni.state() != QPropertyAnimation.Running:
        #     print("running")
        #     self._originalPos = self.pos()
        if self._originalPos.isNull():
            return

        self._startElevateAni(self.pos(), self.pos() - QPoint(0, 3))

    def leaveEvent(self, e):
        super().leaveEvent(e)
        self._startElevateAni(self.pos(), self._originalPos)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self._startElevateAni(self.pos(), self._originalPos)

    def _startElevateAni(self, start, end):
        if end.isNull():
            return
        self.elevatedAni.setStartValue(start)
        self.elevatedAni.setEndValue(end)
        self.elevatedAni.start()

    def _hoverBackgroundColor(self):
        return QColor(255, 255, 255, 16) if isDarkTheme() else QColor(255, 255, 255)

    def _pressedBackgroundColor(self):
        return QColor(255, 255, 255, 6 if isDarkTheme() else 118)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        size = self.size()
        n = int(size.width() / 12)
        self.iconWidget.setFixedSize(size.width() - 60, size.width() - 60)
        self.label.setText(self.file.name if len(self.file.name) <= n else self.file.name[:n] + "...")
        self.get_face = None
        self.get_face = GetFace(self.file.id, self.file.fid, size.width() > 300)
        self.get_face.signal.connect(self.setIcon)
        self.get_face.start()
