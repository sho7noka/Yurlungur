# Yurlungur

|       | Windows | CentOS/macOS | packages |
| ----- | --- | --- | --- |
| status |  |  | [![Latest PyPI version](https://img.shields.io/pypi/v/yurlungur.svg)](https://pypi.python.org/pypi/yurlungur) |


The universal scripting environment with Python which Maya, Houdini and Unreal Engine.

## summary
DCC tool scripting is almost used Python, but these api isn't similarly anything.
If you make lightweight tool, need to remember each application manners.
Yurlungur is common interface which adapted each application for universal wrapper.

Yurlungur is inspired by [PyMEL](https://github.com/LumaPictures/pymel).

### future
Yurlungur is pure Python and can be used **synchronously** in mixed Python2 and Python3 environments with RPC.

* Houdini Object Model like command wrapper.
* Qt for Python shorten accessor.
* Useful snippets for Game&VFX technical artist.

### available
|       | Node | Attribute | Sync |
| ---- | --- | --- | --- |
| Maya (2016~) | ○ | ○ | ○ |
| Substance 3D Designer (2018.1.2~) | ○ | ○ | ☓ |
| Houdini (16~) | ○ | ○ | ○ |
| Unreal Engine (4.22~) | ○ | ○ | ☓ |
| Unity (2019.1~) | ○ | ○ | ○ |
| Blender (2.80~) | ○ | ○ | ○ |
| Nuke (10~) | ○ | ○ | ☓ |
| Davinci Resolve(&Fusion) (15~) | ○ | ○ | ☓ |
| Cinema4D (R21~) | ○ | ○ | ☓ |
| 3dsMax (2017~) | ○ | ○ | ○ |
| Substance 3D Painter (2020~) | ☓ | ☓ | ○ |
| Marmoset Toolbag (3~) | ○ | ○ | ☓ |

We also support Photoshop, Modo, Renderdoc(and RV).


#### Why Sync?
Some DCC applications that support Python, such as Substance3DPainter, MarmosetToolbag, and RenderDoc
There are also applications that specialize in specific functions and require less scene graph manipulation.

A mechanism for pseudo-operation of the linked application from the host application can be created by using a
This is achieved by combining standard formats such as FBX and USD, RPC, shared maps and clipboards.

The SDK can be used for vendor or proprietary applications, or for applications that are restricted by open source licenses and cannot embed the SDK in the application.
Users do not need to be constrained by vendor, proprietary application, or open source license restrictions that prevent the SDK from being built into the application.


### Installation
```bash
$ pip install yurlungur
```

#### optional
If you use UE4 Editor or Standalone for full supports, Yurlungur recommend `Qt for Python` module.

```bash
$ pip install PySide2
```

### semantics

```python
# Blender Python
import bpy
bpy.data.objects["foo"].bar = True
```

```sh
// Maya MEL
setAttr "foo.bar" true;
```

```cs
// Unity C#
using UnityEngine;
UnityEngine.GameObject.Find("foo").bar = true;
```

YNode behaves as a base class for the object.

```python
# yurlungur
import yurlungur as yr

yr.Node("foo").bar.set(True)
``` 

Sample scripts can be found [here](./sample/script/renamer.py).

## contribution

lets see [CONTRIBUTING](./.github/CONTRIBUTING.md).

## License

Yurlungur is [MIT](./LICENSE.md) License.
