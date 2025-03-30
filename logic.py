import random


def check_for_foe(board, character):
    x_pos = character["X-coordinate"]
    y_pos = character["Y-coordinate"]
    if board[(y_pos, x_pos)] == "enemy":
        board[(y_pos, x_pos)] = "space"
        return True
    return False


def validate_move(board, character, direction):
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
    if character["X-coordinate"] == goal_position[1] and character["Y-coordinate"] == goal_position[0]:
        return True
    return False


def move_enemies(board, character):
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
    x_pos = character["X-coordinate"]
    y_pos = character["Y-coordinate"]
    if board[(y_pos, x_pos)] == "Boss":
        board[(y_pos, x_pos)] = "space"
        return True
    return False
