from unittest import TestCase

from logic import check_if_goal_attained


class Test(TestCase):
    def test_check_if_goal_attained_true(self):
        goal_position = (1, 0)
        character = {"X-coordinate": 0, "Y-coordinate": 1}
        expected = True
        actual = check_if_goal_attained(goal_position, character)
        self.assertEqual(expected, actual)

    def test_check_if_goal_attained_false(self):
        goal_position = (0, 1)
        character = {"X-coordinate": 0, "Y-coordinate": 0}
        expected = False
        actual = check_if_goal_attained(goal_position, character)
        self.assertEqual(expected, actual)
