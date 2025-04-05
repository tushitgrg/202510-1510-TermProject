from unittest import TestCase

from logic import check_for_foe


class Test(TestCase):
    def test_check_for_foe_enemy_present(self):
        board = {(0, 0): "enemy", (0, 1): "space"}
        character = {"X-coordinate": 0, "Y-coordinate": 0}
        expected = True
        actual = check_for_foe(board, character)
        self.assertEqual(expected, actual)

    def test_check_for_foe_enemy_absent(self):
        board = {(0, 0): "space", (0, 1): "enemy"}
        character = {"X-coordinate": 0, "Y-coordinate": 0}
        expected = False
        actual = check_for_foe(board, character)
        self.assertEqual(expected, actual)
