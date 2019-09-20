# -*- coding: utf-8 -*-
import sys
import os
import inspect
import multiprocessing
import subprocess
import tempfile

import yurlungur as yr
from yurlungur.core import env

local = os.path.dirname(os.path.dirname(inspect.currentframe().f_code.co_filename))
__all__ = map(lambda x: x[0], inspect.getmembers(sys.modules[__name__], inspect.isclass))


def set(module):
    """
    set external application
    :param module:
    :return:

    >>> yr.application.set(module)
    """
    from yurlungur.core import app

    if module == "photoshop":
        from yurlungur.adapters import photoshop

        app.application = photoshop.app
    else:
        app.application = env.__import__(module)

    assert app.application


def mayapy(pystr):
    assert os.path.getsize(env.MayaBin)

    exe = sys.executable
    multiprocessing.set_executable(
        os.path.join(os.path.dirname(exe), "mayapy")
    )

    multiprocessing.process.ORIGINAL_DIR = os.path.join(
        os.path.dirname(exe),
        "../Python/Lib/site-packages"
    )
    po = multiprocessing.Pool(4)

    subprocess.call(
        "{0}/bin/mayapy -c \"{1};{2};{3}\"".format(
            env.MayaBin, "import maya.standalone;maya.standalone.initialize(name='python')",
            "import sys; sys.path.append('{0}');".format(local) + pystr, "maya.standalone.uninitialize()"
        )
    )


def hython(pystr):
    assert os.path.getsize(env._Houdini())
    subprocess.call(
        "{0}/hython -c\"import sys; sys.path.append('{1}');{2}\"".format(env._Houdini(), local, pystr)
    )


def bpython(pystr):
    assert os.path.getsize(env._Blender())
    print ("{0} --python-expr \"{1}\" -b".format(env._Blender(), pystr))
    subprocess.call(
        "{0} --python-expr \"{1}\" -b".format(env._Blender(), pystr)
    )


def c4dpy(pystr):
    assert os.path.getsize(env._Cinema4D())
    subprocess.call(" ".join(env._Cinema4D(), "-c", pystr))


def maxpy(pystr):
    # http://help.autodesk.com/view/3DSMAX/2019/ENU/?guid=GUID-96D3ABE3-32CA-491D-9CAD-0A0576346E54
    assert os.path.getsize(env._Max())
    subprocess.call(
        "{0}/3dsmaxpy -c \"{1};{2}\"".format(env.MaxBin, sys.path.append(yr), pystr)
    )


def uepython(project, pystr):
    assert os.path.getsize(env.UnrealBin) or os.path.exists(project)

    # temp
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.write(pystr)
    subprocess.call(
        "{0}/UE4Editor-Cmd -run=pythonscript -script={1}".format(env.UnrealBin, tf)
    )


def _cli(args):
    """
    command line parser
    """
    try:
        import argparse
    except ImportError:
        yr.logger.warn("argparse is not found.")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        prog='yr.cli',
        usage='Demonstration of argparser',
        description='yurlungur console.',
        epilog="{0} v.{1} {2}".format(yr.name, yr.version, sys.executable),
        add_help=True,
    )
    parser.add_argument("--dialog", "-d",
                        help="Launch yr.widget if Qt is installed.",
                        action="store_true")
    parser.add_argument("--mayapy", "-ma",
                        help="Run Python from mayapy.",
                        nargs=1)
    parser.add_argument("--hython", "-hou",
                        help="Run Python from hython.",
                        nargs=1)
    parser.add_argument("--unrealpy", "-ue",
                        help="Run Python from unreal editor cmd.",
                        nargs=2)
    parser.add_argument("--maxpy", "-max",
                        help="Run Python from 3dsmaxpy.",
                        nargs=2)
    parser.add_argument("--qt", "-qt",
                        help="install Qt for Python.",
                        nargs=2)
    parser.add_argument("--setenv", "-env",
                        help="init ENV settings.",
                        nargs=2)
    parser.add_argument("--debug", "-debug",
                        help="install ptvsd modules.",
                        nargs=2)

    args = parser.parse_args(args)
    if args.dialog:
        main()

    if args.mayapy:
        mayapy(args.mayapy[0])

    if args.hython:
        hython(args.hython[0])

    if args.unrealpy:
        project, expr = args.unrealpy
        uepython(project, expr)

    if args.maxpy:
        maxpy(args.maxpy[0])

    if args.qt:
        pass

    if args.setenv:
        pass

    if args.debug:
        pass


def main(args=[]):
    from yurlungur.tool import editor
    widget = editor.View()
    yr.ui.show(widget)


if __name__ == '__main__':
    main(sys.argv[1:])
