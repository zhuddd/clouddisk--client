from enum import Enum

from qfluentwidgets import FluentIconBase, Theme, getIconColor

from app.Common.config import ICON_PATH


class MyIcon(FluentIconBase, Enum):
    AI = "file_ai"
    DEFAULT = "default"
    BT = "file_bt"
    CAD = "file_cad"
    CLOUD = "file_cloud"
    CODE = "file_code"
    EXCEL = "file_excel"
    EXE = "file_exe"
    FLASH = "file_flash"
    HTML = "file_html"
    IMG = "file_img"
    ISO = "file_iso"
    MUSIC = "file_music"
    PDF = "file_pdf"
    PPT = "file_ppt"
    PSD = "file_psd"
    TXT = "file_txt"
    VIDEO = "file_video"
    WORD = "file_word"
    ZIP = "file_zip"
    FOLDER = "folder"

    def path(self, theme=Theme.AUTO):
        return str(ICON_PATH / getIconColor(theme) / f"{self.value}.svg")
