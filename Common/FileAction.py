import requests
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit

from Common.DataSaver import dataSaver
from Common.config import FILE_PASTE, FILE_DELETE, FILE_RENAME, FILE_NEWFOLDER


def paste(fileId, parentId) -> requests.Response:
    path = FILE_PASTE
    params = {"id": fileId, "parent": parentId}
    r = requests.post(path, data=params, cookies=dataSaver.get("cookies"))
    return r


def delete(fileId) -> requests.Response:
    path = FILE_DELETE
    params = {"id": fileId}
    r = requests.post(path, data=params, cookies=dataSaver.get("cookies"))
    return r


def rename(fileId, newName) -> requests.Response:
    path = FILE_RENAME
    params = {"id": fileId, "name": newName}
    r = requests.post(path, data=params, cookies=dataSaver.get("cookies"))
    return r


def newfolder(parentId, name) -> requests.Response:
    path = FILE_NEWFOLDER
    params = {"parent": parentId, "name": name}
    r = requests.post(path, data=params, cookies=dataSaver.get("cookies"))
    return r


class NewNameBox(MessageBoxBase):
    """
    新名字输入框
    """

    def __init__(self, parent=None, title='新名字', placeholder='输入新名字', defaultText=''):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(title, self)
        self.nameLineEdit = LineEdit(self)

        self.nameLineEdit.setPlaceholderText(placeholder)
        self.nameLineEdit.setText(defaultText)
        self.nameLineEdit.setClearButtonEnabled(True)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.nameLineEdit)

        self.yesButton.setText('确认')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(350)
        self.yesButton.setDisabled(True)
        self.nameLineEdit.textChanged.connect(self._validateUrl)

    def text(self):
        return self.nameLineEdit.text()

    def _validateUrl(self, text):
        self.yesButton.setEnabled(0 < len(text) <= 200)
