# coding: utf-8
import sys as __sys

try:
    __sys.modules[__name__] = __sys.modules["pymxs"]
    import yurlungur

    for obj in [obj for obj in dir(yurlungur) if obj[0] != "_" and obj != "Qt"]:
        setattr(__sys.modules[__name__], obj, getattr(yurlungur, obj))
except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, quit, connect = __App("3dsmax")._actions

    __all__ = ["run", "shell", "quit", "connect"]


class Layer(object):
    def __init__(self, layer):
        self.layer = layer

    @property
    def keyframes(self):
        return Keyframe(self.layer)


class Keyframe(object):
    def __init__(self, layer):
        self.layer = layer
