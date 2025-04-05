from unittest import TestCase

from minigames import get_alert_message


class Test(TestCase):
    def test_get_alert_message_almost_there(self):
        expected = "Almost there!"
        actual = get_alert_message(24, 30, 2, 5)
        self.assertEqual(expected, actual)

    def test_get_alert_message_times_almost_up(self):
        expected = "Time’s almost up!"
        actual = get_alert_message(10, 30, 4.5, 5)
        self.assertEqual(expected, actual)

    def test_get_alert_message_keep_struggling(self):
        expected = "Keep struggling!"
        actual = get_alert_message(5, 30, 1, 5)
        self.assertEqual(expected, actual)
