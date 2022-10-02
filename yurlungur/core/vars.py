# -*- coding: utf-8 -*-
import sys
import functools
import mmap
import weakref

"""
cb = QtWidgets.QApplication.clipboard()
cb.setText(text)
"""

# shared
# m = mmap.mmap()
d = weakref.WeakValueDictionary()


class __Runtime(object):
    def __getattr__(self, key):
        if key in d:
            return d[key]
        else:
            return None


sys.modules[__name__] = __Runtime()


def ref(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        d[func.__name__] = func
        ret = func(*args, **kwargs)
        return ret

    return wrapper
