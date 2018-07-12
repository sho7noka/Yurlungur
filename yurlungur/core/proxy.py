# -*- coding: utf-8 -*-
import os
import inspect
from functools import partial, total_ordering

from yurlungur.core.wrapper import (
    YException, _YObject, _YNode, _YAttr, OM
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

        if hasattr(meta, "data"):
            meta.data.objects[self.item].name = "".join(args)

    @property
    def name(self):
        return self.item

    @property
    def parent(self):
        raise YException

    @property
    def children(self):
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

        if hasattr(meta, "data"):
            return YAttr(
                meta.data.objects[self.name].name, self.name, val
            )

        raise YException

    @trace
    def hide(self, on=True):
        if hasattr(meta, "data"):
            meta.data.objects[self.name].hide = on

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

        if hasattr(meta, "data"):
            return YAttr(
                meta.data.objects[self.name].name, self.name, item
            )

        raise YException

    @property
    def attrs(self, *args, **kwargs):
        if hasattr(meta, "listAttr"):
            return {meta.listAttr(self.name, *args, **kwargs)}

        if hasattr(meta, "root"):
            return {
                p.name() for p in meta.node(self.name).parms()
            }

        if hasattr(meta, "data"):
            return inspect.getmembers(meta.data.objects[self.name])

        raise YException

    @property
    def id(self):
        if hasattr(meta, "ls"):
            return meta.ls(self.name, uuid=1)[0] or 0

        if hasattr(meta, "root"):
            return meta.node(self.name).sessionId() or 0

        if hasattr(meta, "data"):
            return meta.data.objects[self.name].id_data or 0

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
            return YNode(meta.node(self.name).createNode(*args, **kwargs).path())

        if hasattr(meta, "ops"):
            try:
                getattr(meta.ops.mesh, str(self).lower() + "_add")(*args, **kwargs)
            except AttributeError:
                getattr(meta.ops.object, str(self).lower() + "_add")(*args, **kwargs)

        raise YException

    @trace
    def delete(self, *args, **kwargs):
        if hasattr(meta, "delete"):
            return meta.delete(self.name, *args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(self.name).destroy()

        if hasattr(meta, "context"):
            return meta.context.scene.objects.unlink(meta.data.objects[self.name])

        raise YException

    @trace
    def connect(self, *args, **kwargs):
        if hasattr(meta, "root"):
            return partial(
                meta.node(self.name).setInput, 0)(*args, **kwargs)

        raise YException

    @trace
    def disconnect(self, *args, **kwargs):
        if hasattr(meta, "root"):
            return partial(
                meta.node(self.name).setInput, 0, None)(*args, **kwargs)

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
    
    def inputs(self, *args, **kwargs):
        if hasattr(meta, "listConnections"):
            return partial(meta.listConnections, s=1)(*args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(self.name).inputs()

        raise YException

    def outputs(self, *args, **kwargs):
        if hasattr(meta, "listConnections"):
            return partial(meta.listConnections, d=1)(*args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(self.name).outputs()

        raise YException


@total_ordering
class YAttr(_YAttr):
    """parametric object"""

    def __init__(self, *args, **kwargs):
        assert len(args) > 2, "parameter is invalid."
        self.values = args
        self.obj, self.val = self.values[1:]

    def __getitem__(self, idx):
        return self.values[idx]

    def __repr__(self):
        return str(self.value[0])

    def __eq__(self, other):
        return self.value[0] == other.value[0]

    def __gt__(self, other):
        return self.value[0] >= other.value[0]

    @trace
    def connect(self, val, **kwargs):
        if hasattr(meta, "connectAttr"):
            return partial(
                meta.connectAttr, self.obj +"."+ self.val
            )(val[1] +"."+ val[2], **kwargs)

        raise YException

    @trace
    def disconnect(self, val, **kwargs):
        if hasattr(meta, "disconnectAttr"):
            return partial(
                meta.disconnectAttr, self.obj +"."+ self.val
            )(val[1] +"."+ val[2], **kwargs)

        raise YException

    @trace
    def set(self, *args, **kwargs):
        if hasattr(meta, "setAttr"):
            return meta.setAttr(self.obj + "." + self.val, *args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(self.obj).parm(self.val).set(*args, **kwargs)

        if hasattr(meta, "data"):
            arg = args[0]
            return setattr(meta.data.objects[self.obj], self.val, arg)

        raise YException

    @trace
    def lock(self, on):
        if hasattr(meta, "setAttr"):
            return meta.setAttr(self.obj + "." + self.val, lock=on)

        if hasattr(meta, "root"):
            return meta.node(self.obj).parm(self.val).lock(on)

        raise YException

    @trace
    def hide(self, on=True):
        if hasattr(meta, "setAttr"):
            return meta.setAttr(self.obj + "." + self.val, keyable=not on, channelBox=not on)

        if hasattr(meta, "root"):
            return meta.node(self.obj).parm(self.val).hide(on)

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

        if hasattr(meta, "ops"):
            return cls(meta.ops.wm.open_mainfile(*args, **kwargs))

        raise YException

    @classmethod
    def save(cls, *args, **kwargs):
        if hasattr(meta, "file"):
            return cls(partial(meta.file, s=1)(*args, **kwargs))

        if hasattr(meta, "hipFile"):
            return cls(meta.hipFile.save(*args, **kwargs))

        if hasattr(meta, "ops"):
            return meta.ops.wm.save_mainfile(*args, **kwargs)

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

        if hasattr(meta, "data"):
            return cls(meta.data.filepath)

        raise YException

