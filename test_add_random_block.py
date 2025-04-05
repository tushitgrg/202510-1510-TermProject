from unittest import TestCase
from unittest.mock import patch

from maze import add_random_block


class Test(TestCase):
    @patch('random.randint', return_value=20)
    def test_add_random_block_enemy(self, _):
        expected = "enemy"
        actual = add_random_block()
        self.assertEqual(expected, actual)

    @patch('random.randint', return_value=10)
    def test_add_random_block_heal(self, _):
        expected = "heal"
        actual = add_random_block()
        self.assertEqual(expected, actual)

    @patch('random.randint', return_value=1)
    def test_add_random_block_space(self, _):
        expected = "space"
        actual = add_random_block()
        self.assertEqual(expected, actual)
