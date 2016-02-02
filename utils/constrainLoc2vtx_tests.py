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


gui = False


if __name__ != '__main__':
    """
    if the module is run as a script
    in a terminal window in mayapy
    pymel.core import is skipped
    """
    import pymel.core
    gui = True


import constrainLoc2vtx
reload(constrainLoc2vtx)


class ContrsainLoc2vtxUnittestOffline(unittest.TestCase):
    def test__test_is_running(self):
        self.assertTrue(True)

    # @unittest.skip('--> Passed...')
    @unittest.skipIf(not gui, '--> Not in Maya GUI...')
    def test__skip_if_no_GUI(self):
        self.assertTrue(True)


def run():
    unittest.main(module=__name__, exit=False, verbosity=2)


if __name__ == '__main__':
    run()
