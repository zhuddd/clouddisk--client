import ctypes
import os
import traceback
import winreg
import subprocess
import sys

import psutil
import win32file
import pywintypes
import time
from PyQt5 import QtCore
from PyQt5.QtCore import QLocale, QCoreApplication, Qt
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from app.Common.DataSaver import dataSaver
from app.Common.ErrorBox import ErrorBox
from app.Common.config import cfg, BASE_DIR, is_debug
from app.Index.Verify import Verify


def catch_exception(exc_type, exc_value, tb):
    ErrorMessage = traceback.format_exception(exc_type, exc_value, tb)
    w = ErrorBox('Error', "".join(ErrorMessage))
    w.exec_()
    QCoreApplication.quit()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False




def open_app_path():
    return f"{BASE_DIR}\cloud.exe"


def create_registry_entry():
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"cloud", 0, winreg.KEY_WRITE)
    except:
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"cloud")
    winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")
    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "URL:cloud")
    winreg.CloseKey(key)

    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"cloud\shell\open\command")
    winreg.SetValueEx(key, "", 0, winreg.REG_SZ,
                      '"' + open_app_path() + '"' + ' "%1"')
    winreg.CloseKey(key)
    dataSaver.set("firstTime", False)


def set_reg():
    if dataSaver.get("firstTime", True):
        if not is_admin():
            if is_debug():
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, sys.argv[0], None, 1)
            else:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.argv[0], None, None, 1)
            return 0
        else:
            create_registry_entry()
    return 1


def set_cfg():
    if cfg.get(cfg.dpiScale) == "Auto":
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    else:
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))


def init_window():
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    fluentTranslator = FluentTranslator(QLocale("zh_CN"))

    sys.excepthook = catch_exception
    app = QApplication(sys.argv)
    app.installTranslator(fluentTranslator)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    view = Verify()
    view.show()
    sys.exit(app.exec_())


def connect_to_named_pipe():
    pipe_name = r'\\.\pipe\cloud'
    now = time.time()
    while True:
        if time.time() - now > 60 * 5:
            raise Exception("Timeout")
        try:
            pipe = win32file.CreateFile(
                pipe_name,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            break
        except pywintypes.error as e:
            if e.winerror == 2:
                # Pipe不存在，继续尝试连接
                time.sleep(1)
            else:
                # 其他错误，抛出异常
                raise e
    return pipe


def is_process_running():
    current_pid = psutil.Process().pid
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['pid'] != current_pid and proc.info['name'] == 'cloud.exe':
            return True
    return False


def send_data_to_process(pipe, data):
    data = ' '.join(data)
    data_bytes = data.encode('utf-8')
    win32file.WriteFile(pipe, data_bytes)


def start_process(process_path):
    try:
        subprocess.Popen(process_path).wait(1)
    except Exception as e:
        print(f"Error starting process: {e}")


if __name__ == "__main__":
    if is_debug():
        set_cfg()
        init_window()
    else:
        if not is_process_running():
            if set_reg() == 1:
                set_cfg()
                init_window()
        else:
            pipe = connect_to_named_pipe()
            send_data_to_process(pipe, sys.argv[1:])
