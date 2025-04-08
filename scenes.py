"""
Tushit Garg
A01418176

This module handles game scene displays and animations using curses, including message prompts, fire effects,
and battle outcomes.
"""
import curses
from typing import Optional, Dict, Union

import pyfiglet
import random

from ui import is_screen_size_ok


def play_game_scene(stdscr: curses.window, message: str) -> None:
    """
    Display a game message on the screen and wait for the user to press enter.

    This function first clears the current screen and then displays a centered message on the screen. It waits for the
    user to press enter and then exits.

    :param stdscr: the main curses screen window object
    :param message: a string, representing the message to display on screen
    :precondition: stdscr must be a valid curses window object
    :postcondition: display the message on the screen
    :postcondition: exit when user presses enter
    """
    curses.noecho()
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()

    lines = message.strip().split('\n')
    start_y = max(0, (max_y - len(lines)) // 2)
    for index, line in enumerate(lines):
        if start_y + index < max_y:
            start_x = max(0, (max_x - len(line)) // 2)
            stdscr.addstr(start_y + index, start_x, line[:max_x - 1])

    stdscr.refresh()
    while True:
        if stdscr.getch() == 10:
            break


def initialise_colors_for_fire() -> None:
    """
    Initialize color pairs for the fire animation.

    This function sets up different color pairs, required to simulate fire effects in the curses window.

    :precondition: curses object must be initialized
    :postcondition: set correct colors in curses
    """
    curses.start_color()
    curses.init_pair(1, 0, 0)
    curses.init_pair(2, 1, 0)
    curses.init_pair(3, 3, 0)
    curses.init_pair(4, 4, 0)


def play_animation_fire(stdscr: curses.window, if_won: bool) -> None:
    """
    Display a fire animation with a win or lose message.

    :param stdscr: the main curses screen window object
    :param if_won: a boolean value indicating whether the player has won
    :precondition: stdscr must be a valid curses window object
    :postcondition: play a fire animation with the win or lose message
    :postcondition: exit when user presses enter
    """
    won_message = pyfiglet.figlet_format("You Survived!")
    lost_message = pyfiglet.figlet_format("You Lost!")
    message = won_message if if_won else lost_message
    height, width = stdscr.getmaxyx()
    size = width * height
    char = [" ", ".", ":", "^", "*", "x", "s", "S", "#", "$"]
    lines = message.strip().split('\n')

    curses.curs_set(0)
    initialise_colors_for_fire()

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


def play_battle_end(stdscr: curses.window, character: Dict[str, Union[str, int]], user_decision: str) -> None:
    """
    Display the battle outcome message based on the player's decision.

    :param stdscr: the main curses screen window object
    :param character: a dictionary containing the character's current position and stats
    :param user_decision: string representing the player's choice ('flee' or 'burn')
    :precondition: stdscr must be a valid curses window object
    :precondition: character dictionary must include 'Experience' and 'Level' keys
    :postcondition: the character's experience is updated based on the battle outcome
    """
    xp_change = character["Level"] * 30
    if user_decision == "flee":
        was_harmless = random.choices([True, False], weights=[60, 40])[0]
    else:
        was_harmless = random.choices([True, False], weights=[40, 60])[0]

    chose_wisely_art = pyfiglet.figlet_format("You Chose Wisely!")
    chose_poorly_art = pyfiglet.figlet_format("You Chose Poorly!")
    if was_harmless and user_decision == "flee":
        message = f"""
    {chose_wisely_art}
    Your kindness spared a life that posed no threat.
    A calm resolve settles in your heart, rewarding your mercy.

    You GAINED {xp_change} Exp

    Press Enter/Return to continue...
    """
        character["Experience"] += xp_change

    elif not was_harmless and user_decision == "burn":
        message = f"""
    {chose_wisely_art}
    Your instincts proved true. The wicked threat is extinguished.
    A surge of newfound power courses through your veins.

    You GAINED {xp_change} Exp

    Press Enter/Return to continue...
    """
        character["Experience"] += xp_change

    elif was_harmless and user_decision == "burn":
        message = f"""
    {chose_poorly_art}
    Your flames consumed an innocent soul.
    Remorse gnaws at your conscience, draining your vitality.

    You LOST {xp_change} Exp

    Press Enter/Return to continue...
    """
        character["Experience"] = max(0, character["Experience"] - xp_change)

    else:
        message = f"""
    {chose_poorly_art}
    Her wicked laughter follows you into the darkness.
    In retreat, you forfeit the chance to avert greater tragedy, sapping your resolve.

    You LOST {xp_change} Exp

    Press Enter/Return to continue...
    """
        character["Experience"] = max(0, character["Experience"] - xp_change)
    play_game_scene(stdscr, message)


def get_game_dialogue(name: str, user_name: str) -> Optional[str]:
    """
    Retrieve pre-written game dialogues based on the scene name.

    :param name: a string representing the name of the dialogue scene
    :param user_name: a string representing the player's name for personalized messages
    :postcondition: personalize the dialogues with the user_name
    :return: a formatted string containing the dialogue, or None if the name is invalid
    """
    game_dialogues = {
        "intro": f"""
    Night falls over the cursed realm of Ashen vale,
    where dark magic festers and shadows twist in the cold wind.
    You, {user_name}—the relentless witch hunter—have been summoned
    by the Grand Council of Purity. Your sacred duty: eradicate the witches
    that plague these lands with the holy flames of justice.
    You, {user_name} are entrusted with this holy duty to find the witchlord
    and burn her! Only then you will be able to save the cursed realm of Ashen vale
    [Press ENTER/RETURN to begin your hunt.]


        """,
        "enemy_encountered": """Your torch roars to life as holy fire leaps from your hands!
    The witch screams, her dark incantations drowned by the blaze.
    Press the 'B' key repeatedly to stoke the flames and ensure her doom.
    Keep the fire raging before her foul curses can take hold.

    [Timer: 5 seconds – Mash 'B' to burn her completely!]

    """,
        "boss_encountered": """
        The air turns heavy. The shadows twist unnaturally. You feel it before you see it—the 
        Witch lord stands before you.
        """,
        "game_over": f"""
    {pyfiglet.figlet_format("Game Over!")}  

     Press Enter/Return to quit the game
            """,
        "enemy_warning": """
You have chosen to BURN her...

But she does not go quietly.

She resists — clawing, screaming, unleashing all her dark strength.

🔥 YOU WILL HAVE TO MASH THE 'B' KEY TO COMPLETE THE RITUAL! 🔥
(Your speed determines the outcome...)

Press Enter/Return to begin the struggle!
""",
        "jigsaw_intro": """
You've grown strong... strong enough to challenge the Witch lord herself.

The portal shimmers with eerie violet light, and your footsteps echo into the unknown.

As you arrive before the gates of the Witch lord’s Castle, the air grows colder,
and ancient magic pulses through the ground.

A massive stone door stands in your way — no handle, no keyhole — only a strange carved pattern...

🧩 To enter, you must solve the puzzle the ancients left behind.

Complete the jigsaw to prove your mind is as sharp as your blade.

Press any key to begin the test...
"""
    }
    if name in game_dialogues:
        return game_dialogues[name]
    return None


def main(stdscr: curses.window) -> None:
    """
    Drive the program.
    """
    if not is_screen_size_ok(stdscr):
        stdscr.addstr(0, 0, "Please Increase your window size and try again")
        stdscr.addstr(2, 0, "Press any key to exit")
        stdscr.getkey()
        return
    play_game_scene(stdscr, "This is just another text game")
    play_animation_fire(stdscr, True)


if __name__ == "__main__":
    curses.wrapper(main)
