# -*- coding: utf-8 -*-
import sys
import types
from math import sqrt, pi as PI  #: π
from numbers import Number

from yurlungur.core import env

TO_DEG = 180. / PI  #: Radians を Degrees に変換するための係数。
TO_RAD = PI / 180.  #: Degrees を Radians に変換するための係数。
# TOLERANCE = 1. / (2 ** 30)  #: DCCツールなどで一般的に使用する想定の許容誤差。
# LOOSE_TOLERANCE = 1. / (2 ** 18)  #: DCCツールなどでの緩めの許容誤差。
AVOID_ZERO_DIV_PRECISION = 1.e-13  #: Maya では scale=0 を設定しても matrix 値は 1.e-12 くらいで潰れずに保持するようなので、それを意識した極小値。
_MUTATOR_DICT = {}

# ------------------------------------------------------------------------------
OPTIONAL_MUTATOR_DICT = {
    list: (
        'append',
        'extend',
        'insert',
    ),
    dict: (
        'clear',
        'pop',
        'popitem',
        'setdefault',
        'update',
    ),
    set: (
        'update',
        'intersection_update',
        'difference_update',
        'symmetric_difference_update',
        'add',
        'remove',
        'discard',
        'pop',
        'clear',
    ),
}  #: クラスごとの追加ミューテーターを把握するための辞書。適切なメンテナンスが必要。

if env.Maya():
    import maya.api.OpenMaya as _api2

    _MM = _api2.MMatrix
    _MQ = _api2.MQuaternion
    _ME = _api2.MEulerRotation
    _MP = _api2.MPoint
    _MV = _api2.MVector
    _MX = _api2.MTransformationMatrix
    _MSpace_kTransform = _api2.MSpace.kTransform
    _TOLERANCE = _MM.kTolerance

elif env.Rumba(): # and Katana
    try:
        import imath
    except ImportError:
        import Imath as imath

    _MM = imath.M33f
    _MQ = _api2.MQuaternion
    _ME = _api2.MEulerRotation
    _MP = _api2.MPoint
    _MV = imath.V3f
    _MX = _api2.MTransformationMatrix
    _MSpace_kTransform = _api2.MSpace.kTransform
    _TOLERANCE = _MM.kTolerance

elif env.Houdini() or env.UE4():
    try:
        import hou as application
    except ImportError:
        import unreal as application

    _MV = type('_YVector', (
        application.Vector if hasattr(application, "Vector") else application.Vector3,
    ), dict())

    _MM = type('_YMatrix', (
        application.Matrix if hasattr(application, "Matrix") else application.Matrix4,
    ), dict())

    _MQ = _api2.MQuaternion
    _ME = _api2.MEulerRotation
    _MP = _api2.MPoint
    _MX = _api2.MTransformationMatrix
    _MSpace_kTransform = _api2.MSpace.kTransform
    _TOLERANCE = _MM.kTolerance


elif env.Unity():
    import UnityEngine

    _MM = UnityEngine.Matrix4x4
    _MQ = _api2.MQuaternion
    _ME = _api2.MEulerRotation
    _MP = _api2.MPoint
    _MV = UnityEngine.Vector3
    _MX = _api2.MTransformationMatrix
    _MSpace_kTransform = _api2.MSpace.kTransform
    _TOLERANCE = _MM.kTolerance


elif env.Substance():
    import sd

    _MM = sd.SDValueMatrix
    _MQ = _api2.MQuaternion
    _ME = _api2.MEulerRotation
    _MP = _api2.MPoint
    _MV = sd.SDValueVector
    _MX = _api2.MTransformationMatrix
    _MSpace_kTransform = _api2.MSpace.kTransform
    _TOLERANCE = _MM.kTolerance

elif env.Blender():
    import mathutils

    _MM = mathutils.Matrix
    _MQ = _api2.MQuaternion
    _ME = _api2.MEulerRotation
    _MP = _api2.MPoint
    _MV = mathutils.Vector
    _MX = _api2.MTransformationMatrix
    _MSpace_kTransform = _api2.MSpace.kTransform
    _TOLERANCE = _MM.kTolerance

elif env.Nuke():
    import _nukemath

    _MM = _nukemath.Matrix4
    _MQ = _api2.MQuaternion
    _ME = _api2.MEulerRotation
    _MP = _api2.MPoint
    _MV = _nukemath.Vector3
    _MX = _api2.MTransformationMatrix
    _MSpace_kTransform = _api2.MSpace.kTransform
    _TOLERANCE = _MM.kTolerance

elif env.Max():
    from pymxs import runtime as rt

    _MM = rt.Matrix3
    _MQ = _api2.MQuaternion
    _ME = _api2.MEulerRotation
    _MP = _api2.MPoint
    _MV = _api2.MVector
    _MX = _api2.MTransformationMatrix
    _MSpace_kTransform = _api2.MSpace.kTransform


elif env.C4D():
    import c4d

    _MM = c4d.Matrix
    _MQ = _api2.MQuaternion
    _ME = _api2.MEulerRotation
    _MP = _api2.MPoint
    _MV = c4d.Vector
    _MX = _api2.MTransformationMatrix
    _MSpace_kTransform = _api2.MSpace.kTransform
    _TOLERANCE = _MM.kTolerance

elif env.Davinci():
    _MM = c4d.Matrix
    _MQ = _api2.MQuaternion
    _ME = _api2.MEulerRotation
    _MP = _api2.MPoint
    _MV = c4d.Vector
    _MX = _api2.MTransformationMatrix
    _MSpace_kTransform = _api2.MSpace.kTransform
    _TOLERANCE = _MM.kTolerance

else:
    # marmoset,photoshop,renderdoc
    _MM = None
    _MQ = None
    _ME = None
    _MP = None
    _MV = None
    _MX = None
    _MSpace_kTransform = None
    _TOLERANCE = None


# __all__ = [
#     'OPTIONAL_MUTATOR_DICT',
#     'CymelImmutableError',
#     'immutable',
#     'immutableType',
#     'ImmutableDict',
# ]


# ------------------------------------------------------------------------------
class CymelImmutableError(TypeError):
    u"""
    `immutable` ラップされたオブジェクトが書き換えられた。 
    """

# ------------------------------------------------------------------------------
def _makeImmutableWrapper(cls, clsname):
    u"""
    immutableラッパークラスを生成し、基本的なメソッドをオーバーライドする。
    """
    attrDict = {}

    # クラスごとに決められた追加ミューテーターを封じる。
    nameSet = set()
    for base in cls.mro()[:-1]:
        names = OPTIONAL_MUTATOR_DICT.get(base)
        if names:
            nameSet.update(names)
    for name in nameSet:
        func = _immutableFunc(name)
        attrDict[name] = func

    # __特殊名__ のミューテーターを封じる。
    for name in _SPECIAL_MUTATOR_NAMES:
        if hasattr(cls, name):
            attrDict[name] = _immutableFunc(name)

    # 属性の削除を封じる。
    attrDict['__delattr__'] = _immutableFunc('__delattr__')

    # 把握しているシンプルなクラスや __init__ が無いなら、単に __setattr__ を封じる。
    if cls in _MUTABLE_BUILTIN_TYPES or cls.__init__ is _object_init:
        attrDict['__setattr__'] = _immutableFunc('__setattr__')
        attrDict['__slots__'] = tuple()  # 親方向のクラス全てで徹底されていないと意味がないが一応。

    # __init__ が無いクラスなら、初期化時の属性セットは許容しつつその後の __setattr__ を封じる。
    else:
        cls_init = cls.__init__
        cls_setattr = cls.__setattr__

        def __init__(self, *args, **kwargs):
            cls_init(self, *args, **kwargs)  # この中での __setattr__ は許す。
            self.__dict__['_cymelImmutable'] = True

        attrDict['__init__'] = __init__

        def __setattr__(self, name, val):
            if self.__dict__.get('_cymelImmutable'):
                raise CymelImmutableError('%s.__setattr__' % repr(self))
            cls_setattr(self, name, val)

        attrDict['__setattr__'] = __setattr__

    # ハッシュ関数が実装されていなければ、簡単にサポートして hashable にする。
    h = getattr(cls, '__hash__', None)
    if h is None or h is _object_hash:
        # ラップするクラスインスタンス全てに一致させる。
        h = hash(cls)
        attrDict['__hash__'] = lambda s: h

    # pickle 用の __reduce__ サポート。
    # 元々 pickle 不可なら TypeError になる。
    def __reduce_ex__(self, protocol):
        res = cls.__reduce_ex__(self, protocol)
        if res[0] is cls:
            return newcls_tuple + res[1:]
        return res

    attrDict['__reduce_ex__'] = __reduce_ex__

    # クラスを生成。pickle 用にグローバルスコープにも出す。
    newcls = type(clsname, (cls,), attrDict)
    globals()[clsname] = newcls
    newcls_tuple = (newcls,)
    return newcls

_object_init = object.__init__
_object_hash = object.__hash__


def _immutableFunc(name):
    u"""
    ミューテーターメソッドを封じるオーバーライドを返す。
    """

    def func(self, *args, **kwargs):
        raise CymelImmutableError('%s.%s' % (repr(self), name))

    func.__name__ = name
    return func


_SPECIAL_MUTATOR_NAMES = (
    '__set__',
    '__delete__',
    '__setitem__',
    '__delitem__',
    '__setslice__',
    '__delslice__',
    '__iadd__',
    '__isub__',
    '__imul__',
    '__idiv__',
    '__itruediv__',
    '__ifloordiv__',
    '__imod__',
    '__ipow__',
    '__ilshift__',
    '__irshift__',
    '__iand__',
    '__ixor__',
    '__ior__',
)  #: 既存クラスに存在する場合のみオーバーライドするミューテーター。

_IS_PYTHON2 = sys.version_info[0] is 2
if _IS_PYTHON2:
    _LONG = long
    _BYTES = str
    _UNICODE = unicode
else:
    _LONG = int
    _BYTES = bytes
    _UNICODE = str

_MUTABLE_BUILTIN_TYPES = frozenset([
    bool, int, float, _LONG, complex,
    _BYTES, _UNICODE, list, tuple, dict,
])  #: イミュータブル化の処理を簡易化する組み込み型。
if not _IS_PYTHON2 or sys.version_info[1] >= 6:
    _MUTABLE_BUILTIN_TYPES |= frozenset([bytearray])


