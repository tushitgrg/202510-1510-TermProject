from unittest import TestCase

from character import is_alive


class Test(TestCase):
    def test_is_alive_positive_hp(self):
        character = {"Current HP": 5}
        expected = True
        actual = is_alive(character)
        self.assertEqual(expected, actual)

    def test_is_alive_zero_hp(self):
        character = {"Current HP": 0}
        expected = False
        actual = is_alive(character)
        self.assertEqual(expected, actual)

    def test_is_alive_negative_hp(self):
        character = {"Current HP": -1}
        expected = False
        actual = is_alive(character)
        self.assertEqual(expected, actual)