# -*- coding: utf-8 -*-
import sys
import time
import pprint
import logging
import yurlungur

logger = logging.getLogger(yurlungur.__name__)
logger.setLevel(logging.INFO)


def info(obj):
    return logger.info(pprint.pformat(obj))


def _progress():
    for i in range(1, 101):
        sys.stdout.flush()
        log = "\r%d%% (%d of %d)" % (i, i, 100)
        sys.stdout.write(log + "")
        sys.stdout.flush()
        time.sleep(0.01)


class _GuiLogHandler(logging.Handler):
    def __init__(self):
        super(_GuiLogHandler, self).__init__()

        if yurlungur.env.Maya():
            from maya.OpenMaya import MGlobal
            self.MGlobal = MGlobal

    def emit(self, record):
        msg = self.format(record)
        if record > logging.WARNING:
            if yurlungur.env.Maya():
                self.MGlobal.displayError(msg)

            if yurlungur.env.Blender():
                yurlungur.meta.ops.error.message('INVOKE_DEFAULT', type="Error", message=msg)

            if yurlungur.env.Houdini():
                yurlungur.meta.ui.setStatusMessage(msg, severity=meta.severityType.Error)

        elif record > logging.INFO:
            if yurlungur.env.Maya():
                self.MGlobal.displayWarning(msg)

            if yurlungur.env.Blender():
                yurlungur.meta.ops.error.message('INVOKE_DEFAULT', type="Error", message=msg)

            if yurlungur.env.Houdini():
                yurlungur.meta.ui.setStatusMessage(msg, severity=meta.severityType.Warning)

        else:
            if yurlungur.env.Maya():
                self.MGlobal.displayInfo(msg)

            if yurlungur.env.Blender():
                yurlungur.meta.ops.error.message('INVOKE_DEFAULT', type="Error", message=msg)

            if yurlungur.env.Houdini():
                yurlungur.meta.ui.setStatusMessage(msg, severity=meta.severityType.Message)


# logger.addHandler(_GuiLogHandler)
