import ctypes
import os
import sys
import winreg

import win32file
import win32pipe

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_self_path():
    if getattr(sys, 'frozen', False):
        # 如果是编译后的程序，使用 sys.executable 获取可执行文件的路径
        return os.path.dirname(sys.executable)
    else:
        # 如果是直接运行的脚本，使用 __file__ 获取脚本文件的路径
        return os.path.dirname(os.path.realpath(__file__))

def create_named_pipe():
    pipe_name = r'\\.\pipe\zhuddd_cloud'
    pipe = win32pipe.CreateNamedPipe(
        pipe_name,
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        win32pipe.PIPE_UNLIMITED_INSTANCES,
        65536,
        65536,
        0,
        None
    )
    return pipe

def start_server():
    while True:
        pipe = create_named_pipe()
        win32pipe.ConnectNamedPipe(pipe, None)
        data = read_from_pipe(pipe)
        print(f'Received data: {data}')

def read_from_pipe(pipe):
    buffer_size = 1024
    data = win32file.ReadFile(pipe, buffer_size)[1].decode('utf-8')
    return data

def create_registry_entry():
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"test", 0, winreg.KEY_WRITE)
    except FileNotFoundError:
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"test")
    winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")
    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "URL:test")
    winreg.CloseKey(key)

    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"test\shell\open\command")
    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, '"'+get_self_path()+"/"+sys.argv[0].split("/")[-1]+'"' + ' "%1"')
    winreg.CloseKey(key)



if __name__ == "__main__":
    if is_admin():
        create_registry_entry()
    print("程序自身路径：", get_self_path(),'"'+get_self_path()+"/"+sys.argv[0].split("\\")[-1]+'"' + ' "%1"')
    start_server()

# 打包命令
# nuitka --mingw64 --standalone --show-progress --show-memory --plugin-enable=pylint-warnings --output-dir=out demo.py

# 打包命令
# nuitka --mingw --follow-import-to=test_pipe.py --windows-disable-console  test_pipe.py