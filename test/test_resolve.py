# coding: utf-8
# import sys
#
# sys.path.append("/Users/shosumioka/Yurlungur")
# import yurlungur as yr
#
# reload(yr)
#
# print yr.meta.resolve
#
# sys.exit()


import sys
import contextlib
import pprint

sys.path.append(
    "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")
import DaVinciResolveScript as dvr_script

# root
resolve = dvr_script.scriptapp("Resolve")
if not resolve:
    raise RuntimeError

fusion = resolve.Fusion()
manager = resolve.GetProjectManager()

"""
(root)/Project/MediaPool
              /Timeline/Track/Item
                             /FComp
"""


@contextlib.contextmanager
def DavinchTab(param="fusion"):
    if param in ["media", "edit", "fusion", "color", "fairlight", "deliver"]:
        resolve.OpenPage(param)
    else:
        raise KeyError


class Render:
    def __init__(self, project):
        self.project = project
        self.jobs = self.project.GetRenderJobs()
        self.presets = self.project.GetRenderPresets()
        self.formats = self.project.GetRenderFormats()

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


class File(object):
    """
MediaPool
  GetRootFolder()                                 --> Folder             # Returns the root Folder of Media Pool
  AddSubFolder(folder, name)                      --> Folder             # Adds a new subfolder under specified Folder object with the given name.
  GetCurrentFolder()                              --> Folder             # Returns currently selected Folder.
  SetCurrentFolder(Folder)                        --> Bool               # Sets current folder by given Folder.
Folder
  GetClips()                                      --> [clips...]         # Returns a list of clips (items) within the folder.
  GetName()                                       --> string             # Returns user-defined name of the folder.
  GetSubFolders()                                 --> [folders...]       # Returns a list of subfolders in the folder.

AppendToTimeline(clip1, clip2...)               --> Bool               # Appends specified MediaPoolItem objects in the current timeline. Returns True if successful.
CreateTimelineFromClips(name, clip1, clip2, ...)--> Timeline           # Creates a new timeline with specified name, and appends the specified MediaPoolItem objects.
ImportTimelineFromFile(filePath)                --> Timeline           # Creates timeline based on parameters within given file.

MediaPoolItem
  GetMetadata(metadataType)                       --> [[types],[values]] # Returns a value of metadataType. If parameter is not specified returns all set metadata parameters.
  SetMetadata(metadataType, metadataValue)        --> Bool               # Sets metadata by given type and value. Returns True if successful.
  GetMediaId()                                    --> string             # Returns a unique ID name related to MediaPoolItem.
  AddMarker(frameId, color, name, note, duration) --> Bool               # Creates a new marker at given frameId position and with given marker information.
  GetMarkers()                                    --> [markers...]       # Returns a list of all markers and their information.
  AddFlag(color)                                  --> Bool               # Adds a flag with given color (text).
  GetFlags()                                      --> [colors...]        # Returns a list of flag colors assigned to the item.
  GetClipColor()                                  --> string             # Returns an item color as a string.
  GetClipProperty(propertyName)                   --> [[types],[values]] # Returns property value related to the item based on given propertyName (string). if propertyName is empty then it returns a full list of properties.
  SetClipProperty(propertyName, propertyValue)    --> Bool               # Sets into given propertyName (string) propertyValue (string).


    """

    def importer(self, *args):
        storage = resolve.GetMediaStorage()
        clips = storage.AddItemsToMediaPool(*args)


class Project(object):
    """
    print manager.CreateFolder("LLLL")
    manager.GotoRootFolder(), manager.GotoParentFolder(), manager.OpenFolder("LLLL")
    print manager.GetProjectsInCurrentFolder(), manager.GetFoldersInCurrentFolder()
    """

    def __init__(self, name=""):
        self.manager = resolve.GetProjectManager()
        self.current = self.manager.GetCurrentProject() or self.manager.LoadProject(name)
        self.timelines = self.current.GetTimelineCount()

        if not self.current:
            self.current = self.manager.CreateProject(name)
            self.current.SetName(name)
            self.manager.SaveProject()
        # print project.GetName(), project.GetPresets().values(), project.GetSetting("colorScienceMode"), project.SetSetting("colorScienceMode", "davinciYRGB"), project.GetRenderFormats(), project.GetMediaPool().GetMetadata()

    def name(self):
        return self.current.GetName()

    def attr(self, val):
        return self.current.GetSetting(val)

    def attrs(self):
        return sorted(self.current.GetSetting().keys())

    def timeline(self, val=None):
        """
        tm.GetStartFrame(), tm.GetEndFrame(), tm.GetName(), tm.GetMarkers()
        """
        if type(val) == int:
            return self.current.GetTimelineByIndex(val)

        timeline = self.current.GetCurrentTimeline()
        if not timeline:
            timeline = self.current.GetMediaPool().CreateEmptyTimeline(val)
            timeline.SetName(val)
            self.current.SetCurrentTimeline(timeline)
        return timeline


