#!/usr/bin/env python

"""
Adds the last frame of all clips inside the selected folder to the current timeline
"""

import sys

def GetResolve():
    try:
    # The PYTHONPATH needs to be set correctly for this import statement to work.
    # An alternative is to import the DaVinciResolveScript by specifying absolute path (see ExceptionHandler logic)
        import DaVinciResolveScript as bmd
    except ImportError:
        if sys.platform.startswith("darwin"):
            expectedPath="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
        elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
            import os
            expectedPath=os.getenv('PROGRAMDATA') + "\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules\\"
        elif sys.platform.startswith("linux"):
            expectedPath="/opt/resolve/libs/Fusion/Modules/"

        # check if the default path has it...
        print("Unable to find module DaVinciResolveScript from $PYTHONPATH - trying default locations")
        try:
            import imp
            bmd = imp.load_source('DaVinciResolveScript', expectedPath+"DaVinciResolveScript.py")
        except ImportError:
            # No fallbacks ... report error:
            print("Unable to find module DaVinciResolveScript - please ensure that the module DaVinciResolveScript is discoverable by python")
            print("For a default DaVinci Resolve installation, the module is expected to be located in: "+expectedPath)
            sys.exit()

    return bmd.scriptapp("Resolve")

if __name__ == "__main__":
    resolve = GetResolve()
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    mediaPool = project.GetMediaPool()
    selectedFolder = mediaPool.GetCurrentFolder()
    clips = selectedFolder.GetClipList()

    for clip in clips:
        if clip.GetClipProperty()["Video Codec"] != "":
            clipEnd = clip.GetClipProperty()["End"]
            subClip = {
                "mediaPoolItem": clip,
                "startFrame": int(clipEnd)-1,
                "endFrame": int(clipEnd)-1,
            }

            if mediaPool.AppendToTimeline([ subClip ]):
                print("added frame " + str(int(clipEnd)-1) + " of \"" + clip.GetName() + "\" to current timeline.")

