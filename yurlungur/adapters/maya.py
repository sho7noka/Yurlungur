# coding: utf-8
u"""
# Maya on:
>>> yurlungur.node.create() == yurlungur.maya.node.create()
>>> yurlungur.nuke.node.create() # via rpc

# Nuke on:
>>> yurlungur.node.create() == yurlungur.nuke.node.create()
>>> yurlungur.maya.node.create() # via rpc
"""
import sys as __sys

try:
    __sys.modules[__name__] = __sys.modules["maya.cmds"]
    import yurlungur

    for obj in [obj for obj in dir(yurlungur) if obj[0] != "_" and obj != "Qt"]:
        setattr(__sys.modules[__name__], obj, getattr(yurlungur, obj))

except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, quit, connect = __App("maya")._actions

    __all__ = ["run", "shell", "quit", "connect"]
