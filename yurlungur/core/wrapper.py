# -*- coding: utf-8 -*-
import inspect

import application
import yurlungur as yr

__doc__ = """
http://help.autodesk.com/view/MAYAUL/2017/JPN/?guid=GUID-55B63946-CDC9-42E5-9B6E-45EE45CFC7FC
https://symfoware.blog.fc2.com/blog-entry-1590.html
https://www.yoheim.net/blog.php?q=20160610
import os
print getattr(os, "path").abspath("")
"""

class YException(Exception):
    pass


class YMObject(object):
    """command wrapper for any application"""

    def __getattr__(self, item):
        for cmd, _ in inspect.getmembers(application.application):
            if cmd == item:
                setattr(
                    yr, cmd, (lambda str: dict(inspect.getmembers(application.application))[str])(cmd)
                )
                return getattr(yr, item)

        return getattr(yr, None)

    @property
    def module(self):
        """current application module"""
        return application.application.__name__

    def modules(self, mod=""):
        """switch application"""
        return application.exApplication(mod)


class MetaObject(type):
    def __new__(cls, name, bases, attrs):
        # attrs["name"] = cls
        # attrs["id"] = (None or 0)
        return super(MetaObject, cls).__new__(cls, name, bases, attrs)

    def __getattr__(self, item):
        return item

_YObject = MetaObject("YObject", (object,), {"__doc__": MetaObject.__doc__})


class MetaAttribute(type):
    _node = ''
    _attr = ''

    def __new__(cls, *args, **kwds):
        if len(args) == 2:
            cls._node = args[0]
            cls._attr = args[1]
        elif len(args) == 1:
            cls._node, cls._attr = args[0].split('.')
        return super(MetaAttribute, cls).__new__(cls, cls._node + "." + cls._attr)

    def __getitem__(self, idx):
        return MetaAttribute(self._node, self._attr + "[{0}]".format(idx))

    def get(self, **kwds):
        return YMObject().getAttr(self, **kwds)

    def set(self, *val, **kwds):
        YMObject().setAttr(self, *val, **kwds)

_YParm = MetaAttribute("YParm", (object,), {"__doc__": MetaAttribute.__doc__})


class MetaNode(type):
    def __new__(cls, name, bases, attrs):
        attrs["version"] = "0.0.1"
        return super(MetaNode, cls).__new__(cls, name, bases, attrs)

    def __getattr__(self, name):
        def _(self, name):
            return name

        return _

_YNode = MetaNode("YNode", (object,), {"__doc__": MetaNode.__doc__})

