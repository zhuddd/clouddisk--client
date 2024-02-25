from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QSizePolicy, QVBoxLayout
from qfluentwidgets import  SearchLineEdit
from qframelesswindow import  TitleBarBase

from Common.StyleSheet import StyleSheet


class HomeTitleBar(TitleBarBase):

    searchSignal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.hBoxLayout = QHBoxLayout(self)

        # add buttons to layout
        self.hBoxLayout.setSpacing(10)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.hBoxLayout.addSpacing(20)

        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(20, 20)
        self.hBoxLayout.addWidget( self.iconLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.window().windowIconChanged.connect(self.setIcon)
        self.hBoxLayout.addSpacing(10)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.addWidget( self.titleLabel, 1, Qt.AlignLeft | Qt.AlignVCenter)
        self.titleLabel.setObjectName('titleLabel')
        self.window().windowTitleChanged.connect(self.setTitle)

        # add search line edit
        self.hBoxLayout.addSpacing(100)
        self.search = SearchLineEdit(self)
        self.search.setPlaceholderText("搜索")
        self.search.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # 设置搜索框大小策略为Expanding
        self.hBoxLayout.addWidget(self.search, Qt.AlignCenter)  # 将搜索框添加到布局中并居中显示
        self.search.searchSignal.connect(self.searchSignal.emit)
        self.hBoxLayout.addSpacing(100)

        # Add buttons layout
        self.vBoxLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(Qt.AlignTop)
        self.buttonLayout.addWidget(self.minBtn)
        self.buttonLayout.addWidget(self.maxBtn)
        self.buttonLayout.addWidget(self.closeBtn)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.addStretch(1)
        self.hBoxLayout.addLayout(self.vBoxLayout, 0)

        StyleSheet.HOME_TITLE_BAR.apply(self)
    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(20, 20))