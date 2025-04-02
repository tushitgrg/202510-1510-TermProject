import random


def check_for_foe(board, character):
    """
    Check if the character is on an enemy's position.

    This function checks if the character's current position matches an enemy's position on the game board. If an
    enemy is present, it removes the enemy from the board and returns True. Otherwise, it returns False.

    :param board: a dictionary representing game board, where keys are (y, x) coordinates and values are entity types
    :param character: a dictionary representing the character with keys "X-coordinate" and "Y-coordinate"
    :precondition: the character must have valid "X-coordinate" and "Y-coordinate" keys with integer values
    :postcondition: determine if the character's current position matches an enemy's position
    :postcondition: replace the enemy, if present, with a space
    :return: a boolean, True If an enemy is present, False otherwise

    >>> board_test = {(0, 0): "space", (0, 1): "space", (1, 0): "enemy", (1, 1): "space"}
    >>> character_test = {"X-coordinate": 0, "Y-coordinate": 1}
    >>> check_for_foe(board_test, character_test)
    True

    >>> board_test = {(0, 0): "space", (0, 1): "space", (1, 0): "enemy", (1, 1): "space"}
    >>> character_test = {"X-coordinate": 1, "Y-coordinate": 1}
    >>> check_for_foe(board_test, character_test)
    False
    """
    x_pos = character["X-coordinate"]
    y_pos = character["Y-coordinate"]
    if board[(y_pos, x_pos)] == "enemy":
        board[(y_pos, x_pos)] = "space"
        return True
    return False


def validate_move(board, character, direction):
    """
    Validate a move in the game based on the input direction

    This function checks whether the character's specified direction is valid to move. It verifies that the
    destination place on the board is an eligible space (either "Empty Space" or "Goal").

    :param board: a dictionary representing game board, where keys are (y, x) coordinates and values are entity types
    :param character: a dictionary representing the character with keys "X-coordinate" and "Y-coordinate"
    :param direction: a string representing the move direction which are "w", "a", "s", "d"
    :precondition: board and character are in the correct format
    :precondition: direction is one of "w", "a", "s", or "d"
    :postcondition: determine if the intended move is valid or not
    :postcondition: calculate the new position of the character, correctly
    :postcondition: board and character are unmodified
    :return: a tuple (bool, tuple) where the boolean indicates if the move is valid, and the tuple is the new position

    >>> board_test = {(0, 0): "space", (0, 1): "space", (1, 0): "space", (1, 1): "space"}
    >>> character_test = {"X-coordinate": 0, "Y-coordinate": 0}
    >>> validate_move(board_test, character_test, "d")
    (True, (0, 1))

    >>> board_test = {(0, 0): "space", (0, 1): "space", (1, 0): "wall", (1, 1): "space"}
    >>> character_test = {"X-coordinate": 1, "Y-coordinate": 1}
    >>> validate_move(board_test, character_test, "a")
    (False, (1, 0))

    >>> board_test = {(0, 0): "space", (0, 1): "space", (1, 0): "space", (1, 1): "space"}
    >>> character_test = {"X-coordinate": 1, "Y-coordinate": 1}
    >>> validate_move(board_test, character_test, "s")
    (False, None)
    """
    x_pos = character["X-coordinate"]
    y_pos = character["Y-coordinate"]
    eligible_places = ["space", "Goal", "enemy", "heal", "Boss"]
    new_pos = None
    if direction == "w":
        new_pos = (y_pos - 1, x_pos)
    elif direction == "s":
        new_pos = (y_pos + 1, x_pos)
    elif direction == "a":
        new_pos = (y_pos, x_pos - 1)
    elif direction == "d":
        new_pos = (y_pos, x_pos + 1)
    if new_pos in board:
        return board[new_pos] in eligible_places, new_pos
    return False, None


def check_if_goal_attained(goal_position, character):
    """
    Check if the character has reached the goal.

    This function compares the character's current position with the goal's position to determine if the goal has been
    attained.

    :param goal_position: a tuple representing the goal's (y, x) coordinates
    :param character: a dictionary representing the character with keys "X-coordinate" and "Y-coordinate"
    :precondition: the character must have valid "X-coordinate" and "Y-coordinate" keys with integer values
    :postcondition: determine if the character is at the goal position
    :postcondition: character is unmodified
    :return: a boolean, True if the character has reached the goal, otherwise False

    >>> check_if_goal_attained((1, 1), {"X-coordinate": 1, "Y-coordinate": 0})
    False

    >>> check_if_goal_attained((1, 0), {"X-coordinate": 0, "Y-coordinate": 1})
    True
    """
    if character["X-coordinate"] == goal_position[1] and character["Y-coordinate"] == goal_position[0]:
        return True
    return False


def move_enemies(board, character):
    """
    Move enemies randomly on the board.

    This function moves each enemy randomly to an adjacent "space" on the board, ensuring they do not move onto the
    character's position.

    :param board: a dictionary representing game board, where keys are (y, x) coordinates and values are entity types
    :param character: a dictionary representing the character with keys "X-coordinate" and "Y-coordinate"
    :precondition: board and character are in the correct format
    :postcondition: move enemies to an adjacent empty space, ensuring no overlap with the character
    """
    enemy_positions = sorted((pos for pos, desc in board.items() if desc == "enemy"))

    for row, column in enemy_positions:
        directions = [("row", -1), ("row", 1), ("column", -1), ("column", 1)]
        random.shuffle(directions)

        character_pos = (character["Y-coordinate"], character["X-coordinate"])

        for axis, diff in directions:
            new_row, new_col = row + (diff if axis == "row" else 0), column + (diff if axis == "column" else 0)

            if (new_row, new_col) == character_pos:
                break

            if (new_row, new_col) in board and board[(new_row, new_col)] == "space":
                board[(row, column)], board[(new_row, new_col)] = board[(new_row, new_col)], board[(row, column)]
                break


def check_for_boss(board, character):
    """
    Check if the character is on a boss's position.

    This function checks if the character's current position matches a boss's position on the game board. If a boss is
    present, it removes the boss from the board and returns True. Otherwise, it returns False.

    :param board: a dictionary representing game board, where keys are (y, x) coordinates and values are entity types
    :param character: a dictionary representing the character with keys "X-coordinate" and "Y-coordinate"
    :precondition: the character must have valid "X-coordinate" and "Y-coordinate" keys with integer values
    :postcondition: determine if the character's current position matches a boss's position
    :postcondition: replace the boss, if present, with a space
    :return: a boolean, True If a boss is present, False otherwise

    >>> board_test = {(0, 0): "space", (0, 1): "space", (1, 0): "Boss", (1, 1): "space"}
    >>> character_test = {"X-coordinate": 0, "Y-coordinate": 1}
    >>> check_for_boss(board_test, character_test)
    True

    >>> board_test = {(0, 0): "space", (0, 1): "space", (1, 0): "Boss", (1, 1): "space"}
    >>> character_test = {"X-coordinate": 1, "Y-coordinate": 1}
    >>> check_for_boss(board_test, character_test)
    False
    """
    x_pos = character["X-coordinate"]
    y_pos = character["Y-coordinate"]
    if board[(y_pos, x_pos)] == "Boss":
        board[(y_pos, x_pos)] = "space"
        return True
    return False
