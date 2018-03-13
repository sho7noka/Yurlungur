# -*- coding: utf-8 -*-

import sys
import traceback
import os
import inspect

from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtWidgets import *

class _GCProtector(object):
    """GCプロテクター"""
    widgets = []

def max_protect_window(w):
    w.setWindowFlags(Qt.WindowStaysOnTopHint)
    w.show()
    _GCProtector.widgets.append(w)


def maya_main_window():
    """get pointer for maya widget"""
    from Qt import QtCompat
    ptr = long(OpenMayaUI.MQtUtil.mainWindow())
    return QtCompat.wrapInstance(ptr, QWidget)


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
    local = os.path.dirname(inspect.currentframe().f_code.co_filename)
    with open(local + "/dark.css") as f:
        view.setStyleSheet("".join(f.readlines()))