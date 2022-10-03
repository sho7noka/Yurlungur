# -*- coding: utf-8 -*-
import sys
import subprocess
import tempfile
import os
import functools
import platform
import contextlib


def __import__(name, globals=None, locals=None, fromlist=None):
    """
    Fast path:
    see if the module has already been imported.

    Args:
        name:
        globals:
        locals:
        fromlist:

    Returns:
    """
    try:
        return sys.modules[name]
    except KeyError:
        pass

    try:
        if "DaVinci" not in name:
            raise NameError
        else:
            name = "DaVinciResolveScript"

        if platform.system() == "Windows":
            resolve = "%PROGRAMDATA%\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules"
        if platform.system() == "Darwin":
            resolve = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"
        if platform.system() == "Linux":
            resolve = "/opt/resolve/Developer/Scripting/Modules"
        sys.path.append(resolve)

    except NameError:
        pass

    # https://pythonnet.github.io/ or https://ironpython.net/
    if "clr" in sys.modules:
        import clr
        clr.AddReference("System.IO")
        import System.IO

        try:
            clr.AddReference(name)
        except System.IO.FileNotFoundException:
            pass

    if sys.version_info[0] < 3:
        import imp
        fp, pathname, description = imp.find_module(name)
        return imp.load_module(name, fp, pathname, description)

    else:
        try:
            from importlib import import_module
            return import_module(name)
        except ImportError:
            return False


def set(module=None):
    """
    yurlungur
        yurlungur.env
        modules
            PySide2
            ...
    """
    if platform.system() == "Windows":
        path = os.getenv("USERPROFILE").replace("\\", "/") + r"/Documents/yurlungur/modules"
    if platform.system() == "Darwin":
        path = os.getenv("HOME") + "/Documents/yurlungur/modules"
    if platform.system() == "Linux":
        path = "/opt/yurlungur/modules"

    env_file = os.path.join(os.path.dirname(path), "yurlungur.env")
    if not os.path.exists(path):
        os.makedirs(path)
        with open(env_file, "w") as f:
            f.write("")

    if module:
        pip = get_pip()
        try:
            pip.main(["install", * module.split(" "), "-t", path])
        except:
            pip.main(["install", module, "-t", path])
    sys.path.append(path)


def get_pip():
    """

    Returns:

    """
    try:
        import pip
    except ImportError:
        url = "https://raw.github.com/pypa/pip/master/contrib/get-pip.py"

        if sys.version_info.major >= 3:
            import urllib.request as _urllib
            _urllib.urlretrieve(url, "get-pip.py")
            exec(open("get-pip.py"))
        else:
            import urllib as _urllib
            _urllib.urlretrieve(url, "get-pip.py")
            execfile("get-pip.py")

        os.remove("get-pip.py")

    if not getattr(pip, "main", False):
        from pip import _internal as pip
    return pip


# pip = get_pip()


