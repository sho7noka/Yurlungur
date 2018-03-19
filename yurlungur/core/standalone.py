# -*- coding: utf-8 -*-
import os
import sys
import optparse
import subprocess
import re

from ..Qt.QtCore import *
from ..Qt.QtGui import *
from ..Qt.QtWidgets import *
from ..Qt import __binding__

import yurlungur as yr
from yurlungur.tool import qtutil

class Initialize(object):

    def call(self, pystr):
        os.getcwd()

    def execfile(self, *args, **kwargs):
        pass

    def find_application(self):
        if sys.platform == 'linux':
            "/usr/autodesk/maya2015-x64"
        if sys.platform == 'win32':
            """C:/Program Files/Autodesk/Maya2017"""

            return {
                "adesk" : "C:/Program Files/Autodesk",
                "sidefx" : "C:/Program Files/Side Effects Software",
            }

        if sys.platform == 'darwin':
            "/Applications/Autodesk/maya2017/Maya.app/Contents"
        if sys.platform == 'cygwin':
            pass

    def set_application(self, application):
        pass


def hython(pystr):
    subprocess.call(
        "C:/Program Files/Side Effects Software/Houdini 16.5.323/bin/hython -c\"{0};{1}\"".format(sys.path.append(yr), pystr)
    )


def mayapy(pystr):
    initialize = "import maya.standalone;maya.standalone.initialize(name='python')"
    uninitialize = "maya.standalone.uninitialize()"

    subprocess.call(
        "C:/Program Files/Autodesk/Maya2017/bin/mayapy -c \"{0};{1};{2}\"".format(initialize, pystr, uninitialize)
    )


def maxpy(pystr):
    subprocess.call(
        "C:/Program Files/Autodesk/3ds Max 2018/3dsmaxpy -c \"{0};{1}\"".format(sys.path.append(yr), pystr)
    )


class YurPrompt(QDockWidget):
    def __init__(self, parent=None):
        super(YurPrompt, self).__init__(parent)

        self.setWindowTitle("{0} v{2} {1}".format(yr.name, yr.application.__name__, yr.version))
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
        yr.dark(self)

    def init_attrs(self):
        tmp = []
        for k, v in self.config.find_application().items():
            for app in os.listdir(v):
                tmp.append("")

        for app in list(set(tmp)):
            self.box_application.addItem(app)

        self.box_versions.addItem("aaa")

    def refresh_item(self):
        pass

    def reflesh_msg(self):
        self.status_bar.showMessage("")


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(getattr(QStyle, "SP_DialogApplyButton")))
    widget = YurPrompt()
    widget.show()
    sys.exit(app.exec_())
    yr.application.mel


if __name__ == '__main__':
    main()
