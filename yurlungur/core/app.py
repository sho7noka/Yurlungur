# -*- coding: utf-8 -*-
"""
detect embed python interpreter.
sys.executable or __import__
"""
import sys
from yurlungur.core.env import __import__

application = sys.executable

if __import__("maya.cmds"):
    import maya.cmds as cmds

    application = cmds

elif __import__("hou"):
    import hou

    application = hou

elif __import__("sd.api"):
    import sd.api as sdapi

    application = sdapi

elif __import__("bpy"):
    import bpy

    application = bpy

elif __import__("unreal"):
    import unreal

    application = unreal

elif __import__("UnityEngine"):
    import UnityEngine

    application = UnityEngine

elif __import__("nuke"):
    import nuke

    application = nuke

# Davinci & Fusion

elif __import__("c4d"):
    import c4d

    application = c4d

# Photoshop

elif __import__("pymxs"):
    import pymxs

    application = pymxs

elif __import__("rumba"):
    import rumba

    application = rumba

elif __import__("substance_painter"):
    import substance_painter

    application = substance_painter

elif __import__("mset"):
    import mset

    application = mset

elif __import__("renderdoc"):
    import renderdoc

    application = renderdoc

else:
    from yurlungur.tool import standalone

    application = standalone


def use(module):
    """
    set external application

    Args:
        module: str module

    Returns: None

    >>> import yurlungur
    >>> yurlungur.use("hou")
    """
    global application
    from yurlungur.core import env

    if module == "photoshop":
        from yurlungur.adapters import photoshop

        application = photoshop.app
    else:
        application = env.__import__(module)

    assert application, "application is not found."


def initialize():
    """
    name, stubs and load plugin
    https://docs.python.org/ja/3/reference/import.html#import-hooks
    """


def finalize():
    """"""
