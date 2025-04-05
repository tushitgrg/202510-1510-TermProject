from unittest import TestCase

from jigsaw import is_piece_in_correct_position


class Test(TestCase):
    def test_is_piece_in_correct_position_true(self):
        test_grid = [[(0, 0), (1, 1)], [(2, 2), (3, 3)]]
        expected = True
        actual = is_piece_in_correct_position(test_grid, 0, 0)
        self.assertEqual(expected, actual)

    def test_is_piece_in_correct_position_false(self):
        test_grid = [[(1, 1), (0, 0)], [(2, 2), (3, 3)]]
        expected = False
        actual = is_piece_in_correct_position(test_grid, 0, 1)
        self.assertEqual(expected, actual)
