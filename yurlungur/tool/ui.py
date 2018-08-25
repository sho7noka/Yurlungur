# -*- coding: utf-8 -*-
import inspect
import os
import sys
import traceback

import yurlungur
from yurlungur.core import env

if env.Qt():
    from yurlungur.Qt.QtCore import *
    from yurlungur.Qt.QtGui import *
    from yurlungur.Qt.QtWidgets import *
    from yurlungur.Qt.QtOpenGL import *


@env.Qt
def widgetPtr():
    import yurlungur.core.app
    app_name = yurlungur.core.application.__name__

    if app_name == "maya.cmds":
        from yurlungur.Qt import QtCompat
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


@env.Qt
def show(view):
    try:
        view.deleteLater()
    except:
        yurlungur.logger.log(view)

    try:
        __dark_view(view)

        if env.Max() or env.Unreal():
            __max_protect_show(view)
        else:
            view.show()
    except:
        view.deleteLater()
        yurlungur.logger.warn(traceback.print_exc())

    if not QApplication.instance():
        app = QApplication(sys.argv)
        __dark_view(view)

        if env.Max():
            __max_protect_show(view)
        else:
            view.show()

        sys.exit(app.exec_())


class __GCProtector(object):
    widgets = []


def __max_protect_show(w):
    w.setWindowFlags(Qt.WindowStaysOnTopHint)
    w.show()
    __GCProtector.widgets.append(w)


def __dark_view(view):
    local = os.path.dirname(
        os.path.dirname(inspect.currentframe().f_code.co_filename)
    )
    with open(local + "/user/dark.css") as f:
        view.setStyleSheet("".join(f.readlines()))
