# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
import subprocess
import re

import yurlungur
from yurlungur.Qt.QtCore import *
from yurlungur.Qt.QtGui import *
from yurlungur.Qt.QtWidgets import *
from yurlungur.Qt import __binding__
from yurlungur.tool import util
from yurlungur.core import enviroment as env


class Initialize(object):

    def call(self, pystr):
        pass

    def execfile(self, *args, **kwargs):
        pass

    def find_application(self):
        pass

    def set_application(self, application):
        pass

    def batch(self, appdir):
        for root, folders, files in os.walk(appdir):
            for file in files:
                if file.endswith(".exe"):
                    print file


def _cli(args):
    try:
        import argparse
    except:
        import optparse
        parser = optparse.OptionParser()

    parser = argparse.ArgumentParser()
    parser.add_argument("--convert",
                        help="Path to compiled Python module, e.g. my_ui.py")
    parser.add_argument("--compile",
                        help="Accept raw .ui file and compile with native "
                             "PySide2 compiler.")
    parser.add_argument("--stdout",
                        help="Write to stdout instead of file",
                        action="store_true")
    parser.add_argument("--stdin",
                        help="Read from stdin instead of file",
                        action="store_true")

    args = parser.parse_args(args)

    if args.stdout:
        raise NotImplementedError("--stdout")

    if args.stdin:
        raise NotImplementedError("--stdin")


def hython(pystr):
    assert os.path.exists(env.Houdini)
    subprocess.call(
        "{0}/bin/hython -c\"{1}\"".format(env.Houdini, pystr)
    )


def mayapy(pystr):
    assert os.path.exists(env.Maya)
    subprocess.call(
        "{0}/bin/mayapy -c \"{1};{2};{3}\"".format(
            env.Maya, "import maya.standalone;maya.standalone.initialize(name='python')",
            pystr, "maya.standalone.uninitialize()"
        )
    )


def maxpy(pystr):
    assert os.path.exists(env.Max)
    subprocess.call(
        "{0}/3dsmaxpy -c \"{1};{2}\"".format(env.Max, sys.path.append(yurlungur), pystr)
    )


def bpython(pystr):
    assert sys.version_info > (3, 5, 3), ('blender requires Python 3.5.3')
    assert os.path.exists(env.Blender)
    subprocess.call(
        "{0}.blender --python-expr {1} -b".format(env.Blender, pystr)
    )


class YurPrompt(QDockWidget):
    def __init__(self, parent=None):
        super(YurPrompt, self).__init__(parent)

        self.setWindowTitle("{0} v{2} {1}".format(yurlungur.name, yurlungur.application.__name__, yurlungur.version))
        self.setWindowFlags(Qt.Window)
        # self.setWindowIcon(QIcon(getattr(QStyle, "SP_DialogApplyButton")))
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.config = Initialize()
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


def main():
    app = QApplication(sys.argv)
    QTextCodec.setCodecForCStrings(QTextCodec.codecForLocale())
    # app.setWindowIcon(QIcon(getattr(QStyle, "SP_DialogApplyButton")))
    widget = YurPrompt()
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
