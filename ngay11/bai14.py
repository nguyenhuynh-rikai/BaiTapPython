import unittest

class TestBasic(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(1 + 2, 3)

if __name__ == "__main__":
    unittest.main()