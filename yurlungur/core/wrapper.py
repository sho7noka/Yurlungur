# -*- coding: utf-8 -*-
try:
    import unicode
except:
    unicode = str
import inspect


class Attribute(unicode):
    _node = ''
    _attr = ''

    def __new__(cls, *args, **kwds):
        if len(args) == 2:
            cls._node = args[0]
            cls._attr = args[1]
        elif len(args) == 1:
            cls._node, cls._attr = args[0].split('.')
        return super(Attribute, cls).__new__(cls, cls._node + "." + cls._attr)

    def __getitem__(self, idx):
        return Attribute(self._node, self._attr + "[{0}]".format(idx))

    def get(self, **kwds):
        return cmds.getAttr(self, **kwds)

    def set(self, *val, **kwds):
        cmds.setAttr(self, *val, **kwds)


class HogeMeta(type):

    def __new__(mcs, name, bases, dictionary):
        cls = type.__new__(mcs, name, bases, dictionary)
        setattr(cls, 'member1', 10)
        setattr(cls, 'member2', 20)
        return cls


class AttackSkill(object):
    name = u'特大攻撃'


class HealSkill(object):
    name = u'回復'


class PoisonSkill(object):
    name = u'毒攻撃'


class SkillMeta(type):
    def __new__(mcs, name, bases, dictionary):
        cls = type.__new__(mcs, name, bases, dictionary)
        skills = {'attack': AttackSkill,
                  'heal': HealSkill,
                  'poison': PoisonSkill}
        cls.SKILLS = skills
        return cls


class Skills(object):
    __metaclass__ = SkillMeta
    SKILLS = {}

    @classmethod
    def get(cls, skill_key):
        return cls.SKILLS[skill_key]


class MetaYObject(type):
    def __new__(cls, name, bases, attrs):
        attrs["version"] = "0.0.1"
        return super(MetaYParm, cls).__new__(cls, name, bases, attrs)

    def __getattr__(self, item):
        return item

    def eval(self, *args, **kwargs):
        return text



class MetaYParm(type):
    """
    cmds.getAttr("tx")
    cmds.setAttr("tx", 1)

    node.parm('tx').eval()
    node.parm('tx').set(1)
    """
    def __new__(cls, name, bases, attrs):
        attrs["version"] = "0.0.1"
        return super(MetaYParm, cls).__new__(cls, name, bases, attrs)

    def __getattr__(self, name):
        def _(self, name):
            return name
        return _

class MetaYNode(type):
    """
    createNode
    destroy

    createNode
    delete
    """
    def __new__(cls, name, bases, attrs):
        attrs["version"] = "0.0.1"
        return super(MetaYNode, cls).__new__(cls, name, bases, attrs)

    def __getattr__(self, name):
        def _(self, name):
            return name
        return _


_YNode = MetaYNode("YNode", (object,), {"__doc__": MetaYNode.__doc__})
_YParm = MetaYParm("YParm", (object,), {"__doc__": MetaYParm.__doc__})


