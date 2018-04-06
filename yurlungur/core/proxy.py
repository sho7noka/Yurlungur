# -*- coding: utf-8 -*-
import os
from functools import partial
from wrapper import (
    YMObject, _YObject, _YNode, _YParm, YException
)

meta = YMObject()


"""
'cast', 'contains_emitter_type', 'execute_ubergraph', 'get_class', 'get_editor_property', 'get_fname'
, 'get_full_name', 'get_name', 'get_outer', 'get_outermost', 'get_path_name', 'get_typed_outer', 'get_world', 'modify', 'rename', 'set_editor_property', 'static_class']
"""

class YObject(_YObject):
    """base class
    >>> obj = YObject("pCone")
    >>> obj("cone")
    """

    def __init__(self, item):
        if hasattr(meta, "objExists"):
            assert meta.objExists(item), "{} not found".format(item)
            self.item = item

        if hasattr(meta, "node"):
            assert meta.node(item), "{} not found".format(item)
            self.item = item

    def __call__(self, *args, **kwargs):
        if hasattr(meta, "rename"):
            return meta.rename(self.item, *args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(self.item).setName(*args, **kwargs)

    def attr(self, val, *args, **kwargs):
        if hasattr(meta, "getAttr"):
            return YParm(
                meta.getAttr(self.name + "." + val, *args, **kwargs), self.name, val
            )

        if hasattr(meta, "root"):
            return YParm(
                meta.node(self.name).parm(val).eval(), self.name, val
            )

        raise YException

    @property
    def name(self):
        return self.item

    @property
    def attrs(self, *args, **kwargs):
        if hasattr(meta, "listAttr"):
            return meta.listAttr(*args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(self.item).parms()

        raise YException

    @property
    def id(self):
        if hasattr(meta, "ls"):
            return meta.ls(self.item, uuid=1) or 0

        if hasattr(meta, "root"):
            return meta.node(self.item).sessionId() or 0

        raise YException


class YNode(YObject):
    """connect-able object"""

    def __init__(self, node):
        super(YObject, self).__init__(node)
        self.node = node

    @classmethod
    def create(cls, *args, **kwargs):
        if hasattr(meta, "createNode"):
            return cls(meta.createNode(*args, **kwargs))

        if hasattr(meta, "root"):
            return cls(meta.node(cls.node).createNode(*args, **kwargs))

        raise YException

    def delete(self, *args, **kwargs):
        if hasattr(meta, "delete"):
            meta.delete(self.node, *args, **kwargs)

        if hasattr(meta, "root"):
            meta.node(self.node).destroy()

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


class YParm(_YParm):
    """parametric object"""

    def __init__(self, *args, **kwargs):
        self.values = args

    def __getitem__(self, idx):
        return self.values[idx]

    def set(self, *args, **kwargs):
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

    def __init__(self, file):
        self.file = file

    @property
    def name(self):
        return os.path.basename(self.file)

    @property
    def path(self):
        return os.path.dirname(self.file)

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
    def current(cls):
        if hasattr(meta, "file"):
            return cls(meta.file(exn=1, q=1))

        if hasattr(meta, "hipFile"):
            return cls(meta.hipFile.path())

        raise YException
