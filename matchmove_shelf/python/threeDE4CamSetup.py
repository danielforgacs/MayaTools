import os, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import maya.cmds as cmds

def cameraAttr():
    if len(cmds.ls(sl=True)) != 1:
        QMessageBox.warning(None, 'Warning Message', "Please select one camera", QMessageBox.Ok, QMessageBox.Ok)
        sys.exit()

    camShape = cmds.listRelatives(cmds.ls(sl=True), s=True)


    if not cmds.attributeQuery("tde4_lens_model", node = camShape[0], exists = True):
        cmds.addAttr(camShape[0], longName='tde4_lens_model', dt='string')
        cmds.addAttr(camShape[0], longName='tde4_focal_length_cm', at='double')
        cmds.addAttr(camShape[0], longName='tde4_filmback_width_cm', at='double')
        cmds.addAttr(camShape[0], longName='tde4_filmback_height_cm', at='double')
        cmds.addAttr(camShape[0], longName='tde4_lens_center_offset_x_cm', at='double')
        cmds.addAttr(camShape[0], longName='tde4_lens_center_offset_y_cm', at='double')
        cmds.addAttr(camShape[0], longName='tde4_pixel_aspect', at='double')
        cmds.addAttr(camShape[0], longName='Distortion', at='double')
        cmds.addAttr(camShape[0], longName='Anamorphic_Squeeze', at='double')
        cmds.addAttr(camShape[0], longName='Curvature_X', at='double')
        cmds.addAttr(camShape[0], longName='Curvature_Y', at='double')
        cmds.addAttr(camShape[0], longName='Quartic_Distortion', at='double')
        cmds.addAttr(camShape[0], longName='Distortion_BBox_Scale', at='double')


    cmds.createNode('multiplyDivide', n = camShape[0] + '_focal_length_mdn')
    cmds.connectAttr(camShape[0] + ".focalLength", camShape[0] + '_focal_length_mdn' + ".input1X")
    cmds.setAttr(camShape[0] + '_focal_length_mdn' + ".input2X", 0.10)
    cmds.connectAttr(camShape[0] + '_focal_length_mdn' + ".outputX", camShape[0] + ".tde4_focal_length_cm")

    cmds.createNode('multiplyDivide', n = camShape[0] + '_filmback_width_mdn')
    cmds.connectAttr(camShape[0] + ".horizontalFilmAperture", camShape[0] + '_filmback_width_mdn' + ".input1X")
    cmds.setAttr(camShape[0] + '_filmback_width_mdn' + ".input2X", 2.54)
    cmds.connectAttr(camShape[0] + '_filmback_width_mdn' + ".outputX", camShape[0] + ".tde4_filmback_width_cm")

    cmds.createNode('multiplyDivide', n = camShape[0] + '_filmback_height_mdn')
    cmds.connectAttr(camShape[0] + ".verticalFilmAperture", camShape[0] + '_filmback_height_mdn' + ".input1X")
    cmds.setAttr(camShape[0] + '_filmback_height_mdn' + ".input2X", 2.54)
    cmds.connectAttr(camShape[0] + '_filmback_height_mdn' + ".outputX", camShape[0] + ".tde4_filmback_height_cm")

    cmds.setAttr(camShape[0] + '.tde4_pixel_aspect', 1)
    cmds.setAttr(camShape[0] + '.Anamorphic_Squeeze', 1)
    cmds.setAttr(camShape[0] + '.tde4_lens_model', "tde4_ldp_classic_3de_mixed", type='string')     

    cmds.setAttr(camShape[0] + '.Distortion_BBox_Scale', 0)
