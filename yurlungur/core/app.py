# -*- coding: utf-8 -*-
from yurlungur.tool.util import *  # noQA

__all__ = ["application", "exApplication"]


def exApplication(module=""):
    """NO-Qt application"""
    application = ""
    try:
        import pysbs
        application = pysbs
    except:
        pass

    # return standalone
    if application == "":
        import standalone
        application = standalone
    return application


application = sys.executable
if "maya" in application:
    from maya import cmds, mel

    application = cmds

elif "houdini" in application or "hindie" in application:
    import hou

    application = hou

elif "UE4Editor" in application:
    import unreal

    application = unreal

elif "max" in application:
    import pymxs

    application = pymxs
    global on, off
    on = True
    off = False

else:
    application = exApplication()
