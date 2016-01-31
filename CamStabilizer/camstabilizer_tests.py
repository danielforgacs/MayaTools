#! Python2.7

import unittest
import camstabilizer
reload(camstabilizer)

try:
    import pymel.core
except ImportError:
    pymel = None



class MayaTestScene(unittest.TestCase):
    def setUp(self):
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

        pymel.core.select(clear=True)
        pymel.core.setFocus('outlinerPanel1')

    def tearDown(self):
        pymel.core.select(clear=True)
        pymel.core.setFocus('outlinerPanel1')



class CamStabilizerUnitTests(MayaTestScene):
    # @unittest.skip('already works')
    def test_CamStabilizerUnitTests_is_running(self):
        self.assertTrue(True)

    # @unittest.skip('already works')
    def test_get_selection_errors_on_empty_selection(self):
        pymel.core.select(clear=True)
        self.assertRaises(Exception, camstabilizer.get_selection)

    # @unittest.skip('already works')
    def test_get_selection_errors_on_long_or_no_selection(self):
        pymel.core.select(clear=True)
        self.assertRaises(Exception, camstabilizer.get_selection)

        pymel.core.select(clear=True)
        pymel.core.select('test_box.vtx[1:5]')
        self.assertRaises(Exception, camstabilizer.get_selection)

        pymel.core.select(clear=True)
        pymel.core.select(('test_box', 'test_camera', 'test_locator'))
        self.assertRaises(Exception, camstabilizer.get_selection)

    # @unittest.skip('already works')
    def test_get_selection_returns_selection(self):
        pymel.core.select(clear=True)
        selection = (
            ['test_box',],
            ['test_box', 'test_locator'],
            ['test_box', 'test_camera'],
            ['test_box', 'test_box.vtx[1:3]'],
            )

        for case in selection:
            pymel.core.select(case)
            self.assertEqual(pymel.core.selected(), camstabilizer.get_selection())

    # @unittest.skip('already works')
    def test_get_camera_returns_camera_from_panel(self):
        pymel.core.select(clear=True)
        pymel.core.select('test_box.vtx[1]')
        pymel.core.setFocus('modelPanel4')
        cam = camstabilizer.get_camera()
        camtest = pymel.core.nt.Transform('test_camera')

        self.assertEqual(cam, camtest)

    # @unittest.skip('already works')
    def test_get_camera_returns_camera_from_selection(self):
        pymel.core.select('test_box.vtx[1]')
        pymel.core.select('test_camera', add=True)
        pymel.core.setFocus('scriptEditorPanel1')

        cam = camstabilizer.get_camera()
        camtest = pymel.core.nt.Transform('test_camera')

        self.assertEqual(cam, camtest)

    # @unittest.skip('already works')
    def test_get_camera_errors_wihout_camera(self):
        pymel.core.select(clear=True)

        self.assertRaises(Exception, camstabilizer.get_camera)

    # @unittest.skip('not implemented')
    def test_get_position_object_retruns_queryable_position_object(self):
        nodetypes = (
                    pymel.core.nodetypes.Transform,
                    pymel.core.general.MeshVertex,
                    pymel.core.general.MeshEdge,
                    pymel.core.general.MeshFace,
                )

        selection_sets = (
                ('test_camera',),
                ('test_locator',),
                ('test_camera','test_box'),
                ('test_box', 'test_camera',),
            )

        for selection in selection_sets:
            pymel.core.select(clear=True)
            pymel.core.select(selection)
            obj = camstabilizer.get_position_object()

            self.assertIn(type(obj), nodetypes)

    def test_get_position_object_errors_without_queryable_position(self):
        pass


def main():
    print('/'*50)
    print('\\'*50)
    print('/'*50)

    unittest.main(module='CamStabilizer.camstabilizer_tests', exit=False)
