import os
from os.path import abspath, dirname
import unittest

import constrainLoc2vtx
reload(constrainLoc2vtx)


class ContrsainLoc2vtxUnittestOffline(unittest.TestCase):
    def test__test_is_running(self):
        self.assertTrue(True)


def run():
    unittest.main(module=__name__, exit=False)


if __name__ == '__main__':
    run()