# ------------------------------------------------------------------------------
def immutable(type_or_obj, *args, **kwargs):
    u"""
    オブジェクトが変更不可になるラッパーを生成する。

    `immutableType` を呼び出し、
    デフォルト名のラッパークラスを得て、
    それでラップした新規インスタンスが返される。

    .. warning:
        本機能は、変更してはならないものを
        うっかり変更してしまうミスを防ぐことを目的としており、
        絶対に変更不可能なオブジェクトを作れるわけではない。
        やろうと思えば、いくらでも抜け道を作れるだろう。

    :param type_or_obj:
        ラップするオブジェクトのクラス、又はインスタンス。
        旧スタイルのクラスは非サポート。
        インスタンスが指定された場合のラッパーの初期化引数は
        インスタンス自身となる為、コピーコンストラクタが実装
        されている場合にのみ動作する。
    :param list args:
        type_or_obj にクラスが指定された場合の初期化引数。
    :param dict kwargs:
        type_or_obj にクラスが指定された場合の初期化引数。
    :returns:
        ラッパーオブジェクト。

    >>> import cymel.main as cm
    >>> d = cm.immutable(dict, woo=1, foo=2, boo=3)  # construct a immutable dict.
    >>> d = cm.immutable({'woo':1, 'foo':2, 'boo':3})  # same result via copying.
    >>> d['foo']
    2
    >>> # d['foo'] = 9   # CymelImmutableError
    >>> isinstance(d, dict)
    True
    >>> d.__class__ is dict
    False
    >>> cm.immutable({}).__class__ is d.__class__
    True
    """
    if isinstance(type_or_obj, type):
        cls = type_or_obj
    else:
        if _IS_PYTHON2 and isinstance(type_or_obj, types.ClassType):
            raise TypeError('old style class is not supported.')
        cls = type(type_or_obj)
        args = [type_or_obj]
    return immutableType(cls)(*args, **kwargs)


def immutableType(cls, name=None):
    u"""
    オブジェクトが変更不可になるラッパークラスを生成する。

    .. warning:
        本機能は、変更してはならないものを
        うっかり変更してしまうミスを防ぐことを目的としており、
        絶対に変更不可能なオブジェクトを作れるわけではない。
        やろうと思えば、いくらでも抜け道を作れるだろう。

    ラッパークラスはそのクラス名とともにキャッシュされ再利用される。

    型ごとに初めて生成されたラッパークラスは、型のみをキーとしてもキャッシュされ、
    クラス名が省略された場合には任意の名前としても再利用される。

    ラッパークラスでは、オブジェクトの属性値を書き換える
    メソッドがオーバーライドされ、それらがコールされた際に
    `CymelImmutableError` が送出されるようになる。

    どのメソッドをオーバーライドすべきかは、特殊メソッドの
    有無を検査する事で自動決定されるが、
    それだけでは補い切れないクラスに関しては
    `OPTIONAL_MUTATOR_DICT` 辞書で管理している為、
    必要に応じて拡張しなければならない。

    :param `type` cls:
        イミュータブル化する元のクラス。
    :param `str` name:
        ラッパークラスの名前。
        省略時は ``'Immutable元のクラス名'`` となるが、
        最初にその型で生成されたキャッシュがあれば再利用される。
    :rtype: `type`

    .. note::
        `OPTIONAL_MUTATOR_DICT` には、インスタンスを変更する
        メソッド名をクラスごとに列挙する必要がある。
        これは、対応させたいクラスごとに拡張する必要がある事を
        意味する。ただし、全てのメソッドについて列挙する必要が
        あるわけではない。
        `OPTIONAL_MUTATOR_DICT` をあえて拡張せずとも、
        属性の設定、削除、代入演算子などはデフォルトで封じられる。
        あえてメソッド名を列挙する必要があるのは以下のケースである。

        * 属性のメソッドを呼び出すメソッド。
        * 組み込みやバイナリモジュールで提供される型のメソッド。
    """
    if name:
        key = (cls, name)
    else:
        newcls = _immutable_class_cache.get(cls)
        if newcls:
            return newcls
        key = (cls, 'Immutable%s' % cls.__name__)

    newcls = _immutable_class_cache.get(key)
    if newcls:
        return newcls

    newcls = _makeImmutableWrapper(*key)
    _immutable_class_cache[key] = newcls
    if not name or cls not in _immutable_class_cache:
        _immutable_class_cache[cls] = newcls
    return newcls


_immutable_class_cache = {}  #: 生成済みimmutableラッパークラスのキャッシュ。

ImmutableDict = immutableType(dict, 'ImmutableDict')  #: イミュータブル `dict`


def avoidZeroDiv(v, pre=AVOID_ZERO_DIV_PRECISION):
    u"""
    Maya を模倣したゼロ割を防ぐ為の分母を得る。

    Maya では scale=0 を設定しても matrix が特異値とならないように
    0.0 は 1.e-12 くらいでリミットして保持するようなので、それを意識
    したリミットを掛けた値を返す。

    :param v: チェックする値。
    :param pre: 最小値。デフォルトは `AVOID_ZERO_DIV_PRECISION` 。
    :rtype: リミットを適用した値。
    """

    # if v < 0.:
    #    pre = -pre
    #    return pre if v > pre else v
    # else:
    #    return pre if v < pre else v

    # fix for Python 2.4
    if v < 0.:
        pre = -pre
        if v > pre:
            return pre
        else:
            return v
    else:
        if v < pre:
            return pre
        else:
            return v


XYZ = 0  #: Rotaion order XYZ (0)
YZX = 1  #: Rotaion order YZX (1)
ZXY = 2  #: Rotaion order ZXY (2)
XZY = 3  #: Rotaion order XZY (3)
YXZ = 4  #: Rotaion order YXZ (4)
ZYX = 5  #: Rotaion order ZYX (5)

AXIS_X = 0  #: X軸（+X方向ID） (0)
AXIS_Y = 1  #: Y軸（+X方向ID） (1)
AXIS_Z = 2  #: Z軸（+X方向ID） (2)
# AXIS_XYZ = 4  #: XYZ軸全てを意味する。
AXIS_NEG = 0x10  # X,Y,Z の軸ID（ビットフラグではない）に加算して逆向き扱いする為のビットフラグ。
# AXIS_RNEG = ~AXIS_NEG  #: AXIS_NEG のビット反転。
AXIS_NEG_X = AXIS_NEG + AXIS_X  #: -X方向ID。
AXIS_NEG_Y = AXIS_NEG + AXIS_Y  #: -Y方向ID。
AXIS_NEG_Z = AXIS_NEG + AXIS_Z  #: -Z方向ID。


