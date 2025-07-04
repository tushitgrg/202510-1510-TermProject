"""
Tushit Garg
A01418176

This module drives interactive mini-games, featuring a riddle challenge and a timed key-press struggle event.
"""
import json
import time
import curses

import random
from typing import Dict, List, Tuple, Union

import simpleaudio

from character import make_character
from maze import initialise_colors_for_map
from scenes import play_game_scene, play_battle_end, get_game_dialogue
from ui import is_screen_size_ok


def load_riddles_from_json() -> List[Dict[str, str]]:
    """
    Load riddles from a json file named 'riddles.json'.

    :precondition: 'riddles.json' must exist in the working directory and be valid json
    :postcondition: parse the data into a valid python data structure
    :return: a list of dictionaries, each including a riddle and its answer
    """
    with open('riddles.json', 'r', encoding='utf-8') as file_obj:
        return json.load(file_obj)


def play_riddle(stdscr: curses.window, character: Dict[str, int]) -> None:
    """
    Drive the riddle mini-game

    This function displays a randomly chosen riddle, takes user input, and checks whether the answer is correct.
    If correct, a passage is revealed; if incorrect, the character loses 1 HP.

    :param stdscr: the main curses screen window object
    :param character: a dictionary containing the character's current position and stats
    :precondition: stdscr must be a valid curses window object
    :precondition: character dictionary must contain 'Current HP' key
    :postcondition: update the screen to show the riddle and its result
    :postcondition: decrease the character's HP by 1 if the answer is incorrect
    """
    riddles = load_riddles_from_json()
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
        play_game_scene(stdscr,
                        "You answered correctly. \n The wall slides open, revealing a mysterious passage! \n Press "
                        "Enter/Return to continue")
    else:
        play_game_scene(stdscr, f"""You answered Wrong. 
         The answer was {riddle['answer'][0]}
         You loose 1 HP 
         Press Enter/Return to continue""")
        character["Current HP"] -= 1
    curses.noecho()


def get_bar_color(time_percentage: float) -> int:
    """
    Determine the color of the progress bar based on the remaining time percentage.

    :param time_percentage: float value representing the remaining time as a fraction (0 to 1)
    :precondition: time_percentage should be a float between 0 and 1
    :postcondition: determine a curses color pair corresponding to the time range
    :return: a curses color pair indicating the bar color
    """
    if time_percentage > 0.6:
        return curses.color_pair(2)
    elif time_percentage > 0.3:
        return curses.color_pair(3)
    else:
        return curses.color_pair(4)


def get_alert_message(presses: int, target_presses: int, elapsed_time: float, time_limit: float) -> str:
    """
    Generate an encouraging message based on player progress and remaining time.

    :param presses: the number of times the player has pressed the key
    :param target_presses: the required number of presses to win
    :param elapsed_time: the time that has passed since the start of the mini-game
    :param time_limit: the total time allowed for the struggle event
    :postcondition: determine the correct message according to the progress
    :return: a string message indicating the current state

    >>> get_alert_message(24, 30, 2, 5)
    'Almost there!'

    >>> get_alert_message(10, 30, 4.5, 5)
    'Time’s almost up!'

    >>> get_alert_message(5, 30, 1, 5)
    'Keep struggling!'
    """
    if presses >= target_presses * 0.8:
        return "Almost there!"
    elif elapsed_time >= time_limit * 0.8:
        return "Time’s almost up!"
    else:
        return "Keep struggling!"


