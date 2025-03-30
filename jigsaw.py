import math
import curses
import random


def init_puzzle(rows, cols):
    pieces = list(range(1, rows * cols + 1))
    random.shuffle(pieces)
    grid = [pieces[index * cols:(index + 1) * cols] for index in range(rows)]
    return grid


def draw_grid(stdscr, grid, cursor, selected, rows, cols):
    stdscr.clear()
    height, weight = stdscr.getmaxyx()
    grid_h = rows * 3
    grid_w = cols * 7
    start_y = max((height - grid_h) // 2, 0)
    start_x = max((weight - grid_w) // 2, 0)

    for row in range(rows):
        for col in range(cols):
            piece = grid[row][col]
            cell_y = start_y + row * 3
            cell_x = start_x + col * 7

            if (row, col) == cursor:
                attr = curses.A_REVERSE
            else:
                attr = curses.A_NORMAL

            if selected and (row, col) == selected:
                attr |= curses.A_UNDERLINE

            stdscr.addstr(cell_y, cell_x, "+-----+", attr)
            stdscr.addstr(cell_y + 1, cell_x, f"| {piece:2d}  |", attr)
            stdscr.addstr(cell_y + 2, cell_x, "+-----+", attr)
    message_text = "Use WASD to move, ENTER to select/swap, 'q' to quit."
    stdscr.addstr(start_y + grid_h + 1, start_x - math.floor(len(message_text) / 2), message_text)
    stdscr.refresh()


def is_solved(grid, rows, cols):
    count = 1
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != count:
                return False
            count += 1
    return True


def start_jigsaw_game(stdscr):
    rows, cols = 3, 3
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    grid = init_puzzle(rows, cols)
    cursor = (0, 0)
    selected = None

    while True:
        draw_grid(stdscr, grid, cursor, selected, rows, cols)
        if is_solved(grid, rows, cols):
            break

        key = stdscr.getch()

        if key in (ord('q'), ord('Q')):
            break
        y_cord, x_cord = cursor
        if key in (ord('w'), ord('W')) and y_cord > 0:
            y_cord -= 1
        elif key in (ord('s'), ord('S')) and y_cord < rows - 1:
            y_cord += 1
        elif key in (ord('a'), ord('A')) and x_cord > 0:
            x_cord -= 1
        elif key in (ord('d'), ord('D')) and x_cord < cols - 1:
            x_cord += 1
        elif key in (curses.KEY_ENTER, 10, 13):
            if not selected:
                selected = (y_cord, x_cord)
            else:
                if selected == (y_cord, x_cord):
                    selected = None
                else:
                    sy, sx = selected
                    grid[sy][sx], grid[y_cord][x_cord] = grid[y_cord][x_cord], grid[sy][sx]
                    selected = None
        cursor = (y_cord, x_cord)