class EulerRotation(object):
    u"""
    オイラー角回転クラス。

    - `EulerRotation`
    - x, y, z, order=XYZ
    - 3値のシーケンス, order=XYZ
    - `.Quaternion`
    - `.Matrix`
    """
    __slots__ = ('__data',)
    __hash__ = None

    def __new__(cls, *args):
        if len(args) is 1:
            v = args[0]
            if hasattr(v, '_EulerRotation__data'):
                return _newE(_ME(v.__data), cls)
            if hasattr(v, '_Quaternion__data'):
                return _newE(v._Quaternion__data.asEulerRotation(), cls)
            if hasattr(v, '_Matrix__data'):
                return _newE(_MX(v._Matrix__data).rotation(False), cls)
            args = v  # 一般シーケンスとして。
        try:
            return _newE(_ME(*args), cls)
        except:
            raise ValueError(cls.__name__ + ' : not matching constructor found.')

    def __reduce__(self):
        d = self.__data
        return type(self), (d[0], d[1], d[2], d.order)

    def __repr__(self):
        return type(self).__name__ + str(self)

    def __str__(self):
        s = str(self.__data)
        i = s.index('k')
        return s[:i] + s[i + 1:]

    def __len__(self):
        return 3

    def __getitem__(self, i):
        return self.__data[i]

    def __setitem__(self, i, v):
        self.__data[i] = v

    def __getattr__(self, k):
        try:
            return getattr(self.__data, k)
        except:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, k))

    def __setattr__(self, k, v):
        try:
            return setattr(self.__data, k, v)
        except:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, k))

    def __eq__(self, v):
        try:
            return self.__data == v.__data
        except:
            return False

    def __ne__(self, v):
        try:
            return self.__data != v.__data
        except:
            return True

    def __neg__(self):
        return _newE(-self.__data)

    def __add__(self, v):
        try:
            return _newE(self.__data + v.__data)
        except:
            raise ValueError("%s + %r" % (type(self).__name__, v))

    def __iadd__(self, v):
        try:
            self.__data += v.__data
        except:
            raise ValueError("%s += %r" % (type(self).__name__, v))
        return self

    def __sub__(self, v):
        try:
            return _newE(self.__data - v.__data)
        except:
            raise ValueError("%s - %r" % (type(self).__name__, v))

    def __isub__(self, v):
        try:
            self.__data -= v.__data
        except:
            raise ValueError("%s -= %r" % (type(self).__name__, v))
        return self

    def __mul__(self, v):
        if isinstance(v, Number):
            return _newE(self.__data * v)
        try:
            return _newE(self.__data * v.__data)  # 回転の合成。
        except:
            raise ValueError("%s * %r" % (type(self).__name__, v))

    def __imul__(self, v):
        if isinstance(v, Number):
            self.__data *= v
        else:
            try:
                self.__data *= v.__data  # 回転の合成。
            except:
                raise ValueError("%s *= %r" % (type(self).__name__, v))
        return self

    def __rmul__(self, v):
        try:
            return _newE(self.__data * v)  # MEulerRotation のスカラー倍は __mul__ のみ。
        except:
            raise ValueError("%r * %s" % (v, type(self).__name__))

    def __div__(self, v):
        try:
            return _newE(self.__data * (1. / v))
        except:
            raise ValueError("%s / %r" % (type(self).__name__, v))

    def __idiv__(self, v):
        try:
            self.__data *= 1. / v
        except:
            raise ValueError("%s /= %r" % (type(self).__name__, v))
        return self

    def __rdiv__(self, v):
        try:
            d = self.__data
            return _newE(_ME(v / d[0], v / d[1], v / d[2], d.order))
        except:
            raise ValueError("%r / %s" % (v, type(self).__name__))

    def isEquivalent(self, v, tol=_TOLERANCE):
        u"""
        ほぼ同値かどうか。

        :type v: `EulerRotation`
        :param v: 比較する値。
        :param `float` tol: 許容誤差。
        :rtype: `bool`
        """
        try:
            return self.__data.isEquivalent(v.__data, tol)
        except:
            return False

    def isZero(self, tol=_TOLERANCE):
        u"""
        ほぼゼロかどうか。

        :param `float` tol: 許容誤差。
        :rtype: `bool`
        """
        return self.__data.isZero(tol)

    def set(self, *args):
        u"""
        他の値をセットする。

        コンストラクタと同様に、以下の値を指定可能。

        - `EulerRotation`
        - x, y, z, order=XYZ
        - 3値のシーケンス, order=XYZ
        - `.Quaternion` (現状のorder維持)
        - `.Matrix` (現状のorder維持)

        :rtype: `EulerRotation` (self)
        """
        if len(args) is 1:
            v = args[0]
            if hasattr(v, '_EulerRotation__data'):
                self.__data.setValue(v.__data)
                return self
            if hasattr(v, '_Quaternion__data'):
                self.__data.setValue(v._Quaternion__data)
                return self
            if hasattr(v, '_Matrix__data'):
                if self.__data.order is XYZ:
                    _E_setdata(self, _MX(v._Matrix__data).rotation(False))
                else:
                    _E_setdata(self, _MX(v._Matrix__data).reorderRotation(self.__data.order + 1).rotation(False))
                return self
            if isinstance(v, _ME):  # 一般シーケンスとしてorder無視。
                self.__data.setValue(v[0], v[1], v[2])
                return self
        try:
            self.__data.setValue(*args)
        except:
            raise ValueError(type(self).__name__ + '.set : unsupported arguments.')
        return self

    setValue = set

    def asVector(self):
        u"""
        X, Y, Z をそのままセットした3次元ベクトルを得る。

        :rtype: `.Vector`
        """
        return _newV(_MP(self.__data))

    asV = asVector  #: `asVector` の別名。

    def asDegrees(self):
        u"""
        X, Y, Z を度数法の `list` として得る。

        :rtype: `list`
        """
        return [self.__data[0] * TO_DEG, self.__data[1] * TO_DEG, self.__data[2] * TO_DEG]

    asD = asDegrees  #: `asDegrees` の別名。

    def asQuaternion(self):
        u"""
        クォータニオンとして得る。

        :rtype: `.Quaternion`
        """
        return _newQ(self.__data.asQuaternion())

    asQ = asQuaternion  #: `asQuaternion` の別名。

    def asMatrix(self):
        u"""
        回転行列として得る。

        :rtype: `.Matrix`
        """
        return _newM(self.__data.asMatrix())

    asM = asMatrix  #: `asMatrix` の別名。

    def asTransformation(self):
        u"""
        トランスフォーメーションとして得る。

        :rtype: `.Transformation`
        """
        return _newX(dict(r=_newE(_ME(self.__data), ImmutableEulerRotation)))

    asX = asTransformation  #: `asTransformation` の別名。

    def incrementalRotateBy(axis, angle):
        u"""
        Perform an incremental rotation by the specified axis and angle.
        The rotation is broken down and performed in smaller steps so that the angles update properly.
        """
        self.__data.incrementalRotateBy(_MV(axis._Vector__data), angle)
        return self

    def inverse():
        u"""
        逆回転を得る。

        :rtype: `EulerRotation`
        """
        return _newE(self.__data.inverse())

    def invertIt():
        u"""
        逆回転をセットする。

        :rtype: `EulerRotation` (self)
        """
        self.__data.invertIt()
        return self

    def reorder(self, order):
        u"""
        回転結果を維持しつつ、オーダーを変更した値を得る。

        :param `int` order: 回転オーダー。
        :rtype: `EulerRotation`
        """
        return _newE(self.__data.reorder(order))

    def reorderIt(self, order):
        u"""
        回転結果を維持しつつ、オーダーを変更した値をセットする。

        :param `int` order: 回転オーダー。
        :rtype: `EulerRotation` (self)
        """
        self.__data.reorderIt(order)
        return self

    def bound(self):
        u"""
        回転結果を維持しつつ、各軸の角度を±πの範囲におさめた値を得る。

        :rtype: `EulerRotation`
        """
        return _newE(self.__data.bound())

    def boundIt(self, src=None):
        u"""
        回転結果を維持しつつ、各軸の角度を±πの範囲におさめた値をセットする。

        :type src: `EulerRotation`
        :param src: ソース回転。省略時は現在の回転。
        :rtype: `EulerRotation` (self)
        """
        if src:
            self.__data.boundIt(src.__data)
        else:
            self.__data.boundIt()
        return self

    def alternateSolution(self):
        u"""
        Returns a new `EulerRotation` with a different rotation which is
        equivalent to this one and has the same rotation order.
        Each rotation component will lie within +/- PI.
        """
        return _newE(self.__data.alternateSolution())

    def setToAlternateSolution(self, src):
        if src:
            self.__data.setToAlternateSolution(src.__data)
        else:
            self.__data.setToAlternateSolution()
        return self

    def closestSolution(self, dst):
        u"""
        Returns a new `EulerRotation` containing the rotation equivalent to
        this one which comes closest to target.
        """
        return _newE(self.__data.closestSolution(dst.__data))

    def setToClosestSolution(self, srcOrDst, dst=None):
        if dst:
            self.__data.setToClosestSolution(srcOrDst.__data, dst.__data)
        else:
            self.__data.setToClosestSolution(srcOrDst.__data)
        return self

    def closestCut(self, dst):
        u"""
        Returns a new `EulerRotation` containing the rotation which is full
        spin multiples of this one and comes closest to target.
        """
        return _newE(self.__data.closestCut(dst.__data))

    def setToClosestCut(self, srcOrDst, dst=None):
        if dst:
            self.__data.setToClosestCut(srcOrDst.__data, dst.__data)
        else:
            self.__data.setToClosestCut(srcOrDst.__data)
        return self

    @staticmethod
    def computeAlternateSolution(src):
        u"""
        Returns a rotation equivalent to rot which is not simply a multiple
        of it.
        """
        return _newE(_2_computeAlternateSolution(src.__data))

    @staticmethod
    def computeBound(src):
        u"""
        Returns a rotation equivalent to rot but bound within +/- PI.
        """
        return _newE(_2_computeBound(src.__data))

    @staticmethod
    def computeClosestCut(src, dst):
        u"""
        Returns the rotation which is full spin multiples of src and comes
        closest to target.
        """
        return _newE(_2_computeClosestCut(src.__data, dst.__data))

    @staticmethod
    def computeClosestSolution(src, dst):
        u"""
        Returns the rotation equivalent to src which comes closest to target.
        """
        return _newE(_2_computeClosestSolution(src.__data, dst.__data))

    @staticmethod
    def decompose(m, order):
        u"""
        Extracts from matrix a valid rotation having the specified rotation
        order. Note that this may be just one of several different rotations
        which could each give rise to the same matrix.
        """
        return _newE(_2_decompose(m._Matrix__data, order))

    def orderStr(self):
        u"""
        回転オーダーを文字列で得る。

        :rtype: `str`
        """
        return _ORDER_TO_STR[self.__data.order]

    def isGimbalLocked(self, tol=_TOLERANCE):
        u"""
        ジンバルロック状態かどうかを得る。

        ピッチ回転が±πの状態
        （ロール軸とヨー軸が重なった状態）
        をジンバルロックとする。

        :param `float` tolerance: 許容誤差。
        :rtype: `bool`
        """
        return -tol < abs(boundAngle(self.__data[_ORDER_TO_AXES[self.__data.order][1]])) - _PI_2 < tol

    def reverseDirection(self):
        u"""
        同じ姿勢の逆周り回転を得る。

        `asQuaternion` で得られるクォータニオンが反転する。

        :rtype: `EulerRotation`
        """
        return _newE(_reverseRotation(_ME(self.__data), self.__data.asQuaternion().w))

    def setToReverseDirection(self):
        u"""
        同じ姿勢の逆周り回転をセットする。

        `asQuaternion` で得られるクォータニオンが反転する。

        :rtype: `EulerRotation` (self)
        """
        self.__data = _reverseRotation(self.__data, self.__data.asQuaternion().w)
        return self

    @classmethod
    def makeYawPitch(cls, vec, order=XYZ):
        u"""
        球面上のベクトルからヨーとピッチの2軸回転を得る。

        基準軸を指定方向へ向けるヨー、ピッチの回転が得られる。

        回転オーダーは、そのまま
        初期方向を表す基準軸、ピッチ回転軸、ヨー回転軸
        を表す。

        :type vec: `.Vector`
        :param vec: 球面上の位置を表す単位ベクトル。
        :param `int` order: 回転オーダー。
        :rtype: `EulerRotation`
        """
        return cls(_MAKE_YAW_PITCH[order](vec), order)


E = EulerRotation  #: `EulerRotation` の別名。

_MUTATOR_DICT[E] = (
    'set',
    'setValue',
    'incrementalRotateBy',
    'invertIt',
    'reorderIt',
    'boundIt',
    'setToAlternateSolution',
    'setToClosestSolution',
    'setToClosestCut',
    'setToReverseDirection',
)
ImmutableEulerRotation = immutableType(E)  #: `EulerRotation` の `immutable` ラッパー。

_E_setdata = E._EulerRotation__data.__set__


def _newE(data, cls=E):
    obj = _object_new(cls)
    _E_setdata(obj, data)
    return obj


_object_new = object.__new__


