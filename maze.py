import random
import curses
import simpleaudio


def add_random_block():
    random_number = random.randint(1, 20)
    if random_number == 20:
        return "enemy"
    elif random_number == 10:
        return "heal"
    return "space"


def generate_maze(start_x, start_y, board, rows, cols, goal_position, boss):
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


def make_board(rows, columns, character, boss=False):
    board = {(row, column): "wall" for row in range(0, rows + 1) for column in range(0, columns + 1)}
    board[(0, 0)] = "space"
    goal_position = [0, 0]
    character["Y-coordinate"], character["X-coordinate"] = 0, 0
    generate_maze(0, 0, board, rows, columns, goal_position, boss)
    board[(goal_position[0], goal_position[1])] = "Goal" if not boss else "Boss"
    if not boss:
        return board, goal_position
    else:
        return board, None


def print_game_stats(stdscr, character, ascii_chars):
    max_y, max_x = stdscr.getmaxyx()
    rank_names = {
        1: "Novice Inquisitor",
        2: "Sanctified Purifier",
        3: "Grand Arbiter of Fire",
        4: "The Hand of Divine Wrath"
    }
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
    stats_win.addstr(start_point + 2, 1, f"Name: {character['Name']}", curses.color_pair(4))
    stats_win.addstr(start_point + 3, 1, f"Level: {character['Level']}", curses.color_pair(3))
    stats_win.addstr(start_point + 4, 1, f"Rank: {rank_names[character['Level']]}", curses.color_pair(2))
    stats_win.addstr(start_point + 5, 1, f"Experience: {character['Experience']}/{character['Level'] * 200}",
                     curses.color_pair(1))

    stats_win.addstr(start_point + 6, 1, "HP: [", curses.color_pair(4))
    for index in range(character['Level'] * 5):
        if index < character["Current HP"]:
            stats_win.addch(start_point + 6, 6 + index, '♥', curses.color_pair(5))
        else:
            stats_win.addch(start_point + 6, 6 + index, '.', curses.color_pair(1))

    stats_win.addstr(start_point + 6, 6 + character['Level'] * 5,
                     f"] ({character['Current HP']}/{character['Level'] * 5})",
                     curses.color_pair(4))

    stats_win.addstr(start_point + 8, 1, "Controls:", curses.color_pair(4))
    stats_win.addstr(start_point + 9, 1, "W/A/S/D: Move", curses.color_pair(4))
    stats_win.addstr(start_point + 10, 1, "Q: Quit", curses.color_pair(4))

    for index, (key, value) in enumerate(ascii_chars.items()):
        if key != "space":
            stats_win.addstr(start_point + 11 + index, 1, f"{value['char']} - {key if key!='Goal' else 'Portal'}", value['attr'])


def describe_current_location(stdscr, board, character):
    stdscr.clear()

    if not hasattr(describe_current_location, "colors_initialized"):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
        describe_current_location.colors_initialized = True

    ascii_chars = {
        "space": {"char": " ", "attr": curses.color_pair(1) | curses.A_BOLD},
        "character": {"char": "@", "attr": curses.color_pair(4) | curses.A_BOLD},
        "Goal": {"char": "༒", "attr": curses.color_pair(2) | curses.A_BOLD},
        "wall": {"char": "█", "attr": curses.color_pair(3) | curses.A_BOLD},
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
