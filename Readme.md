# Yurlungur

|       | Windows | Unix | code |
| ----- | ------ | --- | --- |
| OS | [![Build status](https://ci.appveyor.com/api/projects/status/46vinb8jd1jbbhdg?svg=true)](https://ci.appveyor.com/project/sho7noka/yurlungur) | [![Build Status](https://travis-ci.org/sho7noka/Yurlungur.svg?branch=dev)](https://travis-ci.org/sho7noka/Yurlungur) | [![codecov](https://codecov.io/gh/sho7noka/Yurlungur/branch/dev/graph/badge.svg)](https://codecov.io/gh/sho7noka/Yurlungur) |


universal scripting environment with Python which Maya, Houdini and Blender.

## summary
DCC tool scripting is almost used Python, but these api isn't similarly anything.
If you make lightweight tool, need to remember each application manners.
Yurlungur is common interface which adapted each application for universal wrapper.

Yurlungur is inspired by [PyMEL](https://github.com/LumaPictures/pymel).

### future
* HOM (Houdini Object Model) like command wrapper.
* PySide & PyQt shorten accessor.
* Useful py-snippet for Game&VFX technical artist.

### available
|       | Node | Attribute | Anim |
| ---- | --- | --- | --- |
| Maya (2016~) | ○ | ○ | ☓ |
| Houdini (16~) | ○ | ○ | ☓ |
| Substance (2018.1.2~) | ○ | ○ | - |
| 3dsMax (2017~) | ○ | ○ | ☓ |
| Photoshop (CC) | ○ | ○ | - |
| Marvelous Designer 8 (WIP) | ○ | ○ | - |
| Nuke Studio | ○ | ○ | ☓ |
| Davinci Resolve (15~) | ○ | ○ | ☓ |
| Unreal Engine (4.22~) | ○ | ○ | ☓ |

| Blender (2.8) | ○ | ○ | ☓ |

### Installing
```bash
pipenv install yurlungur
```

#### optional
If you use UE4 Editor or Standalone for full supports, Yurlungur require `Qt for Python` module.

```bash
pipenv install PySide2
```

### semantics

```python
# Blender
bpy.data.objects["foo"].bar = 1
```

```mel
// MEL
setAttr "foo.bar" 1;
```

```python
# yurlungur
import yurlungur as yr
yr.YNode("foo").bar.set(1)
```

## TODO
- [x] basic api
- [x] github.io
- [x] UE4 

## contribution
lets see [CONTRIBUTING](./CONTRIBUTING.md).


## License
Yurlungur is [MIT](./LICENSE.md) License.
