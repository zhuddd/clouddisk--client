import json
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QFile, QUrl

from app.Common.DataSaver import dataSaver
from app.Common.config import FILE_DOWNLOAD_TREE


class StreamDownloader:
    def __init__(self):
        self.manager = dataSaver.QNetworkAccessManager_cookies()
        self.manager.finished.connect(self.on_finished)
        data = QtCore.QByteArray()
        data.append("file_id=758")
        self.reply = self.manager.post(self.newQNetworkRequest(),data)

        self.file = QFile("downloaded_file.txt")
        if self.file.open(QFile.WriteOnly):
            self.file.write(b"")  # Create or clear the file
    def newQNetworkRequest(self):
        r = QNetworkRequest(QUrl(FILE_DOWNLOAD_TREE))
        return r

    def on_finished(self,r):
        print((json.loads(r.readAll().data().decode())))
        self.file.close()
        print("Download finished")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    downloader = StreamDownloader()
    sys.exit(app.exec_())
