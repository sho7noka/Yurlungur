# coding: utf-8
u"""
Qt 管理Windowモジュール
"""
import sys
import os
import inspect

from yurlungur.core import env
from yurlungur.tool import logger


def main_window():
    """
    >>> import sys, yurlungur
    >>> app = yurlungur.Qt.QtWidgets.QApplication(sys.argv)
    >>> ptr = yurlungur.Qt.main_window()
    >>> view = yurlungur.Qt.QtWidgets.QMainWindow(ptr)
    >>> yurlungur.Qt.show(view)
    >>> sys.exit(app.exec_())
    :return:
    """
    import yurlungur
    app_name = yurlungur.application.__name__
    logger.pprint(app_name)

    if app_name == "maya.cmds":
        from yurlungur.user.Qt import QtCompat
        from maya import OpenMayaUI

        if sys.version_info[0] < 3:
            ptr = long(OpenMayaUI.MQtUtil.mainWindow())
        else:
            ptr = int(OpenMayaUI.MQtUtil.mainWindow())

        return QtCompat.wrapInstance(ptr, QWidget)

    if app_name == "sd.api":
        from yurlungur.adapters import substance_designer
        return substance_designer.qt.getMainWindow()

    if app_name == "hou":
        import hou
        return hou.qt.mainWindow()

    if app_name == "nuke":
        return QApplication.activeWindow()

    if app_name == "fusion":
        try:
            import fusionscript
        except ImportError:
            import PeyeonScript as fusionscript

        fusion = fusionscript.scriptapp('Fusion')
        return fusion.GetMainWindow()

    if app_name == "renderdoc":
        import qrenderdoc
        return qrenderdoc.MainWindow

    if app_name == "substance_painter":
        import substance_painter
        return substance_painter.ui.get_main_window()

    if app_name == "pymxs":
        try:
            import qtmax
            return qtmax.GetQMaxMainWindow()
        except ImportError:
            import MaxPlus
            return MaxPlus.QtHelpers_GetQmaxMainWindow()

    if app_name == "modo":
        import lxifc
        return lxifc.CustomView

    return None


def show(view):
    """
    >>> view = yurlungur.Qt.QtWidgets.QWidget()
    >>> yurlungur.Qt.show(view)

    :param view:
    :return:
    """
    # try:
    #     view.deleteLater()
    # except:
    #     logger.pprint(view)

    def show_(view):
        __dark_view(view)

        if env.Max():
            __protect_show(view)

        elif env.Unreal():
            import unreal
            unreal.parent_external_window_to_slate(view.winId())

        else:
            view.show()

    from yurlungur.user import Qt
    if not Qt.QtWidgets.QApplication.instance():
        app = Qt.QtWidgets.QApplication(sys.argv)
        show_(view)
        sys.exit(app.exec_())
    else:
        show_(view)


class __GCProtector(object):
    widgets = []


def __protect_show(w):
    from yurlungur.user import Qt
    w.setWindowFlags(Qt.QtCore.Qt.WindowStaysOnTopHint)
    w.show()
    __GCProtector.widgets.append(w)


def __dark_view(view):
    local = os.path.dirname(os.path.dirname(inspect.currentframe().f_code.co_filename))
    with open(local + "/user/dark.css") as f:
        view.setStyleSheet("".join(f.readlines()))
