# -*- coding: utf-8 -*-
import inspect
import os
from functools import partial, total_ordering

from yurlungur.core.wrapper import (
    YException, _YObject, _YAttr, OM
)
from yurlungur.tool.math import (
    YVector, YColor, YMatrix
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

    def parent(self, *args, **kwarg):
        if len(args) > 0:
            return meta.parent(self.item, *args, **kwarg)

        elif len(args) == 0 and len(kwarg) > 0:
            return meta.parent(self.item, *args, **kwarg)

        else:
            if hasattr(meta, "getAttr"):
                return YObject(
                    partial(meta.listRelatives, self.item, p=1)(*args, **kwarg)
                )

            if hasattr(meta, "root"):
                return YObject(
                    meta.node(self.item).parent().name()
                )

    def instance(self, *args, **kwarg):
        if hasattr(meta, "instance"):
            if len(args) > 0:
                return meta.instance(self.item, lf=1)
            else:
                return meta.listRelatives(self.item, ap=1, f=1)[1:] or None

        raise YException

    def select(self, *args, **kwargs):
        if 'shape' not in kwargs and 's' not in kwargs:
            kwargs['s'] = True

        if hasattr(meta, "select"):
            if len(args) == 0 and len(kwargs) == 0:
                meta.select(*args, **kwargs)
            else:
                meta.ls(sl=1)

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

    @property
    def children(self, *args, **kwarg):
        if hasattr(meta, "getAttr"):
            return partial(meta.listRelatives, self.item, c=1)(*args, **kwarg) or None

        raise YException

    @trace
    def hide(self, on=True):
        if hasattr(meta, "data"):
            meta.data.objects[self.name].hide = on

        raise YException

    @trace
    def attr(self, val, *args, **kwargs):
        if hasattr(meta, "getAttr"):
            return YAttr(
                meta.getAttr(self.name + "." + val, *args, **kwargs), self.name, val
            )

        if hasattr(meta, "root"):
            parm = (meta.node(self.name).parm(val)
                    or meta.node(self.name).parmTuple(val))
            return YAttr(
                parm.eval(), self.name, val
            )

        if hasattr(meta, "data"):
            return YAttr(
                meta.data.objects[self.name].name, self.name, val
            )

        raise YException

    def __getattr__(self, item):
        if hasattr(meta, "getAttr"):
            return YAttr(
                meta.getAttr(self.name + "." + item), self.name, item
            )

        if hasattr(meta, "root"):
            parm = (meta.node(self.name).parm(item) or
                    meta.node(self.name).parmTuple(item))
            return YAttr(
                parm.eval(), self.name, item
            )

        if hasattr(meta, "data"):
            return YAttr(
                meta.data.objects[self.name].name, self.name, item
            )

        raise YException

    @property
    def attrs(self, *args, **kwargs):
        if hasattr(meta, "listAttr"):
            return tuple(meta.listAttr(self.name, *args, **kwargs)) or None

        if hasattr(meta, "root"):
            return tuple(
                p.name() for p in meta.node(self.name).parms() or []
            )

        if hasattr(meta, "data"):
            return inspect.getmembers(meta.data.objects[self.name])

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
            if len(args) == 0 and len(kwargs) == 0:
                return YNode(
                    partial(
                        meta.node(self.name).createNode, self.name
                    )(*args, **kwargs).path())
            return YNode(meta.node(self.name).createNode(*args, **kwargs).path())

        if hasattr(meta, "ops"):
            try:
                getattr(meta.ops.mesh, str(self).lower() + "_add")(*args, **kwargs)
            except AttributeError:
                getattr(meta.ops.object, str(self).lower() + "_add")(*args, **kwargs)

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
        self._values = args
        self.obj, self.val = self._values[1:]

    def __getitem__(self, idx):
        return self._values[idx]

    def __repr__(self):
        return str(self.value[0])

    def __eq__(self, other):
        return self.value[0] == other.value[0]

    def __gt__(self, other):
        return self.value[0] >= other.value[0]

    @property
    def value(self):
        return self._values[0]

    @trace
    def set(self, *args, **kwargs):
        if hasattr(meta, "setAttr"):
            return meta.setAttr(self.obj + "." + self.val, *args, **kwargs)

        if hasattr(meta, "root"):
            parm = (meta.node(self.obj).parm(self.val) or
                    meta.node(self.obj).parmTuple(self.val)
                    )
            return parm.set(
                args[0].tolist() if hasattr(args[0], "T") else args[0], **kwargs)

        if hasattr(meta, "data"):
            return setattr(meta.data.objects[self.obj],
                           self.val, args[0].tolist() if hasattr(args[0], "T") else args[0])

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

    @trace
    def connect(self, val, **kwargs):
        if hasattr(meta, "connectAttr"):
            return partial(
                meta.connectAttr, self.obj + "." + self.val
            )(val[1] + "." + val[2], **kwargs)

        raise YException

    @trace
    def disconnect(self, val, **kwargs):
        if hasattr(meta, "disconnectAttr"):
            return partial(
                meta.disconnectAttr, self.obj + "." + self.val
            )(val[1] + "." + val[2], **kwargs)

        raise YException

    @property
    def asVector(self):
        try:
            return YVector(self._values[0])
        except TypeError:
            return YVector(*self._values[0])

    @property
    def asColor(self):
        try:
            return YColor(self._values[0])
        except TypeError:
            return YColor(*self._values[0])

    @property
    def asMatrix(self):
        try:
            return YMatrix(self._values[0])
        except TypeError:
            return YMatrix(*self._values[0])


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
    def current(cls):
        if hasattr(meta, "file"):
            return cls(meta.file(exn=1, q=1))

        if hasattr(meta, "hipFile"):
            return cls(meta.hipFile.path())

        if hasattr(meta, "data"):
            return cls(meta.data.filepath)

        raise YException

    def reference(cls):
        raise YException

    @property
    def name(self):
        return os.path.basename(self.file)

    @property
    def path(self):
        return os.path.dirname(self.file)