def fu_script(comp):
    """comp起点とfusion起点の２つ
    https://www.steakunderwater.com/VFXPedia/96.0.243.189/index1bea.html?title=Eyeon:Script/Reference/Applications/Fusion/Classes/Composition
    """
    # print fusion.MapPath("Fusion:\\"), fusion.GetCompList().items()[0], comp
    print comp.GetToolList().values()[0].GetAttrs()
    # print fusion.GetAttrs()
    fpath = fusion.MapPath("/Users/shosumioka/Documents/aaa.comp")
    mcomp = fusion.LoadComp(fpath)
    pprint.pprint(mcomp.GetAttrs()['COMPS_FileName'])
    # mcomp.Save(), mcomp.Print(), mcomp.Close(), mcomp.Lock(), mcomp.Unlock(), mcomp.Paste()
    mcomp.AddTool()
    print mcomp.GetPrefs()
    mcomp.SetPrefs({})
    mcomp.SetAttrs({"COMPS_FileName": "/Users/shosumioka/Documents/bbb.comp"})


if __name__ == "__main__":
    project = Project()
    tm = project.timeline()
    print tm, tm.GetTrackCount("video")  # , "audio", "subtitle")
    comp = tm.GetItemsInTrack("video", 1).values()[0].AddFusionComp()
    fu_script(comp)

"""
Project
  SetPreset(presetName)                           --> Bool               # Sets preset by given presetName (string) into project.
  LoadRenderPreset(presetName)                    --> Bool               # Sets a preset as current preset for rendering if presetName (text) exists.
  SaveAsNewRenderPreset(presetName)               --> Bool               # Creates a new render preset by given name if presetName(text) is unique.
  SetRenderSettings([settings map])               --> Bool               # Sets given settings for rendering. Settings map is a map, keys of map are: "SelectAllFrames", "MarkIn", "MarkOut", "TargetDir", "CustomName".
  GetRenderJobStatus(idx)                         --> [status info]      # Returns job status and completion rendering percentage of the job by given job index (int).

  GetRenderFormats()                              --> [render formats...]# Returns a list of available render formats.
  GetRenderCodecs(renderFormat)                   --> [render codecs...] # Returns a list of available codecs for given render format (string).
  GetCurrentRenderFormatAndCodec()                --> [format, codec]    # Returns currently selected render format and render codec.
  SetCurrentRenderFormatAndCodec(format, codec)   --> Bool               # Sets given render format (string) and render codec (string) as options for rendering.


Timeline
  AddMarker(frameId, color, name, note, duration) --> Bool               # Creates a new marker at given frameId position and with given marker information.
  ApplyGradeFromDRX(path, gradeMode, item1, item2, ...)--> Bool          # Loads a still from given file path (string) and applies grade to Timeline Items with gradeMode (int): 0 - "No keyframes", 1 - "Source Timecode aligned", 2 - "Start Frames aligned".

TimelineItem
  GetName()                                       --> string             # Returns a name of the item.
  GetDuration()                                   --> int                # Returns a duration of item.
  GetEnd()                                        --> int                # Returns a position of end frame.
  GetLeftOffset()                                 --> int                # Returns a maximum extension by frame for clip from left side.
  GetRightOffset()                                --> int                # Returns a maximum extension by frame for clip from right side.
  GetStart()                                      --> int                # Returns a position of first frame.
  GetMarkers()                                    --> [markers...]       # Returns a list of all markers and their information.
  GetFlags()                                      --> [colors...]        # Returns a list of flag colors assigned to the item.
  GetClipColor()                                  --> string             # Returns an item color as a string.
  AddMarker(frameId, color, name, note, duration) --> Bool               # Creates a new marker at given frameId position and with given marker information.
  GetFusionCompNames()                            --> [names...]         # Returns a list of Fusion composition names associated with the timeline item.
  GetFusionCompCount()                            --> int                # Returns the number of Fusion compositions associated with the timeline item.
  GetFusionCompByIndex(compIndex)                 --> fusionComp         # Returns Fusion composition object based on given index. 1 <= compIndex <= timelineItem.GetFusionCompCount()
  GetFusionCompByName(compName)                   --> fusionComp         # Returns Fusion composition object based on given name.
  ImportFusionComp(path)                          --> fusionComp         # Imports Fusion composition from given file path by creating and adding a new composition for the item.
  ExportFusionComp(path, compIndex)               --> fusionComp         # Exports Fusion composition based on given index into provided file name path.
"""
