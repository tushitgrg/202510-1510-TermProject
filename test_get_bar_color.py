from unittest import TestCase
from unittest.mock import patch

from minigames import get_bar_color


class Test(TestCase):
    @patch('minigames.curses.color_pair', side_effect=lambda x: x)
    def test_get_bar_color_high_time(self, _):
        expected = 2
        actual = get_bar_color(0.7)
        self.assertEqual(expected, actual)

    @patch('minigames.curses.color_pair', side_effect=lambda x: x)
    def test_get_bar_color_mid_time(self, _):
        expected = 3
        actual = get_bar_color(0.4)
        self.assertEqual(expected, actual)

    @patch('minigames.curses.color_pair', side_effect=lambda x: x)
    def test_get_bar_color_low_time(self, _):
        expected = 4
        actual = get_bar_color(0.2)
        self.assertEqual(expected, actual)
