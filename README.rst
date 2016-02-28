==================================================
Maya-tools - Python modules for Autodesk Maya
==================================================

modules
---------

camstabilizer (fstab)
constrain locator to vertex
set overscan
matchmove_shelf
RiggingAid

todo:
    - prerender scripts
    - camera init
    - overscan setter
    - node defaults
    - test render setups
    - precomp setup


install:
----------
1) add to Maya.env (on linux %% = $):

// --> maya tools
mayatoolspath=<MAYA TOOLS PATH>

PYTHONPATH=%mayatoolspath%
XBMLANGPATH=%mayatoolspath%\MayaTools\icons;%mayatoolspath%\MayaTools\matchmove_shelf\matchmove_shelf_icons
MAYA_SHELF_PATH=%mayatoolspath%\MayaTools\shelfs
MAYA_SCRIPT_PATH=%mayatoolspath%\MayaTools\matchmove_shelf\mel
// --> maya tools end

2) prefs script folder: add to userSetup.py:

# --> Maya Tools setup
import MayaTools
import maya.cmds as cmds

cmds.commandPort(name=':6005')
# --> Maya Tools setup end...