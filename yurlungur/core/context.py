# -*- coding: utf-8 -*-

from .. import *
from wrapper import _YNode, _YParm
import app

import inspect
import yurlungur as yr


class YException(Exception):
    pass


class YNotsupportException(YException):
    pass


class YMObject(object):
    def __getattr__(self, item):
        for cmd, _ in inspect.getmembers(app.application):
            if item == cmd:
                setattr(
                    yr, cmd, (lambda str: dict(inspect.getmembers(app.application))[str])(cmd)
                )
                return getattr(yr, item)

        raise YNotsupportException
        return None

    def mod(self):
        return app.application


class YObject(object):
    """base class"""

    def __new__(cls, *args, **kwargs):
        def name(cls):
            pass

        def id(cls):
            pass

        def path(cls):
            pass


class YFile(YObject):

    @staticmethod
    def load(self):
        return

    @staticmethod
    def save(self):
        return


class YNode(_YNode, YObject):
    """connect-able object"""

    def create(self, *args, **keys):
        return YMObject().createNode(args, keys)

    def delete(self):
        return super(YNode, self)

    def connect(self, **keys):
        return

    def disconnect(self, **keys):
        return


class YParm(_YParm, YObject):
    """parametric object"""

    # def __new__():
    #     return cmds.directionalLight(*args, **kwargs)

    def __getitem__(self, item):
        return item

    def __setitem__(self, key, value):
        return


class DynamicProxy(object):
    def __init__(self, value):
        self._value = value

    def __getattr__(self, item):
        return getattr(self._value, item)

# proc = DynamicProxy("hoge")
# print proc.title()
#
# from operator import methodcaller
#
# class NullSafeContainer(object):
#     def __getattr__(self, item):
#         def _(targ):
#             if targ is None:
#                 return lambda *args, **kwargs: None
#             return lambda *args, **kwargs: methodcaller(item, *args, **kwargs)(targ)
#         return _
#
# ns = NullSafeContainer()
# print ns.replace("foo bar baz")("bar", "gege")
#
# class Container(object):
#     pass
#
# c = Container()
#
# def new_method(self, val):
#     return val
#
# Container.new_method = new_method
# print c.new_method("new")
#
# class Spam:
#     def hello(self):
#         print('Hello')
#
# s = Spam()
#
# print(Spam.hello) # => <function Spam.hello at 0x1083388c8>
# print(s.hello) # => <bound method Spam.hello of <__main__.Spam object at 0x1083349b0>>
#
# from types import MethodType
# 2016/09/25 修正 MethodTypeの第2引数はinstanceを渡すの正しいので修正
# spam.bye = MethodType(bye, Spam) <- Spamクラスではなくspamを渡すのが正しい
# spam.bye = MethodType(bye, spam)
# print spam.bye() # => "ByeBye"
