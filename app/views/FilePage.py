import os
from uuid import uuid1

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import FlowLayout, RoundMenu, Action, MenuAnimationType, ScrollArea, BreadcrumbBar, FluentIcon, \
    DropDownPushButton

from app.Common import FileAction
from app.Common.FileAction import NewNameBox
from app.Common.StyleSheet import StyleSheet
from app.Common.Tost import error
from app.Common.GetDir import GetDir
from app.components.IconCard import IconCard
from app.Common.File import File
from app.views.SharePage import SharePage


class FilePage(QtWidgets.QWidget):
    filePath = QtCore.pyqtSignal(tuple)
    preview = QtCore.pyqtSignal(File)
    fileDownload = QtCore.pyqtSignal(File)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.tool_box = QWidget(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tool_box)
        self.tool_box.setLayout(self.horizontalLayout)
        self.dir = BreadcrumbBar(self)
        self.horizontalLayout.addWidget(self.dir, 1)
        self.menu_button = DropDownPushButton(FluentIcon.DOWN, '类型降序', self)
        self.horizontalLayout.addWidget(self.menu_button, 0)
        self.verticalLayout.addWidget(self.tool_box)
        self.ScrollArea = ScrollArea(self)
        self.ScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ScrollArea.setWidgetResizable(True)
        self.box = QtWidgets.QWidget()
        self.ScrollArea.setWidget(self.box)
        self.verticalLayout.addWidget(self.ScrollArea)

        self.sharePage = None
        self.disposable_key = False
        self.setObjectName("FilePage")
        self.setAcceptDrops(True)

        self.layout = FlowLayout(self.box)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setVerticalSpacing(20)
        self.layout.setHorizontalSpacing(10)
        StyleSheet.FILE.apply(self)

        self.page_data = {}

        self.addInterface("Home", 0)
        self.dir.currentItemChanged.connect(self.updatePage)

        self.getDir = GetDir()
        self.getDir.update.connect(self.setIconCard)
        self.getDir.err.connect(self.errFunc)
        self.getDir.get_dir(0)

        self.tmp = None  # type:File
        self.wait = None  # type:tuple[File,str]
        self.sort = 0

        self.update_action = None
        self.download_action = None
        self.cut_action = None
        self.copy_action = None
        self.paste_action = None
        self.delete_action = None
        self.rename_action = None
        self.new_folder_action = None
        self.preview_action = None
        self.share_action = None
        self.initAction()
        self.initSortMenu()

    def initAction(self):
        self.update_action = Action(FluentIcon.SYNC, '刷新')
        self.update_action.triggered.connect(self.updatePage)
        self.download_action = Action(FluentIcon.DOWNLOAD, '下载')
        self.download_action.triggered.connect(self.downloadAction)
        self.cut_action = Action(FluentIcon.CUT, '剪切')
        self.cut_action.triggered.connect(self.cutAction)
        self.copy_action = Action(FluentIcon.COPY, '复制')
        self.copy_action.triggered.connect(self.copyAction)
        self.paste_action = Action(FluentIcon.PASTE, '粘贴')
        self.paste_action.triggered.connect(self.pasteAction)
        self.delete_action = Action(FluentIcon.DELETE, '删除')
        self.delete_action.triggered.connect(self.deleteAction)
        self.rename_action = Action(FluentIcon.EDIT, '重命名')
        self.rename_action.triggered.connect(self.renameAction)
        self.new_folder_action = Action(FluentIcon.FOLDER_ADD, '新建文件夹')
        self.new_folder_action.triggered.connect(self.newfolderAction)
        self.preview_action = Action(FluentIcon.VIEW, '预览')
        self.preview_action.triggered.connect(self.viewAction)
        self.share_action = Action(FluentIcon.SHARE, '分享')
        self.share_action.triggered.connect(self.shareAction)

    def downloadAction(self):
        if self.tmp is not None:
            self.fileDownload.emit(self.tmp)

    def cutAction(self):
        if self.tmp is not None:
            self.wait = [self.tmp, "cut"]
            self.tmp = None

    def copyAction(self):
        if self.tmp is not None:
            self.wait = [self.tmp, "copy"]
            self.tmp = None

    def pasteAction(self):
        if self.wait is None:
            return
        key = self.dir.currentItem().routeKey
        act = self.wait[1]
        file = self.wait[0]
        r = FileAction.paste(file.id, self.page_data[key])
        if r.status_code != 200:
            try:
                error(self, r.json()["data"])
            except:
                error(self, "粘贴失败")
            self.updatePage()
            return
        if act == "cut":
            self.tmp = file
            self.deleteAction()
        self.updatePage()

    def deleteAction(self):
        if self.tmp is None:
            return
        r = FileAction.delete(self.tmp.id)
        if r.status_code != 200:
            try:
                error(self, r.json()["data"])
            except:
                error(self, "删除失败")
        self.updatePage()
        self.tmp = None

    def renameAction(self):
        if self.tmp is None:
            return
        w = NewNameBox(self, title="重命名", defaultText=self.tmp.name)
        if w.exec():
            r = FileAction.rename(self.tmp.id, w.text())
            if r.status_code != 200:
                try:
                    error(self, r.json()["data"])
                except:
                    error(self, "重命名失败")
        self.updatePage()
        self.tmp = None

    def newfolderAction(self):
        key = self.dir.currentItem().routeKey
        w = NewNameBox(self, title="新建文件夹")
        if w.exec():
            r = FileAction.newfolder(self.page_data[key], w.text())
            if r.status_code != 200:
                try:
                    error(self, r.json()["data"])
                except:
                    error(self, "新建文件夹失败")
            self.updatePage()
        self.tmp = None

    def viewAction(self):
        self.preview.emit(self.tmp)
        self.tmp = None

    def shareAction(self):
        file = self.tmp
        self.sharePage = SharePage(file)
        self.tmp = None
        self.sharePage.show()

    def initSortMenu(self):
        name = Action(FluentIcon.UP, '名称升序')
        name.triggered.connect(lambda: self.sortChange(1))
        name_down = Action(FluentIcon.DOWN, '名称降序')
        name_down.triggered.connect(lambda: self.sortChange(2))
        type = Action(FluentIcon.UP, '类型升序')
        type.triggered.connect(lambda: self.sortChange(3))
        type_down = Action(FluentIcon.DOWN, '类型降序')
        type_down.triggered.connect(lambda: self.sortChange(4))
        time = Action(FluentIcon.UP, '时间升序')
        time.triggered.connect(lambda: self.sortChange(5))
        time_down = Action(FluentIcon.DOWN, '时间降序')
        time_down.triggered.connect(lambda: self.sortChange(6))
        self.menu = RoundMenu(parent=self)
        self.menu.addAction(name)
        self.menu.addAction(name_down)
        self.menu.addAction(type)
        self.menu.addAction(type_down)
        self.menu.addAction(time)
        self.menu.addAction(time_down)
        self.menu_button.setMenu(self.menu)

    def sortChange(self, sort):
        self.sort = sort
        self.menu_button.setText(self.menu.actions()[sort - 1].text())
        self.menu_button.setIcon(self.menu.actions()[sort - 1].icon())
        self.updatePage()

    def dragEnterEvent(self, event):
        key = self.dir.currentItem().routeKey
        if isinstance(self.page_data[key], str):
            return
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            file_path = os.path.abspath(url.toLocalFile())
            self.filePath.emit((file_path, self.page_data[self.dir.currentItem().routeKey]))

    def addInterface(self, text: str, n):
        '''
        添加页面
        :param text:  页面名称
        :param n:  页面id
        :return:
        '''
        if not text:
            return
        uid = uuid1().hex
        self.page_data[uid] = n
        # 添加标签
        self.dir.addItem(uid, text)

    def updatePage(self, key=None):
        '''
        更新页面,如果key为None则使用当前页面的key
        :param key:
        :return:
        '''
        if key is None or key not in self.page_data.keys() or key is False:
            key = self.dir.currentItem().routeKey
        self.layout.takeAllWidgets()
        self.getDir.get_dir(self.page_data[key], isinstance(self.page_data[key], str), self.sort)

    def errFunc(self, err):
        error(self, err)

    def setIconCard(self, file: File):
        """
        将文件图标小部件添加到相应页面的布局中。
        """
        widget = IconCard(self.box, file)
        widget.left_clicked_double.connect(self.iconCardClick)
        # widget.left_clicked.connect(self.fileDownload.emit)
        widget.right_clicked.connect(self.contextMenuEvent)
        self.layout.addWidget(widget)

    def iconCardClick(self, data: File):
        """
        处理文件图标上的单击事件。
        """
        if data.folder:
            self.addInterface(data.name, data.id)
        else:
            self.preview.emit(data)

    def contextMenuEvent(self, e, file: File = None):
        self.tmp = file
        menu = RoundMenu(parent=self)
        menu.addAction(self.update_action)
        menu.addAction(self.new_folder_action)
        if self.wait is not None:
            menu.addAction(self.paste_action)
        if file is not None:
            menu.addAction(self.cut_action)
            menu.addAction(self.copy_action)
            menu.addAction(self.delete_action)
            menu.addAction(self.rename_action)
            menu.addAction(self.download_action)
            menu.addAction(self.preview_action)
            menu.addAction(self.share_action)
        menu.exec(e.globalPos(), aniType=MenuAnimationType.DROP_DOWN)
