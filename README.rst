==================================================
Maya-tools - Python modules for Autodesk Maya
==================================================


install:
----------

setup MayaTools:
prefs script folder: add to userSetup.py:
###
import sys

cmds.commandPort(name=':6005')

mayatools_path = 'c:\_store\dev\Maya-tools-env'

if mayatools_path not in sys.path:
    sys.path.append(mayatools_path)


import MayaTools
###


setup matchmove shelf:
MAYA_SHELF_PATH=<PATH>\MayaTools\matchmove_shelf


2a) import MayaTools
    MayaTools.CamStabilizer.camstabilizer.main(task='')

2b) from MayaTools.CamStabilizer import camstabilizer
    camstabilizer.main(task='')


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