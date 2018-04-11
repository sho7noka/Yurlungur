# -*- coding: utf-8 -*-
from yurlungur.tool.util import *  # noQA
import yurlungur.Qt as qt

__all__ = ["application", "exApplication", "isQt"]

isQt = any([qt.IsPyQt4, qt.IsPyQt5, qt.IsPySide, qt.IsPySide2])

def exApplication(module=""):
    """NO-Qt application"""
    application = ""

    try:
        import unreal
        application = unreal
    except:
        pass

    try:
        import bpy
        application = bpy
    except:
        pass

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
    from maya import cmds, mel, OpenMaya
    application = cmds

elif "houdini" in application or "hindie" in application:
    import hou

    application = hou

elif "max" in application:
    import pymxs

    application = pymxs
    global on, off
    on = True
    off = False

else:
    application = exApplication()
