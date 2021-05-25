# -*- coding: utf-8 -*-
def main():
    """
    yurlungur cli entry point
    """
    import sys, os, inspect
    from yurlungur.tool.standalone import _cli

    sys.dont_write_bytecode = True
    local = os.path.dirname(os.path.dirname(inspect.currentframe().f_code.co_filename))
    if not local in sys.path:
        sys.path.append(local)
    _cli(sys.argv[1:])

    del sys, os, inspect, _cli


if __name__ == "__main__":
    main()
