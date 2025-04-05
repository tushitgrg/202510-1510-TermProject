from unittest import TestCase

from logic import validate_move


class Test(TestCase):
    def test_validate_move_valid_move(self):
        board = {(0, 0): "space", (0, 1): "space"}
        character = {"X-coordinate": 0, "Y-coordinate": 0}
        expected = (True, (0, 1))
        actual = validate_move(board, character, "d")
        self.assertEqual(expected, actual)

    def test_validate_move_invalid_wall(self):
        board = {(0, 0): "space", (0, 1): "wall"}
        character = {"X-coordinate": 0, "Y-coordinate": 0}
        expected = (False, (0, 1))
        actual = validate_move(board, character, "d")
        self.assertEqual(expected, actual)

    def test_validate_move_invalid_out_of_bounds(self):
        board = {(0, 0): "space"}
        character = {"X-coordinate": 0, "Y-coordinate": 0}
        expected = (False, None)
        actual = validate_move(board, character, "s")
        self.assertEqual(expected, actual)

    def test_validate_move_valid_boss(self):
        board = {(0, 0): "space", (1, 0): "Boss"}
        character = {"X-coordinate": 0, "Y-coordinate": 0}
        expected = (True, (1, 0))
        actual = validate_move(board, character, "s")
        self.assertEqual(expected, actual)