class Matrix(object):
    def __init__(self, *args, **kwargs):
        super(Matrix, self).__init__(*args, **kwargs)

    __slots__ = ('__data',)
    __hash__ = None

    def __new__(cls, *args, **kwargs):
        n = len(args)
        if n >= 3:
            vx = args[0]._Vector__data
            vy = args[1]._Vector__data
            vz = args[2]._Vector__data
            vt = args[3]._Vector__data if n >= 4 else _ZERO3
            if kwargs.get('transpose'):
                return _newM(_MM([
                    vx[0], vy[0], vz[0], 0.,
                    vx[1], vy[1], vz[1], 0.,
                    vx[2], vy[2], vz[2], 0.,
                    vt[0], vt[1], vt[2], 1.,
                ]), cls)
            else:
                return _newM(_MM([
                    vx[0], vx[1], vx[2], 0.,
                    vy[0], vy[1], vy[2], 0.,
                    vz[0], vz[1], vz[2], 0.,
                    vt[0], vt[1], vt[2], 1.,
                ]), cls)
        return _newM(_MM(*args), cls)

    def __reduce__(self):
        return type(self), (tuple(self.__data),)

    def __repr__(self):
        return type(self).__name__ + str(self.__data)

    def __str__(self):
        return str(self.__data)

    def __len__(self):
        return 16

    def __getitem__(self, i):
        return self.__data[i]

    u'''
    def __contains__(self, v):
        return v in self.__data

    def __iter__(self):
        d = self.__data
        for i in _RANGE16:
            yield d[i]

    def __reversed__(self):
        d = self.__data
        for i in _REVERSED_RANGE16:
            yield d[i]

    def index(self, v):
        d = self.__data
        for i in _RANGE16:
            if d[i] == v:
                return i
        raise ValueError(repr(v) + ' is not in matrix')

    def count(self, v):
        c = 0
        for x in self.__data:
            if x == v:
                c += 1
        return c
    '''

    def __setitem__(self, i, v):
        # Fix DoubleAccessorBug
        vals = [
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
        ]
        vals[i] = v - self[i]
        self.__data += _MM(vals)

    def __eq__(self, v):
        try:
            return self.__data == v.__data
        except:
            return False

    def __ne__(self, v):
        try:
            return self.__data != v.__data
        except:
            return True

    def __neg__(self):
        return _newM(self.__data * -1.)

    def __add__(self, v):
        try:
            return _newM(self.__data + v.__data)
        except:
            raise ValueError("%s + %r" % (type(self).__name__, v))

    def __iadd__(self, v):
        try:
            self.__data += v.__data
        except:
            raise ValueError("%s += %r" % (type(self).__name__, v))
        return self

    def __sub__(self, v):
        try:
            return _newM(self.__data - v.__data)
        except:
            raise ValueError("%s - %r" % (type(self).__name__, v))

    def __isub__(self, v):
        try:
            self.__data -= v.__data
        except:
            raise ValueError("%s -= %r" % (type(self).__name__, v))
        return self

    def __mul__(self, v):
        if isinstance(v, Number):
            return _newM(self.__data * v)
        elif hasattr(v, '_Transformation__data'):
            return _newM(self.__data * v.m.__data)
        else:
            try:
                return _newM(self.__data * v.__data)
            except:
                raise ValueError("%s * %r" % (type(self).__name__, v))

    def __imul__(self, v):
        if isinstance(v, Number):
            self.__data *= v
        elif hasattr(v, '_Transformation__data'):
            self.__data *= v.m.__data
        else:
            try:
                self.__data *= v.__data
            except:
                raise ValueError("%s *= %r" % (type(self).__name__, v))
        return self

    def __rmul__(self, v):
        try:
            return _newM(self.__data.__rmul__(v))
        except:
            raise ValueError("%r * %s" % (v, type(self).__name__))

    def __div__(self, v):
        try:
            return _newM(self.__data * (1. / v))
        except:
            raise ValueError("%s / %r" % (type(self).__name__, v))

    def __idiv__(self, v):
        try:
            self.__data *= (1. / v)
        except:
            raise ValueError("%s /= %r" % (type(self).__name__, v))
        return self

    def __rdiv__(self, v):
        try:
            return _newM(_MM([v / x for x in self]))
        except:
            raise ValueError("%r / %s" % (v, type(self).__name__))

    def isEquivalent(self, m, tol=_TOLERANCE):
        u"""
        ほぼ同値かどうか。

        :type m: `Matrix`
        :param m: 比較するマトリックス。
        :param `float` tol: 許容誤差。
        :rtype: `bool`
        """
        try:
            return self.__data.isEquivalent(m.__data, tol)
        except:
            return False

    def isIdentity(self, tol=_TOLERANCE):
        u"""
        ほぼ単位行列かどうか。

        :param `float` tol: 許容誤差。
        :rtype: `bool`
        """
        return self.__data.isEquivalent(_MM_Identity, tol)

    def isSingular(self):
        u"""
        特異行列かどうか。

        :rtype: `bool`
        """
        return self.__data.isSingular()

    def set(self, v):
        u"""
        他の値をセットする。

        コンストラクタと同様に、以下の値を指定可能。

        - `Matrix`
        - 16値のシーケンス

        :rtype: `Matrix` (self)
        """
        # Fix DoubleAccessorBug
        self.__data += _MM([s - d for s, d in zip(v, self.__data)])
        return self

    def setToIdentity(self):
        u"""
        単位行列をセットする。

        :rtype: `self`
        """
        self.__data.setToIdentity()
        return self

    def init3x3(self):
        u"""
        3x3 部分を初期化する。

        4x4 全て初期化する場合は `setToIdentity` が利用できる。

        平行移動成分のみの行列を新規に得たい場合は
        `asTranslationMatrix` が利用できる。

        :rtype: `Matrix` (self)
        """
        dt = self.__data
        # Fix DoubleAccessorBug:
        dt -= _MM([
            dt[0] - 1., dt[1], dt[2], 0.,
            dt[4], dt[5] - 1., dt[6], 0.,
            dt[8], dt[9], dt[10] - 1., 0.,
            0., 0., 0., 0.,
        ])
        return self

    def initTranslation(self):
        u"""
        4行目の平行移動成分をクリアする。

        3x3 以外を初期化したマトリクスを新規に得たい場合は
        `as3x3` が利用できる。

        :rtype: `Matrix` (self)
        """
        dt = self.__data
        dt[12] = 0.
        dt[13] = 0.
        dt[14] = 0.
        return self

    initT = initTranslation  #: `initTranslation` の別名。

    def getElem(self, row, col):
        u"""
        指定位置の要素を得る。

        :param `int` row: 行インデックス (0-3)
        :param `int` col: 列インデックス (0-3)
        :rtype: `float`
        """
        return self[row * 4 + col]

    def setElem(self, row, col, val):
        u"""
        指定位置の要素をセットする。

        :param `int` row: 行を 0 ～ 3 で指定。
        :param `int` col: 列を 0 ～ 3 で指定。
        :param `float` val: セットする値。
        """
        self[row * 4 + col] = val

    def asTransformation(self):
        u"""
        トランスフォーメーションとして得る。

        :rtype: `.Transformation`
        """
        return _newX(dict(m=_newM(_MM(self.__data), ImmutableMatrix)))

    asX = asTransformation  #: `asTransformation` の別名。

    def asQuaternion(self):
        u"""
        クォータニオンを得る。

        :rtype: `.Quaternion`
        """
        # return _newQ(_MX(self.__data).rotation(True))
        # MQuaternion の場合 MTransformationMatrix より直接の方が速い。
        return _newQ(_MQ().setValue(self.__data.homogenize()))

    asQ = asQuaternion  #: `asQuaternion` の別名。

    def asEulerRotation(self, order=XYZ):
        u"""
        オイラー角回転を得る。

        :param `int` order: 得たい回転オーダー。
        :rtype: `.EulerRotation`

        .. note::
            `EulerRotation` の単位は弧度法なので、
            度数法で得たい場合は `asDegrees` を使用すると良い。
        """
        # return _newE(_ME(0., 0., 0., order).setValue(self.__data.homogenize()))
        # MEulerRotation の場合 MTransformationMatrix の方が直接よりやや速い。
        if order is XYZ:
            return _newE(_MX(self.__data).rotation(False))
        else:
            return _newE(_MX(self.__data).reorderRotation(order + 1).rotation(False))

    asE = asEulerRotation  #: `asEulerRotation` の別名。

    def asDegrees(self, order=XYZ):
        u"""
        オイラー角回転を度数法の `list` として得る。

        :param `int` order: 得たい回転オーダー。
        :rtype: `list`

        .. note::
            単位を弧度法で得たい場合は `asEulerRotation` を使用すると良い。
        """
        if order is XYZ:
            e = _MX(self.__data).rotation(False)
        else:
            e = _MX(self.__data).reorderRotation(order + 1).rotation(False)
        return [e[0] * TO_DEG, e[1] * TO_DEG, e[2] * TO_DEG]

    asD = asDegrees  #: `asDegrees` の別名。

    def asTranslation(self):
        u"""
        平行移動成分を得る。

        :rtype: `.Vector`
        """
        return _newV(_MP(self.__data[12], self.__data[13], self.__data[14]))

    asT = asTranslation  #: `asTranslation` の別名。

    def asScaling(self):
        u"""
        スケーリング成分を得る。

        :rtype: `.Vector`
        """
        return _newV(_MP(_MX(self.__data).scale(_MSpace_kTransform)))

    asS = asScaling  #: `asScaling` の別名。

    def asShearing(self):
        u"""
        シアー成分を得る。

        :rtype: `.Vector`
        """
        return _newV(_MP(_MX(self.__data).shear(_MSpace_kTransform)))

    asSh = asShearing  #: `asShearing` の別名。

    def asTranslationMatrix(self):
        u"""
        平行移動のみの行列を得る。

        :rtype: `Matrix`
        """
        return _newM(_MM([
            1., 0., 0., 0.,
            0., 1., 0., 0.,
            0., 0., 1., 0.,
            self.__data[12], self.__data[13], self.__data[14], 1.,
        ]))

    asTM = asTranslationMatrix  #: `asTranslationMatrix` の別名。

    def asRotationMatrix(self):
        u"""
        回転のみの行列を得る。

        :rtype: `Matrix`
        """
        m = self.__data.homogenize()
        return _newM(_MM([
            m[0], m[1], m[2], 0.,
            m[4], m[5], m[6], 0.,
            m[8], m[9], m[10], 0.,
            0., 0., 0., 1.,
        ]))

    asRM = asRotationMatrix  #: `asRotationMatrix` の別名。

    def asScalingMatrix(self):
        u"""
        スケーリング成分(scale+shear)のみの行列を得る。

        :rtype: `Matrix`:
        """
        xm = _MX(self.__data)
        xm.setTranslation(_MV_Zero, _MSpace_kTransform)
        xm.setRotation(_MQ_Identity)
        return _newM(xm.asMatrix())

    asSM = asScalingMatrix  #: `asScalingMatrix` の別名。

    def as3x3(self):
        u"""
        3x3部分以外を初期化した行列を得る。

        :rtype: `Matrix`
        """
        m = self.__data
        return _newM(_MM([
            m[0], m[1], m[2], 0.,
            m[4], m[5], m[6], 0.,
            m[8], m[9], m[10], 0.,
            0., 0., 0., 1.,
        ]))

    def asTransposed3x3(self):
        u"""
        3x3部分は転置、それ以外の部分は初期化した行列を得る。

        :rtype: `Matrix`
        """
        m = self.__data
        return _newM(_MM([
            m[0], m[4], m[8], 0.,
            m[1], m[5], m[9], 0.,
            m[2], m[6], m[10], 0.,
            0., 0., 0., 1.,
        ]))

    def transpose(self):
        u"""
        転置行列を得る。

        :rtype: `Matrix`
        """
        return _newM(self.__data.transpose())

    def transposeIt(self):
        u"""
        転置行列をセットする。

        :rtype: `Matrix` (self)
        """
        _M_setdata(self, self.__data.transpose())
        return self

    def inverse(self):
        u"""
        逆行列を得る。

        :rtype: `Matrix`
        """
        return _newM(self.__data.inverse())

    def invertIt(self):
        u"""
        逆行列をセットする。

        :rtype: `Matrix` (self)
        """
        _M_setdata(self, self.__data.inverse())
        return self

    def adjoint(self):
        u"""
        余因子行列を得る。

        :rtype: `Matrix`
        """
        return _newM(self.__data.adjoint())

    def adjointIt(self):
        u"""
        余因子行列をセットする。

        :rtype: `Matrix` (self)
        """
        _M_setdata(self, self.__data.adjoint())
        return self

    def homogenize(self):
        u"""
        3x3部分を正規直交化した行列を得る。

        :rtype: `Matrix`
        """
        return _newM(self.__data.homogenize())

    def homogenizeIt(self):
        u"""
        3x3部分を正規直交化した行列をセットする。

        :rtype: `Matrix` (self)
        """
        _M_setdata(self, self.__data.homogenize())
        return self

    def det4x4(self):
        u"""
        行列式を得る。

        :rtype: `float`
        """
        return self.__data.det4x4()

    def det3x3(self):
        u"""
        3x3部分の行列式を得る。

        :rtype: `float`
        """
        return self.__data.det3x3()

    def row(self, i):
        u"""
        行ベクトルを得る。

        :param `int` i: 行インデックス（0～3）。
        :rtype: `.Vector`
        """
        d = self.__data
        i *= 4
        return _newV(_MP(d[i], d[i + 1], d[i + 2], d[i + 3]))

    def rows(self):
        u"""
        行ベクトルを4つ全て得る。

        :rtype: `tuple`
        """
        d = self.__data
        return (
            _newV(_MP(d[0], d[1], d[2], d[3])),
            _newV(_MP(d[4], d[5], d[6], d[7])),
            _newV(_MP(d[8], d[9], d[10], d[11])),
            _newV(_MP(d[12], d[13], d[14], d[15])),
        )

    def setRow(self, i, v):
        u"""
        行ベクトルをセットする。

        :param `int` i: 行インデックス（0～3）。
        :type v: `.Vector`
        :param v: セットする4次元ベクトル。
        """
        # Fix DoubleAccessorBug
        values = [
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
        ]
        data = self.__data
        i *= 4
        values[i] = v[0] - data[i]
        i += 1
        values[i] = v[1] - data[i]
        i += 1
        values[i] = v[2] - data[i]
        i += 1
        values[i] = v[3] - data[i]
        data += _MM(values)

    def setRows(self, v0, v1, v2, v3):
        u"""
        行ベクトルを4つ全てセットする。

        :type v0: `.Vector`
        :param v0: 1行目の4次元ベクトル。
        :type v1: `.Vector`
        :param v1: 2行目の4次元ベクトル。
        :type v2: `.Vector`
        :param v2: 3行目の4次元ベクトル。
        :type v3: `.Vector`
        :param v3: 4行目の4次元ベクトル。
        """
        # Fix DoubleAccessorBug
        m = _MM([
            v0[0], v0[1], v0[2], v0[3],
            v1[0], v1[1], v1[2], v1[3],
            v2[0], v2[1], v2[2], v2[3],
            v3[0], v3[1], v3[2], v3[3],
        ])
        self.__data += m - self.__data

    def column(self, i):
        u"""
        列ベクトルを得る。

        :param `int` i: 列インデックス（0～3）。
        :rtype: `.Vector`
        """
        d = self.__data
        return _newV(_MP(d[i], d[i + 4], d[i + 8], d[i + 12]))

    def columns(self):
        u"""
        列ベクトルを4つ全て得る。

        :rtype: `tuple`
        """
        d = self.__data
        return (
            _newV(_MP(d[0], d[4], d[8], d[12])),
            _newV(_MP(d[1], d[5], d[9], d[13])),
            _newV(_MP(d[2], d[6], d[10], d[14])),
            _newV(_MP(d[3], d[7], d[11], d[15])),
        )

    def setColumn(self, i, v):
        u"""
        列ベクトルをセットする。

        :param `int` i: 列インデックス（0～3）。
        :type v: `.Vector`
        :param v: セットする4次元ベクトル。
        """
        # Fix DoubleAccessorBug
        values = [
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
        ]
        data = self.__data
        values[i] = v[0] - data[i]
        i += 4
        values[i] = v[1] - data[i]
        i += 4
        values[i] = v[2] - data[i]
        i += 4
        values[i] = v[3] - data[i]
        data += _MM(values)

    def setColumns(self, v0, v1, v2, v3):
        u"""
        列ベクトルを4つ全てセットする。

        :type v0: `.Vector`
        :param v0: 1列目の4次元ベクトル。
        :type v1: `.Vector`
        :param v1: 2列目の4次元ベクトル。
        :type v2: `.Vector`
        :param v2: 3列目の4次元ベクトル。
        :type v3: `.Vector`
        :param v3: 4列目の4次元ベクトル。
        """
        # Fix DoubleAccessorBug
        m = _MM([
            v0[0], v1[0], v2[0], v3[0],
            v0[1], v1[1], v2[1], v3[1],
            v0[2], v1[2], v2[2], v3[2],
            v0[3], v1[3], v2[3], v3[3],
        ])
        self.__data += m - self.__data

    def axis(self, i, transpose=False):
        u"""
        3x3部分の行や列を軸ベクトルとして得る。

        `.Vector` の w は 1.0 となる。

        :param `int` i: 軸指定(0=X, 1=Y, 2=Z)。
        :param `bool` transpose:
            転置行列の軸ベクトルを得る。
            言い換えると False では行ベクトルを
            True では列ベクトルを得ることになる。
        :rtype: `.Vector`
        """
        if transpose:
            return _newV(_MP(self.__data[i], self.__data[i + 4], self.__data[i + 8]))
        i *= 4
        return _newV(_MP(self.__data[i], self.__data[i + 1], self.__data[i + 2]))

    def axes(self, transpose=False):
        u"""
        3x3部分の行や列の軸ベクトルを3つ得る。

        各 `.Vector` の w は 1.0 となる。

        :param `bool` transpose:
            転置行列の軸ベクトルを得る。
            言い換えると False では行ベクトルを
            True では列ベクトルを得ることになる。
        :rtype: `tuple`
        """
        m = self.__data
        if transpose:
            return (
                _newV(_MP(m[0], m[4], m[8])),
                _newV(_MP(m[1], m[5], m[9])),
                _newV(_MP(m[2], m[6], m[10])),
            )
        return (
            _newV(_MP(m[0], m[1], m[2])),
            _newV(_MP(m[4], m[5], m[6])),
            _newV(_MP(m[8], m[9], m[10])),
        )

    def setAxis(self, i, v, transpose=False):
        u"""
        3x3部分の行や列のベクトルをセットする。

        :param `int` i: 軸指定(0=X, 1=Y, 2=Z)。
        :type v: `.Vector`
        :param v:
            セットする軸ベクトル。
        :param `bool` transpose:
            転置行列の軸ベクトルをセットする。
            言い換えると False では行ベクトルを
            True では列ベクトルをセットすることになる。
        """
        # Fix DoubleAccessorBug
        values = [
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
        ]
        data = self.__data
        if transpose:
            values[i] = v[0] - data[i]
            i += 4
            values[i] = v[1] - data[i]
            i += 4
            values[i] = v[2] - data[i]
        else:
            i *= 4
            values[i] = v[0] - data[i]
            i += 1
            values[i] = v[1] - data[i]
            i += 1
            values[i] = v[2] - data[i]
        data += _MM(values)

    # def setAxes(self, i, vx, vy, vz, vt=V.Zero, transpose=False):
    #     u"""
    #     3x3部分の行や列と4行目の平行移動ベクトルをセットする。
    # 
    #     :type vx: `.Vector`
    #     :param vx: セットするX軸ベクトル。
    #     :type vy: `.Vector`
    #     :param vy: セットするY軸ベクトル。
    #     :type vz: `.Vector`
    #     :param vz: セットするZ軸ベクトル。
    #     :type vt: `.Vector`
    #     :param vt:
    #         セットする平行移動ベクトル。
    #         これだけは transpose オプションの影響を受けない。
    #     :param `bool` transpose:
    #         3x3部分には転置行列の軸ベクトルをセットする。
    #         言い換えると False では行ベクトルを
    #         True では列ベクトルをセットすることになる。
    #     """
    #     # Fix DoubleAccessorBug
    #     if transpose:
    #         m = _MM([
    #             vx[0], vy[0], vz[0], 0.,
    #             vx[1], vy[1], vz[1], 0.,
    #             vx[2], vy[2], vz[2], 0.,
    #             vt[0], vt[1], vt[2], 1.,
    #         ])
    #     else:
    #         m = _MM([
    #             vx[0], vx[1], vx[2], 0.,
    #             vy[0], vy[1], vy[2], 0.,
    #             vz[0], vz[1], vz[2], 0.,
    #             vt[0], vt[1], vt[2], 1.,
    #         ])
    #     self.__data += m - self.__data

    def mul(self, m):
        u"""
        マトリックス要素同士を乗算する。

        :type m: `Matrix`
        :param m: 乗じるマトリックス。
        :rtype: `Matrix`
        """
        a = self.__data
        b = m.__data
        return _newM(_MM([
            a[0] * b[0], a[1] * b[1], a[2] * b[2], a[3] * b[3],
            a[4] * b[4], a[5] * b[5], a[6] * b[6], a[7] * b[7],
            a[8] * b[8], a[9] * b[9], a[10] * b[10], a[11] * b[11],
            a[12] * b[12], a[13] * b[13], a[14] * b[14], a[15] * b[15],
        ]))

    def imul(self, m):
        u"""
        マトリックス要素同士を乗算してセットする。

        :type m: `Matrix`
        :param m: 乗じるマトリックス。
        :rtype: `Matrix` (self)
        """
        a = self.__data
        b = m.__data
        # Fix DoubleAccessorBug:
        a += _MM([
            a[0] * b[0] - a[0],
            a[1] * b[1] - a[1],
            a[2] * b[2] - a[2],
            a[3] * b[3] - a[3],
            a[4] * b[4] - a[4],
            a[5] * b[5] - a[5],
            a[6] * b[6] - a[6],
            a[7] * b[7] - a[7],
            a[8] * b[8] - a[8],
            a[9] * b[9] - a[9],
            a[10] * b[10] - a[10],
            a[11] * b[11] - a[11],
            a[12] * b[12] - a[12],
            a[13] * b[13] - a[13],
            a[14] * b[14] - a[14],
            a[15] * b[15] - a[15],
        ])
        return self

    def div(self, m, pre=AVOID_ZERO_DIV_PRECISION):
        u"""
        マトリックス要素同士を除算する。

        ゼロ除算を避ける為、分母が `.avoidZeroDiv`
        でフィルタされてから実行される。

        :type m: `Matrix`
        :param m: 分母のマトリックス。
        :param `float` pre: ゼロ除算を避ける為の許容誤差。
        :rtype: `Matrix`
        """
        a = self.__data
        b = m.__data
        return _newM(_MM([
            a[0] / avoidZeroDiv(b[0], pre),
            a[1] / avoidZeroDiv(b[1], pre),
            a[2] / avoidZeroDiv(b[2], pre),
            a[3] / avoidZeroDiv(b[3], pre),
            a[4] / avoidZeroDiv(b[4], pre),
            a[5] / avoidZeroDiv(b[5], pre),
            a[6] / avoidZeroDiv(b[6], pre),
            a[7] / avoidZeroDiv(b[7], pre),
            a[8] / avoidZeroDiv(b[8], pre),
            a[9] / avoidZeroDiv(b[9], pre),
            a[10] / avoidZeroDiv(b[10], pre),
            a[11] / avoidZeroDiv(b[11], pre),
            a[12] / avoidZeroDiv(b[12], pre),
            a[13] / avoidZeroDiv(b[13], pre),
            a[14] / avoidZeroDiv(b[14], pre),
            a[15] / avoidZeroDiv(b[15], pre),
        ]))

    def idiv(self, m, pre=AVOID_ZERO_DIV_PRECISION):
        u"""
        各要素同士を除算し自身を更新する。

        ゼロ除算を避ける為、分母が `~Happy.util.avoidZeroDiv`
        でフィルタされてから実行される。

        :param iterable v: 要素数16個以上のシーケンス。
        :param `float` pre: ゼロ除算を避ける為の許容誤差。
        """
        a = self.__data
        b = m.__data
        # Fix DoubleAccessorBug:
        a += _MM([
            a[0] / avoidZeroDiv(b[0], pre) - a[0],
            a[1] / avoidZeroDiv(b[1], pre) - a[1],
            a[2] / avoidZeroDiv(b[2], pre) - a[2],
            a[3] / avoidZeroDiv(b[3], pre) - a[3],
            a[4] / avoidZeroDiv(b[4], pre) - a[4],
            a[5] / avoidZeroDiv(b[5], pre) - a[5],
            a[6] / avoidZeroDiv(b[6], pre) - a[6],
            a[7] / avoidZeroDiv(b[7], pre) - a[7],
            a[8] / avoidZeroDiv(b[8], pre) - a[8],
            a[9] / avoidZeroDiv(b[9], pre) - a[9],
            a[10] / avoidZeroDiv(b[10], pre) - a[10],
            a[11] / avoidZeroDiv(b[11], pre) - a[11],
            a[12] / avoidZeroDiv(b[12], pre) - a[12],
            a[13] / avoidZeroDiv(b[13], pre) - a[13],
            a[14] / avoidZeroDiv(b[14], pre) - a[14],
            a[15] / avoidZeroDiv(b[15], pre) - a[15],
        ])
        return self

    def hasNonUniformScaling(self, tol=_TOLERANCE):
        u"""
        非一様スケーリングが含まれているかどうか。

        :param `float` tol: 許容誤差。
        :rtype: `bool`
        """
        xm = _MX(self.__data)
        v = xm.shear(_MSpace_kTransform)
        if abs(v[0]) > tol or abs(v[1]) > tol or abs(v[2]) > tol:
            return True
        v = xm.scale(_MSpace_kTransform)
        return abs(v[0] - v[1]) > tol or abs(v[0] - v[2]) > tol

    def setTranslation(self, v):
        u"""
        平行移動値をセットする。

        :type v: `.Vector`
        :param v: 平行移動の3次元ベクトル。
        """
        # Fix DoubleAccessorBug
        data = self.__data
        data += _MM([
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            v[0] - data[12], v[1] - data[13], v[2] - data[14], 0.,
        ])

    setT = setTranslation  #: `setTranslation` の別名。

    def addTranslation(self, v):
        u"""
        平行移動値を加算する。

        :type v: `.Vector`
        :param v: 平行移動の3次元ベクトル。
        """
        # Fix DoubleAccessorBug
        self.__data += _MM([
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            v[0], v[1], v[2], 0.,
        ])

    addT = addTranslation  #: `addTranslation` の別名。

    def subTranslation(self, v):
        u"""
        平行移動値を減算する。

        :type v: `.Vector`
        :param v: 平行移動の3次元ベクトル。
        """
        # Fix DoubleAccessorBug
        self.__data -= _MM([
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            v[0], v[1], v[2], 0.,
        ])

    subT = subTranslation  #: `subTranslation` の別名。

    @classmethod
    def makeTranslation(cls, v):
        u"""
        平行移動行列を作成する。

        :type v: `.Vector`
        :param v: 平行移動の3次元ベクトル。
        :rtype: `Matrix`
        """
        return cls([
            1., 0., 0., 0.,
            0., 1., 0., 0.,
            0., 0., 1., 0.,
            v[0], v[1], v[2], 1.,
        ])

    makeT = makeTranslation  #: `makeTranslation` の別名。

    @classmethod
    def makeInverseTranslation(cls, v):
        u"""
        平行移動の逆行列を作成する。

        :type v: `.Vector`
        :param v: 平行移動の3次元ベクトル。
        :rtype: `Matrix`
        """
        return cls([
            1., 0., 0., 0.,
            0., 1., 0., 0.,
            0., 0., 1., 0.,
            -v[0], -v[1], -v[2], 1.,
        ])

    makeInvT = makeInverseTranslation  #: `makeInverseTranslation` の別名。

    @classmethod
    def makeScaling(cls, v):
        u"""
        スケーリング行列を作成する。

        :type v: `.Vector`
        :param v: スケール値の3次元ベクトル。
        :rtype: `Matrix`
        """
        return cls([
            v[0], 0., 0., 0.,
            0., v[1], 0., 0.,
            0., 0., v[2], 0.,
            0., 0., 0., 1.,
        ])

    makeS = makeScaling  #: `makeScaling` の別名。

    @classmethod
    def makeInverseScaling(cls, v, pre=AVOID_ZERO_DIV_PRECISION):
        u"""
        スケーリングの逆行列を作成する。

        :type v: `.Vector`
        :param v: スケール値の3次元ベクトル。
        :param `float` pre: ゼロ除算を避ける為の許容誤差。
        :rtype: `Matrix`
        """
        return cls([
            1. / avoidZeroDiv(v[0], pre), 0., 0., 0.,
            0., 1. / avoidZeroDiv(v[1], pre), 0., 0.,
            0., 0., 1. / avoidZeroDiv(v[2], pre), 0.,
            0., 0., 0., 1.,
        ])

    makeInvS = makeInverseScaling  #: `makeInverseScaling` の別名。

    @classmethod
    def makeShearing(cls, v):
        u"""
        シアー行列を作成する。

        :type v: `.Vector`
        :param v: シアー値 (xy, yz, yx)
        :rtype: `Matrix`
        """
        return cls([
            1., 0., 0., 0.,
            v[0], 1., 0., 0.,
            v[1], v[2], 1., 0.,
            0., 0., 0., 1.,
        ])

    makeSh = makeShearing  #: `makeShearing` の別名。

    @classmethod
    def makeInverseShearing(cls, v):
        u"""
        シアーの逆行列を作成する。

        :type v: `.Vector`
        :param v: シアー値 (xy, yz, yx)
        :rtype: `Matrix`
        """
        return cls([
            1., 0., 0., 0.,
            -v[0], 1., 0., 0.,
            v[0] * v[2] - v[1], -v[2], 1., 0.,
            0., 0., 0., 1.,
        ])

    makeInvSh = makeInverseShearing  #: `makeInverseShearing` の別名。

    def mirror(self, mirrorAxis=AXIS_X, negAxis=True, t=True):
        u"""
        指定軸方向でミラーしたマトリックスを得る。

        :param `int` mirrorAxis:
            ミラーする基準軸。
            `.AXIS_X` 、 `.AXIS_Y` 、 `.AXIS_Z` のいずれかを指定する。
        :param `int` negAxis:
            行列式（スケール）が反転しないように、
            ミラー結果の逆を向けるローカル軸。
            `.AXIS_X` 、 `.AXIS_Y` 、 `.AXIS_Z` の他に、
            None 、 False 、 True を指定可能。

            省略時(True)はミラー基準軸と同じになる。
            False では 3x3 部は反転しない。
            None ではミラー結果から全軸を逆に向ける。
        :param `bool` t:
            平行移動値（4行目）も反転するかどうか。
        :rtype: `Matrix`
        """
        return _newM(_mirror(self.__data, mirrorAxis, negAxis, t))

    def mirrorIt(self, mirrorAxis=AXIS_X, negAxis=True, t=True):
        u"""
        指定軸方向でミラーしたマトリックスをセットする。

        :param `int` mirrorAxis:
            ミラーする基準軸。
            `.AXIS_X` 、 `.AXIS_Y` 、 `.AXIS_Z` のいずれかを指定する。
        :param `int` negAxis:
            行列式（スケール）が反転しないように、
            ミラー結果の逆を向けるローカル軸。
            `.AXIS_X` 、 `.AXIS_Y` 、 `.AXIS_Z` の他に、
            None 、 False 、 True を指定可能。

            省略時(True)はミラー基準軸と同じになる。
            False では 3x3 部は反転しない。
            None ではミラー結果から全軸を逆に向ける。
        :param `bool` t:
            平行移動値（4行目）も反転するかどうか。
        :rtype: `Matrix` (self)
        """
        self.__data = _mirror(self.__data, mirrorAxis, negAxis, t)
        return self


