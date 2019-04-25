# -*- coding: utf-8 -*-
import platform
import sys
import glob
from yurlungur.core.env import __import__

application = sys.executable
__doc__ = "app modules"


def exApplication(module=""):
    application = ""

    if __import__(module):
        application = __import__(module)

    elif application == "":
        from yurlungur.tool import standalone

        application = standalone

    elif application == "photoshop":
        import pip

        if platform.system() == "Windows":
            pip.main(["install", "comtypes"])
            from comtypes.client import GetActiveObject, CreateObject
            try:
                app = GetActiveObject('Photoshop.Application')
            except WindowsError:
                app = CreateObject("Photoshop.Application")

    return application


if "maya" in application:
    import maya.cmds as cmds

    application = cmds

elif __import__("hou"):
    import hou

    application = hou

elif "Substance" in application:
    import sd.api as sdapi

    application = sdapi


elif "UE4Editor" in application:
    import unreal

    application = unreal

elif "3dsmax" in application:
    import pymxs

    application = pymxs

elif "blender" in application:
    import bpy

    application = bpy

elif "UE4Editor" in application:
    import unreal

    application = unreal

elif "Nuke" in application:
    import nuke

    application = nuke

# elif __import__("DaVinciResolveScript"):
#     import DaVinciResolveScript
#
#     application = DaVinciResolveScript

else:
    if platform.python_implementation() == 'IronPython':
        import clr

        clr.AddReferenceByPartialName('UnityEngine')
        import UnityEngine as unity

        application = unity
    else:
        application = exApplication()

__all__ = ["application", "exApplication"]
