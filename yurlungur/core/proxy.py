# -*- coding: utf-8 -*-
import functools
import inspect

from .. import *
from wrapper import _YObject, _YNode, _YParm, YMObject


class YException(Exception):
    pass


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

    def create(self, *args, **keys):
        return YMObject().createNode(args, keys)

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

    def load(self, *args, **keys):
        """load file"""

        return YMObject().file(args, keys) #or YMObject().hipFile.load(args, keys)


    def save(self, *args, **keys):
        return (
                YMObject().file or
                YMObject().hipFile.save or
                YMObject().rame(_name)
        )

    def export(self, *args, **keys):
        return (

        )
