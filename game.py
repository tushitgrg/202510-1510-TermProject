"""
Tushit Garg
A01418176
"""
import random
import curses


def display_text(stdscr, text, y, x):
    stdscr.addstr(y, x, text)
    stdscr.refresh()


def generate_maze(start_x, start_y, board, rows, cols, goal_position):
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        result_x = start_x + dx
        result_y = start_y + dy
        if 0 <= result_x < cols and 0 <= result_y < rows and board[(result_y, result_x)] == "wall":
            board[(start_y + dy // 2, start_x + dx // 2)] = "space"
            board[(result_y, result_x)] = "space"
            goal_position[0] = result_y
            goal_position[1] = result_x
            generate_maze(result_x, result_y, board, rows, cols, goal_position)


def make_board(rows, columns, character):
    board = {(row, column): "wall" for row in range(0, rows + 1) for column in range(0, columns + 1)}
    board[(0, 0)] = "space"
    goal_position = [0, 0]
    character["Y-coordinate"], character["X-coordinate"] = 0, 0
    generate_maze(0, 0, board, rows, columns, goal_position)
    board[(goal_position[0], goal_position[1])] = "Goal"
    return board, goal_position


def describe_current_location(stdscr, board, character):
    stdscr.clear()

    if not hasattr(describe_current_location, "colors_initialized"):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        describe_current_location.colors_initialized = True

    ascii_chars = {
        "space": {
            "char": " ",
            "attr": curses.color_pair(1) | curses.A_BOLD
        },
        "character": {
            "char": "@",
            "attr": curses.color_pair(1) | curses.A_BOLD
        },
        "Goal": {
            "char": "$",
            "attr": curses.color_pair(2) | curses.A_BOLD
        },
        "wall": {
            "char": "#",
            "attr": curses.color_pair(3) | curses.A_BOLD
        },
    }

    board_copy = board.copy()
    board_copy[(character["Y-coordinate"], character["X-coordinate"])] = 'character'

    current_row = -1
    max_y, max_x = stdscr.getmaxyx()

    for (row, column), description in sorted(board_copy.items()):
        if row != current_row:
            current_row = row
            y_pos = row + 1
            if y_pos < max_y - 3:
                stdscr.addstr(y_pos, 0, "")

        details = ascii_chars.get(description, {"char": "?", "attr": curses.color_pair(4)})
        if row < max_y - 3 and column * 2 < max_x - 1:
            stdscr.addstr(row + 1, column * 2, details['char'], details['attr'])

    location_y = current_row + 3
    if location_y < max_y - 2:
        stdscr.addstr(location_y, 0, f"This is a {board[(character['Y-coordinate'], character['X-coordinate'])]}",
                      curses.color_pair(4))

    health_string = "♥" * character["Current HP"] + "." * (5 - character["Current HP"])
    if location_y + 1 < max_y - 1:
        stdscr.addstr(location_y + 1, 0, f"Current HP: [{health_string}] ({character['Current HP']}/5)",
                      curses.color_pair(4))

    if max_y - 1 < max_y:
        stdscr.addstr(max_y - 1, 0, "Use W/A/S/D to move, Q to quit", curses.color_pair(4) | curses.A_BOLD)

    stdscr.refresh()


def make_character():
    character = {"X-coordinate": 0, "Y-coordinate": 0, "Current HP": 5}
    return character


def validate_move(board, character, direction):
    x_pos = character["X-coordinate"]
    y_pos = character["Y-coordinate"]
    eligible_places = ["space", "Goal"]
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


def move_character(character, new_pos):
    character["Y-coordinate"], character["X-coordinate"] = new_pos


def get_user_choice(stdscr, prompt_y):
    input_direction = ""
    while not input_direction:
        stdscr.addstr(prompt_y, 0, "Please Type W/A/S/D to Move ")
        stdscr.refresh()
        key = stdscr.getkey().lower()
        if key in ['w', 'a', 's', 'd']:
            input_direction = key
        else:
            stdscr.addstr(prompt_y + 1, 0, "Invalid Move!!  ")
            stdscr.refresh()
    return input_direction


def check_for_foes():
    """
    Determine if a foe is encountered.

    This function randomly decided whether if the character encounters a foe. There is only 25% chance of encountering
    a foe.

    :return: True if a foe is encountered, otherwise False
    """
    return False


def check_if_goal_attained(goal_position, character):
    if character["X-coordinate"] == goal_position[1] and character["Y-coordinate"] == goal_position[0]:
        return True
    return False


def guessing_game(stdscr, character):
    monster_art = r"""
                                ,-.                               
       ___,---.__          /'|`\          __,---,___          
    ,-'    \`    `-.____,-'  |  `-.____,-'    //    `-.       
  ,'        |           ~'\     /`~           |        `.      
 /      ___//              `. ,'          ,  , \___      \    
|    ,-'   `-.__   _         |        ,    __,-'   `-.    |    
|   /          /\_  `   .    |    ,      _/\          \   |   
\  |           \ \`-.___ \   |   / ___,-'/ /           |  /  
 \  \           | `._   `\\  |  //'   _,' |           /  /      
  `-.\         /'  _ `---'' , . ``---' _  `\         /,-'     
     ``       /     \    ,='/ \`=.    /     \       ''          
             |__   /|\_,--.,-.--,--._/|\   __|                  
             /  `./  \\`\ |  |  | /,//' \,'  \                  
            /   /     ||--+--|--+-/-|     \   \                 
           |   |     /'\_\_\ | /_/_/`\     |   |                
            \   \__, \_     `~'     _/ .__/   /            
             `-._,-'   `-._______,-'   `-._,-'
    """
    stdscr.clear()
    lines = monster_art.splitlines()
    for idx, line in enumerate(lines):
        stdscr.addstr(idx, 0, line)
    stdscr.addstr(len(lines) + 1, 0, "You have encountered a very powerful monster!")
    stdscr.addstr(len(lines) + 2, 0, "He Says He will let you go if you can guess the Number, He's Thinking Of :")
    stdscr.addstr(len(lines) + 3, 0, "Guess a Number from [1-10] inclusive : ")
    stdscr.refresh()
    guess_number = random.randint(1, 10)
    input_str = ""
    curses.echo()
    while not input_str.isnumeric():
        input_str = stdscr.getstr(len(lines) + 4, 0).decode("utf-8").strip()
    curses.noecho()
    if guess_number == int(input_str):
        stdscr.addstr(len(lines) + 5, 0, "You guessed correctly! You can now continue!")
    else:
        stdscr.addstr(len(lines) + 5, 0, f"You Guessed Wrong! The Number was {guess_number}")
        stdscr.addstr(len(lines) + 6, 0, "You Loose 1 HP")
        character["Current HP"] -= 1
    stdscr.addstr(len(lines) + 8, 0, "Press any key to continue...")
    stdscr.refresh()
    stdscr.getkey()


def is_alive(character):
    """
    Check if the character is still alive.

    This function returns True if the character's current HP is greater than 0, and False if it reaches 0.

    :param character: a dictionary representing the character with atleast a "Current HP" key
    :precondition: character is in the correct format
    :postcondition: determine if character is alive or dead
    :return: True, if character is alive otherwise False

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


def game(stdscr):
    """
    Drive the game.
    """
    rows = 15
    columns = 15
    welcome_message = r"""
 __        __   _                                                   ,~,
 \ \      / /__| | ___ ___  _ __ ___   ___                        (((}
  \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \                      -''-.
   \ V  V /  __/ | (_| (_) | | | | | |  __/                     (\  /\) 
    \_/\_/ \___|_|\___\___/|_| |_| |_|\___|             ~______\) | `\\
                                                        ~~~(         |  ') 
   / \   __| |_   _____ _ __ | |_ _   _ _ __ ___ _ __        | )____(  |
  / _ \ / _` \ \ / / _ \ '_ \| __| | | | '__/ _ \ '__|      /|/     ` /|
 / ___ \ (_| |\ V /  __/ | | | |_| |_| | | |  __/ |         \ \      / |
/_/   \_\__,_| \_/ \___|_| |_|\__|\__,_|_|  \___|_|          |\|\   /| |\\
"""
    lost_message = r"""
 __   __                             ____,
 \ \ / /__  _   _    __ _ _ __ ___  /.---|
  \ V / _ \| | | |  / _` | '__/ _ \ `    |     ___
   | | (_) | |_| | | (_| | | |  __/     (=\.  /-. \
   |_|\___/ \__,_|  \__,_|_|  \___|      |\/\_|"|  |
      _                _                  |_\ |;-|  ;
   __| | ___  __ _  __| |                 | / \| |_/ \
  / _` |/ _ \/ _` |/ _` |                 | )/\/      \
 | (_| |  __/ (_| | (_| |                  | ( '|  \   |
  \__,_|\___|\__,_|\__,_|                   |    \_ /   \
                                            |    /  \_.--\
                                            \    |    (|`\ 
                                             |   |     \
                                             |   |      '.
                                             |  /         \
                                              \  \.__.__.-._)
"""
    character = make_character()
    board, goal_position = make_board(rows, columns, character)
    achieved_goal = False
    character_alive = True
    stdscr.clear()
    stdscr.addstr(0, 0, welcome_message)
    stdscr.addstr(8, 0, "Press any key to continue...")
    stdscr.refresh()
    stdscr.getkey()
    while character_alive and not achieved_goal:
        describe_current_location(stdscr, board, character)
        direction = get_user_choice(stdscr, rows + 4)
        valid_move, new_pos = validate_move(board, character, direction)
        if valid_move:
            move_character(character, new_pos)
            describe_current_location(stdscr, board, character)
            there_is_a_challenger = check_for_foes()
            achieved_goal = check_if_goal_attained(goal_position, character)
            if achieved_goal:
                board, goal_position = make_board(rows, columns, character)
                describe_current_location(board=board, character=character, stdscr=stdscr)
                stdscr.addstr(rows + 6, 0, "Yayyy! You achieved the goal!!")
                stdscr.refresh()
                achieved_goal = False

            if there_is_a_challenger:
                guessing_game(stdscr, character)
            character_alive = is_alive(character)
            if not character_alive:
                stdscr.clear()
                stdscr.addstr(0, 0, lost_message)
                stdscr.refresh()
                stdscr.getkey()
        else:
            stdscr.addstr(rows + 6, 0, "You cant go in that direction lol")
            stdscr.refresh()
            stdscr.getkey()
    stdscr.clear()
    stdscr.addstr(0, 0, "Game Over")
    stdscr.refresh()
    stdscr.getkey()


def main(stdscr):
    """
    Drive the program.
    """
    curses.curs_set(0)
    stdscr.clear()
    game(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)