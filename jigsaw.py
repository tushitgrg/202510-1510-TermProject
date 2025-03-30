import curses
import random
import itertools


def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)


def get_ascii_picture():
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


def init_puzzle(rows, cols):
    pieces = [(num, num) for num in range(rows * cols)]
    random.shuffle(pieces)
    grid = [pieces[row * cols:(row + 1) * cols] for row in range(rows)]
    return grid


def is_solved(grid, rows, cols):
    for row in range(rows):
        for col in range(cols):
            piece_idx, pos = grid[row][col]
            if pos != row * cols + col:
                return False
    return True


def is_piece_in_correct_position(grid, row, col):
    piece_idx, pos = grid[row][col]
    return pos == row * 3 + col


def draw_grid(stdscr, grid, cursor, selected, colors, ascii_picture, rows, cols):
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
        if (row, col) == cursor and (row, col) == selected:
            attr = curses.color_pair(colors["selected"]) | curses.A_BOLD
        elif (row, col) == cursor:
            attr = curses.color_pair(colors["cursor"])
        elif (row, col) == selected:
            attr = curses.color_pair(colors["selected"])
        elif is_piece_in_correct_position(grid, row, col):
            attr = curses.color_pair(colors["correct"])
        else:
            attr = curses.color_pair(colors["normal"])

        stdscr.addstr(cell_y, cell_x, "+-----+", attr)

        art_piece = ascii_picture[piece_idx]
        for i, line in enumerate(art_piece):
            if i < piece_height:
                stdscr.addstr(cell_y + i + 1, cell_x, f"|{line}|", attr)

        stdscr.addstr(cell_y + piece_height + 1, cell_x, "+-----+", attr)

    help_text = "WASD=Move | ENTER=Select/Swap"
    stdscr.addstr(start_y + grid_height + 2, start_x + (grid_width - len(help_text)) // 2, help_text)

    stdscr.refresh()


def start_jigsaw_game(stdscr):
    rows, cols = 3, 3
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)
    if curses.has_colors():
        init_colors()
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
        cursor_y, cursor_x = cursor

        if key in (ord('w'), ord('W')) and cursor_y > 0:
            cursor_y -= 1
        elif key in (ord('s'), ord('S')) and cursor_y < 2:
            cursor_y += 1
        elif key in (ord('a'), ord('A')) and cursor_x > 0:
            cursor_x -= 1
        elif key in (ord('d'), ord('D')) and cursor_x < 2:
            cursor_x += 1
        elif key in (curses.KEY_ENTER, 10, 13):
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