def draw_progress_bar(time_limit: float, elapsed_time: float, presses: int, target_presses: int, stdscr: curses.window,
                      start_y: int, lines: List[str], max_x: int) -> None:
    """
    Draw the progress bar and status messages on the screen for the struggle event.

    :param time_limit: total time allowed for the struggle event
    :param elapsed_time: time that has passed since the start of the mini-game
    :param presses: the number of successful key presses
    :param target_presses: the number of required key presses to win
    :param stdscr: the main curses screen window object
    :param start_y: vertical starting position for drawing
    :param lines: the lines of the message previously displayed
    :param max_x: maximum horizontal screen size
    :postcondition: update the curses screen with a visual progress bar, message, and remaining time
    """
    time_percentage = (time_limit - elapsed_time) / time_limit
    bar_color = get_bar_color(time_percentage)
    progress = int((presses / target_presses) * 20)
    bar = "[" + "█" * progress + " " * (20 - progress) + "]"
    percentage = int((presses / target_presses) * 100)
    complete_string = f"Struggle: {bar} {presses}/{target_presses} ({percentage}%)"
    stdscr.addstr(start_y + len(lines) + 1, max(0, (max_x - len(complete_string)) // 2),
                  complete_string, bar_color)
    message = get_alert_message(presses, target_presses, elapsed_time, time_limit)
    stdscr.addstr(start_y + len(lines) + 2, max(0, (max_x - len(message)) // 2),
                  message, curses.color_pair(1))
    remaining_time = time_limit - elapsed_time
    time_string = f"Time left: {remaining_time:.1f} seconds"
    stdscr.addstr(start_y + len(lines) + 3, max(0, (max_x - len(time_string)) // 2),
                  time_string, bar_color)


def load_sounds() -> Dict[str, simpleaudio.WaveObject]:
    """
    Load and return a dictionary of preloaded sound effects for different game events.

    :precondition: all required sounds are present in the correct path
    :postcondition: load all the required sound effects
    :return: a dictionary containing WaveObject instances for fire, keypress, success, and failure sounds
    """
    return {
        'fire': simpleaudio.WaveObject.from_wave_file("sounds/fire_effect.wav"),
        'keypress': simpleaudio.WaveObject.from_wave_file("sounds/keypress.wav"),
        'success': simpleaudio.WaveObject.from_wave_file("sounds/success.wav"),
        'failure': simpleaudio.WaveObject.from_wave_file("sounds/failure.wav"),
    }


def handle_failure(stdscr: curses.window, play_obj: simpleaudio.PlayObject, sounds: Dict[str, simpleaudio.WaveObject],
                   character: Dict[str, int], boss: bool) -> None:
    """
    Handle the outcome of a failed struggle event.

    :param stdscr: the main curses screen window object
    :param play_obj: the currently playing sound object
    :param sounds: a dictionary of preloaded sound effects
    :param character: a dictionary containing the player's current state
    :param boss: a boolean indicating if the opponent is a boss
    :precondition: stdscr must be a valid curses window object
    :postcondition: set character to 0 HP if boss, or decrease 1 HP otherwise
    """
    stdscr.nodelay(False)
    play_obj.stop()
    sounds["failure"].play()
    stdscr.clear()
    play_game_scene(stdscr, "You were too slow! You Failed. Press return/enter to continue")
    character['Current HP'] = 0 if boss else character['Current HP'] - 1


def handle_success(stdscr: curses.window, play_obj: simpleaudio.PlayObject, sounds: Dict[str, simpleaudio.WaveObject],
                   character: Dict[str, int], boss: bool) -> None:
    """
    Handle the outcome of a successful struggle event.

    :param stdscr: the main curses screen window object
    :param play_obj: the currently playing sound object
    :param sounds: a dictionary of preloaded sound effects
    :param character: a dictionary containing the player's current state
    :param boss: a boolean indicating if the opponent is a boss
    :precondition: stdscr must be a valid curses window object
    :postcondition: trigger next scene only if not a boss
    """
    stdscr.nodelay(False)
    play_obj.stop()
    sounds["success"].play()
    if not boss:
        play_battle_end(stdscr, character, "burn")


def display_centered_message(stdscr: curses.window, message: str, max_y: int, max_x: int) -> Tuple[int, List[str]]:
    """
    Display a multiline message centered on the screen.

    :param stdscr: the main curses screen window object
    :param message: string with newline-separated lines to be displayed
    :param max_y: maximum vertical screen size
    :param max_x: maximum horizontal screen size
    :precondition: stdscr must be a valid curses window object
    :postcondition: print the message centered on the screen
    :return: a tuple (start_y, lines) where start_y is the vertical position of the first line and lines is the
    list of lines
    """
    lines = message.strip().split('\n')
    start_y = max(0, (max_y - len(lines)) // 2)
    for index, line in enumerate(lines):
        if start_y + index < max_y:
            start_x = max(0, (max_x - len(line)) // 2)
            stdscr.addstr(start_y + index, start_x, line[:max_x - 1], curses.color_pair(1))
    return start_y, lines


def struggle_game(stdscr: curses.window, message: str, character: Dict[str, Union[str, int]],
                  boss: bool = False) -> None:
    """
    Simulate a struggle event where the player must press 'B' rapidly to succeed.

    This function initiates a mini-game where the player has a limited time to reach a target number of a key presses.
    If successful, the game is won; if not, they lose HP (or all HP if against a boss).

    :param stdscr: the main curses screen window object
    :param message: a string representing the initial message to be displayed on screen
    :param character: a dictionary containing the character's current position and stats
    :param boss: a boolean indicating if this is a boss fight, default is False
    :precondition: stdscr must be a valid curses window object
    :postcondition: increase experience if player wins
    :postcondition: decrease hp if player looses
    """
    play_game_scene(stdscr, get_game_dialogue('enemy_warning', character['Name']))
    sounds = load_sounds()
    play_obj = sounds["fire"].play()
    stdscr.clear()
    stdscr.nodelay(True)
    stdscr.timeout(100)
    curses.noecho()
    target_presses = 50 if boss else 30
    presses = 0
    start_time = time.time()
    time_limit = 10 if boss else 5
    max_y, max_x = stdscr.getmaxyx()
    start_y, lines = display_centered_message(stdscr, message, max_y, max_x)
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= time_limit:
            handle_failure(stdscr, play_obj, sounds, character, boss)
            break
        key = stdscr.getch()
        if key == ord('b') or key == ord('B'):
            presses += 1
            sounds["keypress"].play()
        draw_progress_bar(time_limit, elapsed_time, presses, target_presses, stdscr, start_y, lines, max_x)
        if presses >= target_presses:
            handle_success(stdscr, play_obj, sounds, character, boss)
            break
        stdscr.refresh()
    play_obj.stop()
    stdscr.nodelay(False)


def main(stdscr: curses.window) -> None:
    """
    Drive the program.
    """
    if not is_screen_size_ok(stdscr):
        stdscr.addstr(0, 0, "Please Increase your window size and try again")
        stdscr.addstr(2, 0, "Press any key to exit")
        stdscr.getkey()
        return
    my_character = make_character('Tushit')
    initialise_colors_for_map()
    struggle_game(stdscr, "Hi, This is a sample Message", my_character)


if __name__ == "__main__":
    curses.wrapper(main)
