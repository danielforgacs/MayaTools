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

		self.transform = node
		self.shape = node

		if isinstance(self.shape, pm.nodetypes.Transform):
			self.shape = self.shape.getShape()

	@property
	def imageplane(self):
		return self.shape.attr('imagePlane').get()[0]


def main_v1():
    imgplane = pm.selected()[0]
    seq = imgplane.imageName.get()
    # seq = '/jobs/fsb/shots/jtj/jtj_0250/work/camera/task01/3De/exports/fsb_jtj_0250_delensed_plate_v001/djv_view fsb_jtj_0250_delensed_plate_v001.1001.jpg'
    # seq = 'djv_view /jobs/fsb/shots/jtj/jtj_0250/work/camera/task01/3De/exports/fsb_jtj_0250_delensed_plate_v004/fsb_jtj_0250_delensed_plate_v004.1001.jpg'
    # seq = '/jobs/fsb/shots/jtj/jtj_0250/work/camera/task01/3De/exports/fsb_jtj_0250_delensed_plate_v004/fsb_jtj_0250_delensed_plate_v004.1001.jpg'
    # subprocess.Popen('djv_view')
    subprocess.Popen(['djv_view', seq])


def main():
	print '~@~'*10
	selection = pm.ls(selection=True)[0]
	cam = Cam(selection)

	print(cam.transform)
	print(cam.shape)
	print(cam.imageplane)
	print(cam.imageplane.attr('imageName').get())


if __name__ == '__main__':
    main()