from unittest import TestCase

from jigsaw import get_ascii_picture


class Test(TestCase):
    def test_get_ascii_picture_length(self):
        expected = 9
        actual = len(get_ascii_picture())
        self.assertEqual(expected, actual)
