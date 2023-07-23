# -*- coding: utf-8 -*-
import sys
from logging import (
    getLogger, Handler, INFO, WARNING, basicConfig
)
from pprint import pformat

try:
    from yurlungur.core import env
except ImportError:
    Handler = object


def pprint(*msgs):
    """

    Args:
        *msgs:

    Returns:

    """
    print (pformat(msgs))


class GuiLogHandler(Handler):
    """
    Log Handler each application
    """

    def __init__(self, *args, **kwargs):
        super(GuiLogHandler, self).__init__(*args, **kwargs)
        if env.Maya():
            import maya.utils, maya.OpenMaya
            maya.utils.formatGuiResult = pformat
            self.MGlobal = maya.OpenMaya.MGlobal

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
                meta.engine.Debug.LogError(msg)

            elif env.Nuke():
                meta.error(msg)

            elif env.C4D():
                meta.modules.net.SetErrorLevel(False, False, True)

            elif env.Max():
                meta.print_(msg, True, False)

            elif env.Toolbag():
                meta.err(msg)

            elif env.Painter():
                meta.logging.error(msg)

            elif env.RenderDoc():
                meta.LogMessage(meta.LogType.Error, "", file, 0, msg)

        elif record.levelno > INFO:
            if env.Maya():
                self.MGlobal.displayWarning(msg)

            elif env.Houdini():
                meta.ui.setStatusMessage(msg, severity=meta.severityType.Warning)

            elif env.Unreal():
                meta.log_warning(msg)

            elif env.Unity():
                meta.engine.Debug.LogWarning(msg)

            elif env.Nuke():
                meta.warning(msg)

            elif env.C4D():
                meta.modules.net.SetErrorLevel(False, True, False)

            elif env.Max():
                meta.print_(msg, True, False)

            elif env.Toolbag():
                meta.fail(msg)

            elif env.Painter():
                meta.logging.warning(msg)

            elif env.RenderDoc():
                meta.LogMessage(meta.LogType.Warning, "", file, 0, msg)

        else:
            if env.Maya():
                self.MGlobal.displayInfo(msg)

            elif env.Houdini():
                meta.ui.setStatusMessage(msg, severity=meta.severityType.Message)

            elif env.Unreal():
                meta.log(msg)

            elif env.Unity():
                meta.engine.Debug.Log(msg)

            elif env.Nuke():
                meta.debug(msg)

            elif env.C4D():
                meta.modules.net.SetErrorLevel(True, False, False)

            elif env.Max():
                meta.print_(msg, False, True)

            elif env.Toolbag():
                meta.log(msg)

            elif env.Painter():
                meta.logging.info(msg)

            elif env.RenderDoc():
                meta.LogMessage(meta.LogType.Warning.Debug, "", file, 0, msg)



if env.Substance():
    import sd

    logger = sd.getContext().getLogger()
    Warning = sd.logger.LogLevel.Warning

else:
    import yurlungur

    logger = getLogger(yurlungur.__name__)
    logger.setLevel(INFO)

    handler = GuiLogHandler()
    logger.addHandler(handler)
    # TODO: switch to stdout
    basicConfig(level=INFO, stream=sys.stdout)
