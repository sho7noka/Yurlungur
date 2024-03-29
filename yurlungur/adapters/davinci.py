# coding: utf-8
import os
from yurlungur.core.env import App as __App

# bmd = fusionscript, fu, comp
# https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=108048
# https://www.steakunderwater.com/wesuckless/viewtopic.php?t=2012

run, shell, quit, _ = __App("davinci")._actions
"""
comp.Execute("print('Hello from Lua!')")
comp.Execute("!Py: print('Hello from default Python!')") 
comp.Execute("!Py2: print 'Hello from Python 2!'")
comp.Execute("!Py3: print ('Hello from Python 3!')")
"""

class Projects(object):
    def __init__(self):
        from yurlungur.tool.meta import meta
        self.manager = meta.resolve.GetProjectManager()
        self.project = self.manager.GetCurrentProject()
        self.projects = self.manager.GetProjectListInCurrentFolder()
        self.v16 = meta.resolve.GetVersion()[0] > 16
        self.v17 = meta.resolve.GetVersion()[0] > 17

    def __repr__(self):
        return self.project.GetName()

    def __getitem__(self, val):
        if val in self.projects:
            self.project = self.manager.LoadProject(val)
        else:
            self.project = self.manager.CreateProject(val)

        return self

    @property
    def current(self):
        return self.project

    @property
    def sequences(self):
        return Timeline(self.project)

    @property
    def render(self):
        return Render(self.project)


class Timeline(object):
    def __init__(self, project):
        self.project = project
        self.timeline = project.GetCurrentTimeline()
        self.media = project.GetMediaPool()
        self.clips = self.media.GetRootFolder().GetClips().values()

    def __repr__(self):
        return self.timeline.GetName() + self.timeline.GetCurrentTimecode()

    def __getitem__(self, val):
        assert isinstance(val, (str, int))

        if type(val) == int:
            if 0 < val < self.project.GetTimelineCount():
                self.timeline = self.project.GetTimelineByIndex(val)

        elif type(val) == str:
            if os.path.exists(val):
                self.timeline = self.media.ImportTimelineFromFile(val)
            elif val in [v.GetName() for v in self.clips]:
                self.project.SetCurrentTimeline(val)
                self.timeline = self.project.GetCurrentTimeline()
            else:
                self.timeline = self.media.CreateEmptyTimeline(val)

        return self

    @property
    def current(self):
        return self.timeline

    def imports(self, *args):
        self.media.AppendToTimeline(*args)
        self.timeline = self.project.GetCurrentTimeline()
        return self

    @property
    def tracks(self):
        return Track(self.timeline)


class Track(object):
    def __init__(self, timeline):
        self.timeline = timeline
        self.track = timeline.GetCurrentVideoItem()

    def __repr__(self):
        return self.track.GetName()

    def __getitem__(self, val):
        assert isinstance(val, int)

        if 0 < val < self.timeline.GetTrackCount("video"):
            self.track = self.timeline.GetItemsInTrack("video", val)
        return self

    @property
    def current(self):
        return self.timeline.GetCurrentVideoItem()

    @property
    def clips(self):
        return Comp(self.track)


class Comp(object):
    def __init__(self, track):
        self.track = track

    def __repr__(self):
        return self.track.GetName() + self.track.GetDuration()

    def __getitem__(self, val):
        assert isinstance(val, (str, int))

        if type(val) == int:
            if 0 < val < self.track.GetFusionCompCount():
                self.track = self.track.GetFusionCompByIndex(val)

        elif type(val) == str:
            if Projects().v16:
                for comp in self.track.GetFusionCompNameList():
                    if val in comp:
                        self.track = self.track.GetFusionCompByName(val)
            else:
                for v in self.track.GetFusionCompNames().values():
                    if val in v.GetName():
                        self.track = self.track.GetFusionCompByName(val)

            if os.path.exists(val):
                self.track = self.track.ImportFusionComp(val)
                self.track = self.track.LoadFusionCompByName(val)
            else:
                self.track = self.track.AddFusionComp()
                self.track.RenameFusionCompByName(self.track.GetName(), val)

        return self

    def exports(self, path):
        return self.track.ExportFusionComp(path, 1)

    def delete(self, name):
        return self.track.DeleteFusionCompByName(name)


class Render(object):
    def __init__(self, project):
        self.project = project
        self.jobs = project.GetRenderJobs()
        self.presets = project.GetRenderPresets()
        self.formats = project.GetRenderFormats()
        # GetCurrentRenderFormatAndCodec

    def add(self):
        self.project.AddRenderJob()

    def start(self, *args):
        """args 無しも可能"""
        self.project.StartRendering(*args)

    def stop(self):
        if self.project.IsRenderingInProgress():
            self.project.StopRendering()

    def delete(self, *args):
        if len(args) == 0:
            self.project.DeleteAllRenderJobs()
        else:
            self.project.DeleteRenderJobIndex(args[0])

    def __enter__(self, *args):
        self.start()

    def __exit__(self, *args):
        self.stop()
