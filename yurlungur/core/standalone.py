# -*- coding: utf-8 -*-
import os
import sys
import inspect
import subprocess
import tempfile

import yurlungur

from yurlungur.core import enviroment as env
from yurlungur.Qt.QtCore import *
from yurlungur.Qt.QtGui import *
from yurlungur.Qt.QtWidgets import *
from yurlungur.Qt import __binding__

__all__ = map(lambda x: x[0], inspect.getmembers(sys.modules[__name__], inspect.isclass))
local = os.path.dirname(os.path.dirname(inspect.currentframe().f_code.co_filename))


def mayapy(pystr):
    assert os.path.getsize(env.MayaBin)
    subprocess.call(
        "{0}/bin/mayapy -c \"{1};{2};{3}\"".format(
            env.MayaBin, "import maya.standalone;maya.standalone.initialize(name='python')",
            "import sys; sys.path.append('{0}');".format(local) + pystr, "maya.standalone.uninitialize()"
        )
    )


def hython(pystr):
    assert os.path.getsize(env.HoudiniBin)
    subprocess.call(
        "{0}/bin/hython -c\"{1}\"".format(env.HoudiniBin, pystr)
    )


def maxpy(pystr):
    assert os.path.getsize(env.MaxBin)
    subprocess.call(
        "{0}/3dsmaxpy -c \"{1};{2}\"".format(env.MaxBin, sys.path.append(yurlungur), pystr)
    )


def bpython(pystr):
    assert sys.version_info > (3, 5, 3), ('blender requires Python 3.5.3') or os.path.getsize(env.BlenderBin)
    subprocess.call(
        "{0}.blender --python-expr {1} -b".format(env.BlenderBin, pystr)
    )


def uepython(project, pystr):
    assert os.path.getsize(env.UnrealBin) or os.path.exists(project)

    # temp
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.write(pystr)
    subprocess.call(
        "{0}/UE4Editor-Cmd {1} ExecutePythonScript = {2}".format(env.UnrealBin, project, pyfile)
    )


class YurPrompt(QDockWidget):
    def __init__(self, parent=None):
        super(YurPrompt, self).__init__(parent)

        self.setWindowTitle("{0} v{2} {1}".format(yurlungur.name, yurlungur.application.__name__, yurlungur.version))
        self.setWindowFlags(Qt.Window)
        # self.setWindowIcon(QIcon(getattr(QStyle, "SP_DialogApplyButton")))
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
        yurlungur.dark_view(self)

    def init_attrs(self):
        tmp = []
        # for k, v in self.config.find_application().items():
        #     for app in os.listdir(v):
        #         tmp.append("")

        for app in list(set(tmp)):
            self.box_application.addItem(app)

        self.box_versions.addItem("aaa")
        sys.stdout.write("\r%d" % 111)
        sys.stdout.flush()

    def refresh_item(self):
        pass

    def reflesh_msg(self):
        self.status_bar.showMessage("")


def cli(args):
    """
    parser.add_argument('path_root_src', \
            action='store', \
            nargs=None, \
            const=None, \
            default=None, \
            type=str, \
            choices=None, \
            help='Directory path where your taken photo files are located.', \
            metavar=None)
    """
    try:
        import argparse
    except ImportError:
        yurlungur.logger.warn("argparse is not found.")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("--dlg",
                        help="Accept raw .ui file and compile with native ",
                        action="store_true")
    parser.add_argument("--mayapy",
                        help="Read from stdin instead of file",
                        action="store_true")
    parser.add_argument("--hython",
                        help="Read from stdin instead of file",
                        action="store_true")
    parser.add_argument("--unrealpy",
                        help="Read from stdin instead of file",
                        action="store_true")
    parser.add_argument("--tests",
                        help="Read from stdin instead of file",
                        action="store_true")
    parser.add_argument("--install",
                        help="Read from stdin instead of file",
                        action="store_true")

    args = parser.parse_args(args)
    if args.dlg:
        main()

    if args.mayapy:
        mayapy()

    if args.hython:
        hython()

    if args.unrealpy:
        uepython()


def main(args=[]):
    app = QApplication(args)
    widget = YurPrompt()
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv[1:])
