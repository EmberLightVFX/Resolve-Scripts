#!/usr/bin/env python

"""
Example DaVinci Resolve script:
Adds subclips [frame 0 .. 23] to current timeline for all media pool root folder clips
Example usage: 7_add_subclips_to_timeline.py
"""

#!/usr/bin/env python

"""
This file serves to return a DaVinci Resolve object
"""

import sys
import os

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
    print(resolve)
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    mediaPool = project.GetMediaPool()
    selectedFolder = mediaPool.GetCurrentFolder()
    print("Replacing files in folder " + selectedFolder.GetName())
    clips = selectedFolder.GetClipList()

    sourceFolder = os.path.abspath("\\\\cpnas2\\UFOSweden\\")
    localSourceFolder = os.path.abspath("G:\\UFOSweden\\")
    sourceExtension = "CRM"

    for clip in clips:
        if clip.GetClipProperty()["Video Codec"] != "" and not sourceFolder in clip.GetClipProperty()["File Path"]:
            if not localSourceFolder in clip.GetClipProperty()["File Path"]:
                print(clip.GetClipProperty()["File Path"] + " is not under local source folder")
            else:
                fileName = os.path.splitext(clip.GetClipProperty()["File Name"])[0] + "." + sourceExtension

                oldPath = os.path.split(clip.GetClipProperty()["File Path"])[0]
                newPath = oldPath.replace("PROXY", "SOURCE")

                for root, dirs, files in os.walk(newPath):
                    for fname in files:
                        if fname == fileName:
                            nasRoot = root.replace(localSourceFolder, sourceFolder)

                            if os.path.isfile(os.path.join(nasRoot, fileName)):
                                clip.ReplaceClip(os.path.join(nasRoot, fileName))
                                print(fileName + " is replaced")
                            else:
                                print(fileName + " is not readable for Resolve. Non-ascii characters in path?")
                            break

print("Done")