import unittest
import setoverscan

try:
    reload(setoverscan)
except:
    import importlib
    importlib.reload(setoverscan)


class SetOverscanTests(unittest.TestCase):
    def setUp(self):
        pass

    def test__setoverscane_tests_are_running(self):
        self.assertTrue(True)


def main():
    unittest.main(module=__name__, exit=False)
