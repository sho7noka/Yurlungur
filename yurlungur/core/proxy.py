# -*- coding: utf-8 -*-
import os
from functools import partial

from yurlungur.core.wrapper import (
    YMObject, YException, _YObject, _YNode, _YAttr, OM, ORM
)
from yurlungur.tool.meta import meta
from yurlungur.tool.util import trace


class YObject(_YObject):
    """base class
    >>> obj = YObject("pCone")
    >>> obj("cone")
    """

    def __init__(self, item):
        self.item = item

    def __repr__(self):
        return self.name

    def __call__(self, *args, **kwargs):
        if hasattr(meta, "rename"):
            return meta.rename(self.item, *args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(self.item).setName(*args, **kwargs)

        if hasattr(meta, "Actor"):
            return meta.Actor(self.item).rename(*args, **kwargs)

        if hasattr(meta, "data"):
            meta.data.objects[self.item] = args

    @property
    def name(self):
        return self.item

    @property
    def parent(self):
        raise YException

    @property
    def child(self):
        raise YException

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
            return YAttr(
                self.get_editor_property(val)
            )

        raise YException

    @trace
    def __getattr__(self, item):
        # something ORM

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
            return tuple(meta.listAttr(self.name, *args, **kwargs))

        if hasattr(meta, "root"):
            return tuple(
                p.name() for p in meta.node(self.name).parms()
            )

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
            return meta.Actor(self.name).tags or 0

        if hasattr(meta, "data"):
            return meta.data.objects[self.name].id_data

        raise YException


class YNode(YObject):
    """connect-able object"""

    def __init__(self, item=None):
        super(YNode, self).__init__(item)
        self.item = item

    @trace
    def create(self, *args, **kwargs):
        if hasattr(meta, "createNode"):
            return YObject(meta.createNode(*args, **kwargs))

        if hasattr(meta, "root"):
            return YNode(meta.node(self.item).createNode(*args, **kwargs).path())

        raise YException

    def delete(self, *args, **kwargs):
        if hasattr(meta, "delete"):
            return meta.delete(self.item, *args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(self.item).destroy()

        if hasattr(meta, "Actor"):
            return meta.destroy_actor()

        if hasattr(meta, "context"):
            return meta.context.scene.objects.unlink(meta.data.objects[self.item])

        raise YException

    def connect(self, *args, **kwargss):
        if hasattr(meta, "connectAttr"):
            return meta.connectAttr(*args, **kwargss)

        if hasattr(meta, ""):
            return meta.setInput(*args, **kwargss)

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

    @trace
    def geometry(self):
        if hasattr(meta, "ls"):
            dag = OM.MGlobal.getSelectionListByName(self.name).getDagPath(0)
            return OM.MFnMesh(dag)

        if hasattr(meta, "root"):
            return meta.node(self.name).geometry()

        if hasattr(meta, "data"):
            return meta.data.meshes[self.name]

        raise YException


class YAttr(_YAttr):
    """parametric object"""

    def __init__(self, *args, **kwargs):
        self.values = args

    def __getitem__(self, idx):
        return self.values[idx]

    @trace
    def set(self, *args, **kwargs):
        assert len(self.values) > 2, "parameter is invalid."
        obj, val = self.values[1:]

        if hasattr(meta, "setAttr"):
            return meta.setAttr(obj + "." + val, *args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(obj).parm(val).set(*args, **kwargs)

        raise YException

    @property
    def value(self):
        return self.values


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
