from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QSystemTrayIcon
from qfluentwidgets import SystemTrayMenu, Action


class SystemTray(QSystemTrayIcon):
    showApp = pyqtSignal()
    closeApp = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setIcon(parent.windowIcon())
        self.menu = SystemTrayMenu(parent=parent)
        self.menu.addActions([
            Action('主界面', triggered=self.showApp.emit),
            Action('退出', triggered=self.closeApp.emit),
        ])
        self.setContextMenu(self.menu)
        self.activated.connect(self.open)

    def open(self,e:QSystemTrayIcon.ActivationReason):
        if e == QSystemTrayIcon.Trigger:
            self.showApp.emit()
