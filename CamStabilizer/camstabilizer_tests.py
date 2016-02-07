#! Python2.7

import unittest
from . import camstabilizer
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
        curve = pymel.core.curve(p=[(-1.5, 0, 2),
                                (-0.8, 0.5, 0.6),
                                (0.1, 0, -0.8),
                                (1, 0, -2.2)])
        cam, camshape = pymel.core.camera(displayResolution=True,
                displayFilmGate=False, overscan=1.8)



        cam.rename('test_camera')
        curve.rename('test_curve')
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

        grp = pymel.core.group('test_curve', 'test_box')
        pymel.core.duplicate(grp)

        pymel.core.select(clear=True)
        pymel.core.setFocus('outlinerPanel1')

    def tearDown(self):
        pymel.core.select(clear=True)
        pymel.core.setFocus('outlinerPanel1')
        # pymel.core.newFile(force=True)



class CamStabilizerUnitTests(MayaTestScene):
    # @unittest.skip('already works')
    def test__CamStabilizerUnitTests__is_running(self):
        self.assertTrue(True)

    # @unittest.skip('already works')
    def test__get_selection__errors_on_empty_selection(self):
        pymel.core.select(clear=True)
        self.assertRaises(Exception, camstabilizer.get_selection)

    # @unittest.skip('already works')
    def test__get_selection__errors_on_long_or_no_selection(self):
        pymel.core.select(clear=True)
        self.assertRaises(Exception, camstabilizer.get_selection)

        pymel.core.select(clear=True)
        pymel.core.select('|group1|test_box.vtx[1:5]')
        self.assertRaises(Exception, camstabilizer.get_selection)

        pymel.core.select(clear=True)
        pymel.core.select(('|group1|test_box', 'test_camera', 'test_locator'))
        self.assertRaises(Exception, camstabilizer.get_selection)

    # @unittest.skip('already works')
    def test__get_selection__returns_selection(self):
        pymel.core.select(clear=True)
        selection = (
            ['|group1|test_box',],
            ['|group1|test_box', 'test_locator'],
            ['|group1|test_box', 'test_camera'],
            ['|group1|test_box', '|group1|test_box.vtx[1:3]'],
            ['|group1|test_box', '|group2|test_box.vtx[1:3]'],
            ['|group2|test_box',],
            ['|group2|test_box', 'test_locator'],
            ['|group2|test_box', 'test_camera'],
            ['|group2|test_box', '|group1|test_box.vtx[1:3]'],
            )

        for case in selection:
            pymel.core.select(case)
            self.assertEqual(pymel.core.selected(), camstabilizer.get_selection())

    # @unittest.skip('already works')
    def test__get_camera__returns_camera_from_panel(self):
        pymel.core.select(clear=True)
        pymel.core.select('|group1|test_box.vtx[1]')
        pymel.core.setFocus('modelPanel4')
        camtest = pymel.core.nt.Transform('test_camera')

        self.assertEqual(camstabilizer.get_camera(), camtest.getShape())

    # @unittest.skip('already works')
    def test__get_camera__returns_camera_from_selection(self):
        pymel.core.select('|group1|test_box.vtx[1]')
        pymel.core.select('test_camera', add=True)
        pymel.core.setFocus('scriptEditorPanel1')

        camtest = pymel.core.nt.Transform('test_camera')

        self.assertEqual(camstabilizer.get_camera(), camtest.getShape())

    # @unittest.skip('already works')
    def test__get_camera__errors_wihout_camera(self):
        pymel.core.select(clear=True)

        self.assertRaises(Exception, camstabilizer.get_camera)

    # @unittest.skip('already works')
    def test__get_position_object__returns_queryable_position_object(self):
        nodetypes = (
                    pymel.core.nodetypes.Transform,
                    pymel.core.general.MeshVertex,
                )

        selection_sets = (
                ('test_locator',),
                ('test_locator', 'test_camera',),
            )

        for selection in selection_sets:
            pymel.core.select(clear=True)
            pymel.core.select(selection)
            obj = camstabilizer.get_position_object()

            self.assertIn(type(obj), nodetypes)

    # @unittest.skip('already works')
    def test__get_position_object__errors_without_queryable_position(self):
        selection_list = (
                    '|group1|test_box',
                    'test_camera',
                    'test_cameraShape',
                    '|group1|test_box.e[2]',
                    '|group1|test_box.f[2]',
                    '|group1|test_curve.cv[0]',
                    '|group1|test_curve.ep[0]',
                    'defaultLightSet',
                    'test_locator_rotateX',
                    'hardwareRenderGlobals',
                    'lambert1',
                    '|group1|test_curve',
                )

        for sel in selection_list:
            pymel.core.select(clear=True)
            pymel.core.select(sel)
            self.assertRaises(Exception, camstabilizer.get_position_object)

    # @unittest.skip('already works')
    def test__main__exits_without_error_with_good_selection(self):
        pymel.core.select('|group2|test_box.vtx[0]')
        pymel.core.setFocus('modelPanel4')

        self.assertIsNone(camstabilizer.main(task='stabilize'))

        super(CamStabilizerUnitTests, self).setUp()
        pymel.core.select('|group2|test_box.vtx[0]', 'test_camera')

        self.assertIsNone(camstabilizer.main(task='stabilize'))

        super(CamStabilizerUnitTests, self).setUp()
        pymel.core.select('test_locator', 'test_camera')

        self.assertIsNone(camstabilizer.main(task='stabilize'))

    # @unittest.skip('already works')
    def test__stabilize__returns_transform_cam_expression_tuple(self):
        pymel.core.select('|group1|test_box.vtx[0]')
        pymel.core.setFocus('modelPanel4')
        stabilize = camstabilizer.stabilize()

        self.assertIsInstance(stabilize, tuple)
        self.assertIsInstance(stabilize[1], pymel.core.nodetypes.Camera)
        self.assertIsInstance(stabilize[2], str)

    # @unittest.skip('already works')
    def test__create_expression__returns_expression_and_node_as_tuple(self):
        cam = pymel.core.PyNode('|test_locator|test_camera|test_cameraShape')
        pos = pymel.core.PyNode('|group1|test_box|test_boxShape.vtx[3]')

        self.assertIsInstance(camstabilizer.create_expression(cam, pos), str)
        self.assertIn(cam.name(), camstabilizer.create_expression(cam, pos))
        self.assertIn(pos.name(), camstabilizer.create_expression(cam, pos))

    # @unittest.skip('already works')
    def test__setup_expression_node__errors_if_expression_exists(self):
        camstabilizer.setup_expression_node('//', 'test_cameraShape', task='create')
        self.assertRaises(Exception,
                        camstabilizer.setup_expression_node,
                        '//', 'test_cameraShape', task='create'
                        )

    # @unittest.skip('already works')
    def test__clear_stabilizer__deletes_expression_if_exists_or_error(self):
        pymel.core.select('|group1|test_box.vtx[0]')
        pymel.core.setFocus('modelPanel4')
        cam = camstabilizer.get_camera()
        camstabilizer.main(task='stabilize')
        camstabilizer.main(task='clear')

        self.assertRaises(Exception, camstabilizer.main, task='clear')

        camstabilizer.main(task='stabilize')
        camstabilizer.main(task='clear')
        self.assertFalse(pymel.core.objExists(cam.name() + '_stabilizer'))

        camstabilizer.main(task='stabilize')
        self.assertIsNone(camstabilizer.main(task='clear'))

    # @unittest.skip('already works')
    def test__get_camera__errors_on_camera_w_offset(self):
        pymel.core.select('|group1|test_box.vtx[0]', '|test_locator|test_camera')
        cam = pymel.core.PyNode('|test_locator|test_camera|test_cameraShape')
        cam.setHorizontalFilmOffset(0.27)
        cam.setVerticalFilmOffset(-0.11)

        self.assertRaises(Exception, camstabilizer.get_camera,)


def main():
    unittest.main(module='MayaTools.CamStabilizer.camstabilizer_tests', exit=False)
