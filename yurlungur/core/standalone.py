# -*- coding: utf-8 -*-
import os
import sys
import inspect
import subprocess
import tempfile
import yurlungur as yr

try:
    from yurlungur.Qt.QtCore import *
    from yurlungur.Qt.QtGui import *
    from yurlungur.Qt.QtWidgets import *
    from yurlungur.Qt import __binding__
except ImportError:
    QDockWidget = object

local = os.path.dirname(os.path.dirname(inspect.currentframe().f_code.co_filename))


def mayapy(pystr):
    assert os.path.getsize(yr.MayaBin)
    subprocess.call(
        "{0}/bin/mayapy -c \"{1};{2};{3}\"".format(
            yr.MayaBin, "import maya.standalone;maya.standalone.initialize(name='python')",
            "import sys; sys.path.append('{0}');".format(local) + pystr, "maya.standalone.uninitialize()"
        )
    )


def hython(pystr):
    assert os.path.getsize(yr.HoudiniBin)
    subprocess.call(
        "{0}/hython -c\"import sys; sys.path.append('{1}');{2}\"".format(yr.HoudiniBin, local, pystr)
    )


def maxpy(pystr):
    assert os.path.getsize(yr.MaxBin)
    subprocess.call(
        "{0}/3dsmaxpy -c \"{1};{2}\"".format(yr.MaxBin, sys.path.append(yr), pystr)
    )


def bpython(pystr):
    assert sys.version_info > (3, 5, 3), ('blender requires Python 3.5.3') or os.path.getsize(yr.BlenderBin)
    subprocess.call(
        "{0}.blender --python-expr {1} -b".format(yr.BlenderBin, pystr)
    )


def uepython(project, pystr):
    assert os.path.getsize(yr.UnrealBin) or os.path.exists(project)

    # temp
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.write(pystr)
    subprocess.call(
        "{0}/UE4Editor-Cmd {1} ExecutePythonScript = {2}".format(yr.UnrealBin, project, pyfile)
    )


class YurPrompt(QDockWidget):
    def __init__(self, parent=None):
        super(YurPrompt, self).__init__(parent)

        self.setWindowTitle("{0} v{2} {1}".format(yr.name, yr.application.__name__, yr.version))
        self.setWindowFlags(Qt.Window)
        self.setAttribute(Qt.WA_DeleteOnClose)
        # print os.path.join(os.path.dirname(sys.executable),
        #                    'Lib',
        #                    'site-packages',
        #                    __binding__,
        #                    'plugins',
        #                    'imageformats')
        self.init_widget()

    def init_widget(self):
        self.box_application = QComboBox()
        self.box_application.currentIndexChanged[str].connect(self.refresh_item)

        self.box_versions = QComboBox()
        self.btn_python = QPushButton("...")
        hLayout = QHBoxLayout()
        for w in [self.box_application, self.box_versions, self.btn_python]:
            hLayout.addWidget(w)

        self.text_edit = QTextEdit()
        vLayout = QVBoxLayout()
        for layout in [self.text_edit]:
            vLayout.addWidget(layout)

        self.status_bar = QStatusBar()
        sLayout = QVBoxLayout()
        self.status_bar.showMessage("Ready...")
        for layout in [self.status_bar]:
            sLayout.addWidget(self.status_bar)

        widget = QWidget()
        Alayout = QVBoxLayout()
        for layout in [hLayout, vLayout, sLayout]:
            Alayout.addLayout(layout)
        widget.setLayout(Alayout)
        self.setWidget(widget)

        self.init_attrs()
        # yr.__dark_view(self)

    def init_attrs(self):
        tmp = []
        for app in list(set(tmp)):
            self.box_application.addItem(app)

        self.box_versions.addItem("aaa")
        # sys.stdout.write("\r%d" % 1)
        sys.stdout.flush()

    def refresh_item(self):
        pass

    def reflesh_msg(self):
        self.status_bar.showMessage("")


def _cli(args):
    """
    command line parser
    """
    try:
        import argparse
    except ImportError:
        yr.logger.warn("argparse is not found.")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        prog='yr.cli',
        usage='Demonstration of argparser',  # プログラムの利用方法
        description='description',  # 引数のヘルプの前に表示
        epilog="{0} v.{1} {2}".format(yr.name, yr.version, sys.executable),  # 引数のヘルプの後で表示
        add_help=True,
    )
    parser.add_argument("--dialog", "-d",
                        help="Launch yr.widget if Qt is installed.",
                        action="store_true")
    parser.add_argument("--mayapy", "-ma",
                        help="Run Python from mayapy.",
                        nargs=1)
    parser.add_argument("--hython", "-hou",
                        help="Run Python from hython.",
                        nargs=1)
    parser.add_argument("--unrealpy", "-ue",
                        help="Run Python from unreal editor cmd.",
                        nargs=2)
    parser.add_argument("--tests",
                        help="Read from stdin instead of file",
                        action="store_true")

    args = parser.parse_args(args)
    if args.dialog:
        main()

    if args.mayapy:
        mayapy(args.mayapy[0])

    if args.hython:
        hython(args.hython[0])

    if args.unrealpy:
        project, expr = args.unrealpy
        uepython(project, expr)

    if args.tests:
        pass


def main(args=[]):
    if yr.Qt():
        app = QApplication(args)
        widget = YurPrompt()
        widget.show()
        sys.exit(app.exec_())
    else:
        yr.logger.warn("Qt isn't available")


if __name__ == '__main__':
    main(sys.argv[1:])

__all__ = map(lambda x: x[0], inspect.getmembers(sys.modules[__name__], inspect.isclass))
