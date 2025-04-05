from unittest import TestCase

from jigsaw import is_solved


class Test(TestCase):
    def test_is_solved_true_when_solved(self):
        test_grid = [[(0, 0), (1, 1)], [(2, 2), (3, 3)]]
        expected = True
        actual = is_solved(test_grid, 2, 2)
        self.assertEqual(expected, actual)

    def test_is_solved_false_when_not_solved(self):
        test_grid = [[(2, 2), (3, 3)], [(0, 0), (1, 1)]]
        expected = False
        actual = is_solved(test_grid, 2, 2)
        self.assertEqual(expected, actual)
