from unittest import TestCase
from unittest.mock import patch

from jigsaw import init_puzzle


class Test(TestCase):
    @patch('random.shuffle', side_effect=lambda x: x)
    def test_init_puzzle_with_patched_random_2_x_2(self, _):
        expected = [[(0, 0), (1, 1)], [(2, 2), (3, 3)]]
        actual = init_puzzle(2, 2)
        self.assertEqual(expected, actual)

    @patch('random.shuffle', side_effect=lambda x: x)
    def test_init_puzzle_with_patched_random_3_x_3(self, _):
        expected = [[(0, 0), (1, 1), (2, 2)], [(3, 3), (4, 4), (5, 5)], [(6, 6), (7, 7), (8, 8)]]
        actual = init_puzzle(3, 3)
        self.assertEqual(expected, actual)