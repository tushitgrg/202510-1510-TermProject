from unittest import TestCase
from unittest.mock import patch

from maze import make_board


class Test(TestCase):

    @patch('random.shuffle', lambda x: x)
    @patch('maze.add_random_block', return_value="space")
    def test_make_board_regular_maze_goal_and_structure_match(self, _):
        character = {"X-coordinate": -1, "Y-coordinate": -1}
        board, goal_position = make_board(4, 4, character, boss=False)
        expected = {(0, 0): 'space',
                    (0, 1): 'wall',
                    (0, 2): 'Goal',
                    (0, 3): 'wall',
                    (0, 4): 'wall',
                    (1, 0): 'space',
                    (1, 1): 'wall',
                    (1, 2): 'space',
                    (1, 3): 'wall',
                    (1, 4): 'wall',
                    (2, 0): 'space',
                    (2, 1): 'space',
                    (2, 2): 'space',
                    (2, 3): 'wall',
                    (2, 4): 'wall',
                    (3, 0): 'wall',
                    (3, 1): 'wall',
                    (3, 2): 'wall',
                    (3, 3): 'wall',
                    (3, 4): 'wall',
                    (4, 0): 'wall',
                    (4, 1): 'wall',
                    (4, 2): 'wall',
                    (4, 3): 'wall',
                    (4, 4): 'wall'}
        self.assertEqual(board, expected)

    @patch('random.shuffle', lambda x: x)
    @patch('maze.add_random_block', return_value="space")
    def test_make_board_boss_maze_has_only_spaces_and_boss(self, _):
        character = {"X-coordinate": -1, "Y-coordinate": -1}
        board, goal_position = make_board(4, 4, character, boss=True)
        expected = {(0, 0): 'space',
                    (0, 1): 'wall',
                    (0, 2): 'Boss',
                    (0, 3): 'wall',
                    (0, 4): 'wall',
                    (1, 0): 'space',
                    (1, 1): 'wall',
                    (1, 2): 'space',
                    (1, 3): 'wall',
                    (1, 4): 'wall',
                    (2, 0): 'space',
                    (2, 1): 'space',
                    (2, 2): 'space',
                    (2, 3): 'wall',
                    (2, 4): 'wall',
                    (3, 0): 'wall',
                    (3, 1): 'wall',
                    (3, 2): 'wall',
                    (3, 3): 'wall',
                    (3, 4): 'wall',
                    (4, 0): 'wall',
                    (4, 1): 'wall',
                    (4, 2): 'wall',
                    (4, 3): 'wall',
                    (4, 4): 'wall'}
        self.assertEqual(board, expected)
