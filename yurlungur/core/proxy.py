# -*- coding: utf-8 -*-
import os
from functools import partial

from yurlungur.core.wrapper import (
    YMObject, YException, _YObject, _YNode, _YAttr
)

meta = YMObject()


class YObject(_YObject):
    """base class
    >>> obj = YObject("pCone")
    >>> obj("cone")
    """

    def __init__(self, item):
        if hasattr(meta, "objExists"):
            assert meta.objExists(item), "{} not found".format(item)
            self.item = item

        if hasattr(meta, "root"):
            assert meta.node(item), "{} not found".format(item)
            self.item = item

        if hasattr(meta, "Actor"):
            assert meta.Actor(item), "{} not found".format(item)
            self.item = item

    @property
    def name(self):
        return self.item

    def __call__(self, *args, **kwargs):
        if hasattr(meta, "rename"):
            return meta.rename(self.item, *args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(self.item).setName(*args, **kwargs)

        if hasattr(meta, "Actor"):
            return meta.Actor(self.item).rename(*args, **kwargs)

    def attr(self, val, *args, **kwargs):
        if hasattr(meta, "getAttr"):
            return YAttr(
                meta.getAttr(self.name + "." + val, *args, **kwargs), self.name, val
            )

        if hasattr(meta, "root"):
            return YAttr(
                meta.node(self.name).parm(val).eval(), self.name, val
            )

        if hasattr(meta, "Actor"):
            return YAttr
            self.get_editor_property(val)

        raise YException

    def __getattr__(self, item):
        if hasattr(meta, "getAttr"):
            return YAttr(
                meta.getAttr(self.name + "." + item), self.name, item
            )

        if hasattr(meta, "root"):
            return YAttr(
                meta.node(self.name).parm(item).eval(), self.name, item
            )

        if hasattr(meta, "Actor"):
            return YAttr

        raise YException

    @property
    def attrs(self, *args, **kwargs):
        if hasattr(meta, "listAttr"):
            return meta.listAttr(*args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(self.item).parms()

        if hasattr(meta, "Actor"):
            return meta.Actor(self.name).get_editor_property()

        raise YException

    @property
    def id(self):
        if hasattr(meta, "ls"):
            return meta.ls(self.name, uuid=1)[0] or 0

        if hasattr(meta, "root"):
            return meta.node(self.name).sessionId() or 0

        if hasattr(meta, "Actor"):
            return meta.Actor(self.name).tags

        raise YException


class YNode(YObject):
    """connect-able object"""

    def __init__(self, item):
        super(YNode, self).__init__(item)
        self.item = item

    @classmethod
    def create(cls, *args, **kwargs):
        if hasattr(meta, "createNode"):
            return cls(meta.createNode(*args, **kwargs))

        if hasattr(meta, "root"):
            return cls(meta.node(cls.item).createNode(*args, **kwargs))

        raise YException

    def delete(self, *args, **kwargs):
        if hasattr(meta, "delete"):
            meta.delete(self.item, *args, **kwargs)

        if hasattr(meta, "root"):
            meta.node(self.item).destroy()

    def connect(self, *args, **kwargss):
        if hasattr(meta, "connectAttr"):
            return meta.connectAttr(*args, **kwargss)

        if hasattr(meta, "root"):
            return

        raise YException

    def disconnect(self, *args, **kwargs):
        if hasattr(meta, "disconnectAttr"):
            return meta.disconnectAttr(*args, **kwargs)

        raise YException

    def inputs(self, *args, **kwargs):
        if hasattr(meta, "listConnections"):
            return partial(meta.listConnections, s=1)(*args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(self.name).inputs()

        raise YException

    def outputs(self):
        if hasattr(meta, "listConnections"):
            return partial(meta.listConnections, d=1)(*args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(self.name).outputs()

        raise YException


class YAttr(_YAttr):
    """parametric object"""

    def __init__(self, *args, **kwargs):
        self.vals = args

    def __getitem__(self, idx):
        return self.vals[idx]

    def set(self, *args, **kwargs):
        assert len(self.vals) > 2, "parameter is invalid."
        obj, val = self.vals[1:]

        if hasattr(meta, "setAttr"):
            return meta.setAttr(obj + "." + val, *args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(obj).parm(val).set(*args, **kwargs)

        raise YException

    def add(self):
        pass

    @property
    def value(self):
        return self.vals


class YFile(object):
    """save, load and export"""

    def __init__(self, file=""):
        self.file = file

    @classmethod
    def load(cls, *args, **kwargs):
        if hasattr(meta, "file"):
            return cls(partial(meta.file, i=1)(*args, **kwargs))

        if hasattr(meta, "hipFile"):
            return cls(meta.hipFile.load(*args, **kwargs))

        raise YException

    @classmethod
    def save(cls, *args, **kwargs):
        if hasattr(meta, "file"):
            return cls(partial(meta.file, s=1)(*args, **kwargs))

        if hasattr(meta, "hipFile"):
            return cls(meta.hipFile.save(*args, **kwargs))

        raise YException

    @property
    def name(self):
        return os.path.basename(self.file)

    @property
    def path(self):
        return os.path.dirname(self.file)

    @property
    def current(cls):
        if hasattr(meta, "file"):
            return cls(meta.file(exn=1, q=1))

        if hasattr(meta, "hipFile"):
            return cls(meta.hipFile.path())

        raise YException
