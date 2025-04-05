from unittest import TestCase
from unittest.mock import MagicMock, patch

from minigames import handle_failure


class Test(TestCase):
    @patch('minigames.play_game_scene')
    def test_handle_failure_boss(self, _):
        stdscr_mock = MagicMock()
        play_obj_mock = MagicMock()
        sounds_mock = {"failure": MagicMock()}
        character_data = {"Current HP": 10}
        handle_failure(stdscr_mock, play_obj_mock, sounds_mock, character_data, True)
        expected = 0
        actual = character_data["Current HP"]
        self.assertEqual(expected, actual)

    @patch('minigames.play_game_scene')
    def test_handle_failure_not_boss(self, _):
        stdscr_mock = MagicMock()
        play_obj_mock = MagicMock()
        sounds_mock = {"failure": MagicMock()}
        character_data = {"Current HP": 10}
        handle_failure(stdscr_mock, play_obj_mock, sounds_mock, character_data, False)
        expected = 9
        actual = character_data["Current HP"]
        self.assertEqual(expected, actual)
