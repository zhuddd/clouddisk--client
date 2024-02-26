from requests.cookies import RequestsCookieJar

import pickle

from Common.config import DAT_PATH


class DataSaver:
    """
    保存数据
    """
    def __init__(self):
        try:
            with open(DAT_PATH, 'rb') as file:
                loaded_data = pickle.load(file)
        except:
            loaded_data = None
        if loaded_data is None:
            self.data = {
                "accounts": [],
            }
        else:
            self.data = loaded_data

    def save(self):
        with open(DAT_PATH, 'wb') as file:
            pickle.dump(self.data, file)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def update(self, key, value):
        if isinstance(self.data.get(key, ), dict):
            self.data[key].update(value)
        elif isinstance(self.data.get(key, ), list):
            if value not in self.data[key]:
                self.data[key].append(value)
        elif isinstance(self.data.get(key, ), RequestsCookieJar):
            self.data[key].update(value)
        else:
            self.data[key] = value

    def getDownloadDir(self):
        if self.data.get("download_dir", None) is not None:
            download_dir = self.data.get("download_dir", None)
        else:
            import winreg
            # 打开Windows注册表
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     "Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
            download_dir = winreg.QueryValueEx(reg_key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
        return download_dir


dataSaver = DataSaver()
