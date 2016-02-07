import unittest
import fractions
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
        old_res_x = 1920
        old_res_y = 1080
        osc_left = 10

        pymel.core.newFile(force=True)

        rendersettings = pymel.core.PyNode('defaultResolution')
        rendersettings.setAttr('width', old_res_x)
        rendersettings.setAttr('height', old_res_y)

        imageaspect = fractions.Fraction(old_res_x, old_res_y)

        self.assertIsNone(setoverscan.main())
        self.assertEqual(rendersettings.getAttr('width'), 1920)
        self.assertEqual(rendersettings.getAttr('height'), 1080)



def main():
    unittest.main(module=__name__, exit=False)


if __name__ == '__main__':
    unittest.main(module=__name__, exit=False)
