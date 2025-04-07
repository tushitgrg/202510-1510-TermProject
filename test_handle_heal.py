from unittest import TestCase
from unittest.mock import patch, MagicMock

from maze import handle_heal


class Test(TestCase):
    @patch("simpleaudio.WaveObject.from_wave_file")
    def test_handle_heal_heals_when_not_at_maximum(self, _):
        mock_stdscr = MagicMock()
        actual_character = {"Current HP": 4, "Level": 2, "Y-coordinate": 0, "X-coordinate": 0}
        actual_board = {(0, 0): "heal"}
        handle_heal(actual_character, actual_board, mock_stdscr, 20)
        expected_character = {"Current HP": 5, "Level": 2, "Y-coordinate": 0, "X-coordinate": 0}
        expected_board = {(0, 0): "space"}
        self.assertEqual((expected_character, expected_board), (actual_character, actual_board))

    @patch("simpleaudio.WaveObject.from_wave_file")
    def test_handle_heal_heals_when_at_maximum(self, __):
        mock_stdscr = MagicMock()
        actual_character = {"Current HP": 5, "Level": 1, "Y-coordinate": 0, "X-coordinate": 0}
        actual_board = {(0, 0): "heal"}
        handle_heal(actual_character, actual_board, mock_stdscr, 20)
        expected_character = {"Current HP": 5, "Level": 1, "Y-coordinate": 0, "X-coordinate": 0}
        expected_board = {(0, 0): "heal"}
        self.assertEqual((expected_character, expected_board), (actual_character, actual_board))
