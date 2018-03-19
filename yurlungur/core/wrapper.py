# -*- coding: utf-8 -*-
import inspect
import application
import yurlungur as yr


class YMObject(object):
    """command wrapper for any application"""

    def __getattr__(self, item):
        for cmd, _ in inspect.getmembers(application.application):
            if cmd == item:
                setattr(
                    yr, cmd, (lambda str: dict(inspect.getmembers(application.application))[str])(cmd)
                )
                return getattr(yr, item)
        return None

    @property
    def module(self):
        """current application module"""
        return application.application.__name__


class MetaYObject(type):
    def __new__(cls, name, bases, attrs):
        # attrs["name"] = cls
        # attrs["id"] = (None or 0)
        return super(MetaYObject, cls).__new__(cls, name, bases, attrs)

    def __getattr__(self, item):
        return item


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


class MetaYNode(type):
    def __new__(cls, name, bases, attrs):
        attrs["version"] = "0.0.1"
        return super(MetaYNode, cls).__new__(cls, name, bases, attrs)

    def __getattr__(self, name):
        def _(self, name):
            return name

        return _


# metaclass interface
_YObject = MetaYObject("YObject", (object,), {"__doc__": MetaYObject.__doc__})
_YNode = MetaYNode("YNode", (object,), {"__doc__": MetaYNode.__doc__})
_YParm = MetaAttribute("YParm", (object,), {"__doc__": MetaAttribute.__doc__})
