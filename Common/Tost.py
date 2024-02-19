from PyQt5.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition


def success(parent,text: str ,duration=2000):
    InfoBar.success(
        title="",
        content=text,
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=duration,
        parent=parent
    )


def warning(parent,text: str,duration:2000):
    InfoBar.warning(
        title="",
        content=text,
        orient=Qt.Horizontal,
        isClosable=True,  # disable close button
        position=InfoBarPosition.TOP,
        duration=duration,
        parent=parent
    )


def error(parent,text: str,duration=2000):
    InfoBar.error(
        title="",
        content=text,
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=duration,
        parent=parent
    )