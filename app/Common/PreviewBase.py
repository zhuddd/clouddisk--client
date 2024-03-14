import requests

from app.Common.DataSaver import dataSaver
from app.Common.File import File
from app.Common.config import FILE_GET_KEY, FILE_PREVIEW_DATA, FILE_PREVIEW, FILE_PREVIEW_POSTER


class PreviewBase:
    def __init__(self):
        self.poster_path = None
        self.data_path = None
        self.preview_path = None
        self.file = None

    def set_file(self, file: File):
        self.file = file
        res = requests.get(FILE_GET_KEY, params={"file_id": file.id}, cookies=dataSaver.get('cookie'))
        if res.status_code != 200:
            return False
        else:
            k = res.json()["data"]
            self.preview_path = f'{FILE_PREVIEW}/{k}'
            self.data_path = f'{FILE_PREVIEW_DATA}/{k}'
            self.poster_path = f'{FILE_PREVIEW_POSTER}/{k}'
            return True
