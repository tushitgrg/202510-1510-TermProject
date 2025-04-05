from unittest import TestCase
from unittest.mock import patch

from logic import move_enemies


class Test(TestCase):
    @patch('random.shuffle', side_effect=lambda x: x)
    def test_move_enemies_no_enemies(self, _):
        board = {(0, 0): "space", (0, 1): "space"}
        character = {"X-coordinate": 0, "Y-coordinate": 0}
        move_enemies(board, character)
        expected = {(0, 0): "space", (0, 1): "space"}
        actual = board
        self.assertEqual(expected, actual)

    @patch('random.shuffle', side_effect=lambda x: x)
    def test_move_enemies_enemy_cannot_move(self, _):
        board = {(0, 0): "enemy", (0, 1): "wall"}
        character = {"X-coordinate": 1, "Y-coordinate": 1}
        move_enemies(board, character)
        expected = {(0, 0): "enemy", (0, 1): "wall"}
        actual = board
        self.assertEqual(expected, actual)

    @patch('random.shuffle', side_effect=lambda x: x)
    def test_move_enemies_enemy_moves(self, _):
        board = {(0, 0): "enemy", (1, 0): "space"}
        character = {"X-coordinate": 1, "Y-coordinate": 1}
        move_enemies(board, character)
        expected = {(0, 0): "space", (1, 0): "enemy"}
        actual = board
        self.assertEqual(expected, actual)

    @patch('random.shuffle', side_effect=lambda x: x)
    def test_move_enemies_enemy_avoids_character(self, _):
        board = {(0, 0): "enemy", (1, 0): "space", (0, 1): "space", (1, 1): "space"}
        character = {"X-coordinate": 1, "Y-coordinate": 0}
        move_enemies(board, character)
        expected = {(0, 0): 'space', (0, 1): 'space', (1, 0): 'enemy', (1, 1): 'space'}
        actual = board
        self.assertEqual(expected, actual)
