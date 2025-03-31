"""
Tushit Garg
A01418176
"""
import simpleaudio
import curses
from character import make_character, move_character, is_alive, check_and_level_up
from jigsaw import start_jigsaw_game
from logic import validate_move, move_enemies, check_for_foe, check_if_goal_attained, check_for_boss
from maze import make_board, describe_current_location
from minigames import play_riddle, struggle_game
from scenes import play_game_scene, play_animation_fire, play_battle_end, get_game_dialogue
from ui import welcome_user_and_ask_for_name, is_screen_size_ok, get_user_choice, get_user_battle_decision


def game(stdscr):
    """
    Drive the game.
    """
    rows = 25
    columns = 38
    music_obj = simpleaudio.WaveObject.from_wave_file("sounds/game-music.wav")
    play_obj = music_obj.play()
    input_name = welcome_user_and_ask_for_name(stdscr)
    character = make_character(input_name)
    board, goal_position = make_board(rows, columns, character)
    achieved_goal = False
    character_alive = True
    stdscr.clear()
    if not is_screen_size_ok(stdscr):
        stdscr.addstr(0, 0, "Please Increase your window size and try again")
        stdscr.addstr(2, 0, "Press any key to exit")
        stdscr.getkey()
        return
    play_game_scene(stdscr, get_game_dialogue("intro", input_name))
    while character_alive and not achieved_goal:
        if not play_obj.is_playing():
            play_obj = music_obj.play()
        describe_current_location(stdscr, board, character)
        direction = get_user_choice(stdscr, rows + 4)
        if direction is None:
            break
        valid_move, new_pos = validate_move(board, character, direction)
        if valid_move:
            if character["Level"] < 3:
                move_enemies(board, character)
            move_character(character, new_pos)
            describe_current_location(stdscr, board, character)
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
                    describe_current_location(stdscr, board, character)
                stdscr.refresh()
                achieved_goal = False
            if check_for_boss(board, character):
                struggle_game(stdscr, get_game_dialogue("boss_encountered", input_name), character, boss=True)
                if is_alive(character):
                    play_animation_fire(stdscr, True)
                    break
            if there_is_a_challenger:
                if get_user_battle_decision(stdscr) == "burn":
                    struggle_game(stdscr, get_game_dialogue("enemy_encountered", input_name), character)
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
    play_game_scene(stdscr, get_game_dialogue("game_over", input_name))


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
