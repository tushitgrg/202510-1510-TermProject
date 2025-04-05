from unittest import TestCase

from logic import check_for_boss


class Test(TestCase):
    def test_check_for_boss_boss_present(self):
        board = {(0, 0): "Boss", (0, 1): "space"}
        character = {"X-coordinate": 0, "Y-coordinate": 0}
        expected = True
        actual = check_for_boss(board, character)
        self.assertEqual(expected, actual)

    def test_check_for_boss_boss_absent(self):
        board = {(0, 0): "space", (0, 1): "Boss"}
        character = {"X-coordinate": 0, "Y-coordinate": 0}
        expected = False
        actual = check_for_boss(board, character)
        self.assertEqual(expected, actual)
