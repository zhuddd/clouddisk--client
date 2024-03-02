import markdown
import requests
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QStackedWidget
from qfluentwidgets import FlowLayout, PushButton, ScrollArea, Action, FluentIcon, MenuAnimationType, \
    RoundMenu, Theme
from qframelesswindow.webengine import FramelessWebEngineView

from app.Common.DataSaver import dataSaver
from app.Common.StyleSheet import StyleSheet
from app.Common.Tost import success, error
from app.Common.config import PAY_MENU, PAY_INFO, PAY_PAY, PAY_SUCCESS, cfg


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


def markdown_to_html(markdown_text, dark_mode=False):
    if dark_mode:
        # 在深色模式下使用的 CSS 样式
        css_style = """
            <style>
                body {
                    background-color: #212834;
                    color: #fff;
                }
                /* 其他样式... */
            </style>
        """
    else:
        # 在浅色模式下使用的 CSS 样式
        css_style = """
            <style>
                body {
                    background-color: #fff;
                    color: #222;
                }
                /* 其他样式... */
            </style>
        """

    # 将 Markdown 转换为 HTML
    html_content = markdown.markdown(markdown_text)

    # 将 CSS 样式和 HTML 内容拼接在一起
    html_with_style = css_style + html_content

    return html_with_style


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
        self.end_time = f'限时: {data["EndTime"]} 结束' if data["EndTime"] != "9999-12-31" else "长期有效"


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
        self.tmp = None  # type:Menu
        self.setObjectName(text.replace(' ', '-'))
        self.base_layout = QVBoxLayout(self)
        self.pages = QStackedWidget(self)
        self.pages.currentChanged.connect(self.on_page_changed)
        self.base_layout.addWidget(self.pages)
        self.menuPage()
        self.infoPage()
        self.payPage()
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

        self.infotext = QWebEngineView(self.infobox)
        self.infotext.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        self.infotext.setContextMenuPolicy(Qt.NoContextMenu)

        self.paybtn = PushButton(self.infobox)
        self.paybtn.setText("购买")
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

    def payPage(self):
        self.payScrollArea = ScrollArea(self.pages)
        self.paybox = QtWidgets.QWidget()
        self.payLayout = QVBoxLayout(self.paybox)

        self.payScrollArea.setWidget(self.paybox)
        self.payScrollArea.setFrameShape(QFrame.NoFrame)
        self.payScrollArea.setWidgetResizable(True)

        self.paytitle = QLabel("支付标题", self.paybox)
        self.paytitle.setFont(QFont("Microsoft YaHei", 15))
        self.paytitle.setWordWrap(True)
        self.paytitle.setAlignment(Qt.AlignHCenter)

        self.payinfo = QLabel("支付详细信息", self.paybox)
        self.payinfo.setFont(QFont("Microsoft YaHei", 12))
        self.payinfo.setWordWrap(True)
        self.payinfo.setAlignment(Qt.AlignHCenter)

        self.payid = QLabel("支付订单号", self.paybox)
        self.payid.setFont(QFont("Microsoft YaHei", 12))
        self.payid.setWordWrap(True)
        self.payid.setAlignment(Qt.AlignHCenter)

        self.paytime = QLabel("请在xx秒内完成支付", self.paybox)
        self.paytime.setFont(QFont("Microsoft YaHei", 12))
        self.paytime.setWordWrap(True)
        self.paytime.setAlignment(Qt.AlignHCenter)

        self.qrbox = FramelessWebEngineView(self.paybox)
        self.qrbox.setFixedSize(200, 200)
        self.qrbox.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)

        self.payprice = QLabel("支付金额", self.paybox)
        self.payprice.setFont(QFont("Microsoft YaHei", 15))
        self.payprice.setWordWrap(True)
        self.payprice.setAlignment(Qt.AlignHCenter)

        self.paypay = PushButton(self.paybox)
        self.paypay.setText("返回首页")
        self.paypay.clicked.connect(self.payback)

        self.payLayout.addWidget(self.paytitle)
        self.payLayout.addWidget(self.payinfo)
        self.payLayout.addWidget(self.payid)
        self.payLayout.addWidget(self.paytime)
        self.payLayout.addWidget(self.qrbox, alignment=Qt.AlignHCenter)
        self.payLayout.addWidget(self.payprice)
        self.payLayout.addWidget(self.paypay)
        self.pages.addWidget(self.payScrollArea)

    def setInfo(self):
        if self.tmp is not None:
            self.infotitle.setText(self.tmp.title)
            req = requests.get(f"{PAY_INFO}?menu_id={self.tmp.id}")
            if req.status_code == 200:
                mode = cfg.get(cfg.themeMode) == Theme.DARK
                self.infotext.setHtml(markdown_to_html(req.json()['data'], mode))
            else:
                self.back()
        else:
            self.pages.setCurrentIndex(0)

    def setMenu(self):
        self.menu = getMenu()
        self.flowLayout.takeAllWidgets()
        for menu in self.menu:
            btn = MenuCard(self, menu)

            btn.clicked.connect(self.clicked)
            self.flowLayout.addWidget(btn)

    def setPay(self, data: dict):
        self.qrbox.setUrl(QUrl(data['url']))
        self.paytitle.setText(data['title'])
        self.payinfo.setText(data['info'])
        self.payprice.setText(f"金额：<a style='font-size:20px;font-weight:bold;color:red;'>{data['price']}</a>")
        self.payid.setText(f"订单号：{data['id']}")
        self.order_id = data['id']

    def clicked(self, menu: Menu):
        self.tmp = menu
        self.setInfo()
        self.pages.setCurrentIndex(1)

    def back(self):
        self.pages.setCurrentIndex(0)

    def pay(self):
        req = requests.get(f"{PAY_PAY}?menu_id={self.tmp.id}", cookies=dataSaver.get("cookies"))
        if req.status_code == 200:
            self.qrbox.setHtml("")
            self.setPay(req.json()['data'])
            self.pages.setCurrentIndex(2)
            self.remainderTime = self.payCountdown
            self.paytime.setText(
                f"请在<a style='font-size:20px;font-weight:bold;color:red;'>{self.remainderTime // 1000}</a>秒内完成支付")

            if self.remainder is not None:
                self.remainder.stop()
                self.remainder.deleteLater()
            self.remainder = QtCore.QTimer()
            self.remainder.timeout.connect(self.payTime)
            self.remainder.start(1000)

            if self.backtime is not None:
                self.backtime.stop()
                self.backtime.deleteLater()
            self.backtime = QtCore.QTimer()
            self.backtime.timeout.connect(self.payback)
            self.backtime.setSingleShot(True)
            self.backtime.start(self.payCountdown)

    def payback(self):
        self.pages.setCurrentIndex(0)
        self.qrbox.setHtml("")
        if self.order_id is not None:
            req = requests.get(f"{PAY_SUCCESS}?order_id={self.order_id}", cookies=dataSaver.get("cookies"))
            if req.status_code == 200:
                req = req.json()
                if req["data"]:
                    success(self, "支付成功")
                else:
                    error(self, "支付失败")

    def payTime(self):
        self.remainderTime -= 1000
        self.paytime.setText(
            f"请在<a style='font-size:20px;font-weight:bold;color:red;'>{self.remainderTime // 1000}</a>秒内完成支付")
        if self.remainderTime <= 0:
            self.remainder.stop()
            self.remainder.deleteLater()
            self.remainder = None

    def on_page_changed(self, index):
        if index == 0:
            self.setMenu()
