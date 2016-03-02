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

WINDOWS:
// --> maya tools
mayatoolspath=<MAYA TOOLS PATH>

PYTHONPATH=%mayatoolspath%
XBMLANGPATH=%mayatoolspath%\MayaTools\icons;%mayatoolspath%\MayaTools\matchmove_shelf\matchmove_shelf_icons
MAYA_SHELF_PATH=%mayatoolspath%\MayaTools\shelfs
MAYA_SCRIPT_PATH=%mayatoolspath%\MayaTools\matchmove_shelf\mel
// --> maya tools end

LINUX:
// --> maya tools
MAYATOOLSPATH=/home/DForgacs/dev

// PYTHONPATH=$MAYATOOLSPATH/MayaTools
XBMLANGPATH=$MAYATOOLSPATH/MayaTools/icons/%B:$MAYATOOLSPATH/MayaTools/matchmove_shelf/matchmove_shelf_icons/%B
MAYA_SHELF_PATH=$MAYATOOLSPATH/MayaTools/shelfs
MAYA_SCRIPT_PATH=$MAYATOOLSPATH/MayaTools/matchmove_shelf/mel
// --> maya tools end

2) prefs script folder: add to userSetup.py:

WINDOWS:
# --> Maya Tools setup
import MayaTools
import maya.cmds as cmds

cmds.commandPort(name=':6005')
# --> Maya Tools setup end...

LINUX:
# --> Maya Tools setup
import sys

mayatools_path = '/home/DForgacs/dev/'

if mayatools_path not in sys.path:
	sys.path.append(mayatools_path)

import MayaTools
import maya.cmds as cmds

cmds.commandPort(name=':6005')
# --> Maya Tools setup end...