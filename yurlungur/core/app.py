# -*- coding: utf-8 -*-
import sys
from yurlungur.tool.util import __import__

application = sys.executable


def exApplication(module=""):
    application = ""

    if __import__("pysbs"):
        import pysbs
        application = pysbs

    if application == "":
        from yurlungur.core import standalone
        application = standalone

    return application


if "maya" in application:
    from maya import cmds

    application = cmds

elif "blender" in application:
    import bpy

    application = bpy
    
elif __import__("hou"):
    import hou

    application = hou

elif "UE4Editor" in application:
    import unreal

    application = unreal

elif "max" in application:
    import pymxs

    application = pymxs

else:
    application = exApplication()

__all__ = ["application", "exApplication"]
