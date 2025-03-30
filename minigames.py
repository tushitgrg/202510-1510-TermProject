import time

import curses

import random
import simpleaudio

from scenes import play_game_scene, play_battle_end


def play_riddle(stdscr, character):
    riddles = [
        {
            "description": """You enter a dimly lit room. A mysterious inscription catches your eye.
            What has keys, but no locks; space, but no room; and you can enter, but not go in?""",
            "answer": ["keyboard"]
        },
        {
            "description": """A chamber of mirrors reflects your every move, casting shifting shadows.
            I am not alive, but I grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. 
            What am I?""",
            "answer": ["fire"]
        },
        {
            "description": """An ancient library with dusty scrolls surrounds you, whispering forgotten tales.
            The more you take, the more you leave behind. What am I?""",
            "answer": ["footsteps", "footstep"]
        },
        {
            "description": """A room filled with water-worn stones and echoing whispers, ancient maps scattered about.
            I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?""",
            "answer": ["map", "maps"]
        },
        {
            "description": """A chamber bathed in soft, ethereal light, with delicate objects casting long shadows.
            What can travel around the world while staying in a corner?""",
            "answer": ["stamp", "stamps"]
        },
        {
            "description": """A room of intricate clockwork and spinning gears, metal glinting in muted light.
            I am always hungry; I must always be fed. The finger I touch will soon turn red. What am I?""",
            "answer": ["fire"]
        },
        {
            "description": """A room filled with floating, luminescent symbols swirling in ethereal patterns.
            I have a head and a tail that will never meet. Having too many of me is always a treat. What am I?""",
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


def struggle_game(stdscr, message, character, boss=False):
    fire_obj = simpleaudio.WaveObject.from_wave_file("sounds/fire_effect.wav")
    keypress_obj = simpleaudio.WaveObject.from_wave_file("sounds/keypress.wav")
    success_obj = simpleaudio.WaveObject.from_wave_file("sounds/success.wav")
    failure_obj = simpleaudio.WaveObject.from_wave_file("sounds/failure.wav")
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
            stdscr.addstr(start_y + index, start_x, line[:max_x - 1], curses.color_pair(1))

    while True:
        elapsed_time = time.time() - start_time

        if elapsed_time >= time_limit:
            stdscr.nodelay(False)
            play_obj.stop()
            failure_obj.play()
            stdscr.clear()
            play_game_scene(stdscr, "You were too slow! You Failed. Press return/enter to continue")
            if not boss:
                character['Current HP'] -= 1
            else:
                character['Current HP'] = 0
            break

        key = stdscr.getch()
        if key == ord('b') or key == ord('B'):
            presses += 1
            keypress_obj.play()

        time_percentage = (time_limit - elapsed_time) / time_limit
        if time_percentage > 0.6:
            bar_color = curses.color_pair(2)
        elif time_percentage > 0.3:
            bar_color = curses.color_pair(3)
        else:
            bar_color = curses.color_pair(4)

        progress = int((presses / target_presses) * 20)
        bar = "[" + "█" * progress + " " * (20 - progress) + "]"
        percentage = int((presses / target_presses) * 100)
        complete_string = f"Struggle: {bar} {presses}/{target_presses} ({percentage}%)"
        stdscr.addstr(start_y + len(lines) + 1, max(0, (max_x - len(complete_string)) // 2),
                      complete_string, bar_color)

        if presses >= target_presses * 0.8:
            message = "Almost there!"
        elif elapsed_time >= time_limit * 0.8:
            message = "Time’s almost up!"
        else:
            message = "Keep struggling!"
        stdscr.addstr(start_y + len(lines) + 2, max(0, (max_x - len(message)) // 2),
                      message, curses.color_pair(1))

        remaining_time = time_limit - elapsed_time
        time_string = f"Time left: {remaining_time:.1f} seconds"
        stdscr.addstr(start_y + len(lines) + 3, max(0, (max_x - len(time_string)) // 2),
                      time_string, bar_color)

        if presses >= target_presses:
            stdscr.nodelay(False)
            play_obj.stop()
            success_obj.play()
            if not boss:
                play_battle_end(stdscr, character, "burn")
            break

        stdscr.refresh()

    play_obj.stop()
    stdscr.nodelay(False)
