# -*- coding: utf-8 -*-
import inspect
import yurlungur
import app
import enviroment as env


class YException(NotImplementedError):
    """
    >>> raise NotImplementedError(app.application)
    """
    pass


class YMObject(object):
    """command wrapper for any application"""

    def __getattr__(self, item):
        for cmd, _ in inspect.getmembers(app.application):
            if cmd == item:
                setattr(
                    yurlungur, cmd, (lambda str: dict(inspect.getmembers(app.application))[str])(cmd)
                )
                return getattr(yurlungur, item)

        return getattr(yurlungur, "")

    @property
    def module(self):
        """current application module"""
        return app.application.__name__

    def modules(self, mod=""):
        """switch application"""
        return app.exApplication(mod)


class MetaObject(type):
    def __new__(cls, name, bases, attrs):
        return super(MetaObject, cls).__new__(cls, name, bases, attrs)


class MetaAttr(type):
    _node = ''
    _attr = ''

    def __new__(cls, name, bases, attrs):
        return super(MetaAttr, cls).__new__(cls, name, bases, attrs)

    # def __new__(cls, *args, **kwds):
    #     if len(args) == 2:
    #         cls._node = args[0]
    #         cls._attr = args[1]
    #     elif len(args) == 1:
    #         cls._node, cls._attr = args[0].split('.')
    #     return super(MetaAttr, cls).__new__(cls, cls._node + "." + cls._attr)

    def __getitem__(self, idx):
        return MetaAttr(self._node, self._attr + "[{0}]".format(idx))


class MetaNode(type):
    def __new__(cls, name, bases, attrs):
        attrs["version"] = "0.0.1"
        return super(MetaNode, cls).__new__(cls, name, bases, attrs)

    def __getattr__(self, name):
        def _(self, name):
            return name

        return _


# dynamicClass
meta = YMObject()

_YObject = MetaObject("YObject", (object,), {"__doc__": MetaObject.__doc__})
_YNode = MetaNode("YNode", (object,), {"__doc__": MetaNode.__doc__})
_YParm = MetaAttr("YParm", (object,), {"__doc__": MetaAttr.__doc__})

if env.Maya():
    import maya.api.OpenMaya as om

    _YVector = type('_YVector', (om.MVector,), dict())
    _YMatrix = type('_YMatrix', (om.MMatrix,), dict())
    _YColor = type('_YColor', (om.MColor,), dict())

else:
    _YVector = type('_YVector', (
        meta.Vector if hasattr(meta, "Vector") else meta.Vector3,
    ), dict())

    _YMatrix = type('_YMatrix', (
        meta.Matrix if hasattr(meta, "Matrix") else meta.Matrix4,
    ), dict())

    _YColor = type('_YColor', (meta.Color,), dict())
