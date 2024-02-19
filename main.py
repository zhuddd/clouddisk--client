import os
import sys
import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

import Index
from Common.config import cfg
from Common.ErrorBox import ErrorBox


def catch_exception(exc_type, exc_value, tb):
    ErrorMessage = traceback.format_exception(exc_type, exc_value, tb)
    w = ErrorBox('Error', "".join(ErrorMessage))
    w.exec_()
    app.quit()


if cfg.get(cfg.dpiScale) == "Auto":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
else:
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

# create application
sys.excepthook = catch_exception
app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
view = Index.Verify()
view.show()
sys.exit(app.exec_())