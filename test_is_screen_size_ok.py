from unittest import TestCase
from unittest.mock import MagicMock

from ui import is_screen_size_ok


class Test(TestCase):
    def test_is_screen_size_ok_screen_too_small(self):
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (20, 100)
        expected = False
        actual = is_screen_size_ok(mock_stdscr)
        self.assertEqual(actual, expected)

    def test_is_screen_size_ok_screen_sufficient(self):
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (55, 165)
        expected = True
        actual = is_screen_size_ok(mock_stdscr)
        self.assertEqual(actual, expected)
