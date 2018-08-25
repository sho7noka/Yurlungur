# -*- coding: utf-8 -*-
from __future__ import print_function

try:
    import __builtin__
except ImportError:
    import builtins as __builtins__

import sys
import time
from logging import (
    getLogger, Handler, INFO, WARNING, basicConfig
)
from pprint import pformat

import yurlungur
from yurlungur.core import env


class GuiLogHandler(Handler):
    def __init__(self, *args, **kwargs):
        super(GuiLogHandler, self).__init__(*args, **kwargs)

        if env.Maya():
            import maya.OpenMaya as om
            self.MGlobal = om.MGlobal

    def emit(self, record):
        from yurlungur.tool.meta import meta

        msg = self.format(record)
        if record.levelno > WARNING:
            if env.Maya():
                self.MGlobal.displayError(msg)
            elif env.Houdini():
                meta.ui.setStatusMessage(msg, severity=meta.severityType.Error)
            elif env.Unreal():
                meta.log_error(msg)
            elif env.Unity():
                meta.Debug.LogError(msg)

        elif record.levelno > INFO:
            if env.Maya():
                self.MGlobal.displayWarning(msg)
            elif env.Houdini():
                meta.ui.setStatusMessage(msg, severity=meta.severityType.Warning)
            elif env.Unreal():
                meta.log_warning(msg)
            elif env.Unity():
                meta.Debug.LogWarning(msg)

        else:
            if env.Maya():
                self.MGlobal.displayInfo(msg)
            elif env.Houdini():
                meta.ui.setStatusMessage(msg, severity=meta.severityType.Message)
            elif env.Unreal():
                meta.log(msg)
            elif env.Unity():
                meta.Debug.Log(msg)


# logger
logger = getLogger(yurlungur.__name__)
logger.setLevel(INFO)

# TODO: https://code.blender.org/2016/05/logging-from-python-code-in-blender/
if not env.Blender():
    handler = GuiLogHandler()
    logger.addHandler(handler)
basicConfig(level=INFO, stream=sys.stdout)


def log(*msgs):
    logger.info(pformat(*msgs))


def print(*args):
    __builtin__.print(pformat(*args))


def _progress():
    for i in range(1, 101):
        sys.stdout.flush()
        log = "\r%d%% (%d of %d)" % (i, i, 100)
        sys.stdout.write(log + "")
        sys.stdout.flush()
        time.sleep(0.01)