M = Matrix  #: `Matrix` の別名。

_MUTATOR_DICT[M] = (
    'set',
    'setToIdentity',
    'init3x3',
    'initTranslation',
    'initT',
    'setElem',
    'transposeIt',
    'invertIt',
    'adjointIt',
    'homogenizeIt',
    'setRow',
    'setRows',
    'setColumn',
    'setColumns',
    'setAxis',
    'setAxes',
    'imul'
    'idiv'
    'setTranslation',
    'setT',
    'addTranslation',
    'addT',
    'subTranslation',
    'subT',
    'mirrorIt',
)
ImmutableMatrix = immutableType(M)  #: `Matrix` の `immutable` ラッパー。


def _newM(data, cls=M):
    obj = _object_new(cls)
    _M_setdata(obj, data)
    return obj


_object_new = object.__new__


class Color(object):
    def __init__(self, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)


class Vector(object):
    __slots__ = ('__data',)
    __hash__ = None

    def __init__(self, *args, **kwargs):
        if env.Blender():
            super(Vector, self).__init__()
            self.vector = [self.x, self.y, self.z]
        else:
            super(Vector, self).__init__(*args, **kwargs)
            self.vector = args

    def __new__(cls, *args):
        if len(args) is 1:
            v = args[0]
            if hasattr(v, '_Vector__data'):
                return _newV(_MP(v.__data), cls)
        try:
            return _newV(_MP(*args), cls)
        except:
            raise ValueError(cls.__name__ + ' : not matching constructor found.')

    def __reduce__(self):
        return type(self), tuple(self.__data)

    def __repr__(self):
        if self.__data[3] == 1.:
            return '%s(%f, %f, %f)' % (type(self).__name__, self.__data[0], self.__data[1], self.__data[2])
        return '%s(%f, %f, %f, %f)' % ((type(self).__name__,) + tuple(self.__data))

    def __str__(self):
        if self.__data[3] == 1.:
            return '(%f, %f, %f)' % (self.__data[0], self.__data[1], self.__data[2])
        return '(%f, %f, %f, %f)' % tuple(self.__data)

    def __len__(self):
        return 3 if self.__data[3] == 1. else 4

    def __getitem__(self, i):
        if 0 <= i < 3 or (i == 3 and self.__data[3] != 1.):
            return self.__data[i]
        raise IndexError('Vector index out of range.')

    def __setitem__(self, i, v):
        if 0 <= i < 4:
            self.__data[i] = v
        raise IndexError('Vector index out of range.')

    def __getattr__(self, k):
        try:
            return getattr(self.__data, k)
        except:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, k))

    def __setattr__(self, k, v):
        try:
            return setattr(self.__data, k, v)
        except:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, k))

    def __eq__(self, v):
        try:
            return self.__data == v.__data
        except:
            return False

    def __ne__(self, v):
        try:
            return self.__data != v.__data
        except:
            return True

    def __neg__(self):
        d = self.__data
        return _newV(_MP(-d[0], -d[1], -d[2], d[3]))

    def __add__(self, v):
        try:
            d = self.__data
            s = v.__data
            return _newV(_MP(d[0] + s[0], d[1] + s[1], d[2] + s[2], d[3]))
        except:
            raise ValueError("%s + %r" % (type(self).__name__, v))

    def __iadd__(self, v):
        try:
            d = self.__data
            s = v.__data
            d[0] += s[0]
            d[1] += s[1]
            d[2] += s[2]
        except:
            raise ValueError("%s += %r" % (type(self).__name__, v))
        return self

    def __sub__(self, v):
        try:
            d = self.__data
            s = v.__data
            return _newV(_MP(d[0] - s[0], d[1] - s[1], d[2] - s[2], d[3]))
        except:
            raise ValueError("%s - %r" % (type(self).__name__, v))

    def __isub__(self, v):
        try:
            d = self.__data
            s = v.__data
            d[0] -= s[0]
            d[1] -= s[1]
            d[2] -= s[2]
        except:
            raise ValueError("%s -= %r" % (type(self).__name__, v))
        return self

    def __mul__(self, v):
        if hasattr(v, '_Matrix__data'):
            return _newV(self.__data * v._Matrix__data)
        elif hasattr(v, '_Quaternion__data'):
            v = _MV(self.__data).rotateBy(v._Quaternion__data)
            return _newV(_MP(v[0], v[1], v[2], self.__data[3]))
        elif isinstance(v, Number):
            return _newV(self.__data * v)
        else:
            try:
                d = self.__data
                s = v.__data
                return d[0] * s[0] + d[1] * s[1] + d[2] * s[2]
            except:
                raise ValueError("%s * %r" % (type(self).__name__, v))

    def __imul__(self, v):
        if hasattr(v, '_Matrix__data'):
            self.__data *= v._Matrix__data
        elif hasattr(v, '_Quaternion__data'):
            d = self.__data
            v = _MV(d).rotateBy(v._Quaternion__data)
            d[0] = v[0]
            d[1] = v[1]
            d[2] = v[2]
        else:
            try:
                self.__data *= v
            except:
                raise ValueError("%s *= %r" % (type(self).__name__, v))
        return self

    def __rmul__(self, v):
        try:
            return _newV(self.__data * v)  # MPoint のスカラー倍は __mul__ のみ。
        except:
            raise ValueError("%r * %s" % (v, type(self).__name__))

    def __div__(self, v):
        try:
            return _newV(self.__data / v)
        except:
            raise ValueError("%s / %r" % (type(self).__name__, v))

    def __idiv__(self, v):
        try:
            self.__data /= v
        except:
            raise ValueError("%s /= %r" % (type(self).__name__, v))
        return self

    def __rdiv__(self, v):
        try:
            d = self.__data
            return _newV(_MP(v / d[0], v / d[1], v / d[2], d[3]))
        except:
            raise ValueError("%r / %s" % (v, type(self).__name__))

    def __xor__(self, v):
        try:
            v = _MV(self.__data) ^ _MV(v.__data)
            return _newV(_MP(v[0], v[1], v[2], self.__data[3]))
        except:
            raise ValueError("%s ^ %r" % (type(self).__name__, v))

    def __ixor__(self, v):
        try:
            d = self.__data
            v = _MV(d) ^ _MV(v.__data)
            d[0] = v[0]
            d[1] = v[1]
            d[2] = v[2]
        except:
            raise ValueError("%s ^= %r" % (type(self).__name__, v))
        return self

    def __abs__(self):
        v = self.__data
        return _newV(_MP(abs(v[0]), abs(v[1]), abs(v[2]), abs(v[3])))

    def isEquivalent(self, v, tol=_TOLERANCE):
        u"""
        ほぼ同値かどうか。

        :type v: `Vector`
        :param v: 比較するベクトル。
        :param `float` tol: 許容誤差。
        :rtype: `bool`
        """
        try:
            return self.__data.isEquivalent(v.__data, tol)
        except:
            return False

    def isZero(self, tol=_TOLERANCE):
        u"""
        ほぼゼロかどうか。

        :param `float` tol: 許容誤差。
        :rtype: `bool`
        """
        return self.__data.isEquivalent(_MP_Zero, tol)

    def isParallel(self, v, tol=_TOLERANCE):
        u"""
        2つの3次元ベクトルが平行かどうか。

        :type v: `Vector`
        :param v: 比較するベクトル。
        :param `float` tol: 許容誤差。
        :rtype: `bool`
        """
        return _MV(self.__data).isParallel(_MV(v.__data), tol)

    def set(self, *args):
        u"""
        他の値をセットする。

        コンストラクタと同様に、以下の値を指定可能。

        - `Vector`
        - x, y, z, w
        - x, y, z
        - x, y
        - 4値までのシーケンス

        :rtype: `Vector` (self)
        """
        if len(args) is 1:
            args = args[0]
            if hasattr(args, '_Vector__data'):
                args = args.__data
        try:
            for i, v in enumerate(args):
                self.__data[i] = v
        except:
            raise ValueError(type(self).__name__ + '.set : unsupported arguments.')
        return self

    def angle(self, v):
        u"""
        2つの3次元ベクトルの成す角を得る。

        :type v: `Vector`
        :param v: もう1方のベクトル。
        :rtype: `float`
        """
        return _MV(self.__data).angle(_MV(v.__data))

    def length(self):
        u"""
        3次元ベクトルの長さを得る。

        :rtype: `float`
        """
        d = self.__data
        return sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2])

    def lengthSq(self):
        u"""
        3次元ベクトルの長さの2乗を得る。

        :rtype: `float`
        """
        d = self.__data
        return d[0] * d[0] + d[1] * d[1] + d[2] * d[2]

    def normal(self):
        u"""
        正規化3次元ベクトルを得る。

        :rtype: `Vector`
        """
        v = _MV(self.__data).normalize()
        return _newV(_MP(v[0], v[1], v[2], self.__data[3]))

    def normalize(self):
        u"""
        正規化3次元ベクトルをセットする。

        :rtype: `Vector` (self)
        """
        d = self.__data
        v = _MV(d).normalize()
        d[0] = v[0]
        d[1] = v[1]
        d[2] = v[2]
        return self

    normalizeIt = normalize

    def rotateBy(self, q):
        u"""
        クォータニオンで回転したベクトルを得る。

        演算子 * でクォータニオンを乗じることと同じ。

        :type q: `.Quaternion`
        :param q: クォータニオン。
        :rtype: `Vector`
        """
        v = _MV(self.__data).rotateBy(q._Quaternion__data)
        return _newV(_MP(v[0], v[1], v[2], self.__data[3]))

    def rotateTo(self, v, factor=1.):
        u"""
        ベクトルを指定方向に向ける最小弧回転を得る。

        `.Quaternion`
        に2つのベクトルを渡して生成することと同じ。

        :type v: `Vector`
        :param v: 向ける方向。
        :param `float` factor: 完全に向ける量を 1.0 とする回転量。
        :rtype: `.Quaternion`
        """
        return _newQ(_MQ(_MV(self.__data), _MV(v.__data), factor))

    def transformAsNormal(self, m):
        u"""
        法線ベクトルとしてトランスフォームしたベクトルを得る。

        :type m: `.Matrix`
        :param m: 変換マトリックス。
        :rtype: `Vector`
        """
        src = self.__data
        w = src[3]
        src[3] = 0.
        dst = src * m._Matrix__data.inverse().transpose()
        src[3] = w
        dst[3] = w
        return _newV(dst)

    def distanceTo(self, v):
        u"""
        2つの位置ベクトル間の距離を得る。

        :type v: `Vector`
        :param v: もう1方の位置。
        :rtype: `float`
        """
        return self.__data.distanceTo(v.__data)

    def distanceSqTo(self, v):
        u"""
        2つの位置ベクトル間の2乗距離を得る。

        :type v: `Vector`
        :param v: もう1方の位置。
        :rtype: `float`
        """
        v = self.__data.distanceTo(v.__data)
        return v * v

    def cartesianize(self):
        u"""
        同次座標を直交座標(W=1)に変換する。

        (W*x, W*y, W*z, W) が (x, y, z, 1) に変換される。

        :rtype: `Vector` (self)
        """
        self.__data.cartesianize()
        return self

    def rationalize(self):
        u"""
        同次座標を有利形式に変換する。

        (W*x, W*y, W*z, W) が (x, y, z, W) に変換される。

        :rtype: `Vector` (self)
        """
        self.__data.rationalize()
        return self

    def homogenize(self):
        u"""
        有理形式の座標を同次座標に変換する。

        (x, y, z, W) が (W*x, W*y, W*z, W) に変換される。

        :rtype: `Vector` (self)
        """
        self.__data.homogenize()
        return self

    def cross(self, v):
        u"""
        3次元ベクトルの外積を得る。

        演算子 ^ と同じ。

        :type v: `Vector`
        :param v: もう1方のベクトル。
        :rtype: `Vector`
        """
        v = _MV(self.__data).__xor__(_MV(v.__data))
        return _newV(_MP(v[0], v[1], v[2], self.__data[3]))

    def dot(self, v):
        u"""
        3次元ベクトルの内積を得る。

        1x3 と 3x1 の行列としての乗算ともいえる。

        演算子 * と同じ。

        :type v: `Vector`
        :param v: もう1方のベクトル。
        :rtype: `float`
        """
        d = self.__data
        s = v.__data
        return d[0] * s[0] + d[1] * s[1] + d[2] * s[2]

    def dot4(self, v):
        u"""
        4次元ベクトルの内積を得る。

        1x4 と 4x1 の行列としての乗算ともいえる。

        :type v: `Vector`
        :param v: もう1方のベクトル。
        :rtype: `float`
        """
        d = self.__data
        s = v.__data
        return d[0] * s[0] + d[1] * s[1] + d[2] * s[2] + d[3] * s[3]

    def dot4r(self, v):
        u"""
        4次元ベクトルを 4x1 と 1x4 の行列として乗算する。

        :type v: `Vector`
        :param v: もう1方のベクトル。
        :rtype: `.Matrix`
        """
        a = self.__data
        b = v.__data
        return _newM(_MM([
            a[0] * b[0], a[0] * b[1], a[0] * b[2], a[0] * b[3],
            a[1] * b[0], a[1] * b[1], a[1] * b[2], a[1] * b[3],
            a[2] * b[0], a[2] * b[1], a[2] * b[2], a[2] * b[3],
            a[3] * b[0], a[3] * b[1], a[3] * b[2], a[3] * b[3],
        ]))

    def xform3(self, m):
        u"""
        3次元ベクトル（方向ベクトル）をトランスフォームする。
        """
        src = self.__data
        w = src[3]
        src[3] = 0.
        dst = src * m._Matrix__data
        src[3] = w
        dst[3] = w
        return _newV(dst)

    def xform4(self, m):
        u"""
        4次元ベクトル（3次元同次座標）をトランスフォームする。

        演算子 * で行列を乗じることと同じ。

        :type m: `.Matrix`
        :param m: 変換マトリックス。
        :rtype: `Vector`
        """
        return _newV(self.__data * m._Matrix__data)

    def abs(self):
        u"""
        4次元ベクトルの各要素を絶対値にしたベクトルを得る。

        abs 組み込み関数を使用する場合と等価。

        :rtype: `Vector`
        """
        v = self.__data
        return _newV(_MP(abs(v[0]), abs(v[1]), abs(v[2]), abs(v[3])))

    def iabs(self):
        u"""
        4次元ベクトルの各要素を絶対値にする。

        :rtype: `Vector` (self)
        """
        v = self.__data
        v[0] = abs(v[0])
        v[1] = abs(v[1])
        v[2] = abs(v[2])
        v[3] = abs(v[3])
        return self

    def mul(self, v):
        u"""
        4次元ベクトルの各要素を乗算したベクトルを得る。

        :type v: `Vector`
        :param v: もう1方のベクトル。
        :rtype: `Vector`
        """
        a = self.__data
        b = v.__data
        return _newV(_MP(a[0] * b[0], a[1] * b[1], a[2] * b[2], a[3] * b[3]))

    def imul(self, v):
        u"""
        4次元ベクトルの各要素を乗算したベクトルをセットする。

        :type v: `Vector`
        :param v: もう1方のベクトル。
        :rtype: `Vector` (self)
        """
        a = self.__data
        b = v.__data
        a[0] *= b[0]
        a[1] *= b[1]
        a[2] *= b[2]
        a[3] *= b[3]
        return self

    def div(self, v, pre=AVOID_ZERO_DIV_PRECISION):
        u"""
        4次元ベクトルの各要素を除算したベクトルを得る。

        :type v: `Vector`
        :param v: 分母のベクトル。
        :param `float` pre: ゼロ除算を避ける為の許容誤差。
        :rtype: `Vector`
        """
        a = self.__data
        b = v.__data
        return _newV(_MP(
            a[0] / avoidZeroDiv(b[0], pre),
            a[1] / avoidZeroDiv(b[1], pre),
            a[2] / avoidZeroDiv(b[2], pre),
            a[3] / avoidZeroDiv(b[3], pre),
        ))

    def idiv(self, v, pre=AVOID_ZERO_DIV_PRECISION):
        u"""
        4次元ベクトルの各要素を除算したベクトルをセットする。

        :type v: `Vector`
        :param v: 分母のベクトル。
        :param `float` pre: ゼロ除算を避ける為の許容誤差。
        :rtype: `Vector` (self)
        """
        a = self.__data
        b = v.__data
        a[0] /= avoidZeroDiv(b[0], pre)
        a[1] /= avoidZeroDiv(b[1], pre)
        a[2] /= avoidZeroDiv(b[2], pre)
        a[3] /= avoidZeroDiv(b[3], pre)
        return self

    def orthogonal(self, vec):
        u"""
        指定ベクトルに直交化したベクトルを得る。

        :type vec: `Vector`
        :param vec: 軸ベクトル。
        :rtype: `Vector`
        """
        a = self.__data
        b = _MV(vec.__data).normalize()
        v = a - b * (a[0] * b[0] + a[1] * b[1] + a[2] * b[2])
        return _newV(_MP(v[0], v[1], v[2], a[3]))

    def orthogonalize(self, vec):
        u"""
        指定ベクトルに直交化したベクトルをセットする。

        :type vec: `Vector`
        :param vec: 軸ベクトル。
        :rtype: `Vector` (self)
        """
        a = self.__data
        b = _MV(vec.__data).normalize()
        a -= b * (a[0] * b[0] + a[1] * b[1] + a[2] * b[2])
        return self

    def maxAxis(self, noSign=False):
        u"""
        絶対値が最大の要素の軸IDを得る。

        :param `bool` noSign: 符号ビットを含まない軸ID (0～2) を得る。
        :rtype: `int`
        """
        dt = self.__data
        ax = abs(dt[0])
        ay = abs(dt[1])
        az = abs(dt[2])
        if ax > ay:
            if ax > az:
                return AXIS_X if (noSign or dt[0] >= 0.) else AXIS_NEG_X
        elif ay > az:
            return AXIS_Y if (noSign or dt[1] >= 0.) else AXIS_NEG_Y
        return AXIS_Z if (noSign or dt[2] >= 0.) else AXIS_NEG_Z

    def minAxis(self, noSign=False):
        u"""
        絶対値が最小の要素の軸IDを得る。

        :param `bool` noSign: 符号ビットを含まない軸ID (0～2) を得る。
        :rtype: `int`
        """
        dt = self.__data
        ax = abs(dt[0])
        ay = abs(dt[1])
        az = abs(dt[2])
        if ax < ay:
            if ax < az:
                return AXIS_X if (noSign or dt[0] >= 0.) else AXIS_NEG_X
        elif ay < az:
            return AXIS_Y if (noSign or dt[1] >= 0.) else AXIS_NEG_Y
        return AXIS_Z if (noSign or dt[2] >= 0.) else AXIS_NEG_Z

    def findNearestAxis(self, asId=False):
        u"""
        方向ベクトルに最も近い X,Y,Z,-X,-Y,-Z 軸方向を得る。

        殆どゼロベクトルで判定できない場合は None となる。

        :param `bool` asId: 結果をIDで得る。
        :rtype: `Vector`, `int` or None
        """
        dt = self.__data
        max_a = 0.
        axis = None
        for key in _XYZ_AXES:
            v = dt[key]
            a = abs(v)
            if a > max_a:
                max_a = a
                axis = key
                if v < 0.:
                    axis += AXIS_NEG
        return axis if asId else _AXIS_VECTOR_DICT.get(axis)

    @env.Numpy
    def ndarray(self):
        import numpy as np
        return np.array(self.vector, dtype=np.float16)


