#! Python2.7

import __future__
import unittest
import pymel.core
import camstabilizer
reload(camstabilizer)


class MayaTestScene(unittest.TestCase):
    def setUp(self):
        # panel = pymel.core.getPanel(withFocus=True)

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

        # pymel.core.setFocus(panel)


class CamStabilizerUnitTests(MayaTestScene):
    def test_CamStabilizerUnitTests_is_running(self):
        self.assertTrue(True)

    def test_get_camera_returns_camera_from_panel(self):
        pymel.core.setFocus('modelPanel4')
        cam = camstabilizer.get_camera()
        camtest = pymel.core.nt.Transform('test_camera')

        self.assertEqual(cam, camtest)

    def test_get_camera_returns_camera_from_selection(self):
        pymel.core.select('test_camera', add=True)
        pymel.core.setFocus('scriptEditorPanel1')

        cam = camstabilizer.get_camera()
        camtest = pymel.core.nt.Transform('test_camera')

        self.assertEqual(cam, camtest)

    def test_get_camera_errors_wihout_camera(self):
        pymel.core.select(clear=True)

        self.assertRaises(Exception, camstabilizer.get_camera)

    def test_get_aimtransform_returns_transform_object_or_error(self):
        objects = ['test_camera']

        # for obj in objects:
        #     pymel.core.select(obj)
        #     transform = camstabilizer.get_aimtransform()

        #     if transform:
        #         print(type(transform))
        #         has_get_pos = hasattr(transform, 'getPosition')
        #         has_get_trans = hasattr(transform, 'getTransform')
        #         self.assertTrue(has_get_pos or has_get_trans)


def main():
    print('/'*50)
    print('\\'*50)
    print('/'*50)

    loader = unittest.TestLoader()

    suite_units = loader.loadTestsFromTestCase(CamStabilizerUnitTests)

    unittest.TextTestRunner(verbosity=1).run(suite_units)
