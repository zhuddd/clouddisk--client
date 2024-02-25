import requests
from PyQt5.QtWidgets import QTableWidgetItem,  QWidget, QHeaderView, QVBoxLayout
from qfluentwidgets import TableWidget,  Action
from qfluentwidgets import FluentIcon as FIF

from Common import config
from Common.DataSaver import dataSaver
from Common.commandbarR import CommandBarR


class ShareListPage(QWidget):

    def __init__(self, name,parent=None):
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
        self.tableView.setHorizontalHeaderLabels(['文件名', '文件类型', '分享日期', '结束日期', '分享码','提取码'])
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setSortingEnabled(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.menu)
        self.vBoxLayout.addWidget(self.tableView)

        self.initAction()
        self.updateList()


    def initAction(self):
        self.update_action = Action(FIF.SYNC, self.tr('刷新'))
        self.update_action.triggered.connect(self.updateList)
        self.menu.addAction(self.update_action)

        self.del_action = Action(FIF.DELETE, self.tr('删除'))
        self.del_action.triggered.connect(self.delShare)
        self.menu.addAction(self.del_action)

        self.menu.setSpaing(10)

    def updateList(self):
        req=requests.get(config.FILE_SHARE_LIST, cookies=dataSaver.get("cookies"))
        if req.status_code !=200:
            return
        self.data=req.json()["data"]
        self.tableView.clearContents()
        self.tableView.setRowCount(len(self.data))
        for i, d in enumerate(self.data):
            for j in range(6):
                self.tableView.setItem(i, j, QTableWidgetItem(d[j]))

    def delShare(self):
        items=self.tableView.selectedItems()
        if not items:
            return
        item=items[0]
        row=item.row()
        try:
            share_code=self.data[row][4]
            req=requests.post(config.FILE_SHARE_DEL, cookies=dataSaver.get("cookies"), data={"code":share_code})
            if req.status_code==200:
                self.updateList()
                self.tableView.setCurrentItem(None)
        except:
            pass
