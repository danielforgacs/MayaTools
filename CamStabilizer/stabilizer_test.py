"""
!!! test currently don't test second eye functions !!!
"""

import unittest
import time
import pymel.core
# import pymel.core.uitypes
import stabilizer
reload(stabilizer)


class TestSceneSetup(unittest.TestCase):
    def setUp(self):
        window = pymel.core.uitypes.Window('Stabilizer')

        try:
            window.delete()
        except:
            pass

        pymel.core.newFile(force=True)

        pymel.core.polyCube()

        camaim = pymel.core.spaceLocator()
        cam, camshape = pymel.core.camera(displayResolution=True,
            displayFilmGate=False, overscan=1.8)

        cam.setAttr('translateZ', 5)
        cam.setParent(camaim)

        pymel.core.setKeyframe(camaim)
        pymel.core.currentTime(120, edit=True)

        camaim.setAttr('rotateY', 60)
        camaim.setAttr('rotateX', -45)
        camaim.setAttr('translateY', 5)
        camaim.setAttr('translateZ', 3)

        pymel.core.setKeyframe(camaim)
        pymel.core.lookThru('perspView', camshape)

        pymel.core.select('pCube1.vtx[5]')

    def tearDown(self):
        pass


class StabizilerGUITests(TestSceneSetup):
    def test_unittests_running(self):
        self.assertTrue(True)

    def test_gui_creates_stabilizer_window(self):
        stabilizer.gui()
        self.assertTrue(pymel.core.window('Stabilizer', query=True, exists=True))

    def test_window_has_stabilize_button(self):
        stabilizer.gui()
        self.assertTrue(pymel.core.uitypes.Button('button_stabilizer'))

    def test_stabilizer_button_command_is_stabilize(self):
        stabilizer.gui()
        button = pymel.core.uitypes.Button('button_stabilizer')

        self.assertEqual(button.getCommand(), 'fstab.stabilizer("start")')

    def test_stabilizer_button_color_is_green_turned_off(self):
        stabilizer.gui()
        button = pymel.core.uitypes.Button('button_stabilizer')

        for k, value in enumerate([0, 0.5, 0]):
            self.assertAlmostEqual(button.getBackgroundColor()[k], value, 4)


def main():
    print('/'*50)
    print('\\'*50)
    print('/'*50)

    loader = unittest.TestLoader()
    suite_GUI = loader.loadTestsFromTestCase(StabizilerGUITests)

    unittest.TextTestRunner(verbosity=1).run(suite_GUI)


if __name__ == '__main__':
    unittest.main(verbosity=1)
