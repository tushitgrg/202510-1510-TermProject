from unittest import TestCase

from character import make_character


class Test(TestCase):
    def test_make_character_hero(self):
        expected = {'X-coordinate': 0, 'Y-coordinate': 0, 'Current HP': 5, 'Experience': 0, 'Level': 1, 'Name': 'Hero'}
        actual = make_character("Hero")
        self.assertEqual(expected, actual)

    def test_make_character_tushit(self):
        expected = {'X-coordinate': 0, 'Y-coordinate': 0, 'Current HP': 5, 'Experience': 0, 'Level': 1,
                    'Name': 'Tushit'}
        actual = make_character("Tushit")
        self.assertEqual(expected, actual)
