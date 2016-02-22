==================================================
Maya-tools - Python modules for Autodesk Maya
==================================================

setup:
1) add project root folder to python access path

2a) import MayaTools
    MayaTools.CamStabilizer.camstabilizer.main(task='')

2b) from MayaTools.CamStabilizer import camstabilizer
    camstabilizer.main(task='')


modules
---------

CamStabilizer
RiggingAid
Utils

todo:
    - prerender scripts

    (- overscan setter)
    (- stabilizer hardcoded nodes clean)


Install:
---------
updated userSetup.py in preferences:

import sys
import maya.cmds as cmds
import pymel.core as pm


cmds.commandPort(name=':6005')

mayatools_path = '<PATH TO CONTAINING FOLDER>'

if mayatools_path not in sys.path:
    sys.path.append(mayatools_path)


import MayaTools