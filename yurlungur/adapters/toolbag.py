# coding: utf-8
import sys as __sys

u"""
https://marmoset.co/posts/python-scripting-toolbag/
https://marmoset.co/python/reference.html#header-variables
https://marmoset.co/toolbag/history/
"""

try:
    __sys.modules[__name__] = __sys.modules["mset"]
    import yurlungur

    for obj in [obj for obj in dir(yurlungur) if obj[0] != "_" and obj != "Qt"]:
        setattr(__sys.modules[__name__], obj, getattr(yurlungur, obj))

    ismap = lambda obj: issubclass(obj, __sys.modules[__name__].BakerMap)
    isobj = lambda obj: issubclass(obj, __sys.modules[__name__].SceneObject)
    is4 = __sys.modules[__name__].getToolbagVersion() > 4000

    class Timeline(object):
        def __init__(self):
            self.timeline = __sys.modules[__name__].getTimeline()

        def __repr__(self):
            return self.timeline.currentFrame

        def __getitem__(self, val):
            return self


except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    _, run, quit, _ = __App("toolbag")._actions

    __all__ = ["run", "quit"]
