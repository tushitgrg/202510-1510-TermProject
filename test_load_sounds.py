from unittest import TestCase
from unittest.mock import patch

from minigames import load_sounds


class Test(TestCase):
    @patch('simpleaudio.WaveObject.from_wave_file', side_effect=lambda x: x)
    def test_load_sounds(self, _):
        actual = load_sounds()
        expected = {'failure': 'sounds/failure.wav',
                    'fire': 'sounds/fire_effect.wav',
                    'keypress': 'sounds/keypress.wav',
                    'success': 'sounds/success.wav'}
        self.assertEqual(expected, actual)
