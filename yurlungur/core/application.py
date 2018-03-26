# -*- coding: utf-8 -*-
from yurlungur.tool.qtutil import *

__all__ = ["application", "exApplication"]
application = QCoreApplication.applicationName().lower()

if "maya" in application:
    from maya import cmds, mel, OpenMaya
    application = cmds

elif "houdini" in application or "hindie" in application:
    import hou
    application = hou

elif "max" in application:
    import pymxs
    application = pymxs

    on = True
    off = False

else:
    import standalone
    application = standalone


def exApplication(module=""):
    """NO-Qt application"""
    application = ""
    
    try:
        import bpy
        application = bpy
    except:
        pass

    try:
        import arnold
        application = arnold
    except:
        pass

    try:
        import pysbs
        application = pysbs
    except:
        pass

    try:
        import c4d
        application = c4d
    except:
        pass

    return application