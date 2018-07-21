# -*- coding: utf-8 -*-
import sys
import time
from pprint import pformat
from logging import getLogger, Handler, INFO, WARNING, basicConfig

import yurlungur
from yurlungur.core import env

class GuiLogHandler(Handler):
    def __init__(self, *args, **kwargs):
        super(GuiLogHandler, self).__init__(*args, **kwargs)

        if env.Maya():
            from maya.OpenMaya import MGlobal
            self.MGlobal = MGlobal

    def emit(self, record):
        from yurlungur.tool.meta import meta
        
        msg = self.format(record)
        if record.levelno > WARNING:
            if hasattr(meta, "ops"):
                meta.ops.error.message('INVOKE_DEFAULT', type="Error", message=msg)
            elif env.Maya():
                self.MGlobal.displayError(msg)
            else:
                meta.ui.setStatusMessage(msg, severity=meta.severityType.Error)

        elif record.levelno > INFO:
            if hasattr(meta, "ops"):
                meta.ops.error.message('INVOKE_DEFAULT', type="Error", message=msg)
            elif env.Maya():
                self.MGlobal.displayWarning(msg)
            else:
                meta.ui.setStatusMessage(msg, severity=meta.severityType.Warning)

        else:
            if hasattr(meta, "ops"):
                meta.ops.error.message('INVOKE_DEFAULT', type="Error", message=msg)
            elif env.Maya():
                self.MGlobal.displayInfo(msg)
            else:
                meta.ui.setStatusMessage(msg, severity=meta.severityType.Message)


logger = getLogger(yurlungur.__name__)
logger.setLevel(INFO)
handler = GuiLogHandler()
logger.addHandler(handler)
basicConfig(level=INFO, stream=sys.stdout)


def info(obj):
    logger.info(pformat(obj))


def _progress():
    for i in range(1, 101):
        sys.stdout.flush()
        log = "\r%d%% (%d of %d)" % (i, i, 100)
        sys.stdout.write(log + "")
        sys.stdout.flush()
        time.sleep(0.01)
