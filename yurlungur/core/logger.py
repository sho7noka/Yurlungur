# -*- coding: utf-8 -*-
from __future__ import print_function

import __builtin__
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
            else:
                meta.ui.setStatusMessage(msg, severity=meta.severityType.Error)

        elif record.levelno > INFO:
            if env.Maya():
                self.MGlobal.displayWarning(msg)
            else:
                meta.ui.setStatusMessage(msg, severity=meta.severityType.Warning)

        else:
            if env.Maya():
                self.MGlobal.displayInfo(msg)
            else:
                meta.ui.setStatusMessage(msg, severity=meta.severityType.Message)


# logger
logger = getLogger(yurlungur.__name__)
logger.setLevel(INFO)

# TODO: https://code.blender.org/2016/05/logging-from-python-code-in-blender/
if not env.Blender():
    handler = GuiLogHandler()
    logger.addHandler(handler)
basicConfig(level=INFO, stream=sys.stdout)


def log(obj):
    logger.info(pformat(obj))


def _progress():
    for i in range(1, 101):
        sys.stdout.flush()
        log = "\r%d%% (%d of %d)" % (i, i, 100)
        sys.stdout.write(log + "")
        sys.stdout.flush()
        time.sleep(0.01)
