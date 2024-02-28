from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, qconfig

from app.Common.config import STYLE_FILE_PATH


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """
    HOME = "home"
    VERIFY = "verify"
    SETTING = "setting"
    FILE = "file"
    DOWNLOAD = "download"
    UPLOAD = "upload"
    FILEINFO = "fileinfo"
    LOGIN = "login"
    REGISTER = "register"
    PAY = "pay"
    HOME_TITLE_BAR = "home_title_bar"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return str(STYLE_FILE_PATH/f"{theme.value.lower()}"/f"{self.value}.qss")
