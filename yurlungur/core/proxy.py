# -*- coding: utf-8 -*-
import functools
import inspect

from wrapper import YMObject, _YObject, _YNode, _YParm
import yurlungur.tool.meta as meta



class YObject(_YObject):
    """base class"""

    def __init__(self, item):
        self._item = item

    @property
    def name(self):
        return self._item

    def name(cls, _name):
        return (
                super(YObject, self).renme(_name) or
                super(YObject, self).rename(cls._item, _name) or
                super(YObject, self).rame(_name)
        )

    @property
    def id(self):
        return (
                YMObject().ls(self, uuid=1) or 0
        )


class YNode(_YNode):
    """connect-able object"""

    def __init__(self, node):
        self._node = node

    @staticmethod
    def create(self, *args, **keys):
        meta.createNode(args, keys)
        return self._node
        # return super(YNode, self)

    def delete(self, *args):
        return (
                super(YNode, self).destroy() or
                super(YNode, self).delete(args)
        )

    def connect(self, **keys):
        return

    def disconnect(self, **keys):
        return


class YParm(_YParm):
    """parametric object"""

    # def __new__():
    #     return cmds.directionalLight(*args, **kwargs)

    def __getitem__(self, item):
        return item

    def __setitem__(self, key, value):
        return


class YFile(object):
    """save, load and export"""

    def load(self, *args, **kwargs):
        """load file"""
        if hasattr(YMObject(), "file"):
            return YMObject().file(kwargs)

        if hasattr(YMObject(), "hipFile"):
            return YMObject().hipFile.load(args, kwargs)

    def save(self, *args, **keys):
        return (
                YMObject().file or
                YMObject().hipFile.save or
                YMObject().rame(_name)
        )

    def export(self, *args, **keys):
        return (

        )
