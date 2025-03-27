"""
Tushit Garg
A01418176
"""
import simpleaudio
import time

import random
import curses
import pyfiglet


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
            board[(start_y + dy // 2, start_x + dx // 2)] = add_random_block()
            board[(result_y, result_x)] = add_random_block()
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
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
        describe_current_location.colors_initialized = True

    ascii_chars = {
        "space": {
            "char": " ",
            "attr": curses.color_pair(1) | curses.A_BOLD
        },
        "character": {
            "char": "@",
            "attr": curses.color_pair(4) | curses.A_BOLD
        },
        "Goal": {
            "char": "༒",
            "attr": curses.color_pair(2) | curses.A_BOLD
        },
        "wall": {
            "char": "█",
            "attr": curses.color_pair(3) | curses.A_BOLD
        },
        "enemy": {
            "char": "Ψ",
            "attr": curses.color_pair(1) | curses.A_BOLD
        },
        "heal": {
            "char": "ɸ",
            "attr": curses.color_pair(5) | curses.A_BOLD
        }
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

    # location_y = current_row + 3

    # stdscr.addstr(location_y, 0, f"This is a {board[(character['Y-coordinate'], character['X-coordinate'])]}",
    #               curses.color_pair(4))
    heal_obj = simpleaudio.WaveObject.from_wave_file("sounds/heal_effect.wav")

    health_string = "♥" * character["Current HP"] + "." * (5 - character["Current HP"])
    if board[(character["Y-coordinate"], character["X-coordinate"])] == "heal":

        if character["Current HP"] + 1 <= 5:
            heal_obj.play()
            character["Current HP"] += 1
            board[(character["Y-coordinate"], character["X-coordinate"])] = "space"
            stdscr.refresh()

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
        input_name = stdscr.getstr(max_y - 2, 0).decode("utf-8")
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
    eligible_places = ["space", "Goal", "enemy", "heal"]
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
        stdscr.refresh()
        key = stdscr.getkey().lower()
        if key in ['w', 'a', 's', 'd']:
            input_direction = key
        elif key == 'q':
            return None
        else:
            stdscr.addstr(prompt_y + 1, 0, "Invalid Move!! ")
            stdscr.refresh()
    return input_direction


def add_random_block():
    random_number = random.randint(1, 20)
    if random_number == 20:
        return "enemy"
    elif random_number == 10:
        return "heal"
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


def is_screen_size_ok(stdscr):
    max_y, max_x = stdscr.getmaxyx()
    if max_y < 45 or max_x < 100:
        return False
    return True


def struggle_game(stdscr, message, character):
    fire_obj = simpleaudio.WaveObject.from_wave_file("sounds/fire_effect.wav")
    play_obj = fire_obj.play()
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
    play_obj.stop()
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


def play_riddle(stdscr, character):
    riddles = [
        {
            "description": "You enter a dimly lit room. A mysterious inscription catches your eye.\n\nWhat has keys, but no locks; space, but no room; and you can enter, but not go in?",
            "answer": ["keyboard"]
        },
        {
            "description": "A chamber of mirrors reflects your every move, casting shifting shadows.\n\nI am not alive, but I grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I?",
            "answer": ["fire"]
        },
        {
            "description": "An ancient library with dusty scrolls surrounds you, whispering forgotten tales.\n\nThe more you take, the more you leave behind. What am I?",
            "answer": ["footsteps", "footstep"]
        },
        {
            "description": "A room filled with water-worn stones and echoing whispers, ancient maps scattered about.\n\nI have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?",
            "answer": ["map", "maps"]
        },
        {
            "description": "A chamber bathed in soft, ethereal light, with delicate objects casting long shadows.\n\nWhat can travel around the world while staying in a corner?",
            "answer": ["stamp", "stamps"]
        },
        {
            "description": "A room of intricate clockwork and spinning gears, metal glinting in muted light.\n\nI am always hungry; I must always be fed. The finger I touch will soon turn red. What am I?",
            "answer": ["fire"]
        },
        {
            "description": "A room filled with floating, luminescent symbols swirling in ethereal patterns.\n\nI have a head and a tail that will never meet. Having too many of me is always a treat. What am I?",
            "answer": ["coin"]
        }
    ]
    riddle = random.choice(riddles)
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    lines = riddle["description"].strip().split('\n')
    start_y = max(0, (max_y - len(lines)) // 2)

    for i, line in enumerate(lines):
        if start_y + i < max_y:
            start_x = max(0, (max_x - len(line)) // 2)
            stdscr.addstr(start_y + i, start_x, line[:max_x - 1])

    stdscr.refresh()
    curses.echo()
    input_answer = ""
    while not input_answer.strip():
        input_answer = stdscr.getstr(start_y + len(lines) + 1, 20).decode("utf-8").lower()
    if input_answer in riddle["answer"]:
        play_game_scene(stdscr, "You answered correctly. \n The wall slides open, revealing a mysterious passage!")
    else:
        play_game_scene(stdscr, "You answered Wrong. \n You loose 1 HP")
        character["Current HP"] -= 1
    curses.noecho()


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


def play_animation_fire(stdscr, if_won):
    won_message = pyfiglet.figlet_format("You Survived!")
    lost_message = pyfiglet.figlet_format("You Lost!")
    message = won_message if if_won else lost_message
    height, width = stdscr.getmaxyx()
    size = width * height
    char = [" ", ".", ":", "^", "*", "x", "s", "S", "#", "$"]
    lines = message.strip().split('\n')

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


def welcome_user_and_ask_for_name(stdscr):
    welcome_message = pyfiglet.figlet_format("Welcome \n To \n Inferno \n Trials")
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    stdscr.clear()

    max_y, max_x = stdscr.getmaxyx()

    lines = welcome_message.strip().split('\n')
    start_y = max(0, (max_y - len(lines)) // 2)
    for i, line in enumerate(lines):
        start_x = max(0, (max_x - len(line)) // 2)

        for j in range(len(line) + 1):
            stdscr.clear()
            for k, prev_line in enumerate(lines[:i]):
                prev_start_x = max(0, (max_x - len(prev_line)) // 2)
                stdscr.addstr(start_y + k, prev_start_x, prev_line, curses.color_pair(3))

            stdscr.addstr(start_y + i, start_x, line[:j], curses.color_pair(3))

            stdscr.refresh()
            time.sleep(0.007)

    stdscr.refresh()
    return get_user_name(stdscr)


def game(stdscr):
    """
    Drive the game.
    """
    rows = 15
    columns = 30
    character = make_character()
    music_obj = simpleaudio.WaveObject.from_wave_file("sounds/game-music.wav")
    play_obj = music_obj.play()
    board, goal_position = make_board(rows, columns, character)
    achieved_goal = False
    character_alive = True
    stdscr.clear()

    if not is_screen_size_ok(stdscr):
        stdscr.addstr(0, 0, "Please Increase your window size and try again")
        stdscr.addstr(2, 0, "Press any key to exit")
        stdscr.getkey()
        return
    input_name = welcome_user_and_ask_for_name(stdscr)
    game_dialogues = {
        "intro": f"""
    Night falls over the cursed realm of Ashenvale,
    where dark magic festers and shadows twist in the cold wind.
    You, {input_name}—the relentless witch hunter—have been summoned
    by the Grand Council of Purity. Your sacred duty: eradicate the witches
    that plague these lands with the holy flames of justice.

    [Press ENTER to begin your hunt.]


        """,
        "enemy_encountered": """Your torch roars to life as holy fire leaps from your hands!
    The witch screams, her dark incantations drowned by the blaze.
    Press the 'B' key repeatedly to stoke the flames and ensure her doom.
    Keep the fire raging before her foul curses can take hold.

    [Timer: 5 seconds – Mash 'B' to burn her completely!]

    """,
        "game_over": f"""
    {pyfiglet.figlet_format("Game Over!")}  

     Press any Key to Quit the Game
            """
    }
    play_game_scene(stdscr, game_dialogues["intro"])

    while character_alive and not achieved_goal:
        if not play_obj.is_playing():
            play_obj = music_obj.play()

        describe_current_location(stdscr, board, character, input_name)
        direction = get_user_choice(stdscr, rows + 4)
        if direction is None:
            break
        valid_move, new_pos = validate_move(board, character, direction)
        if valid_move:
            move_enemies(board, character)
            move_character(character, new_pos)

            describe_current_location(stdscr, board, character, input_name)
            there_is_a_challenger = check_for_foe(board, character)
            achieved_goal = check_if_goal_attained(goal_position, character)
            if achieved_goal:
                play_riddle(stdscr, character)
                board, goal_position = make_board(rows, columns, character)
                describe_current_location(stdscr, board, character, input_name)

                stdscr.refresh()
                achieved_goal = False

            if there_is_a_challenger:
                struggle_game(stdscr, game_dialogues["enemy_encountered"], character)
                stdscr.getkey()
                # guessing_game(stdscr, character)
            character_alive = is_alive(character)
            if not character_alive:
                play_animation_fire(stdscr, False)
        else:
            stdscr.addstr(rows + 6, 0, "You cant go in that direction lol")
            stdscr.refresh()
            stdscr.getkey()

    play_game_scene(stdscr, game_dialogues["game_over"])


def main(stdscr):
    """
    Drive the program.
    """
    curses.curs_set(0)
    stdscr.clear()
    #todo add a try block for curses.error
    try:
        game(stdscr)
    except KeyboardInterrupt:
        print("Game exited Successfully!")


if __name__ == "__main__":
    curses.wrapper(main)
