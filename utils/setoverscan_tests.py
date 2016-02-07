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
    def test__setoverscan(self):
        res_x = 1000
        res_y = 500
        osc_left = 50
        res_x_new = 1200
        res_y_new = 600
        image_ratio = Fraction(res_x, res_y)
        # res_x_new = res_x+(osc_left*2)
        # res_y_new = float(res_x_new / image_ratio)

        print('image_ratio: ', float(image_ratio))
        print('overscan left / right: ', osc_left*2)
        print('res_x: ', res_x)
        print('res_x_new: ', res_x_new)
        print('res_y: ', res_y)
        print('res_y_new: ', res_y_new)

        pymel.core.newFile(force=True)

        rendersettings = pymel.core.PyNode('defaultResolution')
        rendersettings.setAttr('width', res_x)
        rendersettings.setAttr('height', res_y)

        self.assertIsNone(setoverscan.main(pixels=osc_left))
        self.assertEqual(rendersettings.getAttr('width'), res_x_new)
        self.assertEqual(rendersettings.getAttr('height'), res_y_new)



def main():
    unittest.main(module=__name__, exit=False)


if __name__ == '__main__' and pymel:
    unittest.main(module=__name__, exit=False)
