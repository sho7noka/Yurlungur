# -*- coding: utf-8 -*-
import fnmatch
from yurlungur.core.proxy import YNode
from yurlungur.tool.meta import meta


class _NodeType(object):
    def __getattr__(self, item):
        if hasattr(meta, "types"):
            nodes = fnmatch.filter(dir(meta.types), str(item))
        else:
            nodes = self.findNodes(item)

        for node in nodes:
            setattr(self, str(item), YNode(node))

        return YNode(item)

    def findNodes(self, pattern):
        if hasattr(meta, "listNodeTypes"):
            # http://help.autodesk.com/cloudhelp/2016/JPN/Maya-Tech-Docs/CommandsPython/shadingNode.html
            categories = [
                "geometry", "camera", "light", "utility",
                "color", "shader", "texture", "rendering", "postprocess"
            ]
            # meta.allNodeTypes(ia=1)
            for category in categories:
                yield fnmatch.filter(meta.listNodeTypes(category), pattern)

        if hasattr(meta, "nodeTypes"):
            for category in meta.nodeTypeCategories().keys():
                yield fnmatch.filter(
                    meta.nodeTypeCategories()[category].nodeTypes().keys(),
                    pattern
                )


YType = _NodeType()
