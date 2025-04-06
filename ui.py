"""
Tushit Garg
A01418176

This module manages user interactions, handling battle decisions, name input with animated welcome, screen size
validation, and movement choices.
"""
import time

import curses
from typing import Optional

import pyfiglet


def get_user_battle_decision(stdscr: curses.window) -> str:
    """
    Prompt the user to make a battle decision in the game.

    This function displays a message about the consequences of burning or fleeing from a witch. It accepts user input
    until a valid decision ('burn' or 'flee') is entered.

    :param stdscr: the main curses screen window object
    :precondition: stdscr must be a valid curses window object
    :postcondition: prompt the user for their decision
    :postcondition: exit only when a valid input is given
    :return: a string, representing the user decision ('burn' or 'flee')
    """
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    witch_art = pyfiglet.figlet_format("WITCHES AMONG US!")
    message = f"""
    {witch_art}
    The villagers warned you—witches walk among us. Some bring ruin, some bring fortune.
    But no one truly knows which... until it’s too late.

    Burn Her  (Type "Burn") – If she is evil, the land is safe. But if she is good... you bear a dreadful curse.
    Let Her Flee (Type "Flee") – If she is good, fortune will follow. But if she is evil.. her darkness grows unchecked.

    Choose wisely, for the fate of many rests in your hands...
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


def welcome_user_and_ask_for_name(stdscr: curses.window) -> str:
    """
    Prompt the user for their name.

    This function displays a welcome message with an animated text effect and prompts the user for their name.

    :param stdscr: the main curses screen window object
    :precondition: stdscr must be a valid curses window object
    :postcondition: print the welcome message
    :return: a string, representing the name
    """
    welcome_art = pyfiglet.figlet_format("Welcome To \n Inferno Trials")
    welcome_message = f"""         
                               .=======-         
                             =++-.               
                           **+-                  
                         :#*+*                   
                        :**+=+-                  
                       -*+===++                  
                      :+=====++                  
                     .=+++*=+===                 
                     =====+++**+.                
                    -===+++++***:                
                    ===++==**+=+.                
                   -*=+=++*++++*-                
                   =##*=+++=+====                
                  :+***%***==+===                
     :****++++=======+++++*****+*+-              
 :*++++********--==++++*#*+++***#*++=++*+.       
+++++=====++++*+=++=++*%%##**++++**++++++++*:    
:*++++++======-::.                :-+##*+++++*-  
                                          -##++# 
                                               ++
    
    {welcome_art}
    """

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
            time.sleep(0.001)

    stdscr.refresh()
    return get_user_name(stdscr)


def is_screen_size_ok(stdscr: curses.window) -> bool:
    """
    Check if the terminal screen size meets the required dimensions.

    :param stdscr: the main curses screen window object
    :precondition: stdscr must be a valid curses window object
    :return: a boolean, True if the screen size is sufficient, False otherwise
    """
    max_y, max_x = stdscr.getmaxyx()
    if max_y < 53 or max_x < 163:
        return False
    return True


def get_user_choice(stdscr: curses.window, prompt_y: int) -> Optional[str]:
    """
    Get the user's movement choice from the keyboard.

    This function listens for valid keys: 'w', 'a', 's', 'd' for movement, 'q' to quit. If an invalid key is pressed,
    an error message is displayed.

    :param stdscr: the main curses screen window object
    :param prompt_y: the Y-coordinate to display invalid input messages
    :precondition: stdscr must be a valid curses window object
    :postcondition: listen for valid keystrokes
    :postcondition: display an error message if an invalid key is pressed
    :return: the movement direction as a string ('w', 'a', 's', 'd') or None if 'q' is pressed
    """
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


def get_user_name(stdscr: curses.window) -> str:
    """
    Prompt the user to enter their name.

    :param stdscr: the main curses screen window object
    :precondition: stdscr must be a valid curses window object
    :postcondition: ask the user for their name
    :return: a string, representing the name
    """
    max_y, max_x = stdscr.getmaxyx()
    stdscr.addstr(max_y - 3, 0, "Enter your name and continue using the return key!")

    curses.echo()
    input_name = ""
    while not input_name.strip():
        input_name = stdscr.getstr(max_y - 2, 0).decode("utf-8")
    return input_name


def main(stdscr: curses.window) -> None:
    """
    Drive the program.
    """
    if not is_screen_size_ok(stdscr):
        stdscr.addstr(0, 0, "Please Increase your window size and try again")
        stdscr.addstr(2, 0, "Press any key to exit")
        stdscr.getkey()
        return
    input_name = welcome_user_and_ask_for_name(stdscr)
    stdscr.clear()
    stdscr.addstr(f"User chose {input_name} as the name")
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
