# -*- coding: utf-8 -*-
import os
import sys
import inspect
import subprocess
import tempfile
import multiprocessing
import multiprocessing.process as process

import yurlungur as yr
from yurlungur.core import env

local = os.path.dirname(os.path.dirname(inspect.currentframe().f_code.co_filename))
__all__ = map(lambda x: x[0], inspect.getmembers(sys.modules[__name__], inspect.isclass))


try:
    from yurlungur.Qt.QtCore import *
    from yurlungur.Qt.QtGui import *
    from yurlungur.Qt.QtWidgets import *
    from yurlungur.Qt import __binding__

    # script editor
    sys.path.append(os.path.join(
        os.path.dirname(local), "scriptEditor", "pw_multiScriptEditor")
    )
    from pw_multiScriptEditor import scriptEditorClass

except ImportError as e:
    pass


def mayapy(pystr):
    assert os.path.getsize(env.MayaBin)

    exe = sys.executable
    multiprocessing.set_executable(
        os.path.join(os.path.dirname(exe), "mayapy")
    )

    process.ORIGINAL_DIR = os.path.join(
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
    assert os.path.getsize(env.HoudiniBin)
    subprocess.call(
        "{0}/hython -c\"import sys; sys.path.append('{1}');{2}\"".format(env.HoudiniBin, local, pystr)
    )


def bpython(pystr):
    assert os.path.getsize(env.BlenderBin)
    subprocess.call(
        "{0}.blender --python-expr {1} -b".format(env.BlenderBin, pystr)
    )

def maxpy(pystr):
    assert os.path.getsize(env.MaxBin)
    subprocess.call(
        "{0}/3dsmaxpy -c \"{1};{2}\"".format(env.MaxBin, sys.path.append(yr), pystr)
    )

def uepython(project, pystr):
    assert os.path.getsize(env.UnrealBin) or os.path.exists(project)

    # temp
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.write(pystr)
    subprocess.call(
        "{0}/UE4Editor-Cmd {1} ExecutePythonScript = {2}".format(env.UnrealBin, project, pyfile)
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


def main(args=[]):
    if yr.Qt():
        app = QApplication(args)
        widget = scriptEditorClass()
        widget.show()
        sys.exit(app.exec_())
    else:
        yr.logger.warn("Qt isn't available")


if __name__ == '__main__':
    main(sys.argv[1:])
