from unittest import TestCase
from unittest.mock import patch

from maze import generate_maze


class Test(TestCase):

    @patch('random.shuffle', lambda x: x)
    @patch('maze.add_random_block', return_value="space")
    def test_generate_maze_standard(self, _):
        board = {(row, col): "wall" for row in range(5) for col in range(5)}
        board[(0, 0)] = "space"
        goal_position = [0, 0]
        generate_maze(0, 0, board, 5, 5, goal_position, boss=False)
        expected = {(0, 0): 'space',
                    (0, 1): 'wall',
                    (0, 2): 'space',
                    (0, 3): 'space',
                    (0, 4): 'space',
                    (1, 0): 'space',
                    (1, 1): 'wall',
                    (1, 2): 'space',
                    (1, 3): 'wall',
                    (1, 4): 'space',
                    (2, 0): 'space',
                    (2, 1): 'wall',
                    (2, 2): 'space',
                    (2, 3): 'wall',
                    (2, 4): 'space',
                    (3, 0): 'space',
                    (3, 1): 'wall',
                    (3, 2): 'wall',
                    (3, 3): 'wall',
                    (3, 4): 'space',
                    (4, 0): 'space',
                    (4, 1): 'space',
                    (4, 2): 'space',
                    (4, 3): 'space',
                    (4, 4): 'space'}
        self.assertEqual(board, expected)
