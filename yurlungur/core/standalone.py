import os
import sys
import optparse
import subprocess

from ..Qt.QtCore import *
from ..Qt.QtGui import *
from ..Qt.QtWidgets import *
from ..Qt import __binding__

import yurlungur as yr


class Initialize(object):

    def __init__(self, application):
        pass

    def call(self, ):
        subprocess.call(
            "C:\Program Files\Autodesk\Maya2017\bin\mayapy.exe -c \"{}\"".format(pystr)
        )

    def execfile(self, *args, **kwargs):
        pass

    def find_application(self):
        if sys.platform == 'linux':
            pass
        if sys.platform == 'win32':
            pass
        if sys.platform == 'cygwin':
            pass
        if sys.platform == 'darwin':
            pass

    def set_application(self, app_root):
        pass


def maya():
    # argparse
    # subprocess.call("hython {}".format(""))

    import maya.standalone
    maya.standalone.initialize(name='python')
    maya.standalone.uninitialize()


class WidgetHelper(QMainWindow):
    def __init__(self, parent=None):
        super(WidgetHelper, self).__init__(parent)

        self.setWindowTitle("{0} v{2} {1}".format(yr.name, yr.application.__name__, yr.version))
        self.setWindowFlags(Qt.Window)
        # self.setWindowIcon(QIcon("{}/res/jam.png".format(local)))
        self.setAttribute(Qt.WA_DeleteOnClose)
        # self.config = 'X:/.maya/{}/config.json'.format(toolName)

        # print os.path.join(os.path.dirname(sys.executable),
        #                    'Lib',
        #                    'site-packages',
        #                    __binding__,
        #                    'plugins',
        #                    'imageformats')


def main():
    app = QApplication(sys.argv)
    widget = WidgetHelper()
    yr.dark(widget)
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
