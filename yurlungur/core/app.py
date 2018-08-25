# -*- coding: utf-8 -*-
import platform
import sys

from yurlungur.core.env import __import__

application = sys.executable

__doc__ = "app modules"

def exApplication(module=""):
    application = ""

    if __import__(module):
        application = __import__(module)

    elif application == "":
        from yurlungur.core import standalone

        application = standalone

    return application


if "maya" in application:
    import maya.cmds as cmds

    application = cmds

elif __import__("hou"):
    import hou

    application = hou

elif "blender" in application:
    import bpy

    application = bpy

elif "Substance" in application:
    import sd

    application = sd

elif "UE4Editor" in application:
    import unreal

    application = unreal

elif "max" in application:
    import pymxs

    application = pymxs

else:
    if platform.python_implementation() == 'IronPython':
        import clr

        clr.AddReferenceByPartialName('UnityEngine')
        import UnityEngine as unity

        application = unity
    else:
        application = exApplication()

__all__ = ["application", "exApplication"]
