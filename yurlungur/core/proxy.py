# -*- coding: utf-8 -*-
import os
from functools import partial
import inspect
import types

from wrapper import YMObject, _YObject, _YNode, _YParm
import yurlungur.tool.meta as meta
meta = YMObject()


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

    def __init__(self, node=None):
        self._node = node

    @classmethod
    def create(cls, *args, **kwargs):
        if hasattr(meta, "createNode"):
            return cls(meta.createNode(*args, **kwargs))

    def delete(self, *args, **kwargs):
        if hasattr(meta, "delete"):
            return meta.delete(*args, **kwargs)

        if hasattr(meta, "destroy"):
            return meta.destroy()

    def connect(self, *args, **kwargss):
        return

    def disconnect(self, *args, **kwargs):
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

    def __init__(self, f=None):
        self.file = f

    @property
    def file(self):
        return os.path.dirname(self.file)

    @property
    def path(self):
        return os.path.abspath(self.file)

    @classmethod
    def load(cls, *args, **kwargs):
        """load file"""

        if hasattr(meta, "file"):
            return cls(partial(meta.file, i=1)(*args, **kwargs))

        if hasattr(meta, "hipFile"):
            return cls(meta.hipFile.load(*args, **kwargs))

    @classmethod
    def save(cls, *args, **kwargs):
        """save file"""

        if hasattr(meta, "file"):
            return cls(partial(meta.file, s=1)(*args, **kwargs))

        if hasattr(meta, "hipFile"):
            return cls(meta.hipFile.save(*args, **kwargs))