V = Vector  #: `Vector` の別名。

_MUTATOR_DICT[V] = (
    'set',
    'normalize',
    'normalizeIt',
    'cartesianize',
    'rationalize',
    'homogenize',
    'iabs',
    'imul',
    'idiv',
    'orthogonalize',
)
ImmutableVector = immutableType(V)  #: `Vector` の `immutable` ラッパー。


def _newV(data, cls=V):
    obj = _object_new(cls)
    _V_setdata(obj, data)
    return obj


# _MV_Zero = _MV.kZeroVector
# _MQ_Identity = _MQ.kIdentity
# _MM_Identity = _MM.kIdentity

_ZERO3 = (0., 0., 0.)

_object_new = object.__new__

_V_setdata = V._Vector__data.__set__

V.Tolerance = _TOLERANCE  #: 同値とみなす許容誤差。

V.Zero4 = ImmutableVector(0., 0., 0., 0.)  #: 4次元ゼロベクトル。
V.Zero = ImmutableVector()  #: ゼロベクトル。
V.Origin = V.Zero  #: `Zero` と同じ。
V.One = ImmutableVector(1., 1., 1.)  #: 各要素が 1.0 のベクトル。
V.XAxis = ImmutableVector(1., 0., 0.)  #: X軸ベクトル。
V.YAxis = ImmutableVector(0., 1., 0.)  #: Y軸ベクトル。
V.ZAxis = ImmutableVector(0., 0., 1.)  #: Z軸ベクトル。
V.XNegAxis = ImmutableVector(-1., 0., 0.)  #: -X軸ベクトル。
V.YNegAxis = ImmutableVector(0., -1., 0.)  #: -Y軸ベクトル。
V.ZNegAxis = ImmutableVector(0., 0., -1.)  #: -Z軸ベクトル。

