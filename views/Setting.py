# coding:utf-8
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard,
                            OptionsSettingCard, PushSettingCard, ScrollArea,
                            ExpandLayout, CustomColorSettingCard,
                            setTheme, setThemeColor)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog

from Common.StyleSheet import StyleSheet
from Common.config import cfg


class Setting(ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel(self.tr("设置"), self)
        self.downloadGroup = SettingCardGroup(
            self.tr("下载"), self.scrollWidget)
        self.downloadFolderCard = PushSettingCard(
            self.tr('选择文件夹'),
            FIF.DOWNLOAD,
            self.tr("下载目录"),
            cfg.get(cfg.downloadFolder),
            self.downloadGroup
        )

        # 个性化
        self.personalGroup = SettingCardGroup(
            self.tr('个性化'), self.scrollWidget)
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr('应用主题'),
            self.tr("更改应用程序的外观"),
            texts=[
                self.tr('浅色'), self.tr('深色'),
                self.tr('使用系统设置'),
            ],
            parent=self.personalGroup
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr('主题色'),
            self.tr('更改应用程序的主题颜色'),
            self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            self.tr("界面缩放"),
            self.tr("更改小部件和字体的大小"),
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                self.tr("使用系统设置"),
            ],
            parent=self.personalGroup
        )


        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        # 初始化样式表
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        StyleSheet.SETTING.apply(self)

        # 初始化布局
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        # 将卡片添加到组
        self.downloadGroup.addSettingCard(self.downloadFolderCard)

        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.zoomCard)


        # 将设置卡组添加到布局
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.downloadGroup)
        self.expandLayout.addWidget(self.personalGroup)

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.success(
            self.tr('已成功更新'),
            self.tr('配置重启后生效'),
            duration=1500,
            parent=self
        )

    def __onDownloadFolderCardClicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("选择文件夹"), "./")
        if not folder or cfg.get(cfg.downloadFolder) == folder:
            return

        cfg.set(cfg.downloadFolder, folder)
        self.downloadFolderCard.setContent(folder)

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.appRestartSig.connect(self.__showRestartTooltip)

        # music in the pc
        self.downloadFolderCard.clicked.connect(
            self.__onDownloadFolderCardClicked)

        # personalization
        self.themeCard.optionChanged.connect(lambda ci: setTheme(cfg.get(ci),lazy=True))
        self.themeColorCard.colorChanged.connect(setThemeColor)
