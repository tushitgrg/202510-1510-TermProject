from unittest import TestCase
from unittest.mock import MagicMock, patch

from minigames import display_centered_message


class Test(TestCase):
    @patch('minigames.curses.color_pair', side_effect=lambda x: x)
    def test_display_centered_message_multiline(self, _):
        stdscr_mock = MagicMock()
        message_data = "line1\nline2"
        result = display_centered_message(stdscr_mock, message_data, 10, 10)
        expected = (4, ["line1", "line2"])
        actual = result
        self.assertEqual(expected, actual)

    @patch('minigames.curses.color_pair', side_effect=lambda x: x)
    def test_display_centered_message_singleline(self, _):
        stdscr_mock = MagicMock()
        message_data = "line1"
        result = display_centered_message(stdscr_mock, message_data, 10, 10)
        expected = (4, ["line1"])
        actual = result
        self.assertEqual(expected, actual)

    @patch('minigames.curses.color_pair', side_effect=lambda x: x)
    def test_display_centered_message_no_text(self, _):
        stdscr_mock = MagicMock()
        message_data = ""
        result = display_centered_message(stdscr_mock, message_data, 10, 10)
        expected = (4, [""])
        actual = result
        self.assertEqual(expected, actual)