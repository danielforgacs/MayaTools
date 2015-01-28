#! python2


__version__     = '0.1'
__author__      = 'github/danielforgacs'


"""/
maya camera overscan setup

todo:
- imageplane name is hardcoded
"""


import  maya.cmds   as cmds
# import  pymel.core  as pm


OVERSCAN    = 1.2


class Scene():
    def __init__(self):
        self.res_x    = cmds.getAttr('defaultResolution.width')
        self.res_y    = cmds.getAttr('defaultResolution.height')

    def set_overscan(self):
        cmds.setAttr('defaultResolution.width', self.res_x * OVERSCAN)
        cmds.setAttr('defaultResolution.height', self.res_y * OVERSCAN)

        old_x              = self.res_x
        self.__init__()
        self.underscan      = float(old_x) / float(self.res_x)


class Camera():
    def __init__(self, name = 'camera1'):
        self.name = cmds.ls(selection =True)[0]
        cmds.setAttr(self.name + '.displayFilmGate', 0)
        cmds.setAttr(self.name + '.displayResolution', 1)
        cmds.setAttr(self.name + '.overscan', 1.35)

    def set_overscan(self, postScale):
        cmds.setAttr(self.name + '.postScale', postScale)
        cmds.setAttr('imagePlane1.sizeX', postScale)


def main():
    scene       = Scene()
    scene.set_overscan()

    cam         = Camera()
    cam.set_overscan(scene.underscan)