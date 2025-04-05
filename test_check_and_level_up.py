from unittest import TestCase
from unittest.mock import Mock, patch

from character import check_and_level_up


class Test(TestCase):

    @patch("character.play_game_scene", return_value=None)
    def test_check_and_level_up_no_level_up(self, _):
        stdscr = Mock()
        character = {'Experience': 100, 'Level': 1, 'Current HP': 5}
        check_and_level_up(character, stdscr)
        expected = {'Experience': 100, 'Level': 1, 'Current HP': 5}
        actual = character
        self.assertEqual(expected, actual)

    @patch("character.play_game_scene", return_value=None)
    def test_check_and_level_up_exact_exp_threshold(self, _):
        stdscr = Mock()
        character = {'Experience': 200, 'Level': 1, 'Current HP': 5}
        check_and_level_up(character, stdscr)
        expected = {'Experience': 0, 'Level': 2, 'Current HP': 10}
        actual = character
        self.assertEqual(expected, actual)

    @patch("character.play_game_scene", return_value=None)
    def test_check_and_level_up_exceed_exp_threshold(self, _):
        stdscr = Mock()
        character = {'Experience': 250, 'Level': 1, 'Current HP': 5}
        check_and_level_up(character, stdscr)
        expected = {'Experience': 50, 'Level': 2, 'Current HP': 10}
        actual = character
        self.assertEqual(expected, actual)
