import unittest
import pymel.core
import camstabilizer
reload(camstabilizer)


class MayaTestScene(unittest.TestCase):
    def setUp(self):
        panel = pymel.core.getPanel(withFocus=True)

        pymel.core.newFile(force=True)
        cube = pymel.core.polyCube()
        camaim = pymel.core.spaceLocator()
        cam, camshape = pymel.core.camera(displayResolution=True,
                displayFilmGate=False, overscan=1.8)



        cam.rename('test_camera')
        camaim.rename('test_locator')
        cube[0].rename('test_box')
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

        pymel.core.select('test_box.vtx[5]')

        pymel.core.setFocus(panel)


class CamStabilizerUnitTests(MayaTestScene):
    def test_CamStabilizerUnitTests_is_running(self):
        self.assertTrue(True)

    def test_get_camera_returns_camera_from_panel_or_selection(self):
        cam = camstabilizer.get_camera()
        camtest = pymel.core.nt.Transform('test_camera')

        # print('\n\n')
        # print(cam)
        # print('\n\n')
        # print(camtest)
        # print('\n\n')

        self.assertEqual(cam, camtest)


def main():
    print('/'*50)
    print('\\'*50)
    print('/'*50)

    loader = unittest.TestLoader()

    suite_units = loader.loadTestsFromTestCase(CamStabilizerUnitTests)

    unittest.TextTestRunner(verbosity=1).run(suite_units)
