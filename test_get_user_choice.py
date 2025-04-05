from unittest import TestCase
from unittest.mock import MagicMock

from ui import get_user_choice


class Test(TestCase):
    def test_get_user_choice_user_presses_q(self):
        mock_stdscr = MagicMock()
        mock_stdscr.getkey.side_effect = ["q"]
        expected = None
        actual = get_user_choice(mock_stdscr, 10)
        self.assertEqual(actual, expected)

    def test_get_user_choice_user_presses_w(self):
        mock_stdscr = MagicMock()
        mock_stdscr.getkey.side_effect = ["w"]
        expected = "w"
        actual = get_user_choice(mock_stdscr, 10)
        self.assertEqual(actual, expected)

    def test_get_user_choice_user_presses_a(self):
        mock_stdscr = MagicMock()
        mock_stdscr.getkey.side_effect = ["a"]
        expected = "a"
        actual = get_user_choice(mock_stdscr, 10)
        self.assertEqual(actual, expected)

    def test_get_user_choice_user_presses_s(self):
        mock_stdscr = MagicMock()
        mock_stdscr.getkey.side_effect = ["s"]
        expected = "s"
        actual = get_user_choice(mock_stdscr, 10)
        self.assertEqual(actual, expected)

    def test_get_user_choice_user_presses_d(self):
        mock_stdscr = MagicMock()
        mock_stdscr.getkey.side_effect = ["d"]
        expected = "d"
        actual = get_user_choice(mock_stdscr, 10)
        self.assertEqual(actual, expected)

    def test_get_user_choice_invalid_key_first(self):
        mock_stdscr = MagicMock()
        mock_stdscr.getkey.side_effect = ["x", "w"]
        expected = "w"
        actual = get_user_choice(mock_stdscr, 10)
        self.assertEqual(actual, expected)
