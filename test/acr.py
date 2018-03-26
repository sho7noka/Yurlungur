# -*- coding: utf-8 -*-
import unittest
import doctest
import yurlungur as yr

# # docs.python.jp/2.7/reference/datamodel.html#object.__new__
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

# class MyDynamicProxy:
#
#     def __init__(self, target):
#         self.target = target
#
#     def __getattr__(self, attrname):
#         print("result : ")
#         return getattr(self.target, attrname)

class TestScene(unittest.TestCase):

    def test_get(self):
        cmds.file(new=True, f=True)
        cube = cmds.polyCube()[0]
        print cube
        m = mtn.M(u"pCube1")



print yr.meta
# yr.application.mayapy("import sys; print sys.path")
# yr.application.maxpy("import yurlungur as yr; print yr.meta")
# yr.application.hython("import yurlungur as yr; print yr.meta.pwd()")

# yr.YurPrompt()
#
# widget = yr.YurPrompt()
# widget.show()
