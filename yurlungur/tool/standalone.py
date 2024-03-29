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
        epilog='yurlungur console', add_help=True,
    )

    parser.add_argument("--command", "-c",
                        help="program passed in as string (terminates option list)",
                        nargs=2, type=str, metavar=("app", "cmd"), )

    parser.add_argument("--environ", "-e",
                        help="set ENV settings for module",
                        nargs=1, type=str, metavar="mod", )

    parser.add_argument("--qtforpython", "-q",
                        help="install Qt for Python.",
                        action="store_true", )

    parser.add_argument("--usd", "-u",
                        help="install pixar usd core modules.",
                        action="store_true", )

    parser.add_argument("--window", "-w",
                        help="show console window",
                        action="store_true", )

    arguments = parser.parse_args(args)

    if arguments.command:
        app, cmd = arguments.command
        try:
            getattr(sys.modules[__name__], app).run(cmd)
        except AttributeError:
            print(
                "%s is not found." % app,
                [m for m in dir(sys.modules[__name__]) if not m.startswith("_") and m != "sys"]
            )

    if arguments.environ:
        from yurlungur.core.app import use
        use(arguments.environ[0])

    # https://code.visualstudio.com/api/advanced-topics/python-extension-template
    # https://www.jetbrains.com/help/pycharm/console-python-console.html
    if arguments.window:
        import code #, codeop
        console = code.InteractiveConsole(locals=locals())
        console.interact()

    if arguments.qtforpython:
        from yurlungur.core.env import set
        set("vfxwindow PySide2")

    if arguments.usd:
        from yurlungur.core.env import set
        set("usd-core")

if __name__ == '__main__':
    _cli(sys.argv[1:])
