"""
Tushit Garg
A01418176

This module generates and manages a maze-based game board with random blocks like enemies and heals, using curses for
display. It handles maze creation, character stats rendering, and real-time map updates with sound effects.
"""
import random
import curses
from typing import Tuple, Dict, List, Union, Optional

import simpleaudio

from character import make_character
from ui import is_screen_size_ok


def add_random_block() -> str:
    """
    Generate a random block type for the maze.

    This function randomly selects one of three block types: 'enemy', 'heal', or 'space'. The probability of selecting
    enemy and heal is 1/20.

    :return: a string representing the type of block ('enemy', 'heal', or 'space')
    """
    random_number = random.randint(1, 20)
    if random_number == 20:
        return "enemy"
    elif random_number == 10:
        return "heal"
    return "space"


def generate_maze(start_x: int, start_y: int, board: Dict[Tuple[int, int], str], rows: int, cols: int,
                  goal_position: List[int], boss: bool) -> None:
    """
    Carve out paths in the board in the form of a maze.

    This function carves out paths in the board and places random blocks. If the boss parameter is True, it avoids
    placing random blocks.

    :param start_x: an integer representing the starting x-coordinate of the maze generation
    :param start_y: an integer representing the starting y-coordinate of the maze generation
    :param board: a dictionary representing game board, where keys are (y, x) coordinates and values are entity types
    :param rows: an integer representing the total number of rows in the maze
    :param cols: an integer representing the total number of columns in the maze
    :param goal_position: a list storing the goal's coordinates
    :param boss: a boolean indicating if the boss level is being generated
    :precondition: board dictionary must be initialized with 'wall' values
    :postcondition: modify board dictionary to a game maze that contains paths and obstacles in random places
    """
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        result_x = start_x + dx
        result_y = start_y + dy
        if 0 <= result_x < cols and 0 <= result_y < rows and board[(result_y, result_x)] == "wall":
            board[(start_y + dy // 2, start_x + dx // 2)] = add_random_block() if not boss else "space"
            board[(result_y, result_x)] = add_random_block() if not boss else "space"
            goal_position[0] = result_y
            goal_position[1] = result_x
            generate_maze(result_x, result_y, board, rows, cols, goal_position, boss)


def make_board(rows: int, columns: int, character: Dict[str, Union[int, str]], boss: bool = False) -> Tuple[
    Dict[Tuple[int, int], str], Optional[Tuple[int, int]]]:
    """
    Create a maze board and generate its structure.

    This function initializes the game board dictionary with walls and carves out a maze structure.

    :param rows: an integer representing the total number of rows in the maze
    :param columns: an integer representing the total number of columns in the maze
    :param character: a dictionary representing the character with keys "X-coordinate" and "Y-coordinate"
    :param boss: a boolean indicating if this is a boss-level maze
    :precondition: rows and columns must be greater than 1
    :precondition: the character must have valid "X-coordinate" and "Y-coordinate" keys with integer values
    :postcondition: generate a game board dictionary that contains paths, obstacles in random places
    :return: a tuple (maze dictionary, goal_position) if not boss, otherwise (maze dictionary, None)
    """
    board = {(row, column): "wall" for row in range(0, rows + 1) for column in range(0, columns + 1)}
    board[(0, 0)] = "space"
    goal_position = [0, 0]
    character["Y-coordinate"], character["X-coordinate"] = 0, 0
    generate_maze(0, 0, board, rows, columns, goal_position, boss)
    board[(goal_position[0], goal_position[1])] = "Goal" if not boss else "Boss"
    if not boss:
        return board, (goal_position[0], goal_position[1])
    else:
        return board, None


def draw_character_info(stats_win, start_point: int, character: Dict[str, Union[str, int]]) -> None:
    """
    Display the character's basic information such as name, level, rank, and experience.

    :param stats_win: a curses window object for stats display
    :param start_point: an integer representing the starting line number for character info
    :param character: a dictionary containing keys 'Name', 'Level', and 'Experience'
    :precondition: character and rank_names are correctly formatted dictionaries
    :postcondition: render the character information in the stats window
    """
    rank_names = {
        1: "Novice Inquisitor",
        2: "Sanctified Purifier",
        3: "Grand Arbiter of Fire",
        4: "The Hand of Divine Wrath"
    }
    stats_win.addstr(start_point + 2, 1, f"Name: {character['Name']}", curses.color_pair(4))
    stats_win.addstr(start_point + 3, 1, f"Level: {character['Level']}", curses.color_pair(3))
    stats_win.addstr(start_point + 4, 1, f"Rank: {rank_names[character['Level']]}", curses.color_pair(2))
    stats_win.addstr(start_point + 5, 1, f"Experience: {character['Experience']}/{character['Level'] * 200}",
                     curses.color_pair(1))


def draw_health_bar(stats_win, start_point: int, character: Dict[str, int]) -> None:
    """
    Display the character's health bar on the stats window.

    :param stats_win: a curses window object for stats display
    :param start_point: an integer representing the starting line number for the health bar
    :param character: a dictionary containing 'Current HP' and 'Level' keys
    :precondition: character has valid health data, and stats_win is properly initialized
    :postcondition: render the health bar on the stats window
    """
    stats_win.addstr(start_point + 6, 1, "HP: [", curses.color_pair(4))
    max_hp = character['Level'] * 5
    for index in range(max_hp):
        if index < character["Current HP"]:
            stats_win.addch(start_point + 6, 6 + index, '♥', curses.color_pair(5))
        else:
            stats_win.addch(start_point + 6, 6 + index, '.', curses.color_pair(1))
    stats_win.addstr(start_point + 6, 6 + max_hp,
                     f"] ({character['Current HP']}/{max_hp})", curses.color_pair(4))


def print_game_stats(stdscr: curses.window, character: Dict[str, Union[str, int]],
                     ascii_chars: Dict[str, Dict[str, Union[str, int]]]) -> None:
    """
    Display the game statistics and title art on the screen.

    This function renders the character's stats and game title art in a curses sub-window. This includes the player's
    name, level, rank, experience, and health status, along with controls and key mappings.

    :param stdscr: the main curses screen window object
    :param character: a dictionary containing character information such as 'Name', 'Level', 'Experience', 'Current HP'
    :param ascii_chars: a dictionary mapping game elements to their ASCII representation and curses attributes
    :precondition: stdscr must be a valid curses window object
    :precondition: character and ascii_chars must be properly formatted dictionaries
    :postcondition: create the stats window with the current game and character statistics
    """
    max_y, max_x = stdscr.getmaxyx()

    stats_win = stdscr.subwin(max_y - 3, int(max_x / 2) - 3, 0, 0)

    stats_win.box()
    game_name_art = """
    
    ██╗███╗░░██╗███████╗███████╗██████╗░███╗░░██╗░█████╗░
    ██║████╗░██║██╔════╝██╔════╝██╔══██╗████╗░██║██╔══██╗
    ██║██╔██╗██║█████╗░░█████╗░░██████╔╝██╔██╗██║██║░░██║
    ██║██║╚████║██╔══╝░░██╔══╝░░██╔══██╗██║╚████║██║░░██║
    ██║██║░╚███║██║░░░░░███████╗██║░░██║██║░╚███║╚█████╔╝
    ╚═╝╚═╝░░╚══╝╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝░╚════╝░
    
    ████████╗██████╗░██╗░█████╗░██╗░░░░░░██████╗
    ╚══██╔══╝██╔══██╗██║██╔══██╗██║░░░░░██╔════╝
    ░░░██║░░░██████╔╝██║███████║██║░░░░░╚█████╗░
    ░░░██║░░░██╔══██╗██║██╔══██║██║░░░░░░╚═══██╗
    ░░░██║░░░██║░░██║██║██║░░██║███████╗██████╔╝
    ░░░╚═╝░░░╚═╝░░╚═╝╚═╝╚═╝░░╚═╝╚══════╝╚═════╝░
"""

    stats_win.addstr(0, 3, " Character Stats ", curses.A_BOLD | curses.color_pair(4))
    lines = game_name_art.split('\n')
    for index, line in enumerate(lines):
        stats_win.addstr(index, 10, line)
    start_point = 2 + len(lines)
    draw_character_info(stats_win, start_point, character)
    draw_health_bar(stats_win, start_point, character)
    stats_win.addstr(start_point + 8, 1, "Controls:", curses.color_pair(4))
    stats_win.addstr(start_point + 9, 1, "W/A/S/D: Move", curses.color_pair(4))
    stats_win.addstr(start_point + 10, 1, "Q: Quit", curses.color_pair(4))

    for index, (key, value) in enumerate(ascii_chars.items()):
        if key != "space":
            stats_win.addstr(start_point + 11 + index, 1, f"{value['char']} - {key if key != 'Goal' else 'Portal'}",
                             value['attr'])


def initialise_colors_for_map() -> None:
    """
    Initialize color pairs for the main game.

    This function sets up color pairs for different elements in the main game.

    :precondition: curses must be initialized
    :postcondition: initialize colors for different elements of the game
    """
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)


def describe_current_location(stdscr: curses.window, board: Dict[Tuple[int, int], str],
                              character: Dict[str, Union[int, str]]) -> None:
    """
    Render the current dungeon map and update character status.

    This function clears and refreshes the main screen window with the current state of the dungeon map, including the
    character's position, obstacles, and items.

    :param stdscr: the main curses screen window object
    :param board: a dictionary representing game board, where keys are (y, x) coordinates and values are entity types
    :param character: a dictionary containing the character's current position and stats
    :precondition: stdscr must be a valid curses window object
    :precondition: board must be a dictionary with valid maze data
    :precondition: character must include 'Y-coordinate' and 'X-coordinate' keys
    :postcondition: update the screen with the ascii map of current maze state
    :postcondition: refresh the stats window with the latest character's stats
    """
    stdscr.clear()
    initialise_colors_for_map()

    ascii_chars = {
        "space": {"char": " ", "attr": curses.color_pair(1) | curses.A_BOLD},
        "character": {"char": "@", "attr": curses.color_pair(4) | curses.A_BOLD},
        "Goal": {"char": "🏰", "attr": curses.color_pair(3) | curses.A_BOLD},
        "wall": {"char": "█", "attr": curses.color_pair(2) | curses.A_BOLD},
        "enemy": {"char": "Ψ", "attr": curses.color_pair(1) | curses.A_BOLD},
        "heal": {"char": "ɸ", "attr": curses.color_pair(5) | curses.A_BOLD},
        "Boss": {"char": "Ж", "attr": curses.color_pair(1) | curses.A_BOLD}
    }

    board_copy = board.copy()
    board_copy[(character["Y-coordinate"], character["X-coordinate"])] = 'character'

    max_y, max_x = stdscr.getmaxyx()
    map_win = stdscr.subwin(max_y - 3, int(max_x / 2) - 3, 0, int(max_x / 2) - 1)
    map_win.box()
    map_win.addstr(0, 3, " Dungeon Map ", curses.A_BOLD)

    for (row, column), description in sorted(board_copy.items()):
        details = ascii_chars.get(description, {"char": "?", "attr": curses.color_pair(4)})
        map_win.addstr(row + 1, 1 + column * 2, details['char'], details['attr'])

    print_game_stats(stdscr, character, ascii_chars)

    heal_obj = simpleaudio.WaveObject.from_wave_file("sounds/heal_effect.wav")
    if board[(character["Y-coordinate"], character["X-coordinate"])] == "heal":
        if character["Current HP"] + 1 <= character['Level'] * 5:
            heal_obj.play()
            character["Current HP"] += 1
            board[(character["Y-coordinate"], character["X-coordinate"])] = "space"

    stdscr.refresh()


def main(stdscr: curses.window) -> None:
    """
    Drive the program.
    """
    if not is_screen_size_ok(stdscr):
        stdscr.addstr(0, 0, "Please Increase your window size and try again")
        stdscr.addstr(2, 0, "Press any key to exit")
        stdscr.getkey()
        return
    my_character = make_character('Tushit')
    my_board, goal_pos = make_board(36, 36, my_character)
    describe_current_location(stdscr, my_board, my_character)
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
