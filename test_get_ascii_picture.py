from unittest import TestCase

from jigsaw import get_ascii_picture


class Test(TestCase):
    def test_get_ascii_picture_(self):
        expected = [
            [
                "     ",
                "  _  ",
                " / \\_",
                "/    ",
                "|    "
            ],
            [
                "     ",
                "___  ",
                "   \\_",
                "     ",
                "     "
            ],
            [
                "     ",
                "     ",
                "_    ",
                " \\   ",
                "  \\  "
            ],
            [
                "|    ",
                "|    ",
                "| O  ",
                "|    ",
                "\\    "
            ],
            [
                "     ",
                "     ",
                "     ",
                "     ",
                "     "
            ],
            [
                "     ",
                "     ",
                "  O  ",
                "     ",
                "    /"
            ],
            [
                " \\   ",
                "  \\  ",
                "   \\ ",
                "    \\",
                "     "
            ],
            [
                "     ",
                "     ",
                "     ",
                "\\___/",
                "     "
            ],
            [
                "   / ",
                "  /  ",
                " /   ",
                "/    ",
                "     "
            ]
        ]
        actual = get_ascii_picture()
        self.assertEqual(expected, actual)
