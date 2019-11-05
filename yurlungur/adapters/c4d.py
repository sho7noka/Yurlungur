# coding: utf-8
try:
    import c4d
except ImportError:
    from yurlungur.core.env import App as _

    run, shell, end = _("c4d")._actions


class Project(object):
    def __init__(self, project):
        self.project = project

    def __repr__(self):
        return self.project.name()

    @property
    def sequences(self):
        return Timeline(self.project)


class Timeline(object):
    def __init__(self, timeline):
        self.timeline = timeline

    @property
    def tracks(self):
        return Track(self.timeline)


class Track(object):
    def __init__(self, track):
        self.track = track

    @property
    def clips(self):
        return Item(self.track)


class Item(object):
    pass
