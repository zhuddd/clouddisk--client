import requests

from Common.DataSaver import dataSaver
from Common.config import FILE_USED


def getStorageSpace():

    req=requests.get(FILE_USED, cookies=dataSaver.get("cookies"))
    if req.status_code!=200:
        return (0,0)
    data=req.json()

    return data["data"]["used"],data["data"]["total"]