"""
Tushit Garg
A01418176

This module implements a 3x3 jigsaw puzzle game, allowing players to move and swap ASCII art pieces.
"""
import curses
import random
import itertools
from typing import List, Tuple, Dict, Optional

from ui import is_screen_size_ok


def init_colors() -> None:
    """
    Initialize color pairs for the jigsaw game.

    This function sets up color pairs for different elements in the jigsaw game.

    :precondition: curses must be initialized
    :postcondition: initialize colors for different elements of the game
    """
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)


def get_ascii_picture() -> List[List[str]]:
    """
    Get a list of ASCII arts used for the puzzle pieces.

    :return: a list of ASCII arts for the puzzle

    >>> len(get_ascii_picture())
    9
    """
    return [
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


def init_puzzle(rows: int, cols: int) -> List[List[Tuple[int, int]]]:
    """
    Initialize the jigsaw puzzle by creating a shuffled grid of pieces.

    :param rows: the number of rows in the puzzle
    :param cols: the number of columns in the puzzle
    :precondition: rows and cols must be positive integers
    :postcondition: generate a shuffled list of lists, each containing tuples of two integers less than rows and cols
    :return: a list of lists, each containing tuples of two integers
    """
    pieces = [(num, num) for num in range(rows * cols)]
    random.shuffle(pieces)
    grid = [pieces[row * cols:(row + 1) * cols] for row in range(rows)]
    return grid


def is_solved(grid: List[List[Tuple[int, int]]], rows: int, cols: int) -> bool:
    """
    Check if the puzzle is solved.

    This function checks if each piece is in its correct position, that is, the puzzle is solved.

    :param grid: a list representing the current state of the puzzle grid
    :param rows: the number of rows in the puzzle
    :param cols: the number of columns in the puzzle
    :precondition: grid must be a list of lists, each containing tuples of two integers representing the puzzle
    :postcondition: determine if the puzzle is solved
    :return: a boolean, True if the puzzle is solved, False otherwise

    >>> test_grid = [[(0, 0), (1, 1)], [(2, 2), (3, 3)]]
    >>> is_solved(test_grid, 2, 2)
    True

    >>> test_grid = [[(2, 2), (3, 3)], [(0, 0), (1, 1)]]
    >>> is_solved(test_grid, 2, 2)
    False
    """
    for row in range(rows):
        for col in range(cols):
            piece_idx, pos = grid[row][col]
            if pos != row * cols + col:
                return False
    return True


def is_piece_in_correct_position(grid: List[List[Tuple[int, int]]], row: int, col: int) -> bool:
    """
    Check if a piece is in its correct position.

    :param grid: a list representing the current state of the puzzle grid
    :param row: the row index of the piece
    :param col: the column index of the piece
    :precondition: grid must be a list of lists, each containing tuples of two integers representing the puzzle
    :postcondition: determine if the piece is in the correct position
    :return: a boolean, True if the piece is in the correct position, False otherwise

    >>> test_grid = [[(0, 0), (1, 1)], [(2, 2), (3, 3)]]
    >>> is_piece_in_correct_position(test_grid, 0, 0)
    True

    >>> test_grid = [[(1, 1), (0, 0)], [(2, 2), (3, 3)]]
    >>> is_piece_in_correct_position(test_grid, 0, 1)
    False
    """
    piece_idx, pos = grid[row][col]
    return pos == row * 3 + col


def get_cell_attribute(row: int, col: int, cursor: Tuple[int, int], selected: Optional[Tuple[int, int]],
                       colors: Dict[str, int], grid: List[List[Tuple[int, int]]]) -> int:
    """
    Determine the color attribute for a specific cell in the puzzle grid.

    :param row: the row index of the cell
    :param col: the column index of the cell
    :param cursor: a tuple representing the current cursor position
    :param selected: a tuple representing the currently selected piece or None if no selection
    :param colors: a dictionary mapping color names to curses color pair numbers
    :param grid: a list representing the current state of the puzzle grid
    :precondition: grid must be a list of lists, each containing tuples of two integers representing the puzzle
    :precondition: curses must be initialized
    :postcondition: find the correct color attribute for a specific cell
    :return: a curses color pair indicating the cell color
    """
    if (row, col) == cursor and (row, col) == selected:
        return curses.color_pair(colors["selected"]) | curses.A_BOLD
    elif (row, col) == cursor:
        return curses.color_pair(colors["cursor"])
    elif (row, col) == selected:
        return curses.color_pair(colors["selected"])
    elif is_piece_in_correct_position(grid, row, col):
        return curses.color_pair(colors["correct"])
    else:
        return curses.color_pair(colors["normal"])


def draw_piece(stdscr: curses.window, cell_y: int, cell_x: int, attr: int, ascii_picture: List[List[str]],
               piece_idx: int, piece_height: int) -> None:
    """
    Draw an ASCII puzzle piece at a given position on the screen.

    :param stdscr: a curses window object
    :param cell_y: the y-coordinate of the top-left corner of the piece
    :param cell_x: the x-coordinate of the top-left corner of the piece
    :param attr: the curses color attribute for the piece's display
    :param ascii_picture: a list containing ASCII art representations of puzzle pieces
    :param piece_idx: the index of the ASCII piece to draw
    :param piece_height: the height of the puzzle piece
    :precondition: stdscr must be a valid curses window object
    :precondition: piece_idx must be a valid index in ascii_picture
    :postcondition: draw the specified puzzle piece on the screen at the given coordinates
    """
    stdscr.addstr(cell_y, cell_x, "+-----+", attr)
    art_piece = ascii_picture[piece_idx]
    for i, line in enumerate(art_piece):
        if i < piece_height:
            stdscr.addstr(cell_y + i + 1, cell_x, f"|{line}|", attr)

    stdscr.addstr(cell_y + piece_height + 1, cell_x, "+-----+", attr)


def draw_grid(stdscr: curses.window, grid: List[List[Tuple[int, int]]], cursor: Tuple[int, int],
              selected: Optional[Tuple[int, int]], colors: Dict[str, int], ascii_picture: List[List[str]], rows: int,
              cols: int) -> None:
    """
    Draw the puzzle grid on the screen using curses.

    This function handles the display of the puzzle grid, pieces, cursor, and selected pieces.

    :param stdscr: a curses window object
    :param grid: a list representing the current state of the puzzle grid
    :param cursor: a tuple representing the current cursor position
    :param selected: a tuple representing the currently selected puzzle piece or None if nothing is selected
    :param colors: a dictionary with color descriptions as keys and cursor color pairs as value
    :param ascii_picture: a list of ASCII arts for the puzzle pieces
    :param rows: the number of rows in the puzzle
    :param cols: the number of columns in the puzzle
    :precondition: stdscr must be a valid curses window object
    :precondition: grid must be a list of lists, each containing tuples of two integers representing the puzzle
    :postcondition: draw the puzzle grid and update the screen
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    piece_height = 5
    piece_width = 5
    grid_height = rows * (piece_height + 1)
    grid_width = cols * (piece_width + 3)
    start_y = max((height - grid_height) // 2, 0)
    start_x = max((width - grid_width) // 2, 0)

    title = "SOLVE THE PUZZLE"
    stdscr.addstr(start_y - 2, start_x + (grid_width - len(title)) // 2, title,
                  curses.color_pair(colors["message"]) | curses.A_BOLD)

    for row, col in itertools.product(range(rows), range(cols)):
        piece_idx, pos = grid[row][col]
        cell_y = start_y + row * (piece_height + 1)
        cell_x = start_x + col * (piece_width + 3)
        attr = get_cell_attribute(row, col, cursor, selected, colors, grid)
        draw_piece(stdscr, cell_y, cell_x, attr, ascii_picture, piece_idx, piece_height)

    help_text = "WASD=Move | ENTER=Select/Swap"
    stdscr.addstr(start_y + grid_height + 2, start_x + (grid_width - len(help_text)) // 2, help_text)

    stdscr.refresh()


def setup_screen(stdscr: curses.window) -> None:
    """
    Configure the curses screen for the jigsaw game.

    This function sets up the screen by hiding the cursor, configuring input delays, enabling keypad support, and
    initializing colors if available.

    :param stdscr: a curses window object
    :precondition: stdscr must be a valid curses window object
    :postcondition: prepare the screen for game rendering and input
    """
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)
    if curses.has_colors():
        init_colors()


def move_cursor(key: int, cursor: Tuple[int, int]) -> Tuple[int, int]:
    """
    Update the cursor position based on the user input key.

    This function interprets movement keys ('w', 'a', 's', 'd') to adjust the cursor position, ensuring it stays within
    bounds.

    :param key: the key code received from stdscr.getch()
    :param cursor: a tuple (y, x) representing the current cursor position
    :precondition: key is a valid key code for movement
    :precondition: cursor is a tuple of two integers
    :postcondition: calculate the new cursor position after applying the key input
    :return: a tuple (new_y, new_x) representing the updated cursor position
    """
    cursor_y, cursor_x = cursor
    if key in (ord('w'), ord('W')) and cursor_y > 0:
        cursor_y -= 1
    elif key in (ord('s'), ord('S')) and cursor_y < 2:
        cursor_y += 1
    elif key in (ord('a'), ord('A')) and cursor_x > 0:
        cursor_x -= 1
    elif key in (ord('d'), ord('D')) and cursor_x < 2:
        cursor_x += 1
    return cursor_y, cursor_x


def start_jigsaw_game(stdscr: curses.window) -> None:
    """
    Start the jigsaw game.

    This function initializes the jigsaw mini-game, sets up the grid, and handles user input for moving and swapping
    pieces.

    :param stdscr: a curses window object
    :precondition: stdscr must be a valid curses window object
    :postcondition: run the jigsaw game
    :postcondition: exit only when the jigsaw is solved
    """
    rows, cols = 3, 3
    setup_screen(stdscr)
    colors = {
        "normal": 1,
        "selected": 2,
        "cursor": 3,
        "correct": 4,
        "message": 5
    }

    ascii_picture = get_ascii_picture()
    grid = init_puzzle(rows, cols)
    cursor = (0, 0)
    selected = None

    while True:
        draw_grid(stdscr, grid, cursor, selected, colors, ascii_picture, rows, cols)
        if is_solved(grid, rows, cols):
            break
        key = stdscr.getch()
        cursor = move_cursor(key, cursor)
        cursor_y, cursor_x = cursor
        if key in (curses.KEY_ENTER, 10, 13):
            if not selected:
                selected = (cursor_y, cursor_x)
            else:
                if selected == (cursor_y, cursor_x):
                    selected = None
                else:
                    selected_y, selected_x = selected
                    grid[selected_y][selected_x], grid[cursor_y][cursor_x] = grid[cursor_y][cursor_x], grid[selected_y][
                        selected_x]
                    selected = None
        cursor = (cursor_y, cursor_x)


def main(stdscr: curses.window) -> None:
    """
    Drive the program.
    """
    if not is_screen_size_ok(stdscr):
        stdscr.addstr(0, 0, "Please Increase your window size and try again")
        stdscr.addstr(2, 0, "Press any key to exit")
        stdscr.getkey()
        return
    start_jigsaw_game(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)