"""
Tests for Constrain Locator To Vertex module

offline tests run in mayapy in a terminal
skipping tests requireing GUI

for offline testing run:
mayapy constrainLoc2vtx_tests.py
"""


import os
from os.path import abspath, dirname
import unittest

import pymel.core

import constrainLoc2vtx
reload(constrainLoc2vtx)


gui = False if __name__ == '__main__' else True

### skipping tests:
# @unittest.skip('--> Passed...')
# @unittest.skipIf(not gui, '--> Not in Maya GUI...')


class ContrsainLoc2vtxUnittest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        pymel.core.newFile(force=True)
        transform, shape = pymel.core.polyCube()
        pymel.core.select(clear=True)

        transform.rename('test_cube')
        pymel.core.setKeyframe(transform)
        transform.setTranslation((1, 2, 3))
        transform.setRotation((35, 148, 323))
        transform.setScale((1, 2, 1))
        pymel.core.setKeyframe(transform, time=120)

    # @unittest.skip('--> Passed...')
    def test__test_is_running(self):
        self.assertTrue(True)


class ContrsainLoc2vtxTest(unittest.TestCase):
    def setUp(self):
        ContrsainLoc2vtxUnittest.setUp()

    def test__functional_test(self):
        pymel.core.select('test_cube.vtx[1]')

        constrainLoc2vtx.constrain_loc_to_vtx()

        """
        creates locator with name:
        locator_vtx_constrain_test_cube

        FIX THIS
        """
        self.assertTrue(pymel.core.PyNode('locator_vertexConstrained'))

        """
        creates expression node with name:
        expression_vtx_constrain_test_cube

        FIX THIS
        """
        self.assertTrue(pymel.core.PyNode('locator_vertexConstrained1'))


        """
        expression is:
        """
        expression = ("""float $BBoxSize = test_cube.boundingBoxMinX;"""
        """\n\n$vertexWorldPos = `pointPosition -world test_cube.vtx[1]`;"""
        """\nlocator_vertexConstrained.translateX = $vertexWorldPos[0];"""
        """\nlocator_vertexConstrained.translateY = $vertexWorldPos[1];"""
        """\nlocator_vertexConstrained.translateZ = $vertexWorldPos[2];""")

        self.assertEqual(
                pymel.core.PyNode('locator_vertexConstrained1').getExpression(),
                expression
                )

        """
        Locator position equals
        vertex position
        """

        loc = pymel.core.PyNode('locator_vertexConstrained')
        vtx = pymel.core.PyNode('test_cube.vtx[1]')

        loc_x, loc_y, loc_z = loc.getTranslation(space='world')
        vtx_x, vtx_y, vtx_z = vtx.getPosition(space='world')

        pymel.core.currentTime(2)
        self.assertEqual(loc_x, vtx_x)
        self.assertEqual(loc_y, vtx_y)
        self.assertEqual(loc_z, vtx_z)

        pymel.core.currentTime(50)
        self.assertEqual(loc_x, vtx_x)
        self.assertEqual(loc_y, vtx_y)
        self.assertEqual(loc_z, vtx_z)



def run():
    print('//'*25)
    print('\\\\'*25)
    print('//'*25)
    unittest.main(module=__name__, exit=False, verbosity=1)


if __name__ == '__main__':
    run()
