# -*- coding: utf-8 -*-
import sys

application = sys.executable


def exApplication(module=""):
    application = ""

    try:
        import pysbs
        application = pysbs
    except:
        pass

    if application == "":
        from yurlungur.core import standalone
        application = standalone
    return application


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

else:
    application = exApplication()

__all__ = ["application", "exApplication"]
