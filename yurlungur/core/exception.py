# -*- coding: utf-8 -*-
"""
TODO: bind logger
yurlungur exceptions
"""
import contextlib
with contextlib.suppress(ImportError):
    import sys
    print(sys.executable)


class YException(RuntimeError):
    """
    runtime error
    >>> raise YException(application)
    """
    pass


class YEnvException(OSError):
    """
    env error
    >>> raise YEnvException(application)
    """
    pass


class YKeyException(KeyError):
    """
    key error
    >>> raise YKeyException(application)
    """
    pass
