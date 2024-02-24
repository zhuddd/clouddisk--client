import re

import requests
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import TreeWidget, PushButton
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow

from Common import config, FileAction
from Common.DataSaver import DataSaver
from Common.FileAction import NewNameBox
from Common.Tost import error, success

pattern = r"code=([^&]+)&pwd=([^/]*[^&]*)"


class FolderList:
    id = None
    name = None
    parent = None

    def __str__(self):
        return f"{self.id} {self.name} {self.parent}"

    def __repr__(self):
        return self.__str__()


def byList(data: list) -> list[FolderList]:
    r = []
    for item in data:
        folder = FolderList()
        folder.id = item["id"]
        folder.name = item["name"]
        folder.parent = item["parent"]
        r.append(folder)
    return r


class SaveShare(FramelessWindow):

    def __init__(self, msg, parent=None):
        super().__init__(parent=parent)
        self.folderList = None  # type: list[FolderList]
        matches = re.findall(pattern, msg)
        print(matches,msg)
        if matches:
            self.code, self.pwd = matches[0]
            self.pwd=self.pwd.replace("/","")

        self.vlayout = QVBoxLayout(self)
        self.tree = TreeWidget(self)
        self.tree.setHeaderHidden(True)

        self.btn_box = QWidget(self)
        self.hlayout = QHBoxLayout(self)
        self.newfolder_btn = PushButton("新建文件夹", self)
        self.save_btn = PushButton("保存", self)
        self.hlayout.addWidget(self.newfolder_btn)
        self.hlayout.addWidget(self.save_btn)
        self.btn_box.setLayout(self.hlayout)

        self.vlayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.vlayout.addWidget(self.tree)
        self.vlayout.addWidget(self.btn_box)

        self.getFolderList()
        self.initTree()
        self.initSlot()
        self.initWindow()

    def initSlot(self):
        self.save_btn.clicked.connect(self.save)
        self.newfolder_btn.clicked.connect(self.newFolder)

    def getFolderList(self):
        req = requests.get(config.FILE_FOLDER_LIST, cookies=DataSaver.get("cookies"))
        if req.status_code == 200:
            data = req.json()
            d = data["data"]
            self.folderList = byList(d)

    def initTree(self):
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["文件夹"])
        if self.folderList is None:
            return
        # 添加根目录
        home = QtWidgets.QTreeWidgetItem(["Home"])
        home.id=0
        self.tree.addTopLevelItem(home)
        # 创建一个字典来保存树项目
        tree_items = {0: home}
        # 首先，创建所有的QTreeWidgetItem
        for folder in self.folderList:
            tree_items[folder.id] = QtWidgets.QTreeWidgetItem([folder.name])
            tree_items[folder.id].id = folder.id
        # 然后，建立亲子关系
        for folder in self.folderList:
            if folder.parent in tree_items:
                tree_items[folder.parent].addChild(tree_items[folder.id])
            else:
                # 如果该文件夹没有父文件夹，则将其添加到树的根目录
                self.tree.addTopLevelItem(tree_items[folder.id])
        self.tree.expandItem(home)

    def save(self):
        item = self.tree.selectedItems()
        if not item:
            return
        self.save_btn.setDisabled(True)
        self.repaint()
        item = item[0]
        req = requests.post(config.FILE_SHARE_SAVE, cookies=DataSaver.get("cookies"),
                            data={"code": self.code, "pwd": self.pwd, "parent": item.id})
        if req.status_code != 200:
            try:
                error(self, req.json()["data"])
            except:
                error(self, "保存失败")
        else:
            success(self, "保存成功")
            self.save_btn.setDisabled(False)

    def newFolder(self):
        item = self.tree.selectedItems()
        if not item:
            return
        self.newfolder_btn.setDisabled(True)
        self.repaint()
        p = item[0]
        w = NewNameBox(self, title="新建文件夹")
        if w.exec():
            r = FileAction.newfolder(p.id, w.text())
            if r.status_code != 200:
                try:
                    error(self, r.json()["data"])
                except:
                    error(self, "新建文件夹失败")
                self.newfolder_btn.setDisabled(False)
                return
            else:
                id = r.json()["data"]
            new_folder = QtWidgets.QTreeWidgetItem([w.text()])
            new_folder.id = id
            p.addChild(new_folder)
            self.tree.expandItem(p)
            self.tree.setCurrentItem(new_folder)
        self.newfolder_btn.setDisabled(False)

    def initWindow(self):
        self.resize(400, 400)


# if __name__ == '__main__':
#     import sys
#     from PyQt5.QtWidgets import QApplication, QVBoxLayout, QTreeWidget, QHBoxLayout, QWidget
#
#     # enable dpi scale
#     QApplication.setHighDpiScaleFactorRoundingPolicy(
#         Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
#     QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
#     QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
#
#     app = QApplication(sys.argv)
#     w = SaveShare("cloud://code=u6i88qc1nja7g7eh&pwd=777777/")
#     w.show()
#     app.exec_()
