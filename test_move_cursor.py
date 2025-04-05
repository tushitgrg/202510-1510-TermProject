from unittest import TestCase

from jigsaw import move_cursor


class Test(TestCase):
    def test_move_cursor_up(self):
        expected = (0, 0)
        actual = move_cursor(ord('w'), (0, 0))
        self.assertEqual(expected, actual)

    def test_move_cursor_down(self):
        expected = (1, 0)
        actual = move_cursor(ord('s'), (0, 0))
        self.assertEqual(expected, actual)

    def test_move_cursor_left(self):
        expected = (0, 0)
        actual = move_cursor(ord('a'), (0, 0))
        self.assertEqual(expected, actual)

    def test_move_cursor_right(self):
        expected = (0, 1)
        actual = move_cursor(ord('d'), (0, 0))
        self.assertEqual(expected, actual)

    def test_move_cursor_no_movement(self):
        expected = (1, 1)
        actual = move_cursor(ord('x'), (1, 1))
        self.assertEqual(expected, actual)
