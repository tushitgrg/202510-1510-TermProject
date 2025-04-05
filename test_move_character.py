from unittest import TestCase

from character import move_character


class Test(TestCase):
    def test_move_character_new_position(self):
        character = {'X-coordinate': 0, 'Y-coordinate': 0, 'Current HP': 5, 'Experience': 0, 'Level': 1, 'Name': 'Hero'}
        move_character(character, (3, 5))
        expected = {'X-coordinate': 5, 'Y-coordinate': 3, 'Current HP': 5, 'Experience': 0, 'Level': 1, 'Name': 'Hero'}
        actual = character
        self.assertEqual(expected, actual)

    def test_move_character_same_position(self):
        character = {'X-coordinate': 0, 'Y-coordinate': 0, 'Current HP': 5, 'Experience': 0, 'Level': 1, 'Name': 'Hero'}
        move_character(character, (0, 0))
        expected = {'X-coordinate': 0, 'Y-coordinate': 0, 'Current HP': 5, 'Experience': 0, 'Level': 1, 'Name': 'Hero'}
        actual = character
        self.assertEqual(expected, actual)