class App(object):
    def __init__(self, name):
        d = {
            "maya": v(_Maya), "houdini": v(_Houdini), "substance_designer": v(_Substance),
            "unreal": v(_Unreal), "unity": v(_Unity), "blender": v(_Blender), 
            "nuke": v(_Nuke), "c4d": v(_Cinema4D), "davinci": v(_Davinci),
            "3dsmax": v(_Max), "marmoset": v(_Marmoset),"substance_painter": v(_SubstancePainter),
            "photoshop": v(_Photoshop), "renderdoc": v(_RenderDoc), # "rv": v(_RV),
            "modo": v(_Modo)
        }
        self.app_name = d[name]
        self.process = None

        # add PYTHONAPATH
        import yurlungur
        pypath = os.path.dirname(os.path.dirname(yurlungur.__file__))

        if platform.system() == "Windows":
            self.python_path = "set PYTHONPATH=%PYTHONPATH$;{0}&&".format(pypath)
        else:
            self.python_path = "export PYTHONPATH=$PYTHONPATH:{0};".format(pypath)

    def run(self):
        self.app_name = self.python_path + "\"" + self.app_name + "\""

        try:
            self.process = subprocess.Popen(self.app_name, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            while self.process.poll() is None:
                print(self.process.stdout.readline().decode().strip())

        except (KeyboardInterrupt, SystemExit):
            self.quit()

        except OSError:
            print("%s is not found" % self.app_name)

    def shell(self, cmd=""):
        cmd = "from yurlungur.api import *;" + cmd

        # https://knowledge.autodesk.com/ja/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2018/JPN/Maya-Scripting/files/GUID-83799297-C629-48A8-BCE4-061D3F275215-htm.html
        if "maya" in self.app_name:
            mayapy = self.app_name.replace("bin/maya", "bin/mayapy")
            _cmd = "\"%s\" -i -c \"import maya.standalone;maya.standalone.initialize(name='python');%s\"" % (mayapy, cmd)

        # https://www.sidefx.com/ja/docs/houdini/hom/commandline.html
        elif "houdini" in self.app_name:
            if platform.system() == "Windows":
                hython = self.app_name.replace("houdini.exe", "hython.exe")
            else:
                hython = "cd %s; source ./houdini_setup; hython" % os.path.dirname(os.path.dirname(self.app_name))
            _cmd = "%s -i -c \"%s\"" % (hython, cmd)

        # https://help.autodesk.com/view/3DSMAX/2018/ENU/?guid=__developer_executing_python_scripts_from_th_html
        elif "3dsmax" in self.app_name:
            if sys.version_info.major > 2:
                maxpy = os.path.join(os.path.dirname(self.app_name), "Python37\\python.exe")
            else:
                maxpy = self.app_name.replace("3dsmax.exe", "3dsmaxpy.exe")

            _cmd = "%s -i -c \"%s\"" % (maxpy, cmd)

        # https://docs.unrealengine.com/ja/Engine/Editor/ScriptingAndAutomation/Python/index.html
        # UnrealEditor-Cmd.exe
        elif "UE_" in self.app_name:
            with tempfile.NamedTemporaryFile(delete=False) as tf:
                tmp = tf.name + '.py'
                with open(tmp, 'w') as fp:
                    fp.write(cmd)
                    _app = os.path.join(os.path.dirname(self.app_name), "UE4Editor-Cmd")
                    if not os.path.exists(_app):
                        _app = _app.replace("UE4Editor-Cmd", "UnrealEditor-Cmd")
                    _cmd = " ".join([_app, "-run=pythonscript -script={0}".format(tmp)])

        # https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html#python-options
        elif "Blender" in self.app_name:
            _cmd = "{0} --python-expr '{1}' -b".format(self.app_name, cmd)

        # https://docs.unity3d.com/jp/460/Manual/CommandLineArguments.html
        elif "Unity" in self.app_name:
            from yurlungur.adapters import unity
            unity.initialize_package()
            _cmd = "%s -batchmode -executeMethod PythonExtensions.Startup.Exec \"%s\"" % (self.app_name, cmd)

        # https://learn.foundry.com/nuke/8.0/content/user_guide/configuring_nuke/command_line_operations.html
        elif "nuke" in self.app_name:
            _cmd = self.app_name + " -t"

        # https://developers.maxon.net/docs/Cinema4DPythonSDK/html/manuals/introduction/python_c4dpy.html
        elif "c4d" in self.app_name:
            self.app_name = self.app_name.replace("Cinema 4D", "c4dpy")

        # https://www.steakunderwater.com/wesuckless/viewtopic.php?t=2012
        elif "Resolve" in self.app_name:
            # "%PROGRAMFILES%\\Blackmagic Design\\DaVinci Resolve\\fuscript.exe <script> [args] -l python3
            _cmd = self.app_name + " -nogui"

        # toolbag.exe -pypath "C:/More/Python/Here" "C:/myscript.py"
        elif "toolbag" in self.app_name:
            with tempfile.NamedTemporaryFile(delete=False) as tf:
                tmp = tf.name + '.py'
                with open(tmp, 'w') as fp:
                    fp.write(cmd)

                import yurlungur
                pypath = os.path.dirname(os.path.dirname(yurlungur.__file__))
                _cmd = f"\"{self.app_name}\" -pypath \"{pypath}\" \"{tmp}\""  

        # https://substance3d.adobe.com/documentation/spdoc/remote-control-with-scripting-216629326.html
        elif "Painter" in self.app_name:
            _cmd = f"\"{self.app_name}\" --enable-remote-scripting"

        elif "renderdoc" in self.app_name:
            _cmd = self.app_name

        elif "modo" in self.app_name:
            _cmd = self.app_name.replace("/modo", "/modo_cl") + " -console:python -cmdlate:@mytelnet.py"

        try:
            os.system(self.python_path + _cmd)
        except (KeyboardInterrupt, SystemExit):
            raise

    @contextlib.contextmanager
    def connect(self, port=18811):
        """
        https://qiita.com/QUANON/items/c5868b6c65f8062f5876
        """
        from yurlungur.tool.rpc import session
        try:
            self.shell("from yurlungur.tool.rpc import listen; listen(%d)" % port)
            yield session(port)
        finally:
            print("revert")

    def quit(self):
        """
        リモートから終了
        Returns:

        """
        try:
            self.process.terminate()

        except AttributeError:
            if "maya" in self.app_name:
                import maya
                maya.standalone.uninitialize()
                maya.cmds.quit(force=True)
            elif "houdini" in self.app_name:
                import hou
                hou.releaseLicense()
                hou.exit()
            elif "Resolve" in self.app_name:
                import yurlungur
                yurlungur.meta.resolve.Quit()
            elif "Painter" in self.app_name:
                import yurlungur
                r = yurlungur.substance_painter.RemotePainter()
                r.checkConnection()
                r.execScript("from yurlungur.tool import window; window.main_window().close()")
            elif "photoshop" in self.app_name:
                from yurlungur.adapters.photoshop import do
                do("quit")  # do("var idquit = charIDToTypeID(\"quit\"); executeAction(idquit, undefined, DialogModes.ALL);")

            sys.exit()

    @property
    def _actions(self):
        """
        Returns:
           run, shell, quit, connect
        """
        return self.run, self.shell, self.quit, self.connect


def Maya(func=None):
    if func is None:
        return "maya" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "maya" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def Houdini(func=None):
    if func is None:
        return __import__("hou")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("hou"):
            return func(*args, **kwargs)

    return wrapper


def Substance(func=None):
    if func is None:
        return __import__("substance_designer")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("substance_designer"):
            return func(*args, **kwargs)

    return wrapper


def Blender(func=None):
    if func is None:
        return "blender" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "blender" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def Unreal(func=None):
    if func is None:
        return __import__("unreal")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("unreal"):
            return func(*args, **kwargs)

    return wrapper


def Unity(func=None):
    if func is None:
        return __import__("UnityEngine")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("UnityEngine"):
            return func(*args, **kwargs)

    return wrapper


def Nuke(func=None):
    if func is None:
        return "Nuke" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "Nuke" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def C4D(func=None):
    if func is None:
        return "Cinema 4D" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "Cinema 4D" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def Davinci(func=None):
    if func is None:
        return __import__("DaVinciResolveScript")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("DaVinciResolveScript"):
            return func(*args, **kwargs)

    return wrapper


def Marmoset(func=None):
    if func is None:
        return __import__("mset")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("mset"):
            return func(*args, **kwargs)

    return wrapper


def SPainter(func=None):
    if func is None:
        return __import__("substance_painter")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("substance_painter"):
            return func(*args, **kwargs)

    return wrapper


def Max(func=None):
    if func is None:
        return "3dsmax" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "3dsmax" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def Photoshop(func=None):
    if func is None:
        try:
            from yurlungur.adapters import photoshop
            return photoshop.app.isRunning()
        except Exception:
            return False

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            from yurlungur.adapters import photoshop
            if photoshop.app.isRunning():
                return func(*args, **kwargs)
            else:
                raise WindowsError
        except Exception:
            return False

    return wrapper


def RenderDoc(func=None):
    if func is None:
        return __import__("renderdoc")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("renderdoc"):
            return func(*args, **kwargs)

    return wrapper


def RV(func=None):
    if func is None:
        return __import__("rv")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("rv"):
            return func(*args, **kwargs)

    return wrapper


def Modo(func=None):
    if func is None:
        return __import__("modo")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("modo"):
            return func(*args, **kwargs)

    return wrapper


def _Maya(v=2022):
    d = {
        "Linux": "/usr/Autodesk/maya%d-x64/bin/maya" % v,
        "Windows": r"{1}/Autodesk/Maya{0}/bin/maya.exe".format(v, os.environ.get("PROGRAMFILES").replace("\\", "/")),
        "Darwin": "/Applications/Autodesk/maya%d/Maya.app/Contents/bin/maya" % v,
    }
    return d[platform.system()]


def _Houdini(v="17.5.173"):
    d = {
        "Linux": "/opt/hfs%s/houdini" % v,
        "Windows": os.environ.get("PROGRAMFILES") + "\\Side Effects Software\\Houdini {0}\\bin\\houdini.exe".format(v),
        "Darwin": "/Applications/Houdini/Houdini%s/Frameworks/Houdini.framework/Versions/%s/Resources/bin/houdini" % (
            v, v[:4]),
    }
    return os.environ.get("HIP") or d[platform.system()]


def _Substance():
    d = {
        "Linux": "/opt/Allegorithmic/Substance_Designer/Substance Designer",
        "Windows": os.environ.get("PROGRAMFILES") + "\\Adobe\\Adobe Substance 3D Designer\\Adobe Substance 3D Designer.exe",
        "Darwin": "/Applications/Substance\ Designer.app/Contents/MacOS/Substance\ Designer",
    }
    return d[platform.system()]


def _Blender():
    d = {
        "Linux": "/usr/bin/blender",
        "Windows": os.environ.get("PROGRAMFILES") + "\\Blender Foundation\\Blender",
        "Darwin": "/Applications/Blender.app/Contents/MacOS/Blender"
    }
    return d[platform.system()]


def _Unreal(v=4.27):
    d = {
        "Linux": "",
        "Windows": os.environ.get("PROGRAMFILES") + "\\Epic Games\\UE_{0}\\Engine\\Binaries\\Win64\\UE4Editor.exe".format(v),
        "Darwin": "/Users/Shared/Epic\ Games/UE_%s/Engine/Binaries/Mac/UE4Editor.app/Contents/MacOS/UE4Editor" % v
    }
    return d[platform.system()]


def _Unity(v="2021.1.0b4"):
    # https://docs.unity3d.com/ja/2019.1/Manual/CommandLineArguments.html
    d = {
        "Linux": "",
        "Windows": os.environ.get("PROGRAMFILES") + "\\Unity\\Hub\\Editor\\{0}\\Editor\\Unity.exe".format(v),
        #os.environ.get("PROGRAMFILES") +  \\Unity 2021.1.0b12\\Editor\\Unity.exe"
        "Darwin": "/Applications/Unity/Hub/Editor/{0}/Unity.app/Contents/MacOS/Unity".format(v)
    }
    return d[platform.system()]


def _Nuke(v="12.2v5"):
    d = {
        "Linux": "/usr/local/Nuke%s/Nuke%s" % (v, v[:4]),
        "Windows": os.environ.get("PROGRAMFILES") + "\\Nuke{0}\\Nuke{1}.exe".format(v, v[:4]),
        "Darwin": "/Applications/Nuke%s/Nuke%s.app/Contents/MacOS/Nuke%s" % (v, v, v[:4])
    }
    return d[platform.system()]


def _Cinema4D(v=21):
    d = {
        "Linux": "",
        "Windows": "C:/Cinema/R%d/Cinema 4D.exe" % v,
        "Darwin": "/Applications/Maxon\ Cinema\ 4D\ R%d/Cinema\ 4D.app/Contents/MacOS/Cinema\ 4D" % v
    }
    return d[platform.system()]


def _Davinci():
    d = {
        "Linux": "/opt/resolve/bin/resolve",
        "Windows": os.environ.get("PROGRAMFILES") + "\\Blackmagic Design\\DaVinci Resolve Studio\\Resolve.exe",
        "Darwin": "/Applications/DaVinci Resolve Studio.app/Contents/MacOS/Resolve"
    }
    return d[platform.system()]


def _Marmoset(v=4):
    d = {
        "Linux": "",
        "Windows": r"{0}/Marmoset/Toolbag {1}/toolbag.exe".format(os.environ.get("PROGRAMFILES").replace("\\", "/"), v),
        "Darwin": "/Applications/Marmoset\ Toolbag\ %d/Marmoset\ Toolbag.app/Contents/MacOS/Marmoset\ Toolbag" % v
    }
    return d[platform.system()]


def _SubstancePainter():
    """https://substance3d.adobe.com/documentation/spdoc/retrieving-the-installation-path-170460205.html"""
    d = {
        "Linux": "	/opt/Adobe/Adobe_Substance_3D_Painter",
        "Windows":  r"{0}/Adobe/Adobe Substance 3D Painter/Adobe Substance 3D Painter.exe".format(os.environ.get("PROGRAMFILES").replace("\\", "/")),
        "Darwin": "/Applications/Adobe\ Substance\ 3D\ Painter.app/Contents/MacOS/Adobe\ Substance\ 3D\ Painter"
    }
    return d[platform.system()]


def _Max(v=2021):
    return (os.getenv("ADSK_3DSMAX_X64_%d" % v) or os.environ.get("PROGRAMFILES") + "\\Autodesk\\3ds Max {0}\\".format(v)) + "3dsmax.exe"


def _Photoshop(v=2018):
    d = {
        "Linux": "",
        "Windows": os.environ.get("PROGRAMFILES") + "\\Adobe\\Adobe Photoshop CC {0}\\Photoshop.exe".format(v),
        "Darwin": "/Applications/Adobe\ Photoshop\ CC\ {0}/Adobe\ Photoshop\ CC\ {0}.app/Contents/MacOS/Adobe\ Photoshop\ CC\ {0}".format(
            v),
    }
    return d[platform.system()]


def _RenderDoc(v=1.13):
    d = {
        "Linux": "/opt/renderdoc_%d/bin/qrenderdoc" % v,
        "Windows": os.environ.get("PROGRAMFILES") + "\\RenderDoc\\qrenderdoc.exe",
        "Darwin": "coming soon..."
    }
    return d[platform.system()]


def _RV():
    d = {
        "Linux": "/opt/renderdoc_%d/bin/qrenderdoc" % v,
        "Windows": os.environ.get("PROGRAMFILES") + "\\RenderDoc\\qrenderdoc.exe",
        "Darwin": "coming soon..."
    }
    return d[platform.system()]


def _Modo(v="16.0v3"):
    d = {
        "Linux": "/opt/modo_{0}/bin/modo".format(v),
        "Windows": "\"{0}/Foundry/Modo/{1}/modo.exe\"".format(os.environ.get("PROGRAMFILES").replace("\\", "/"), v),
        "Darwin": "/Applications/Foundry/Modo/{0}/modo.app/Contents/MacOS/modo".format(v)
    }
    return d[platform.system()]


def Qt(func=None):
    """
    except for Cinema4D, Marmoset

    Args:
        func:

    Returns:

    """
    try:
        from yurlungur.user import Qt
        is_Qt = any([Qt])
    except ImportError:
        return False

    if func is None:
        return is_Qt

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if is_Qt:
            return func(*args, **kwargs)

    return wrapper


def Numpy(func=None):
    """
    Blender, Houdini, Rumba

    Args:
        func:

    Returns:

    """
    try:
        import numpy
        is_numpy = True
    except ImportError:
        return False

    if func is None:
        return numpy

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if is_numpy:
            return func(*args, **kwargs)

    return wrapper


def is_version(app):
    """
    TODO: 力技でバージョンを探す

    無し : Blender, Substance Painter/Designer, Davinci Resolve
    西暦 : Maya, Cinema4D, 3dsMax, Photoshop
    容易 : Unreal4.27-, Marmoset4-, RenderDoc1.13-
    独自 : Unity2021.-, Nuke12-, Houdini18.5-

    Args:
        app:

    Returns:

    """
    import os, datetime, re

    if list(filter(lambda x: app == x, [_Blender, _Substance, _SubstancePainter, _Davinci])):
        if os.path.exists(app()):
            return app()
        return None

    if app == _Marmoset:
        for i in range(3):
            v = 5 - i
            if os.path.exists(app(v)):
                return app(v)
        return None

    if app == _RenderDoc:
        for i in range(20):
            v = (120 - i) / 100
            if os.path.exists(app(v)):
                return app(v)
        return None

    if app == _Unreal:
        for i in range(120):
            v = (400 + i) / 100

            # ue5
            if v >= 5:
                app = app(v).replace("UE4Editor", "UnrealEditor")
                if v == 5.0:
                    app = app.replace("\\Engine", "EA\\Engine")
                if os.path.exists(app):
                    return app
                return None

            # ue4
            if os.path.exists(app(v)):
                return app(v)
        return None

    if app == _Unity:
        hub = "%PROGRAMFILES%\\Unity\\Hub\\Editor" if platform.system() == "Windows" else "/Applications/Unity/Hub/Editor"

        try:
            versions = os.listdir(hub)
            return app(versions[-1])
        except FileNotFoundError:
            return None

    # TODO
    if app == _Nuke or app == _Modo:
        v = 10
        # re.search("\d\d\.\dv\d", app(v))
        return app()

    if app == _Houdini:
        # re.search("\d\d\.\d\.\d\d\d")
        return app()

    # LTS < 5
    for i in range(6):
        v = datetime.date.today().year + 1 - i
        if os.path.exists(app(v)):
            return app(v)

    return None


v = is_version
