import os
import sys
from pathlib import Path

from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, Theme, FolderValidator)
def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000

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


BASE_DIR = Path(os.path.dirname(os.path.realpath(sys.argv[0])))
DAT_PATH = BASE_DIR / "dat"
STYLE_FILE_PATH = BASE_DIR / "app" / "Resource" / "qss"
ICON_PATH = BASE_DIR / "app" / "Resource" / "images"
LOGO = BASE_DIR / "app" / "Resource" / "logo.svg"
CONFIG = BASE_DIR / "config" / "config.json"

# BASE_URL = "http://127.0.0.1"
# BASE_URL = "http://110.40.174.23"

BASE_URL = "http://cloud.zhuddd.icu"
'''定义基础 URL 地址'''

LOGIN_URL = BASE_URL + "/api/account/login"
'''登录 URL 地址'''

REGISTER_URL = BASE_URL + "/api/account/register"
'''注册 URL 地址'''

CAPTCHA_URL = BASE_URL + "/api/account/captcha"
'''获取验证码 URL 地址'''

UPDATE_PASSWORD_URL = BASE_URL + "/api/account/update_password"
'''更新密码 URL 地址'''

FILE_UPLOAD = BASE_URL + "/api/upload/upload"
'''文件上传 URL 地址'''

FILE_UPLOAD_DIR = BASE_URL + "/api/upload/creat_contents"
'''文件上传目录创建 URL 地址'''

FILE_DOWNLOAD = BASE_URL + "/api/download/download"
'''文件下载 URL 地址'''

FILE_DOWNLOAD_TREE = BASE_URL + "/api/download/tree"
'''文件下载目录树 URL 地址'''

FILE_USED = BASE_URL + "/api/file/used"
'''容量使用情况 URL 地址'''

FILE_DIR = BASE_URL + "/api/file/filedir"
'''文件目录 URL 地址'''

FILE_FOLDER_LIST = BASE_URL + "/api/file/folderlist"
'''文件夹列表 URL 地址'''

FILE_FACE = BASE_URL + "/api/file/face"
'''获取封面 URL 地址'''

FILE_DELETE = BASE_URL + "/api/file/delete"
'''文件删除 URL 地址'''

FILE_RENAME = BASE_URL + "/api/file/rename"
'''文件重命名 URL 地址'''

FILE_PASTE = BASE_URL + "/api/file/paste"
'''文件粘贴 URL 地址'''

FILE_NEWFOLDER = BASE_URL + "/api/file/newfolder"
'''新建文件夹 URL 地址'''

FILE_PREVIEW = BASE_URL + "/preview"
'''文件预览 URL 地址'''

FILE_GET_KEY = BASE_URL + "/api/file/getkey"
'''获取文件预览密钥 URL 地址'''

FILE_SHARE_NEW = BASE_URL + "/share/new"
'''新建文件分享 URL 地址'''

FILE_SHARE_GET = BASE_URL + "/share/get"
'''获取文件分享 URL 地址'''

FILE_SHARE_SAVE = BASE_URL + "/share/save"
'''保存分享文件 URL 地址'''

FILE_SHARE_LIST = BASE_URL + "/share/list"
'''分享文件列表 URL 地址'''

FILE_SHARE_DEL = BASE_URL + "/share/delete"
'''删除分享文件 URL 地址'''

PAY_MENU = BASE_URL + "/api/pay/menu"
'''订阅列表 URL 地址'''

PAY_INFO = BASE_URL + "/api/pay/info"
'''订阅包详情 URL 地址'''

PAY_PAY = BASE_URL + "/api/pay/pay"
'''支付 URL 地址'''

PAY_SUCCESS = BASE_URL + "/api/pay/paysuccess"
'''支付验证 URL 地址'''

cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load(CONFIG, cfg)
