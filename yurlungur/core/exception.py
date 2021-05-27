# -*- coding: utf-8 -*-
"""
TODO: bind logger
yurlungur exceptions
"""
class YException(RuntimeError):
    pass


class YEnvException(OSError):
    pass


class YKeyException(KeyError):
    pass


# available on latest application interpreter
import sys

if sys.version_info.major >= 3:
    import contextlib

    except_runtime = contextlib.suppress(YException)
    except_os = contextlib.suppress(YEnvException)
    except_key = contextlib.suppress(YKeyException)

    del contextlib
del sys
