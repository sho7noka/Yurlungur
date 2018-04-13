# -*- coding: utf-8 -*-
from yurlungur.core.app import application
from yurlungur.tool.math import YVector, YMatrix, YColor
from yurlungur.core.enviroment import Maya

if Maya():
    from yurlungur.core.wrapper import OM


class Builder(object):
    def data(self):
        pass

    def geometry(self):
        pass

    def camera(self):
        pass

    def light(self):
        pass


class Shader(object):
    def texture(self):
        pass

    def material(self):
        pass

    def render(self):
        pass
