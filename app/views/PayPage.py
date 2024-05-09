import requests
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QFont, QDesktopServices
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QStackedWidget
from qfluentwidgets import FlowLayout, PushButton, ScrollArea, Action, FluentIcon, MenuAnimationType, \
    RoundMenu, TextEdit

from app.Common.DataSaver import dataSaver
from app.Common.StyleSheet import StyleSheet
from app.Common.Tost import success, error
from app.Common.config import PAY_MENU, PAY_INFO, PAY_PAY, PAY_SUCCESS


def getMenu():
    try:
        req = requests.get(PAY_MENU, cookies=dataSaver.get("cookies"))
        datas = req.json()['data']

        if req.status_code != 200:
            return []
        return [Menu(i) for i in datas]
    except Exception as e:
        print(e)
        return []


def setStorage(unit: int):
    if unit == 1:
        return "B"
    if unit == 1024:
        return "KB"
    if unit == 1048576:
        return "MB"
    if unit == 1073741824:
        return "GB"
    if unit == 1099511627776:
        return "TB"
    return "unknown"


class Menu:
    def __init__(self, data: dict):
        self.id = data["Id"]
        self.title = data["Title"]
        self.storage_size = data["StorageSize"]
        self.storage_unit = setStorage(data["storage_unit"])
        self.price = (data["Price"]) / 100
        self.valid_time = f'{data["ValidTime"]}天' if data["ValidTime"] != -1 else "永久有效"
        self.start_time = data["StartTime"]
        self.end_time = f'套餐限时: {data["EndTime"]} 结束' if data["EndTime"] != "9999-12-31" else "套餐长期有效"


class MenuCard(PushButton):
    """ Icon card """

    clicked = pyqtSignal(Menu)

    def __init__(self, parent, menu: Menu):
        super().__init__(parent=parent)
        self.menu = menu
        self.mtitle = self.menu.title if len(self.menu.title) < 6 else self.menu.title[:6] + "..."
        self.msize = f"{self.menu.storage_size}{self.menu.storage_unit}"
        self.mprice = f"{self.menu.price}元"
        self.mvalid = f"有效期：{self.menu.valid_time}"
        self.mend = f"{self.menu.end_time}"

        self.box = QLabel(self)
        self.mlayout = QVBoxLayout(self)

        self.box.setText(f"<p style='font-size:20px;font-weight:bold;'>{self.mtitle}</p>"
                         f"<p style='font-size:18px;color:green;'>{self.msize}</p>"
                         f"<p style='font-size:18px;color:red;'>{self.mprice}</p>"
                         f"<p style='font-size:12px;'>{self.mvalid}</p>"
                         f"<p style='font-size:12px;'>{self.mend}</p>")
        self.box.setAlignment(Qt.AlignHCenter)
        self.box.setFont(QFont("Microsoft YaHei"))
        self.box.setWordWrap(True)
        self.setFixedSize(200, 200)

        self.mlayout.addWidget(self.box)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.menu)


