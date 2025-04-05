from unittest.mock import patch

import curses
from unittest import TestCase

from jigsaw import get_cell_attribute


class Test(TestCase):
    @patch('jigsaw.is_piece_in_correct_position', return_value=False)
    @patch('jigsaw.curses.color_pair', side_effect=lambda x: x)
    def test_get_cell_attribute_cursor_and_selected(self, _, __):
        colors = {"selected": 10, "cursor": 20, "correct": 30, "normal": 40}
        grid = [[(0, 0)]]
        expected = 10 | curses.A_BOLD
        actual = get_cell_attribute(0, 0, (0, 0), (0, 0), colors, grid)
        self.assertEqual(expected, actual)

    @patch('jigsaw.is_piece_in_correct_position', return_value=False)
    @patch('jigsaw.curses.color_pair', side_effect=lambda x: x)
    def test_get_cell_attribute_cursor_only(self, _, __):
        colors = {"selected": 10, "cursor": 20, "correct": 30, "normal": 40}
        grid = [[(0, 0)]]
        expected = 20
        actual = get_cell_attribute(0, 0, (0, 0), None, colors, grid)
        self.assertEqual(expected, actual)

    @patch('jigsaw.is_piece_in_correct_position', return_value=False)
    @patch('jigsaw.curses.color_pair', side_effect=lambda x: x)
    def test_get_cell_attribute_selected_only(self, _, __):
        colors = {"selected": 10, "cursor": 20, "correct": 30, "normal": 40}
        grid = [[(0, 0)]]
        expected = 10
        actual = get_cell_attribute(0, 0, (1, 1), (0, 0), colors, grid)
        self.assertEqual(expected, actual)

    @patch('jigsaw.is_piece_in_correct_position', return_value=True)
    @patch('jigsaw.curses.color_pair', side_effect=lambda x: x)
    def test_get_cell_attribute_piece_in_correct_position(self, _, __):
        colors = {"selected": 10, "cursor": 20, "correct": 30, "normal": 40}
        grid = [[(0, 0)]]
        expected = 30
        actual = get_cell_attribute(0, 0, (1, 1), (2, 2), colors, grid)
        self.assertEqual(expected, actual)

    @patch('jigsaw.is_piece_in_correct_position', return_value=False)
    @patch('jigsaw.curses.color_pair', side_effect=lambda x: x)
    def test_get_cell_attribute_normal(self, _, __):
        colors = {"selected": 10, "cursor": 20, "correct": 30, "normal": 40}
        grid = [[(0, 0)]]
        expected = 40
        actual = get_cell_attribute(0, 0, (1, 1), (2, 2), colors, grid)
        self.assertEqual(expected, actual)
