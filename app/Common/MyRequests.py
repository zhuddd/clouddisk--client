import json
import time
from urllib.parse import unquote

import requests
from requests import Response
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from app.Common.DataSaver import dataSaver
from app.Common.MyFile import *


class MyRequestThread(requests.Session, QThread):
    response = pyqtSignal(Response)
    error = pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        requests.Session.__init__(self)
        QThread.__init__(self, *args, **kwargs)
        self.method = None
        self.url = None
        self.request_args = None
        try:
            if dataSaver.get("cookies") is not None:
                self.cookies = dataSaver.get("cookies")
            else:
                dataSaver.set("cookies", self.cookies)
        except Exception as e:
            print("MyRequestThread init", e)
            self.error.emit({"message": "初始化失败"})

    def request(self, method, url, *args, **kwargs):
        self.method = method
        self.url = url
        self.request_args = (args, kwargs)

    def run(self):
        try:
            if not self.method or not self.url or not self.request_args:
                raise Exception("No request data set")
            args, kwargs = self.request_args
            response = super(MyRequestThread, self).request(self.method, self.url, *args, **kwargs)
            dataSaver.update("cookie", response.cookies)
            self.response.emit(response)
            response.close()
        except requests.exceptions.RequestException as e:
            print("MyRequestThread run", e)
            self.error.emit({"message": str(e).split(":")[-1]})


class ResumableUploader(QThread):
    response = pyqtSignal(Response)
    error = pyqtSignal(str)
    progress = pyqtSignal(tuple)
    finish = pyqtSignal()
    stop = pyqtSignal()

    def __init__(self, url, filepath, file_hash, check_hash, start_byte=0, chunk_size=1024 * 1024, auto_size=False,
                 all_file=True):
        """
        多线程上传文件，支持断点续传
        finish: -1 上传失败 0 暂停 1 上传成功
        :param url: 上传地址
        :param filepath:  文件路径
        :param file_hash:  文件hash
        :param check_hash:  文件check_hash
        :param start_byte:  从第几个字节开始上传
        :param chunk_size:  每次上传的大小 default 1MB
        :param auto_size:  自动调整上传大小
        :param all_file:  上传全部文件
        """
        super().__init__()
        self.is_run = False
        self.file_size = 0
        self.start_time = None
        self.url = url
        self.filepath = Path(filepath)
        self.file_hash = file_hash
        self.check_hash = check_hash
        self.chunk_size = chunk_size
        self.start_byte = start_byte
        self.uploaded_bytes = start_byte
        self.auto_size = auto_size
        self.all_file = all_file

    def init(self):
        self.start_time = None
        self.is_run = False
        self.file_size = self.filepath.stat().st_size

    def run(self):
        """
        开始上传
        :return:
        """
        self.init()
        self.is_run = True
        if self.file_size <= 0:
            self.error.emit("文件大小为0")
            return
        if self.chunk_size > self.file_size:
            self.chunk_size = self.file_size
        self.upload_file()

    def set_stop(self):
        """
        停止上传
        :return:
        """
        self.is_run = False

    def upload_monitor(self, monitor):
        """
        上传进度监控
        :param monitor:
        :return:
        """
        elapsed_time = time.time() - self.start_time
        if elapsed_time == 0:
            return
        speed = (monitor.bytes_read / elapsed_time)
        if speed > 0 and self.auto_size:
            self.chunk_size = int(speed)
            if self.chunk_size > self.file_size:
                self.chunk_size = self.file_size
        self.progress.emit((self.uploaded_bytes + monitor.bytes_read, self.file_size))

    def upload_file(self):
        """
        上传文件
        :return:
        """
        headers = {}
        with open(self.filepath, 'rb') as file_stream:
            while self.uploaded_bytes < self.file_size and self.is_run:
                file_stream.seek(self.start_byte)
                if self.chunk_size is not None:
                    remaining_bytes = min(self.chunk_size, self.file_size - self.start_byte)
                    file_data = file_stream.read(remaining_bytes)
                else:
                    file_data = file_stream.read()

                chunk_hash = get_file_hash_file(file_data)
                multipart_encoder = MultipartEncoder(
                    fields={
                        'metadata': (
                            'metadata',
                            json.dumps({"start_byte": self.start_byte,
                                        "chunk_size": len(file_data),
                                        "hash": self.file_hash,
                                        "check_hash": self.check_hash,
                                        "size": self.file_size,
                                        "chunk_hash": chunk_hash
                                        }),
                            'application/json'
                        ),
                        'file': (
                            'file',
                            file_data,
                            ''
                        )
                    }
                )

                monitor = MultipartEncoderMonitor(multipart_encoder, self.upload_monitor)
                headers['Content-Type'] = multipart_encoder.content_type
                self.start_time = time.time()
                try:
                    r = requests.post(
                        self.url,
                        data=monitor,
                        headers=headers,
                        cookies=dataSaver.get("cookies")
                    )
                    if r.status_code == 200:
                        self.uploaded_bytes += len(file_data)
                        self.start_byte = self.uploaded_bytes
                    else:
                        self.error.emit("上传失败")
                    self.response.emit(r)
                except Exception as e:
                    self.error.emit("服务器错误")
                if not self.all_file:
                    break
        if self.is_run:
            self.finish.emit()
        else:
            self.stop.emit()
        self.is_run = False


