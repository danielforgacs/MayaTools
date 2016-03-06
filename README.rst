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

Maya version: Maya 2015 Extension 1 + SP5

todo:
    - prerender scripts
    - test render setups
    - precomp setup
    - second eye

    (- overscan setter)
    (- camera init)
    (- node defaults)
    (- HARDCODED NODES: clear_stabilizer())
    (- turn off camera reset)


install:
----------
1) add to Maya.env (on linux %% = $):

// --> maya tools ------------------
MAYATOOLSPATH=<MAYA TOOLS PATH>

// --> WINDOWS:
XBMLANGPATH=%MAYATOOLSPATH%\MayaTools\icons;%MAYATOOLSPATH%\MayaTools\matchmove_shelf\matchmove_shelf_icons
MAYA_SHELF_PATH=%MAYATOOLSPATH%\MayaTools\shelfs
MAYA_SCRIPT_PATH=%MAYATOOLSPATH%\MayaTools\matchmove_shelf\mel

// --> LINUX:
XBMLANGPATH=$MAYATOOLSPATH/MayaTools/icons/%B:$MAYATOOLSPATH/MayaTools/matchmove_shelf/matchmove_shelf_icons/%B
MAYA_SHELF_PATH=$MAYATOOLSPATH/MayaTools/shelfs
MAYA_SCRIPT_PATH=$MAYATOOLSPATH/MayaTools/matchmove_shelf/mel
// --> maya tools end ------------------

2) prefs script folder: add to userSetup.py:

# ## --> Maya Tools setup -------------------
import os
import maya.cmds as cmds

os.sys.path.append(os.environ['MAYATOOLSPATH'])

import MayaTools

cmds.commandPort(name=':6005')
# ## --> Maya Tools setup end... -------------