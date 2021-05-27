# coding: utf-8
u"""
Qt 管理Windowモジュール
"""
import sys
import os
import inspect

import yurlungur
from yurlungur.core import env
from yurlungur.tool import logger


def main_window():
    """
    >>> import sys, yurlungur.Qt as Qt
    >>> app = Qt.QtWidgets.QApplication(sys.argv)
    >>> ptr = Qt.main_window()
    >>> view = Qt.QtWidgets.QMainWindow(ptr)
    >>> Qt.show(view)
    >>> app.exec_()

    :return:
    """
    import yurlungur

    app_name = yurlungur.application.__name__

    if app_name == "maya.cmds":
        from yurlungur.user.Qt import QtCompat
        from maya import OpenMayaUI

        ptr = long(OpenMayaUI.MQtUtil.mainWindow())
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

    if app_name == "pymxs":
        try:
            import qtmax
            return qtmax.GetQMaxMainWindow()
        except ImportError:
            import MaxPlus
            return MaxPlus.QtHelpers_GetQmaxMainWindow()

    if app_name == "substance_painter":
        import substance_painter
        return substance_painter.ui.get_main_window()

    if app_name == "rumba":
        import rumbapy
        return rumbapy.widget("MainWindow")

    if app_name == "renderdoc":
        import qrenderdoc
        return qrenderdoc.MainWindow

    return None


def show(view):
    """
    >>> view = yurlungur.Qt.QWidget()
    >>> yurlungur.Qt.show(view)

    :param view:
    :return:
    """
    try:
        view.deleteLater()
    except:
        logger.pprint(view)

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

    import Qt
    if not Qt.QtWidgets.QApplication.instance():
        app = Qt.QtWidgets.QApplication(sys.argv)
        __dark_view(view)

        if env.Max():
            __protect_show(view)
        else:
            view.show()

        sys.exit(app.exec_())


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


# from Qt import QtWidgets
from PySide2 import QtWidgets


class UIWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(UIWindow, self).__init__(parent)
        self.setWindowTitle("UI")
        self.setupUI()

    def setupUI(self):
        btn = QtWidgets.QPushButton("Hello World")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(btn)
        self.setLayout(self.layout)


def console():
    button = UIWindow()
    button.show()

if __name__ == "__main__":
    console()
