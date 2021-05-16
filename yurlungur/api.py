# -*- coding: utf-8 -*-
u"""
名前空間にモジュールを展開する

短く書く際の各モジュールのimportに使用している
console起動時に標準で読み込まれる他に、読み込まれることはない

.. code-block:: python

    from yurlungur.api import *

これによって以下が行われる。

.. code-block:: python

    import yurlungur
    from yurlungur.core.proxy import Node, File
    from yurlungur.core.command import node, file
    # from yurlungur.core.datatype import Vector
    from yurlungur.core.deco import UndoGroup, threads
    from yurlungur.tool.logger import pprint
    from yurlungur.tool.meta import meta
    from yurlungur.tool.standalone import * # noQA
    from yurlungur.tool.patch import *      # noQA
"""
import sys

sys.dont_write_bytecode = True

import yurlungur
from yurlungur.core.proxy import Node, File, Attribute
from yurlungur.core.command import node, file, attr
from yurlungur.core import runtime
# from yurlungur.core.datatype import Vector
from yurlungur.core.deco import UndoGroup, threads
from yurlungur.tool.meta import meta
from yurlungur.tool.logger import pprint
from yurlungur.tool.standalone import *  # noQA
from yurlungur.tool.patch import *  # noQA

# pprint("initialize interpreter on {0}".format(sys.executable))
del sys
