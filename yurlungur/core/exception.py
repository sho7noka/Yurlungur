# -*- coding: utf-8 -*-
"""
TODO: bind logger
yurlungur exceptions
"""
import sys


class YException(RuntimeError):
    pass


class YEnvException(OSError):
    pass


class YKeyException(KeyError):
    pass


# available on latest application interpreter
if sys.version_info.major > 2:
    import contextlib
    except_runtime = contextlib.suppress(YException)
    except_os = contextlib.suppress(YEnvException)
    except_key = contextlib.suppress(YKeyException)
