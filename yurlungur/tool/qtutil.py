# -*- coding: utf-8 -*-
import sys
import os
import traceback
import inspect

from ..Qt.QtCore import *
from ..Qt.QtGui import *
from ..Qt.QtWidgets import *

import yurlungur.core.application


class _GCProtector(object):
    """GCプロテクター"""
    widgets = []


def max_protect_window(w):
    w.setWindowFlags(Qt.WindowStaysOnTopHint)
    w.show()
    _GCProtector.widgets.append(w)


def main_window():
    app_name = yurlungur.core.application.__name__

    if app_name == "maya.cmds":
        from ..Qt import QtCompat
        from maya import OpenMayaUI
        ptr = long(OpenMayaUI.MQtUtil.mainWindow())
        return QtCompat.wrapInstance(ptr, QWidget)

    if app_name == "pymxs":
        import MaxPlus
        return MaxPlus.QtHelpers_GetQmaxMainWindow()
        # MaxPlus.NotifyQWidgetModalityChange(w, false)
        # MaxPlus.MakeQWidgetDockable(w, 14)

    if app_name == "hou":
        import hou
        return hou.qt.mainWindow()

    return None


def show(view):
    try:
        view.deleteLater()
    except:
        pass

    try:
        view.show()
    except:
        view.deleteLater()
        traceback.print_exc()

    if not QApplication.instance():
        app = QApplication(sys.argv)
        dark(view)
        view.show()
        sys.exit(app.exec_())


def dark(view):
    local = os.path.dirname(
        os.path.dirname(inspect.currentframe().f_code.co_filename)
    )
    with open(local + "/user/dark.css") as f:
        view.setStyleSheet("".join(f.readlines()))
