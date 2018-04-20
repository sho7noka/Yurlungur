# -*- coding: utf-8 -*-
import inspect

import yurlungur
from yurlungur.core import app, env
from yurlungur.tool import util


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
                    yurlungur, cmd,
                    (lambda str: dict(inspect.getmembers(app.application))[str])(cmd)
                )
                return getattr(yurlungur, item)

        return getattr(yurlungur, "")

    @property
    def module(self):
        """current application module"""
        return app.application.__name__


class ORM(object):
    def __getattr__(self, item):
        util.__db_loader()
        return getattr(self, item)


class MetaObject(type):
    def __new__(cls, name, bases, attrs):
        return super(MetaObject, cls).__new__(cls, name, bases, attrs)


class MetaAttr(type):
    def __new__(cls, name, bases, attrs):
        return super(MetaAttr, cls).__new__(cls, name, bases, attrs)


class MetaNode(type):
    def __new__(cls, name, bases, attrs):
        return super(MetaNode, cls).__new__(cls, name, bases, attrs)


# Dynamic Class
_YVector = _YMatrix = _YColor = OM = object
_YObject = MetaObject("YObject", (object,), {"__doc__": MetaObject.__doc__})
_YNode = MetaNode("YNode", (object,), {"__doc__": MetaNode.__doc__})
_YAttr = MetaAttr("YAttr", (object,), {"__doc__": MetaAttr.__doc__})

if env.Maya():
    import maya.api.OpenMaya as OM

    _YVector = type('_YVector', (OM.MVector,), dict())
    _YMatrix = type('_YMatrix', (OM.MMatrix,), dict())
    _YColor = type('_YColor', (OM.MColor,), dict())

elif env.Houdini() or env.Unreal():
    meta = YMObject()

    _YVector = type('_YVector', (
        meta.Vector if hasattr(meta, "Vector") else meta.Vector3,
    ), dict())

    _YMatrix = type('_YMatrix', (
        meta.Matrix if hasattr(meta, "Matrix") else meta.Matrix4,
    ), dict())

    _YColor = type('_YColor', (meta.Color,), dict())