_AXIS_VECTOR_DICT = ImmutableDict({
    AXIS_X: V.XAxis,
    AXIS_Y: V.YAxis,
    AXIS_Z: V.ZAxis,
    AXIS_NEG_X: V.XNegAxis,
    AXIS_NEG_Y: V.YNegAxis,
    AXIS_NEG_Z: V.ZNegAxis,
})
V.AXIS_VECTOR_DICT = _AXIS_VECTOR_DICT  #: 軸 ID からベクトルを得る辞書。

_M_setdata = M._Matrix__data.__set__

M.Tolerance = _TOLERANCE  #: 同値とみなす許容誤差。

M.Identity = ImmutableMatrix()  #: 単位行列。
M.Zero = ImmutableMatrix([0] * 16)  #: ゼロ。


# ------------------------------------------------------------------------------
def _mirror(d, mirrorAxis, negAxis, t):
    if mirrorAxis is AXIS_X:
        t = -d[12] if t else d[12]
        if negAxis is mirrorAxis or negAxis is True:
            return _MM([d[0], -d[1], -d[2], 0., -d[4], d[5], d[6], 0., -d[8], d[9], d[10], 0., t, d[13], d[14], 1.])
        elif negAxis is None:
            return _MM([d[0], -d[1], -d[2], 0., d[4], -d[5], -d[6], 0., d[8], -d[9], -d[10], 0., t, d[13], d[14], 1.])
        elif negAxis is AXIS_Y:
            return _MM([-d[0], d[1], d[2], 0., d[4], -d[5], -d[6], 0., -d[8], d[9], d[10], 0., t, d[13], d[14], 1.])
        elif negAxis is AXIS_Z:
            return _MM([-d[0], d[1], d[2], 0., -d[4], d[5], d[6], 0., d[8], -d[9], -d[10], 0., t, d[13], d[14], 1.])
        else:
            return _MM([d[0], d[1], d[2], 0., d[4], d[5], d[6], 0., d[8], d[9], d[10], 0., t, d[13], d[14], 1.])

    elif mirrorAxis is AXIS_Y:
        t = -d[13] if t else d[13]
        if negAxis is mirrorAxis or negAxis is True:
            return _MM([d[0], -d[1], d[2], 0., -d[4], d[5], -d[6], 0., d[8], -d[9], d[10], 0., d[12], t, d[14], 1.])
        elif negAxis is None:
            return _MM([-d[0], d[1], -d[2], 0., -d[4], d[5], -d[6], 0., -d[8], d[9], -d[10], 0., d[12], t, d[14], 1.])
        elif negAxis is AXIS_X:
            return _MM([-d[0], d[1], -d[2], 0., d[4], -d[5], d[6], 0., d[8], -d[9], d[10], 0., d[12], t, d[14], 1.])
        elif negAxis is AXIS_Z:
            return _MM([d[0], -d[1], d[2], 0., d[4], -d[5], d[6], 0., -d[8], d[9], -d[10], 0., d[12], t, d[14], 1.])
        else:
            return _MM([d[0], d[1], d[2], 0., d[4], d[5], d[6], 0., d[8], d[9], d[10], 0., d[12], t, d[14], 1.])

    else:  # AXIS_Z
        t = -d[14] if t else d[14]
        if negAxis is mirrorAxis or negAxis is True:
            return _MM([d[0], d[1], -d[2], 0., d[4], d[5], -d[6], 0., -d[8], -d[9], d[10], 0., d[12], d[13], t, 1.])
        elif negAxis is None:
            return _MM([-d[0], -d[1], d[2], 0., -d[4], -d[5], d[6], 0., -d[8], -d[9], d[10], 0., d[12], d[13], t, 1.])
        elif negAxis is AXIS_X:
            return _MM([-d[0], -d[1], d[2], 0., d[4], d[5], -d[6], 0., d[8], d[9], -d[10], 0., d[12], d[13], t, 1.])
        elif negAxis is AXIS_Y:
            return _MM([d[0], d[1], -d[2], 0., -d[4], -d[5], d[6], 0., d[8], d[9], -d[10], 0., d[12], d[13], t, 1.])
        else:
            return _MM([d[0], d[1], d[2], 0., d[4], d[5], d[6], 0., d[8], d[9], d[10], 0., d[12], d[13], t, 1.])
