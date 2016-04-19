"""
previews footage from the selected
imagePlane in djv_view

# c:\software\djv-1.1.0-Windows-64\bin\djv_view.exe d:\_store\footage\vfx_72_001_010.0001.png
"""


import subprocess

try:
    import pymel.core as pm
except:
    pm = None


class Cam(object):
    def __init__(self, camtransform):
        node = pm.PyNode(camtransform)
        self.transform = None
        self.shape = None

        if isinstance(node, pm.nodetypes.Transform):
            self.transform = node
            self.shape = node.getShape()
        elif isinstance(node, pm.nodetypes.Camera):
            self.transform = node.getTransform()
            self.shape = node


    @property
    def imageplane(self):
        path = self.shape.attr('imagePlane').get()

        try: 
            return path[0]
        except:
            return None


def main_v1():
    imgplane = pm.selected()[0]
    seq = imgplane.imageName.get()
    # seq = '/jobs/fsb/shots/jtj/jtj_0250/work/camera/task01/3De/exports/fsb_jtj_0250_delensed_plate_v001/djv_view fsb_jtj_0250_delensed_plate_v001.1001.jpg'
    # seq = 'djv_view /jobs/fsb/shots/jtj/jtj_0250/work/camera/task01/3De/exports/fsb_jtj_0250_delensed_plate_v004/fsb_jtj_0250_delensed_plate_v004.1001.jpg'
    # seq = '/jobs/fsb/shots/jtj/jtj_0250/work/camera/task01/3De/exports/fsb_jtj_0250_delensed_plate_v004/fsb_jtj_0250_delensed_plate_v004.1001.jpg'
    # subprocess.Popen('djv_view')
    subprocess.Popen(['djv_view', seq])


def main(viewer=None):
    print '~@~'*10

    if not viewer:
        viewer = 'C:/software/djv-1.1.0-Windows-64/bin/djv_view.exe'

    cam = None

    try:
        selection = pm.ls(selection=True)[0]
    except:
        print('--> select a camera')
        return

    cam = Cam(selection)

    if not cam.shape:
        return  

    # print(cam.transform)
    # print(cam.shape)
    # print(cam.imageplane)

    if not cam.imageplane:
        return

    planepath = cam.imageplane.attr('imageName').get()
    # print(planepath)

    cmd = ' '.join([viewer, planepath])
    # print(cmd)
    
    subprocess.call(cmd)



if __name__ == '__main__':
    main()