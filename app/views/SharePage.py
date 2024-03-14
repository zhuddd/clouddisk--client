import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import  RadioButton, LineEdit, PushButton, CaptionLabel, CalendarPicker

from app.Common import config
from app.Common.DataSaver import dataSaver
from app.Common.File import File
from app.Common.Tost import error, success
from app.components.IconCard import IconCard
from app.components.IndependentWindow import IndependentWindow


class SharePage(IndependentWindow):

    def __init__(self, file: File = None, parent=None):
        super().__init__(parent=parent)
        self.file = file
        self.file_card = IconCard(self, self.file)
        # 有效期选择
        self.nameLabel1 = CaptionLabel('有效期:', self)
        self.nameLabel1.pixelFontSize = 15
        self.time_picker_box = QWidget(self)
        self.time_picker_layout = QHBoxLayout(self.time_picker_box)
        self.set_time = RadioButton('永久有效', self.time_picker_box)
        self.set_time.setChecked(True)
        self.set_time2 = RadioButton('自定义时间', self.time_picker_box)
        self.timePicker = CalendarPicker(self.time_picker_box)
        self.timePicker.setDisabled(True)
        self.time_picker_layout.addWidget(self.nameLabel1)
        self.time_picker_layout.addWidget(self.set_time)
        self.time_picker_layout.addWidget(self.set_time2)
        self.time_picker_layout.addWidget(self.timePicker)
        self.time_picker_box.adjustSize()
        # 提取码选择
        self.nameLabel2 = CaptionLabel('提取码:', self)
        self.nameLabel2.pixelFontSize = 15
        self.pwd_box = QWidget(self)
        self.pwd_layout = QHBoxLayout(self.pwd_box)
        self.set_pwd = RadioButton('无需提取码', self.pwd_box)
        self.set_pwd.setChecked(True)
        self.set_pwd2 = RadioButton('自定义提取码', self.pwd_box)
        self.extract_code = LineEdit(self.pwd_box)
        self.extract_code.setDisabled(True)
        self.pwd_layout.addWidget(self.nameLabel2)
        self.pwd_layout.addWidget(self.set_pwd)
        self.pwd_layout.addWidget(self.set_pwd2)
        self.pwd_layout.addWidget(self.extract_code)
        self.pwd_box.adjustSize()

        self.share_btn = PushButton("分享", self)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.file_card, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.nameLabel1)
        self.vBoxLayout.addWidget(self.time_picker_box)
        self.vBoxLayout.addWidget(self.nameLabel2)
        self.vBoxLayout.addWidget(self.pwd_box)
        self.vBoxLayout.addWidget(self.share_btn)

        self.initWindow()
        self.setSlot()

    def initWindow(self):
        self.setWindowIcon(QIcon(str(config.LOGO)))
        self.setWindowTitle("分享")
        self.resize(400, 400)
        self.vBoxLayout.setContentsMargins(30, self.titleBar.height(), 30, 30)

    def setSlot(self):
        self.set_time2.clicked.connect(self.customTime)
        self.set_time.clicked.connect(self.defaultTime)
        self.set_pwd2.clicked.connect(self.customPwd)
        self.set_pwd.clicked.connect(self.defaultPwd)
        self.share_btn.clicked.connect(self.share)

    def customTime(self):
        self.timePicker.setDisabled(False)

    def defaultTime(self):
        self.timePicker.setDisabled(True)
        self.end_time = ''

    def customPwd(self):
        self.extract_code.setDisabled(False)

    def defaultPwd(self):
        self.extract_code.setDisabled(True)

    def share(self):
        end_time = ''
        pwd = ''
        if self.set_time2.isChecked():
            end_time = self.timePicker.getDate().toString('yyyy-MM-dd')
            if end_time == '':
                error(self, "请选择有效期")
                return
            if end_time < QDate.currentDate().toString('yyyy-MM-dd'):
                error(self, "有效期不能小于当前日期")
                return
        if self.set_pwd2.isChecked():
            pwd = self.extract_code.text()
            if 4 > len(pwd) or len(pwd) > 16:
                error(self, "提取码长度应为4-16位")
                return
        req = requests.post(
            config.FILE_SHARE_NEW,
            data={
                "file_id": self.file.id,
                "end_time": end_time,
                "pwd": pwd
            },
            cookies=dataSaver.get('cookie')
        )
        if req.status_code != 200:
            error(self, "分享失败")
        else:
            self.showLink(req.json()["data"])

    def showLink(self, data):
        code = data["share_code"]
        end_time = data["end_time"]
        pwd = data["pwd"]
        self.nameLabel1.close()
        self.nameLabel2.close()
        self.time_picker_box.close()
        self.pwd_box.close()
        self.share_btn.close()
        link = f"{config.FILE_SHARE_GET}/{code}"
        text = f"文件:{self.file.name}\n"
        text += f"提取链接:{link}\n"
        text += f"提取码:{pwd}\n" if pwd else "无需提取码\n"
        text += f"有效期:{end_time}" if end_time else "永久有效"
        self.link_label = CaptionLabel(text, self)
        self.link_label.pixelFontSize = 15
        self.link_label.setOpenExternalLinks(True)
        self.link_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.link_label.setContextMenuPolicy(Qt.NoContextMenu)
        self.copy_btn = PushButton("复制分享链接", self)
        self.copy_btn.clicked.connect(lambda: self.copyLink(link))
        self.vBoxLayout.addWidget(self.link_label)
        self.vBoxLayout.addWidget(self.copy_btn)

    def copyLink(self, link):
        QtWidgets.QApplication.clipboard().setText(link)
        success(self, "已复制到剪贴板")
