import unittest

class TestBasic(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(3 + 2, 5)

if __name__ == "__main__":
    unittest.main()