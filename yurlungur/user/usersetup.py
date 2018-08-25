# encoding: utf-8
from __future__ import print_function
import sys
import os

PORT = 10000  # sample
USER = os.environ.get("APPDATA")
PTH = [p for p in os.listdir(USER) if os.path.isdir("{}/{}".format(USER, p))]
EGG = "{}/{}/debug-eggs/pycharm-debug.egg".format(USER, PTH[0 if len(PTH) == 1 else -1])
PDV = "{}/{}/helpers/pydev".format(USER, PTH[0 if len(PTH) == 1 else -1])

for lib in [EGG, PDV]:
    if lib not in sys.path:
        sys.path.insert(0, lib)

import pydevd


def main():
    try:
        try:
            import maya.cmds as cmds
            import maya.utils

            if not cmds.commandPort(':{}'.format(PORT), q=1):
                cmds.commandPort(n=':{}'.format(PORT))
                # maya.utils.executeDeferred(cmds.commandPort(n=':{}'.format(PORT)))
            print(cmds.commandPort(':{}'.format(PORT), q=1))

        except ImportError:
            import hou, hrpyc
            hrpyc.start_server(PORT, False, False)

        pydevd.stoptrace()
        pydevd.settrace(
            "localhost", port=PORT - 1, stdoutToServer=True, stderrToServer=True
        )
        print("trace start")

    except:
        pydevd.stoptrace()
        cmds.commandPort(n=':{}'.format(PORT), close=1)
        print("trace stop", "maya port {}".format(cmds.commandPort(':{}'.format(PORT), q=1)))


if __name__ == '__main__':
    main()
