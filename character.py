"""
Tushit Garg
A01418176

This module creates and manages game characters, tracking their health, position, and experience. It includes functions
to check vitality, move characters, initialize stats, and handle leveling up.
"""

from scenes import play_game_scene


def is_alive(character: dict):
    """
    Check if the character is still alive.

    This function returns True if the character's current HP is greater than 0, and False if it reaches 0.

    :param character: a dictionary representing the character with at least a "Current HP" key
    :precondition: character is in the correct format
    :postcondition: determine if character is alive or dead
    :return: True if character is alive, otherwise False

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


def move_character(character: dict, new_pos: tuple):
    """
    Move the character to a new position.

    This function updates the character's X and Y coordinates based on the new position provided.

    :param character: a dictionary representing the character with "X-coordinate" and "Y-coordinate" keys
    :param new_pos: a tuple (y, x) representing the new coordinates
    :precondition: character must be a dictionary with at least "X-coordinate" and "Y-coordinate" keys
    :precondition: new_pos must be a tuple of two integers
    :postcondition: update character's position correctly

    >>> my_character = {'X-coordinate': 0, 'Y-coordinate': 0, 'Current HP': 5, 'Experience': 0, 'Level': 1,
    ... 'Name': 'Hero'}
    >>> move_character(my_character, (3, 5))
    >>> my_character == {'X-coordinate': 5, 'Y-coordinate': 3, 'Current HP': 5, 'Experience': 0, 'Level': 1,
    ... 'Name': 'Hero'}
    True

    >>> my_character = {'X-coordinate': 0, 'Y-coordinate': 0, 'Current HP': 5, 'Experience': 0, 'Level': 1,
    ... 'Name': 'Hero'}
    >>> move_character(my_character, (0, 0))
    >>> my_character == {'X-coordinate': 0, 'Y-coordinate': 0, 'Current HP': 5, 'Experience': 0, 'Level': 1,
    ... 'Name': 'Hero'}
    True
    """
    character["Y-coordinate"], character["X-coordinate"] = new_pos


def make_character(name):
    """
    Create a new character with the given name.

    This function initializes a character dictionary with default stats and the provided name.

    :param name: a string representing the character's name
    :precondition: name must be a non-empty string
    :postcondition: return a dictionary with default character attributes
    :return: a dictionary representing the new character

    >>> char = make_character("Hero")
    >>> char == {'X-coordinate': 0, 'Y-coordinate': 0, 'Current HP': 5, 'Experience': 0, 'Level': 1, 'Name': 'Hero'}
    True

    >>> char = make_character("Tushit")
    >>> char == {'X-coordinate': 0, 'Y-coordinate': 0, 'Current HP': 5, 'Experience': 0, 'Level': 1, 'Name': 'Tushit'}
    True
    """
    character = {"X-coordinate": 0, "Y-coordinate": 0, "Current HP": 5, "Experience": 0, "Level": 1, "Name": name}
    return character


def check_and_level_up(character, stdscr):
    """
    Check and level up the character if they have enough experience.

    This function levels up the character if their experience reaches or exceeds their level multiplied by 200. Any
    excess experience is deducted, and the character's HP is increased.

    :param character: a dictionary representing the character with "Experience", "Level", and "Current HP" keys
    :param stdscr: a curses window object for displaying messages
    :precondition: character must be a dictionary with "Experience", "Level", and "Current HP" keys
    :precondition: stdscr must be a valid curses window object
    :postcondition: level up the character and update their stats correctly if conditions are met
    """
    if character['Experience'] >= character['Level'] * 200:
        play_game_scene(stdscr, "New Achievement: You Just Levelled Up! \n Press Enter/Return to continue")
        character['Experience'] -= character['Level'] * 200
        character['Level'] += 1
        character['Current HP'] = 5 * character['Level']


def main():
    """
    Drive the program.
    """
    my_character = make_character("Tushit")
    print(my_character)
    move_character(my_character, (2, 3))
    print("After moving the character!")
    print(my_character)
    print("Is my character alive?", end=" ")
    print(is_alive(my_character))


if __name__ == "__main__":
    main()
