import requests
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QHeaderView, QVBoxLayout
from qfluentwidgets import TableWidget, Action
from qfluentwidgets import FluentIcon

from app.Common import config
from app.Common.DataSaver import dataSaver
from app.Common.Tost import success, error
from app.Common.commandbarR import CommandBarR


class ShareListPage(QWidget):

    def __init__(self, name, parent=None):
        super().__init__(parent=parent)
        self.data = []
        self.setObjectName(name)
        self.vBoxLayout = QVBoxLayout(self)
        self.menu = CommandBarR(parent=self)

        self.tableView = TableWidget(self)
        # enable border
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)
        self.tableView.setEditTriggers(TableWidget.NoEditTriggers)

        self.tableView.setWordWrap(False)
        self.tableView.setColumnCount(6)

        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(['文件名', '文件类型', '分享日期', '结束日期', '分享码', '提取码'])
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setSortingEnabled(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.menu)
        self.vBoxLayout.addWidget(self.tableView)

        self.initAction()
        self.updateList()

    def initAction(self):
        self.update_action = Action(FluentIcon.SYNC, self.tr('刷新'))
        self.update_action.triggered.connect(self.updateList)
        self.menu.addAction(self.update_action)

        self.copy_action = Action(FluentIcon.COPY, self.tr('复制链接'))
        self.copy_action.triggered.connect(self.copyLink)
        self.menu.addAction(self.copy_action)

        self.del_action = Action(FluentIcon.DELETE, self.tr('删除'))
        self.del_action.triggered.connect(self.delShare)
        self.menu.addAction(self.del_action)

    def updateList(self):
        req = requests.get(config.FILE_SHARE_LIST, cookies=dataSaver.get("cookies"))
        if req.status_code != 200:
            error(self, "获取分享列表失败")
            return
        self.data = req.json()["data"]
        self.tableView.clearContents()
        self.tableView.setRowCount(len(self.data))
        self.tableView.setSortingEnabled(False)
        for i, d in enumerate(self.data):
            for j in range(6):
                item = QTableWidgetItem(d[j])
                item.code = d[4]
                self.tableView.setItem(i, j, item)
        self.tableView.setSortingEnabled(True)

    def delShare(self):
        items = self.tableView.selectedItems()
        if not items:
            return
        item = items[0]
        try:
            share_code = item.code
            req = requests.post(config.FILE_SHARE_DEL, cookies=dataSaver.get("cookies"), data={"code": share_code})
            if req.status_code == 200:
                self.updateList()
                self.tableView.setCurrentItem(None)
                success(self, "删除成功")
            else:
                error(self, req.json()["data"])
        except:
            error(self, "删除失败")

    def copyLink(self):
        items = self.tableView.selectedItems()
        if not items:
            return
        item = items[0]
        try:
            share_code = item.code
            link = f"{config.FILE_SHARE_GET}/{share_code}"
            QtWidgets.QApplication.clipboard().setText(link)
            success(self, "复制成功")
        except:
            error(self, "复制失败")
