# -*- coding: utf-8 -*-
import sys

try:
    import os
    import inspect
    import fnmatch
    import traceback
except:
    pass

import yurlungur
from yurlungur.core import env

if env.Qt():
    from yurlungur.Qt.QtCore import *
    from yurlungur.Qt.QtGui import *
    from yurlungur.Qt.QtWidgets import *

elif "MarvelousDesigner" in str(yurlungur.application):
    from PythonQt.QtCore import *
    from PythonQt.QtGui import *


@env.Qt
def widgetPtr():
    """
    >>> ptr = yurlungur.ui.widgetPtr()
    >>> view = yurlungur.Qt.QMainWindow(ptr)
    >>> memoryview.show()

    :return:
    """
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

    if app_name == "hou":
        import hou
        return hou.qt.mainWindow()

    if app_name == "sd.api":
        from yurlungur.adapters import substance
        return substance.qt.getMainWindow()

    if app_name == "nuke":
        return QApplication.activeWindow()

    return None


@env.Qt
def show(view):
    """
    >>> view = yurlungur.Qt.QWidget()
    >>> yurlungur.ui.show(view)

    :param view:
    :return:
    """
    try:
        view.deleteLater()
    except:
        yurlungur.logger.pprint(view)

    try:
        __dark_view(view)

        if env.Max():
            __protect_show(view)

        elif env.Unreal():
            import unreal
            unreal.parent_external_window_to_slate(view.winId())

        else:
            view.show()

    except:
        view.deleteLater()
        yurlungur.logger.warn(traceback.print_exc())

    if not QApplication.instance():
        app = QApplication(sys.argv)
        __dark_view(view)

        if env.Max():
            __protect_show(view)
        else:
            view.show()

        sys.exit(app.exec_())


class OpenGL(object):
    """
    >>> yurlungur.ui.OpenGL()
    """

    def __getattr__(self, item):
        def _getGL(mod):
            for cmd, _ in inspect.getmembers(mod):
                if fnmatch.fnmatch(item, "".join(["*", cmd])):
                    setattr(
                        self, cmd, (lambda str: dict(inspect.getmembers(mod))[str])(cmd)
                    )
                    return getattr(self, item)

        _tmp = []

        if env.Maya():
            from maya import OpenMayaRender as _mgl

            _tmp.extend(_mgl, _mgl.MHardwareRenderer.theRenderer().glFunctionTable())

        if env.Blender():
            import bgl

            _tmp.extend(bgl)

        for gl in _tmp:
            if _getGL(gl):
                return _getGL(gl)

        try:
            from OpenGL import GL as gl

            return gl
        except ImportError:
            import ctypes

            return ctypes.cdll.OpenGL32


class __GCProtector(object):
    widgets = []


def __protect_show(w):
    w.setWindowFlags(Qt.WindowStaysOnTopHint)
    w.show()
    __GCProtector.widgets.append(w)


def __dark_view(view):
    local = os.path.dirname(os.path.dirname(inspect.currentframe().f_code.co_filename))
    with open(local + "/user/dark.css") as f:
        view.setStyleSheet("".join(f.readlines()))
