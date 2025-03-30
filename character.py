from scenes import play_game_scene


def is_alive(character):
    """
    Check if the character is still alive.

    This function returns True if the character's current HP is greater than 0, and False if it reaches 0.

    :param character: a dictionary representing the character with atleast a "Current HP" key
    :precondition: character is in the correct format
    :postcondition: determine if character is alive or dead
    :return: True, if character is alive otherwise False

    >>> is_alive({"X-coordinate": 0, "Y-coordinate": 0, "Current HP": 4})
    True

    >>> is_alive({"X-coordinate": 0, "Y-coordinate": 0, "Current HP": 0})
    False

    >>> is_alive({"X-coordinate": 0, "Y-coordinate": 0, "Current HP": -1})
    False
    """
    if character["Current HP"] > 0:
        return True
    return False

def move_character(character, new_pos):
    character["Y-coordinate"], character["X-coordinate"] = new_pos

def make_character(name):
    character = {"X-coordinate": 0, "Y-coordinate": 0, "Current HP": 5, "Experience": 0, "Level": 1, "Name": name}
    return character


def check_and_level_up(character, stdscr):
    if character['Experience'] >= character['Level'] * 200:
        play_game_scene(stdscr, "New Achievement: You Just Levelled Up!")
        character['Experience'] -= character['Level'] * 200
        character['Level'] += 1
        character['Current HP'] = 5 * character['Level']

