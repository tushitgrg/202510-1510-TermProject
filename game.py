"""
Tushit Garg
A01418176
"""
import time

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
            board[(start_y + dy // 2, start_x + dx // 2)] = add_enemy_or_space()
            board[(result_y, result_x)] = add_enemy_or_space()
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


def describe_current_location(stdscr, board, character, user_name):
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
        "enemy": {
            "char": "%",
            "attr": curses.color_pair(1) | curses.A_BOLD
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

    stdscr.addstr(location_y, 0, f"This is a {board[(character['Y-coordinate'], character['X-coordinate'])]}",
                  curses.color_pair(4))

    health_string = "♥" * character["Current HP"] + "." * (5 - character["Current HP"])

    stdscr.addstr(max_y - 2, 0, f"{user_name} Current HP: [{health_string}] ({character['Current HP']}/5)",
                  curses.color_pair(4))

    stdscr.addstr(max_y - 1, 0, f"Use W/A/S/D to move, Q to quit {max_y} {max_x}", curses.color_pair(4) | curses.A_BOLD)

    stdscr.refresh()


def make_character():
    character = {"X-coordinate": 0, "Y-coordinate": 0, "Current HP": 5}
    return character


def get_user_name(stdscr):
    max_y, max_x = stdscr.getmaxyx()
    stdscr.addstr(max_y - 3, 0, "Enter your name and continue using the return key!")

    curses.echo()
    input_name = ""
    while not input_name.strip():
        input_name = stdscr.getstr(max_y - 2, 0)
    return input_name


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
    eligible_places = ["space", "Goal", "enemy"]
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
            stdscr.addstr(prompt_y + 1, 0, "Invalid Move!! ")
            stdscr.refresh()
    return input_direction


def add_enemy_or_space():
    random_number = random.randint(1, 10)
    if random_number > 8:
        return "enemy"
    return "space"


def check_if_goal_attained(goal_position, character):
    if character["X-coordinate"] == goal_position[1] and character["Y-coordinate"] == goal_position[0]:
        return True
    return False

#todo remove this
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


def struggle_game(stdscr, message, character):
    stdscr.clear()
    stdscr.nodelay(True)
    stdscr.timeout(100)
    curses.noecho()
    target_presses = 30
    presses = 0
    start_time = time.time()
    time_limit = 5
    max_y, max_x = stdscr.getmaxyx()

    lines = message.strip().split('\n')
    start_y = max(0, (max_y - len(lines)) // 2)

    for index, line in enumerate(lines):
        if start_y + index < max_y:
            start_x = max(0, (max_x - len(line)) // 2)
            stdscr.addstr(start_y + index, start_x, line[:max_x - 1])

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= time_limit:
            stdscr.nodelay(False)
            play_game_scene(stdscr, "You were too slow! You Failed. Press return/enter to continue")
            character['Current HP'] -= 1
            break

        key = stdscr.getch()
        if key == ord('b') or key == ord('B'):
            presses += 1

        progress = int((presses / target_presses) * 20)
        bar = "[" + "=" * progress + " " * (20 - progress) + "]"
        complete_string = f"Struggle: {bar} {presses}/{target_presses}"
        stdscr.addstr(start_y + len(lines) + 1, max(0, (max_x - len(complete_string)) // 2), complete_string,
                      curses.color_pair(1))

        if presses >= target_presses:
            stdscr.nodelay(False)
            play_game_scene(stdscr, "You broke free and counterattacked! Press return/enter to continue")
            break

        stdscr.refresh()
    stdscr.nodelay(False)


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


def play_game_scene(stdscr, message):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()

    lines = message.strip().split('\n')
    start_y = max(0, (max_y - len(lines)) // 2)

    for i, line in enumerate(lines):
        if start_y + i < max_y:
            start_x = max(0, (max_x - len(line)) // 2)
            stdscr.addstr(start_y + i, start_x, line[:max_x - 1])

    stdscr.refresh()
    stdscr.getkey()


def play_animation_fire(stdscr):
    won_message = r"""
__   __            ____                   _               _ _ 
\ \ / /__  _   _  / ___| _   _ _ ____   _(_)_   _____  __| | |
 \ V / _ \| | | | \___ \| | | | '__\ \ / / \ \ / / _ \/ _` | |
  | | (_) | |_| |  ___) | |_| | |   \ V /| |\ V /  __/ (_| |_|
  |_|\___/ \__,_| |____/ \__,_|_|    \_/ |_| \_/ \___|\__,_(_)
    """
    height, width = stdscr.getmaxyx()
    size = width * height
    char = [" ", ".", ":", "^", "*", "x", "s", "S", "#", "$"]
    lines = won_message.strip().split('\n')

    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, 0, 0)
    curses.init_pair(2, 1, 0)
    curses.init_pair(3, 3, 0)
    curses.init_pair(4, 4, 0)
    stdscr.clear()
    b = [0 for _ in range(size + width + 1)]

    while True:

        for i in range(int(width / 9)): b[int((random.random() * width) + width * (height - 1))] = 65
        for i in range(size):
            b[i] = int((b[i] + b[i + 1] + b[i + width] + b[i + width + 1]) / 4)
            color = (4 if b[i] > 15 else (3 if b[i] > 9 else (2 if b[i] > 4 else 1)))
            if i < size - 1:
                stdscr.addstr(int(i / width), i % width, char[(9 if b[i] > 9 else b[i])],
                              curses.color_pair(color) | curses.A_BOLD)

        for i, line in enumerate(lines):
            if 0 + i < height:
                start_x = max(0, (width - len(line)) // 2)
                stdscr.addstr(0 + i, start_x, line[:width - 1], curses.color_pair(2))
        info_message = "Press Enter/Return to Continue"
        stdscr.addstr(1 + len(lines), max(0, (width - len(info_message)) // 2), info_message)
        stdscr.refresh()
        stdscr.timeout(30)

        if stdscr.getch() != -1:
            break
    stdscr.nodelay(False)


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

 _____ ___  
|_   _/ _ \ 
  | || | | |
  | || |_| |
  |_| \___/ 
  
   ___        __                       _            
|_ _|_ __  / _| ___ _ __ _ __   ___ ( )___        
 | || '_ \| |_ / _ \ '__| '_ \ / _ \|// __|       
 | || | | |  _|  __/ |  | | | | (_) | \__ \       
|___|_| |_|_|  \___|_|  |_| |_|\___/  |___/   _   
    | |_   _  __| | __ _ _ __ ___   ___ _ __ | |_ 
 _  | | | | |/ _` |/ _` | '_ ` _ \ / _ \ '_ \| __|
| |_| | |_| | (_| | (_| | | | | | |  __/ | | | |_ 
 \___/ \__,_|\__,_|\__, |_| |_| |_|\___|_| |_|\__|
                   |___/                             
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
    game_dialogues = {
        "intro": """
Night falls over the cursed realm of Ashenvale,
where dark magic festers and shadows twist in the cold wind.
You, Sir Garrick—the relentless witch hunter—have been summoned
by the Grand Council of Purity. Your sacred duty: eradicate the witches
that plague these lands with the holy flames of justice.

[Press ENTER to begin your hunt.]


    """,
        "enemy_encountered": """Your torch roars to life as holy fire leaps from your hands!
The witch screams, her dark incantations drowned by the blaze.
Press the 'B' key repeatedly to stoke the flames and ensure her doom.
Keep the fire raging before her foul curses can take hold.

[Timer: 5 seconds – Mash 'B' to burn her completely!]

"""
    }
    stdscr.addstr(0, 0, welcome_message)
    input_name = get_user_name(stdscr)
    play_game_scene(stdscr, game_dialogues["intro"])
    play_animation_fire(stdscr)
    while character_alive and not achieved_goal:
        describe_current_location(stdscr, board, character, input_name)
        direction = get_user_choice(stdscr, rows + 4)
        valid_move, new_pos = validate_move(board, character, direction)
        if valid_move:
            move_character(character, new_pos)
            describe_current_location(stdscr, board, character, input_name)
            there_is_a_challenger = check_for_foe(board, character)
            achieved_goal = check_if_goal_attained(goal_position, character)
            if achieved_goal:
                board, goal_position = make_board(rows, columns, character)
                describe_current_location(stdscr, board, character, input_name)
                stdscr.addstr(rows + 6, 0, "Yayyy! You achieved the goal!!")
                stdscr.refresh()
                achieved_goal = False

            if there_is_a_challenger:
                struggle_game(stdscr,game_dialogues["enemy_encountered"], character)
                stdscr.getkey()
                # guessing_game(stdscr, character)
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
    #todo add a try block for curses.erro
    game(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
