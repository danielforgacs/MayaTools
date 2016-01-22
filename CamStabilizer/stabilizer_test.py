"""
"""

import unittest


class TestSceneSetup(unittest.TestCase):
    def setUp(self):
        import pymel.core

        pymel.core.newFile(force=True)

        pymel.core.polyCube()

        camaim = pymel.core.spaceLocator()
        cam, camshape = pymel.core.camera(displayResolution=True, displayFilmGate=True, overscan=1.8)

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


class StabizilerTests(TestSceneSetup):
    def test_unittests_running(self):
        self.assertTrue(True)


class StabilizerFunctionalTests(TestSceneSetup):
    def test_functional_tests_running(self):
        self.assertTrue(True)



def main():
    print('/'*50)
    print('\\'*50)
    print('/'*50)

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(StabizilerTests)
    suite_func = loader.loadTestsFromTestCase(StabilizerFunctionalTests)

    unittest.TextTestRunner(verbosity=1).run(suite)
    unittest.TextTestRunner(verbosity=1).run(suite_func)


if __name__ == '__main__':
    unittest.main(verbosity=1)
