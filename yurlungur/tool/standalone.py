# coding: utf-8
import sys
from yurlungur.adapters import *  # noQA


def _cli(args):
    """
    yurlungur command line parser

    Args:
        args:

    Returns:

    """
    import argparse, yurlungur

    parser = argparse.ArgumentParser(
        prog='yurlungur.tool.standalone._cli',
        description="{0} v.{1} {2}".format(yurlungur.name, yurlungur.version, sys.executable),
        epilog='yurlungur console',
        add_help=True,
    )

    parser.add_argument("--command", "-c",
                        help="program passed in as string (terminates option list)",
                        nargs=2, type=str, metavar=("cmd", "app"), )

    parser.add_argument("--environ", "-e",
                        help="set ENV settings for module",
                        nargs=1, type=str, metavar="mod", )

    parser.add_argument("--qt4python", "-q",
                        help="install Qt for Python.",
                        action="store_true", )

    parser.add_argument("--shotg", "-s",
                        help="install shotgrid(shotgun) modules.",
                        action="store_true", )

    parser.add_argument("--window", "-w",
                        help="show editor window",
                        action="store_true", )

    arguments = parser.parse_args(args)

    if arguments.command:
        cmd, app = arguments.command
        try:
            getattr(sys.modules[__name__], app).shell(cmd)
        except AttributeError:
            print(
                "%s is not found." % app,
                [m for m in dir(sys.modules[__name__]) if not m.startswith("_") and m != "sys"]
            )

    if arguments.environ:
        from yurlungur.core.app import use;
        use(arguments.environ[0])

    if arguments.window:
        from yurlungur.tool.window import console;
        console()

    if arguments.qt4python:
        from yurlungur.core.env import set;
        set("vfxwindow PySide2")

    if arguments.shotg:
        from yurlungur.core.env import set;
        set("git+git://github.com/shotgunsoftware/python-api.git")

if __name__ == '__main__':
    _cli(sys.argv[1:])
