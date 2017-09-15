
from __future__ import print_function
import sys
import traceback

from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtWidgets import *

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from hutil.Qt.QtCore import *
from hutil.Qt.QtGui import *
from hutil.Qt.QtWidgets import *


def hou_main_window():
    pass


def maya_main_window():
    try:
        from Qt.QtCompat import *
    except: 
        from shiboken2 import wrapInstance

    ptr = long(OpenMayaUI.MQtUtil.mainWindow())
    return wrapInstance(ptr, QWidget)
 

def max_protect_window(w):
    w.setWindowFlags(Qt.WindowStaysOnTopHint)
    w.show()
    _GCProtector.widgets.append(w)


class _GCProtector(object):
    """GCプロテクター"""
    widgets = []


def show(cls):
    try:
        view.deleteLater()
    except:
        pass

    view = cls
    
    try:
        view.show()
    except:
        view.deleteLater()
        traceback.print_exc()

    if not QApplication.instance():
        app = QApplication(sys.argv)
        view.show()
        sys.exit(app.exec_())