# -*- coding: utf-8 -*-
import sys, types
from math import sqrt, pi as PI  #: π
from numbers import Number
from yurlungur.core import env


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

elif env.Rumba():  # and Katana
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

elif env.Houdini() or env.Unreal():
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

Vector = _MV
Matrix = _MM
Color = _MV
