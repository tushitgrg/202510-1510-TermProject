from unittest import TestCase
from unittest.mock import patch, MagicMock

from ui import get_user_name


class Test(TestCase):
    @patch("curses.echo")
    def test_get_user_name_returns_user_name_when_input_is_valid(self, _):
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        mock_stdscr.getstr.side_effect = [b"Tushit"]
        expected = "Tushit"
        actual = get_user_name(mock_stdscr)
        self.assertEqual(actual, expected)

    @patch("curses.echo")
    def test_get_user_name_skips_whitespace_until_valid_input(self, _):
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        mock_stdscr.getstr.side_effect = [b"   ", b"Tushit"]
        expected = "Tushit"
        actual = get_user_name(mock_stdscr)
        self.assertEqual(actual, expected)
