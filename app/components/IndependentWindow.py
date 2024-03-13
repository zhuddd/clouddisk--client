

from qfluentwidgets import MSFluentTitleBar, isDarkTheme,  qconfig

from app.Common.config import isWin11

if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


class IndependentWindow(Window):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setTitleBar(MSFluentTitleBar(self))
        self.setTheme()
        qconfig.themeChangedFinished.connect(self.setTheme)
    def setTheme(self):
        if isWin11():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())