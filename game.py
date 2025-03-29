"""
Tushit Garg
A01418176
"""
import simpleaudio
import time

import random
import curses
import pyfiglet

from jigsaw import start_jigsaw_game


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
        },
        "Boss": {
            "char": "Ж",
            "attr": curses.color_pair(1) | curses.A_BOLD
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
    rank_names = {
        1: "Novice Inquisitor",
        2: "Sanctified Purifier",
        3: "Grand Arbiter of Fire",
        4: "The Hand of Divine Wrath"
    }
    health_string = "♥" * character["Current HP"] + "." * (character['Level'] * 5 - character["Current HP"])
    if board[(character["Y-coordinate"], character["X-coordinate"])] == "heal":

        if character["Current HP"] + 1 <= character['Level'] * 5:
            heal_obj.play()
            character["Current HP"] += 1
            board[(character["Y-coordinate"], character["X-coordinate"])] = "space"
            stdscr.refresh()
    stdscr.addstr(max_y - 4, 0, f"You are Level {character['Level']}, {rank_names[character['Level']]}",
                  curses.color_pair(4))
    stdscr.addstr(max_y - 3, 0, f"Current Experience {character['Experience']}/{character['Level'] * 200}",
                  curses.color_pair(4))
    stdscr.addstr(max_y - 2, 0,
                  f"{user_name} Current HP: [{health_string}] ({character['Current HP']}/{character['Level'] * 5})",
                  curses.color_pair(4))

    stdscr.addstr(max_y - 1, 0, f"Use W/A/S/D to move, Q to quit {max_y} {max_x}", curses.color_pair(4) | curses.A_BOLD)

    stdscr.refresh()


def make_character():
    character = {"X-coordinate": 0, "Y-coordinate": 0, "Current HP": 5, "Experience": 0, "Level": 1}
    return character


def check_and_level_up(character, stdscr):
    if character['Experience'] >= character['Level'] * 200:
        play_game_scene(stdscr, "New Achievement: You Just Levelled Up!")
        character['Experience'] -= character['Level'] * 200
        character['Level'] += 1
        character['Current HP'] = 5 * character['Level']


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
    eligible_places = ["space", "Goal", "enemy", "heal", "Boss"]
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


def is_screen_size_ok(stdscr):
    max_y, max_x = stdscr.getmaxyx()
    if max_y < 45 or max_x < 100:
        return False
    return True


def struggle_game(stdscr, message, character, boss=False):
    fire_obj = simpleaudio.WaveObject.from_wave_file("sounds/fire_effect.wav")
    play_obj = fire_obj.play()
    stdscr.clear()
    stdscr.nodelay(True)
    stdscr.timeout(100)
    curses.noecho()
    target_presses = 50 if boss else 30
    presses = 0
    start_time = time.time()
    time_limit = 10 if boss else 5
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
            if not boss:
                character['Current HP'] -= 1
            else:
                character['Current HP'] = 0
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
            if not boss:
                play_battle_end(stdscr, character, "burn")
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


def show_help_message(stdscr):
    pass


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

    for index, line in enumerate(lines):
        if start_y + index < max_y:
            start_x = max(0, (max_x - len(line)) // 2)
            stdscr.addstr(start_y + index, start_x, line[:max_x - 1])

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

    for index, line in enumerate(lines):
        if start_y + index < max_y:
            start_x = max(0, (max_x - len(line)) // 2)
            stdscr.addstr(start_y + index, start_x, line[:max_x - 1])

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
    num_arr = [0 for _ in range(size + width + 1)]

    while True:

        for index in range(int(width / 9)): num_arr[int((random.random() * width) + width * (height - 1))] = 65
        for index in range(size):
            num_arr[index] = int(
                (num_arr[index] + num_arr[index + 1] + num_arr[index + width] + num_arr[index + width + 1]) / 4)
            color = (4 if num_arr[index] > 15 else (3 if num_arr[index] > 9 else (2 if num_arr[index] > 4 else 1)))
            if index < size - 1:
                stdscr.addstr(int(index / width), index % width, char[(9 if num_arr[index] > 9 else num_arr[index])],
                              curses.color_pair(color) | curses.A_BOLD)

        for index, line in enumerate(lines):
            if 0 + index < height:
                start_x = max(0, (width - len(line)) // 2)
                stdscr.addstr(0 + index, start_x, line[:width - 1], curses.color_pair(2))
        info_message = "Press Enter/Return to Continue"
        stdscr.addstr(1 + len(lines), max(0, (width - len(info_message)) // 2), info_message)
        stdscr.refresh()
        stdscr.timeout(30)

        if stdscr.getch() == 10:
            break
    stdscr.nodelay(False)


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


def get_user_battle_decision(stdscr):
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
        input_decision = stdscr.getstr(max_y - 2, 0).decode("utf-8")
    return input_decision.strip().lower()


def play_battle_end(stdscr, character, user_decison):
    she_was_good = random.choice([True, False])
    if she_was_good:
        innocent_art = pyfiglet.figlet_format('She was Innocent!')
        if user_decison == "flee":
            message = f"""
             {innocent_art}
             She vanishes into mist. A strange warmth fills your soul. 
             You gained {character["Level"] * 30} Exp
             Press any [key] to return
                """
            character["Experience"] += character["Level"] * 30

        else:
            message = f"""
                        {innocent_art}
                         As the flames rise, her final words whisper through your mind. 
                        You lost {character["Level"] * 30} Exp
                        Press any [key] to return
                            """
            character["Experience"] = max(0, character["Experience"] - character["Level"] * 30)
    else:
        not_innocent_art = pyfiglet.figlet_format('She was NOT Innocent!')
        if user_decison == "flee":
            message = f"""
                {not_innocent_art}
                 A distant cackle. The village burns. You feel weaker.
                You lost {character["Level"] * 30} Exp
                Press any [key] to return
                """
            character["Experience"] = max(0, character["Experience"] - character["Level"] * 30)
        else:
            message = f"""
                       {not_innocent_art}
                        A shriek echoes. The curse lifts. You are safe... for now.
                       You gained {character["Level"] * 30} Exp
                       Press any [key] to return
                       """
            character["Experience"] += character["Level"] * 30

    play_game_scene(stdscr, message)


def check_for_boss(board, character):
    x_pos = character["X-coordinate"]
    y_pos = character["Y-coordinate"]
    if board[(y_pos, x_pos)] == "Boss":
        board[(y_pos, x_pos)] = "space"
        return True
    return False

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
        "boss_encountered" : """
        The air turns heavy. The shadows twist unnaturally. You feel it before you see it—the 
        Witchlord stands before you.
        """,
        "game_over": f"""
    {pyfiglet.figlet_format("Game Over!")}  

     Press any Key to Quit the Game
            """
    }
    play_game_scene(stdscr, game_dialogues["intro"])
    # start_jigsaw_game(stdscr)
    while character_alive and not achieved_goal:
        if not play_obj.is_playing():
            play_obj = music_obj.play()

        describe_current_location(stdscr, board, character, input_name)
        direction = get_user_choice(stdscr, rows + 4)
        if direction is None:
            break
        valid_move, new_pos = validate_move(board, character, direction)
        if valid_move:
            if character["Level"] < 3:
                move_enemies(board, character)
            move_character(character, new_pos)

            describe_current_location(stdscr, board, character, input_name)
            there_is_a_challenger = check_for_foe(board, character)
            if goal_position:
                achieved_goal = check_if_goal_attained(goal_position, character)
                if achieved_goal:
                    if character["Level"] < 3:
                        play_riddle(stdscr, character)
                        board, goal_position = make_board(rows, columns, character)
                    else:
                        start_jigsaw_game(stdscr)
                        board, goal_position = make_board(rows, columns, character, boss=True)
                    describe_current_location(stdscr, board, character, input_name)

                stdscr.refresh()
                achieved_goal = False
            if check_for_boss(board, character):
                struggle_game(stdscr, game_dialogues["boss_encountered"], character, boss=True)
                if is_alive(character):
                    play_animation_fire(stdscr, True)
                    break

            if there_is_a_challenger:
                if get_user_battle_decision(stdscr) == "burn":
                    struggle_game(stdscr, game_dialogues["enemy_encountered"], character)
                else:
                    play_battle_end(stdscr, character, "flee")
                stdscr.getkey()

            character_alive = is_alive(character)

            if not character_alive:
                play_animation_fire(stdscr, False)
                break
            check_and_level_up(character, stdscr)
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
    # todo add a try block for curses.error
    try:
        game(stdscr)
    except KeyboardInterrupt:
        print("Game exited Successfully!")


if __name__ == "__main__":
    curses.wrapper(main)
