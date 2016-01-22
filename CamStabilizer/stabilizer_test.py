import unittest


class StabizilerTests(unittest.TestCase):
    def test_unittests_running(self):
        self.assertTrue(True)


class StabilizerFunctionalTests(unittest.TestCase):
    def test_functional_tests_running(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main(verbosity=1)
