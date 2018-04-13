# -*- coding: utf-8 -*-
import yurlungur as yr
import sys
import yurlungur.tool.util as util

__doc__ = """
https://docs.python.org/ja/2.7/reference/datamodel.html#customization
https://docs.python.jp/2.7/reference/datamodel.html#object.__new__
"""

from yurlungur.core import standalone
from yurlungur.core import command

command.Command.
standalone.env

# from operator import methodcaller
# from types import MethodType
#
# def nodf(self):
#     return 10
#
# class Obj(object):
#     def __init__(self, value):
#         self._value = value
#
#     def hello(self):
#         print('Hello')
#     # def __getattr__(self, item):
#     #     return getattr(self._value, item)
#
#     def __getattr__(self, item):
#         def _(targ):
#             if targ is None:
#                 return lambda *args, **kwargs: None
#             return lambda *args, **kwargs: methodcaller(item, *args, **kwargs)(targ)
#         return _
#
# def bye():
#     return 2

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
#
# print proc.replace("foo bar baz")("bar", "gege")
#
# Obj.no = nodf
# print proc.no()

# print(Obj.hello) # => <function Spam.hello at 0x1083388c8>
# print(proc.hello()) # => <bound method Spam.hello of <__main__
#
# # proc.bye = MethodType(bye, Obj)
# # print proc.bye("Ddd") # => "ByeBye"