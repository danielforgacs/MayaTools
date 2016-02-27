==================================================
Maya-tools - Python modules for Autodesk Maya
==================================================

modules
---------

CamStabilizer
RiggingAid
Utils
matchmove_shelf

todo:
    - prerender scripts
    - camera init
    - overscan setter

    (- stabilizer hardcoded nodes clean)

install:
----------
1) add to Maya.env (on linux %% = $):

// --> maya tools
mayatoolspath=c:\_store\dev\Maya-tools-env

PYTHONPATH=%mayatoolspath%
MAYA_SHELF_PATH=%mayatoolspath%\MayaTools\shelfs
MAYA_SCRIPT_PATH=%mayatoolspath%\MayaTools\matchmove_shelf\mel
// --> maya tools end

2) prefs script folder: add to userSetup.py:

# --> Maya Tools setup
import MayaTools
import maya.cmds as cmds

cmds.commandPort(name=':6005')
# --> Maya Tools setup end...

3) copy matchmove_shelf_icons folder
in prefs/icons

4) set cone.ma locations in createCones.mel line 61