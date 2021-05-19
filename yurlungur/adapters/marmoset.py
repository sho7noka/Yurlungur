# coding: utf-8
import sys as __sys

try:
    __sys.modules[__name__] = __sys.modules["mset"]
    import yurlungur

    for obj in [obj for obj in dir(yurlungur) if obj[0] != "_" and obj != "Qt"]:
        setattr(__sys.modules[__name__], obj, getattr(yurlungur, obj))

    ismap = lambda obj: issubclass(obj, __sys.modules[__name__].BakerMap)
    isobj = lambda obj: issubclass(obj, __sys.modules[__name__].SceneObject)

except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, _, quit, connect = __App("marmoset")._actions

    __all__ = ["run", "quit", "connect"]
