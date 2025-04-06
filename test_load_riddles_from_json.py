from unittest import TestCase
from unittest.mock import patch, mock_open

from minigames import load_riddles_from_json


class Test(TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load", return_value=[{
        "description": """A chamber of mirrors reflects your every move, casting shifting shadows.
        I am not alive, but I grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. 
        What am I?""",
        "answer": [
            "fire"
        ]
    }])
    def test_load_riddles_from_json_returns_correct_data_single(self, _, __):
        expected_data = [{
            "description": """A chamber of mirrors reflects your every move, casting shifting shadows.
        I am not alive, but I grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. 
        What am I?""",
            "answer": [
                "fire"
            ]
        }]
        actual_data = load_riddles_from_json()
        self.assertEqual(expected_data, actual_data)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load",
           return_value=[{
               "description": """A room filled with water-worn stones and echoing whispers, 
               ancient maps scattered about. I have cities, but no houses. I have mountains, but no trees. 
               I have water, but no fish. What am I?""",
               "answer": [
                   "map",
                   "maps"
               ]
           },
               {
                   "description": """A chamber bathed in soft, ethereal light, 
                   with delicate objects casting long shadows.What can travel around 
                   the world while staying in a corner?""",
                   "answer": [
                       "stamp",
                       "stamps"
                   ]
               }])
    def test_load_riddles_from_json_returns_correct_data_multiple(self, _, __):
        expected_data = [{
            "description": """A room filled with water-worn stones and echoing whispers, 
               ancient maps scattered about. I have cities, but no houses. I have mountains, but no trees. 
               I have water, but no fish. What am I?""",
            "answer": [
                "map",
                "maps"
            ]
        },
            {
                "description": """A chamber bathed in soft, ethereal light, 
                   with delicate objects casting long shadows.What can travel around 
                   the world while staying in a corner?""",
                "answer": [
                    "stamp",
                    "stamps"
                ]
            }]
        actual_data = load_riddles_from_json()
        self.assertEqual(expected_data, actual_data)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load", return_value=[])
    def test_load_riddles_from_json_returns_correct_data_empty(self, _, __):
        expected_data = []
        actual_data = load_riddles_from_json()
        self.assertEqual(expected_data, actual_data)
