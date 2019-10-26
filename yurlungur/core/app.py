# -*- coding: utf-8 -*-
import sys
from yurlungur.core.env import __import__


class YException(NotImplementedError):
    """
    >>> raise NotImplementedError(application)
    """
    pass


application = sys.executable

if "maya" in application:
    import maya.cmds as cmds

    application = cmds

elif __import__("hou"):
    import hou

    application = hou

elif "Nuke" in application:
    import nuke

    application = nuke

# Photoshop

elif "Substance" in application:
    import sd.api as sdapi

    application = sdapi

elif "Cinema 4D" in application:
    import c4d

    application = c4d

elif "UE4Editor" in application:
    import unreal

    application = unreal

elif "3dsmax" in application:
    import pymxs

    application = pymxs

# Davinci

elif "Blender" in application:
    import bpy

    application = bpy

elif "MarvelousDesigner" in application:
    import MarvelousDesigner.MarvelousDesigner

    application = MarvelousDesigner.MarvelousDesigner()
    application.initialize()

else:
    from yurlungur.tool import standalone

    application = standalone


def use(module):
    """
    set external application
    :param module:
    :return:
    >>> import yurlungur
    >>> yurlungur.use("hou")
    """
    from yurlungur.core import env

    if module == "photoshop":
        from yurlungur.adapters import photoshop

        application = photoshop.app
    else:
        application = env.__import__(module)

    assert application, "application is not found."