class ResumableDownloader(QThread):
    error = pyqtSignal(str)
    progress = pyqtSignal(tuple)
    finish = pyqtSignal()
    stop = pyqtSignal()
    set_file_name = pyqtSignal(str)

    def __init__(self, url, save_path, f_id, uid):
        """
        多线程下载文件，支持断点续传
        :param url:
        :param save_path:
        :param f_id:
        """
        super().__init__()
        self.file_path = None
        self.file_hash = None
        self.file_size = None
        self.file_name = None
        self.is_run = False
        self.first = True
        self.url = url
        self.save_path = Path(save_path)
        self.f_id = f_id
        self.uid = uid
        self.started_byte = 0

    def run(self):
        """
        开始下载
        :return:
        """
        self.first = True
        self.download_file()

    def set_stop(self):
        """
        停止下载
        :return:
        """
        self.is_run = False

    def file_name_replace(self, file_name):
        name = file_name
        t = 0
        while True:
            t += 1
            if self.save_path.joinpath(file_name).exists():
                if '.' in name:
                    a = len(name.split(".")[-1])
                    file_name = f"{name[:-a - 1]} ({t}).{name[-a:]}"
                else:
                    file_name = f"{name} ({t})"
            else:
                break
        return file_name

    def check_file(self, res):
        """
        检查文件是否存在和完整
        :return:
        """
        data = res.json().get("data")
        if data is not None:
            self.file_name = data.get("file_name")
            self.file_size = data.get("file_size")
            self.file_hash = data.get("file_hash")
            self.set_file_name.emit(self.file_name)
        self.file_path = self.save_path / str(self.file_hash + self.uid)
        if not self.file_path.exists():
            try:
                self.file_path.parent.mkdir(parents=True)
            except:
                pass
        else:
            self.started_byte = self.file_path.stat().st_size
        self.first = False
        self.download_file()

    def write_file(self, res):
        """
        写入文件
        :param file_data:
        :return:
        """
        try:
            download_size = self.started_byte
            file_name = unquote(res.headers.get("Content-Disposition").split("filename=")[-1])
            size = int(res.headers.get("Content-Length"))
            mode = 'wb' if self.started_byte == 0 else 'ab'
            with open(self.file_path, mode) as f:
                t = time.time()
                for chunk in res.iter_content(max(min(int(size / 100), 1024), 1)):
                    if self.is_run is False:
                        self.first = True
                        res.close()
                        self.stop.emit()
                        return
                    f.write(chunk)
                    download_size += len(chunk)
                    if time.time() - t > 0.1:
                        t = time.time()
                        self.progress.emit((download_size, self.file_size))
                self.progress.emit((download_size, self.file_size))
            file_hash, _ = get_file_hash(str(self.file_path))
            if file_hash == self.file_hash:
                file_name = self.file_name_replace(file_name)
                self.file_path.rename(self.file_path.parent / file_name)
                self.set_file_name.emit(file_name)
                self.finish.emit()
            else:
                self.error.emit("文件损坏")
            self.is_run = False
        except Exception as e:
            print("MyRequest Download write_file", e)
            self.run()

    def download_file(self):
        """
        下载文件
        :return:
        """
        self.is_run = True
        with requests.get(self.url,
                          params={"file_id": self.f_id, "Only_header": self.first},
                          stream=not self.first,
                          cookies=dataSaver.get("cookies"),
                          headers={"Range": f"bytes={self.started_byte}-"},
                          ) as res:
            if res.status_code in (200, 206):
                if self.first:
                    self.check_file(res)
                else:
                    self.write_file(res)
            else:
                self.error.emit("网络异常")
                self.is_run = False


# if __name__ == '__main__':
#     import sys
#     from PyQt5 import QtWidgets
#
#     # 示例用法
#     url = 'http://0000000/download/download'
#     file_path = "D:\Desktop\\test"
#     # url = "https://0000000/developer/article/2192086"
#
#     uploader = ResumableDownloader(url, file_path, f_id=12)
#
#     app = QtWidgets.QApplication(sys.argv)
#     uploader.start()
#     sys.exit(app.exec_())
