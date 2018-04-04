import sys

sys.dont_write_bytecode = True

if __name__ == "__main__":
    from yurlungur.core.standalone import _cli
    _cli(sys.argv[1:])
