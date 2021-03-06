# coding: utf-8
import sys as __sys

try:
    __sys.modules[__name__] = __sys.modules["mset"]

    ismap = lambda obj: issubclass(obj, __sys.modules[__name__].BakerMap)
    isobj = lambda obj: issubclass(obj, __sys.modules[__name__].SceneObject)

except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, _, end, connect = __App("marmoset")._actions

    __all__ = ["run", "end", "connect"]