class PayPage(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.remainder = None
        self.backtime = None
        self.order_id = None
        self.qrbox = None
        self.paytime = None
        self.payCountdown = 300000
        self.remainderTime = 0
        self.menu_tmp = None  # type:Menu
        self.pay_url_tmp = None # type:QUrl
        self.setObjectName(text.replace(' ', '-'))
        self.base_layout = QVBoxLayout(self)
        self.pages = QStackedWidget(self)
        self.pages.currentChanged.connect(self.on_page_changed)
        self.base_layout.addWidget(self.pages)
        self.menuPage()
        self.infoPage()
        self.pages.setCurrentIndex(0)
        StyleSheet.PAY.apply(self)
        self.setMenu()

    def menuPage(self):
        self.ScrollArea = ScrollArea(self.pages)
        self.box = QtWidgets.QWidget()
        self.flowLayout = FlowLayout(self.box)

        self.ScrollArea.setWidget(self.box)
        self.ScrollArea.setFrameShape(QFrame.NoFrame)
        self.ScrollArea.setWidgetResizable(True)

        self.flowLayout.setContentsMargins(30, 30, 30, 30)
        self.flowLayout.setVerticalSpacing(20)
        self.flowLayout.setHorizontalSpacing(10)
        self.pages.addWidget(self.ScrollArea)

        self.update_action = Action(FluentIcon.SYNC, '刷新')
        self.update_action.triggered.connect(self.setMenu)
        self.box.contextMenuEvent = self.updatemenu

    def updatemenu(self, e):
        menu = RoundMenu(parent=self)
        menu.addAction(self.update_action)
        menu.exec(e.globalPos(), aniType=MenuAnimationType.DROP_DOWN)

    def infoPage(self):
        self.infoScrollArea = ScrollArea(self.pages)
        self.infobox = QtWidgets.QWidget()
        self.infovBoxLayout = QVBoxLayout(self.infobox)

        self.infotitle = QLabel("测试，标题栏", self.infobox)
        self.infotitle.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.infotitle.setFont(QFont("Microsoft YaHei", 15))
        self.infotitle.setWordWrap(True)

        self.infotext = TextEdit(self.infobox)
        self.infotext.setFocusPolicy(QtCore.Qt.NoFocus)
        self.infotext.contextMenuEvent = lambda event: None

        self.paybtn = PushButton(self.infobox)
        self.paybtn.setText("前往浏览器支付")
        self.paybtn.clicked.connect(self.pay)
        self.backbtn = PushButton(self.infobox)
        self.backbtn.setText("返回")
        self.backbtn.clicked.connect(self.back)

        self.infoScrollArea.setFrameShape(QFrame.NoFrame)
        self.infoScrollArea.setWidgetResizable(True)

        self.infovBoxLayout.addWidget(self.infotitle)
        self.infovBoxLayout.addWidget(self.infotext)
        self.infovBoxLayout.addWidget(self.paybtn)
        self.infovBoxLayout.addWidget(self.backbtn)

        self.infoScrollArea.setWidget(self.infobox)
        self.pages.addWidget(self.infoScrollArea)

    def setInfo(self, menu: Menu):
        self.menu_tmp = menu
        self.infotitle.setText(self.menu_tmp.title)
        req = requests.get(f"{PAY_INFO}?menu_id={self.menu_tmp.id}")
        if req.status_code == 200:
            self.infotext.setMarkdown(req.json()['data'])
            self.pages.setCurrentIndex(1)
        else:
            error(self, "获取信息失败")

    def setMenu(self):
        self.menu = getMenu()
        self.flowLayout.takeAllWidgets()
        for menu in self.menu:
            btn = MenuCard(self, menu)

            btn.clicked.connect(self.setInfo)
            self.flowLayout.addWidget(btn)

    def pay(self):
        if self.pay_url_tmp is not None:
            QDesktopServices.openUrl(self.pay_url_tmp)
            return
        req = requests.get(f"{PAY_PAY}?menu_id={self.menu_tmp.id}", cookies=dataSaver.get("cookies"))
        if req.status_code == 200:
            self.pay_url_tmp=QUrl(req.json()['data']['url'])
            QDesktopServices.openUrl(self.pay_url_tmp)
            self.order_id = req.json()['data']['id']
        else:
            error(self, "支付创建失败")

    def back(self):
        self.pages.setCurrentIndex(0)
        if self.order_id is not None:
            req = requests.get(f"{PAY_SUCCESS}?order_id={self.order_id}", cookies=dataSaver.get("cookies"))
            if req.status_code == 200:
                req = req.json()
                if req["data"]:
                    success(self, "支付成功")
                else:
                    error(self, "支付失败")
        self.order_id = None
        self.pay_url_tmp = None
        self.menu_tmp = None

    def on_page_changed(self, index):
        if index == 0:
            self.setMenu()
