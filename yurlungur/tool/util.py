# -*- coding: utf-8 -*-
import sys
import os
import re
import string
import itertools
import traceback
import functools
import time
import inspect
import cProfile

try:
    import builtins
except ImportError:
    import __builtin__ as builtins


def iterator(l0, l1):
    """shallow iteration"""
    for a, b in itertools.product(l0, l1):
        yield (a, b)


def make_completer(mod):
    header = "\"\"\"this document generated by internal module.\"\"\"\n\n\n"

    local = os.path.dirname(os.path.dirname(inspect.currentframe().f_code.co_filename))
    completer = os.path.join(local, "user", "completer.pyi").replace(os.sep, "/")

    with open(completer, "w") as f:
        f.write(header)

        for fn, _ in inspect.getmembers(mod):
            if fn.startswith("_"):
                continue

            f.write("def {0}(*args, **kwargs):\n".format(fn))
            f.write("   \"\"\"{0}\"\"\"\n".format(inspect.getdoc(fn)))
            f.write("   pass\n\n")


def analyze(func):
    @functools.wraps(func)
    def Wrapper(*args, **kw):
        try:
            ret = func(*args, **kw)
            return ret
        except:
            print(traceback.format_exc())
        return

    return Wrapper


def timer(func):
    @functools.wraps(func)
    def Wrapper(*args, **kw):
        print('{0} start'.format(func.__name__))
        start_time = time.clock()
        ret = func(*args, **kw)
        end_time = time.clock()
        print('\n{0}: {1:,f}s'.format("total: ", (end_time - start_time)))
        return ret

    return Wrapper


from yurlungur.Qt.QtCore import *
from yurlungur.Qt.QtGui import *
from yurlungur.Qt.QtWidgets import *


class _GCProtector(object):
    widgets = []


def max_protect_window(w):
    w.setWindowFlags(Qt.WindowStaysOnTopHint)
    w.show()
    _GCProtector.widgets.append(w)


def qmain_window():
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
        dark_view(view)
        view.show()
        sys.exit(app.exec_())


def dark_view(view):
    local = os.path.dirname(
        os.path.dirname(inspect.currentframe().f_code.co_filename)
    )
    with open(local + "/user/dark.css") as f:
        view.setStyleSheet("".join(f.readlines()))
