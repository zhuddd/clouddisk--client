from pathlib import Path

from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, Theme, FolderValidator)


def DownloadDir():
    import winreg
    # 打开Windows注册表
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             "Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
    download_dir = winreg.QueryValueEx(reg_key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
    return download_dir


class Config(QConfig):
    """ Config of application """
    downloadFolder = ConfigItem("Folders", "Download", DownloadDir(), FolderValidator())
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    checkUpdateAtStartUp = ConfigItem("Update", "CheckUpdateAtStartUp", True, BoolValidator())


cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load('config/config.json', cfg)

BASE_DIR = Path(__file__).resolve().parent.parent

DAT_PATH = BASE_DIR / "dat"
STYLE_FILE_PATH = BASE_DIR / "Resource" / "qss"
ICON_PATH = BASE_DIR / "Resource" / "images"
TEMP_PATH = BASE_DIR / "temp"

# BASE_URL = "http://127.0.0.1"
BASE_URL = "http://api.cloud.zhuddd.icu"
# BASE_URL = "http://110.40.174.23"
LOGIN_URL = BASE_URL + "/account/login"
REGISTER_URL = BASE_URL + "/account/register"
CAPTCHA_URL = BASE_URL + "/account/captcha"
UPDATE_PASSWORD_URL = BASE_URL + "/account/update_password"

FILE_UPLOAD = BASE_URL + "/upload/upload"
FILE_UPLOAD_CHECK = BASE_URL + "/upload/check"
FILE_UPLOAD_DIR = BASE_URL + "/upload/creat_contents"

FILE_DOWNLOAD = BASE_URL + "/download/download"
FILE_DOWNLOAD_TREE = BASE_URL + "/download/tree"

FILE_USED = BASE_URL + "/file/used"

FILE_DIR = BASE_URL + "/file/filedir"
FILE_FACE = BASE_URL + "/file/face"
FILE_DELETE = BASE_URL + "/file/delete"
FILE_RENAME = BASE_URL + "/file/rename"
FILE_PASTE = BASE_URL + "/file/paste"
FILE_NEWFOLDER = BASE_URL + "/file/newfolder"
FILE_SETFACE = BASE_URL + "/file/setface"
FILE_PREVIEW = BASE_URL + "/file/preview"
FILE_GET_KEY = BASE_URL + "/file/getkey"

FILE_SHARE_NEW = BASE_URL + "/share/new"
FILE_SHARE_GET = BASE_URL + "/share/get"

PAY_MENU = BASE_URL + "/pay/menu"
PAY_INFO = BASE_URL + "/pay/info"
PAY_PAY = BASE_URL + "/pay/pay"
PAY_SUCCESS = BASE_URL + "/pay/paysuccess"

STYLE_TYPE = "home.qss"
