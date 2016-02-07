import unittest
from fractions import Fraction
import setoverscan

try:
    reload(setoverscan)
except:
    import importlib
    importlib.reload(setoverscan)


try:
    import pymel.core
except:
    pymel = None


class SetOverscanFuncTests(unittest.TestCase):
    def setUp(self):
        """start empty maya scene with camera:"""

        pymel.core.newFile(force=True)
        camtransform, self.cam = pymel.core.camera()
        pymel.core.select(camtransform)

    def test__setoverscan(self):
        """
        test with resolutions:
        1000 x 500
        overscan is 100 pixels horizontally
        overscan resolution:
        1200 x 600
        """
        res_x = 1000
        res_y = 500
        osc_left = 50
        res_x_new = 1200
        res_y_new = 600
        image_ratio = Fraction(res_x, res_y)
        post_scale = Fraction(res_x, res_x_new)

        # print('image_ratio: ', float(image_ratio))
        # print('overscan left / right: ', osc_left*2)
        # print('res_x: ', res_x)
        # print('res_x_new: ', res_x_new)
        # print('res_y: ', res_y)
        # print('res_y_new: ', res_y_new)

        """set final render resoolution without overscan:"""
        rendersettings = pymel.core.PyNode('defaultResolution')
        rendersettings.setAttr('width', res_x)
        rendersettings.setAttr('height', res_y)

        """check if main() runs without error:"""
        self.assertIsNone(setoverscan.main(pixels=osc_left))

        """test if new global render resolution is working"""
        self.assertEqual(rendersettings.getAttr('width'), res_x_new)
        self.assertEqual(rendersettings.getAttr('height'), res_y_new)

        """check camera post scale"""
        self.assertAlmostEqual(self.cam.getAttr('postScale'), float(post_scale), 9)

        """test for error if camera has post scale
        value already set to other than 1.0"""



def main():
    unittest.main(module=__name__, exit=False)


if __name__ == '__main__' and pymel:
    unittest.main(module=__name__, exit=False)
