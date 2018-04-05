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
        self.item = item

    def __call__(self, *args, **kwargs):
        if hasattr(meta, "rename"):
            meta.rename(*args, **kwargs)
        raise NotImplementedError

    def attr(self):

        return YParm()

        raise NotImplementedError

    @property
    def attrs(self, *args, **kwargs):
        if hasattr(meta, "listAttr"):
            return meta.listAttr(*args, **kwargs)

        raise NotImplementedError

    @property
    def id(self):
        if hasattr(meta, "ls"):
            return meta.ls(self.item, uuid=1) or 0

        raise NotImplementedError


class YNode(_YNode):
    """connect-able object"""

    def __init__(self, node=None):
        self.node = node

    @classmethod
    def create(cls, *args, **kwargs):
        if hasattr(meta, "createNode"):
            return cls(meta.createNode(*args, **kwargs))

        raise NotImplementedError

    def delete(self, *args, **kwargs):
        if hasattr(meta, "delete"):
            meta.delete(self.node, *args, **kwargs)

        if hasattr(meta, "destroy"):
            meta.destroy()

        raise NotImplementedError

    def connect(self, *args, **kwargss):
        if hasattr(meta, "connectAttr"):
            return meta.connectAttr(*args, **kwargss)

        raise NotImplementedError

    def disconnect(self, *args, **kwargs):
        if hasattr(meta, "disconnectAttr"):
            return meta.disconnectAttr(*args, **kwargs)

        raise NotImplementedError

    def inputs(self):
        pass

    def outputs(self):
        pass


class YParm(_YParm):
    """parametric object"""

    def __init__(self, attr):
        self.attr = attr
        if hasattr(meta, "getAttr"):
            return meta.getAttr("")

        if hasattr(meta, "parm"):
            return meta.node().parm()

    def __getitem__(self, item):
        return item

    def __setitem__(self, key, value):
        return


class YFile(object):
    """save, load and export"""

    def __init__(self, file):
        self.file = file

    @property
    def filename(self):
        return os.path.basename(self.file)

    @property
    def filepath(self):
        return os.path.dirname(self.file)

    @classmethod
    def load(cls, *args, **kwargs):
        if hasattr(meta, "file"):
            return cls(partial(meta.file, i=1)(*args, **kwargs))

        if hasattr(meta, "hipFile"):
            return cls(meta.hipFile.load(*args, **kwargs))

        raise NotImplementedError

    @classmethod
    def save(cls, *args, **kwargs):
        if hasattr(meta, "file"):
            return cls(partial(meta.file, s=1)(*args, **kwargs))

        if hasattr(meta, "hipFile"):
            return cls(meta.hipFile.save(*args, **kwargs))

        raise NotImplementedError

    @property
    def current(self):
        if hasattr(meta, "file"):
            return meta.file(exn=1, q=1)

        raise NotImplementedError
