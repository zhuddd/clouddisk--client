import ctypes
import os
import sys
import traceback
import winreg
from pathlib import Path

from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

import Index
from Common.config import cfg
from Common.ErrorBox import ErrorBox


def catch_exception(exc_type, exc_value, tb):
    ErrorMessage = traceback.format_exception(exc_type, exc_value, tb)
    w = ErrorBox('Error', "".join(ErrorMessage))
    w.exec_()
    app.quit()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def open_app_path():
    return str(Path(sys.argv[0]).resolve().parent / 'open.exe')


def create_registry_entry():
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"cloud", 0, winreg.KEY_WRITE)
    except FileNotFoundError:
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"cloud")
    winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")
    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "URL:cloud")
    winreg.CloseKey(key)

    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"cloud\shell\open\command")
    winreg.SetValueEx(key, "", 0, winreg.REG_SZ,
                      '"' + open_app_path() + '"' + ' "%1"')
    winreg.CloseKey(key)


if is_admin():
    create_registry_entry()

if cfg.get(cfg.dpiScale) == "Auto":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    print("Auto", Qt.HighDpiScaleFactorRoundingPolicy.PassThrough, Qt.AA_EnableHighDpiScaling)
else:
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

fluentTranslator = FluentTranslator(QLocale("zh_CN"))

sys.excepthook = catch_exception
app = QApplication(sys.argv)
app.installTranslator(fluentTranslator)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
view = Index.Verify()
view.show()
sys.exit(app.exec_())
