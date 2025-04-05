from unittest import TestCase
from unittest.mock import MagicMock, patch

from minigames import play_riddle


class Test(TestCase):
    @patch('random.choice', side_effect=lambda x: x[0])
    @patch('minigames.play_game_scene', return_value=None)
    @patch('curses.echo', return_value=None)
    @patch('curses.noecho', return_value=None)
    def test_play_riddle_correct_answer(self, _, __, ___, ____):
        stdscr_mock = MagicMock()
        stdscr_mock.getstr.return_value = b'keyboard'
        stdscr_mock.getmaxyx.return_value = (40, 40)
        character_data = {"Current HP": 10}
        play_riddle(stdscr_mock, character_data)
        expected = 10
        actual = character_data["Current HP"]
        self.assertEqual(expected, actual)

    @patch('random.choice', side_effect=lambda x: x[0])
    @patch('minigames.play_game_scene', return_value=None)
    @patch('curses.echo', return_value=None)
    @patch('curses.noecho', return_value=None)
    def test_play_riddle_wrong_answer(self, _, __, ___, ____):
        stdscr_mock = MagicMock()
        stdscr_mock.getstr.return_value = b'hi'
        stdscr_mock.getmaxyx.return_value = (40, 40)
        character_data = {"Current HP": 10}
        play_riddle(stdscr_mock, character_data)
        expected = 9
        actual = character_data["Current HP"]
        self.assertEqual(expected, actual)