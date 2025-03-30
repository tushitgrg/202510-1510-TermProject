import curses

import pyfiglet
import random


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


def get_game_dialogue(name, user_name):
    game_dialogues = {
        "intro": f"""
    Night falls over the cursed realm of Ashenvale,
    where dark magic festers and shadows twist in the cold wind.
    You, {user_name}—the relentless witch hunter—have been summoned
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
        "boss_encountered": """
        The air turns heavy. The shadows twist unnaturally. You feel it before you see it—the 
        Witchlord stands before you.
        """,
        "game_over": f"""
    {pyfiglet.figlet_format("Game Over!")}  

     Press any Key to Quit the Game
            """
    }
    if name in game_dialogues:
        return game_dialogues[name]
    return None
