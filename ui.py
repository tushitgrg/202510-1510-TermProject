import time

import curses
import pyfiglet


def get_user_battle_decision(stdscr):
    """
    Prompt the user to make a battle decision in the game.

    This function displays a message about the consequences of burning or fleeing from a witch. It accepts user input
    until a valid decision ('burn' or 'flee') is entered.

    :param stdscr: the main curses screen window object
    :precondition: stdscr must be a valid curses window object
    :postcondition: prompt the user for their decision
    :postcondition: exit only when a valid input is given
    """
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    message = """
   The villagers warned you—witches walk among us. Some bring ruin, some bring fortune. 
   But no one truly knows which until it’s too late.

 Burn Her (Type “Burn”) – If she is evil, the land is safe. If she is good... you are cursed.
 Let Her Flee (Type “Flee”) – If she is good, fortune follows. If she is evil... you are cursed.
    """
    lines = message.strip().split('\n')
    start_y = max(0, (max_y - len(lines)) // 2)

    for index, line in enumerate(lines):
        if start_y + index < max_y:
            start_x = max(0, (max_x - len(line)) // 2)
            stdscr.addstr(start_y + index, start_x, line[:max_x - 1])

    stdscr.refresh()
    curses.echo()
    input_decision = ""
    while not input_decision.strip().lower() in ["burn", "flee"]:
        stdscr.move(max_y - 2, 0)
        stdscr.clrtoeol()
        stdscr.refresh()
        input_decision = stdscr.getstr(max_y - 2, 0).decode("utf-8")
    return input_decision.strip().lower()


def welcome_user_and_ask_for_name(stdscr):
    welcome_message = pyfiglet.figlet_format("Welcome \n To \n Inferno \n Trials")
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    stdscr.clear()

    max_y, max_x = stdscr.getmaxyx()

    lines = welcome_message.strip().split('\n')
    start_y = max(0, (max_y - len(lines)) // 2)
    for counter_x, line in enumerate(lines):
        start_x = max(0, (max_x - len(line)) // 2)

        for counter_j in range(len(line) + 1):
            stdscr.clear()
            for counter_z, prev_line in enumerate(lines[:counter_x]):
                prev_start_x = max(0, (max_x - len(prev_line)) // 2)
                stdscr.addstr(start_y + counter_z, prev_start_x, prev_line, curses.color_pair(3))

            stdscr.addstr(start_y + counter_x, start_x, line[:counter_j], curses.color_pair(3))

            stdscr.refresh()
            time.sleep(0.007)

    stdscr.refresh()
    return get_user_name(stdscr)


def is_screen_size_ok(stdscr):
    max_y, max_x = stdscr.getmaxyx()
    if max_y < 46 or max_x < 135:
        return False
    return True


def get_user_choice(stdscr, prompt_y):
    input_direction = ""
    while not input_direction:
        stdscr.refresh()
        key = stdscr.getkey().lower()
        if key in ['w', 'a', 's', 'd']:
            input_direction = key
        elif key == 'q':
            return None
        else:
            stdscr.addstr(prompt_y, 2, "Invalid Move!! ")
            stdscr.refresh()
    return input_direction


def get_user_name(stdscr):
    max_y, max_x = stdscr.getmaxyx()
    stdscr.addstr(max_y - 3, 0, "Enter your name and continue using the return key!")

    curses.echo()
    input_name = ""
    while not input_name.strip():
        input_name = stdscr.getstr(max_y - 2, 0).decode("utf-8")
    return input_name
