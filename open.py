import subprocess
import sys
from pathlib import Path

import psutil
import win32file
import pywintypes
import time


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


def is_process_running(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
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
    process_name = "cloud.exe"
    process_path = str(Path(sys.argv[0]).resolve().parent / 'cloud.exe')
    print(process_path)
    print(sys.argv)
    if not is_process_running(process_name):
        start_process(process_path)
    pipe = connect_to_named_pipe()
    send_data_to_process(pipe, sys.argv[1:])
