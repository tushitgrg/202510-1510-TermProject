from unittest import TestCase
from unittest.mock import MagicMock, patch

from ui import get_user_battle_decision


class Test(TestCase):
    @patch("curses.echo")
    def test_get_user_battle_decision_input_is_invalid_first(self, _):
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        mock_stdscr.getstr.side_effect = [b"invalid", b"BuRn"]
        expected = "burn"
        actual = get_user_battle_decision(mock_stdscr)
        self.assertEqual(actual, expected)

    @patch("curses.echo")
    def test_get_user_battle_decision_input_is_burn_lowercased(self, _):
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        mock_stdscr.getstr.side_effect = [b"burn"]
        expected = "burn"
        actual = get_user_battle_decision(mock_stdscr)
        self.assertEqual(actual, expected)

    @patch("curses.echo")
    def test_get_user_battle_decision_input_is_burn_uppercased(self, _):
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        mock_stdscr.getstr.side_effect = [b"BURN"]
        expected = "burn"
        actual = get_user_battle_decision(mock_stdscr)
        self.assertEqual(actual, expected)

    @patch("curses.echo")
    def test_get_user_battle_decision_input_is_burn_inconsistent_case(self, _):
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        mock_stdscr.getstr.side_effect = [b"BuRn"]
        expected = "burn"
        actual = get_user_battle_decision(mock_stdscr)
        self.assertEqual(actual, expected)

    @patch("curses.echo")
    def test_get_user_battle_decision_input_is_burn_with_whitespace(self, _):
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        mock_stdscr.getstr.side_effect = [b"   burn      "]
        expected = "burn"
        actual = get_user_battle_decision(mock_stdscr)
        self.assertEqual(actual, expected)

    @patch("curses.echo")
    def test_get_user_battle_decision_input_is_flee_lowercased(self, _):
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        mock_stdscr.getstr.side_effect = [b"flee"]
        expected = "flee"
        actual = get_user_battle_decision(mock_stdscr)
        self.assertEqual(actual, expected)

    @patch("curses.echo")
    def test_get_user_battle_decision_input_is_flee_uppercased(self, _):
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        mock_stdscr.getstr.side_effect = [b"FLEE"]
        expected = "flee"
        actual = get_user_battle_decision(mock_stdscr)
        self.assertEqual(actual, expected)

    @patch("curses.echo")
    def test_get_user_battle_decision_input_is_flee_inconsistent_case(self, _):
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        mock_stdscr.getstr.side_effect = [b"FlEe"]
        expected = "flee"
        actual = get_user_battle_decision(mock_stdscr)
        self.assertEqual(actual, expected)

    @patch("curses.echo")
    def test_get_user_battle_decision_input_is_flee_with_whitespace(self, _):
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        mock_stdscr.getstr.side_effect = [b"   flee      "]
        expected = "flee"
        actual = get_user_battle_decision(mock_stdscr)
        self.assertEqual(actual, expected)