import os

from requests.cookies import RequestsCookieJar

import atexit
import pickle

from Common.config import DAT_PATH


class DataSaver:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            try:
                with open(DAT_PATH, 'rb') as file:
                    loaded_data = pickle.load(file)
            except:
                loaded_data = None
            cls._instance = super().__new__(cls)
            if loaded_data is None:
                cls._instance.data = {
                    "accounts": [],
                }
            else:
                cls._instance.data = loaded_data
        return cls._instance

    def __init__(self):
        atexit.register(self.save)

    def save(self):
        with open(DAT_PATH, 'wb') as file:
            pickle.dump(self.data, file)

    @staticmethod
    def get(key, default=None):
        return DataSaver().data.get(key, default)

    @staticmethod
    def set(key, value):
        DataSaver().data[key] = value

    @staticmethod
    def update(key, value):
        if isinstance(DataSaver().data.get(key, ), dict):
            DataSaver().data[key].update(value)
        elif isinstance(DataSaver().data.get(key, ), list):
            if value not in DataSaver().data[key]:
                DataSaver().data[key].append(value)
        elif isinstance(DataSaver().data.get(key, ), RequestsCookieJar):
            DataSaver().data[key].update(value)
        else:
            DataSaver().data[key] = value

    @staticmethod
    def getDownloadDir():
        if DataSaver().data.get("download_dir", None) is not None:
            download_dir = DataSaver().data.get("download_dir", None)
        else:
            import winreg
            # 打开Windows注册表
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     "Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
            download_dir = winreg.QueryValueEx(reg_key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
        return download_dir


