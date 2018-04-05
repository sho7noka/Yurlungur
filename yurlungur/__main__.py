import sys

sys.dont_write_bytecode = True

if __name__ == "__main__":
    from yurlungur.core.standalone import cli
    cli(sys.argv[1:])
