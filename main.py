import sys
from colours import Colours
from map import Map
from keys_and_input import Input
from brezelheim import Brezelheim
from player import Player
from replay import Replay
from messagebox import Messagebox
from screen import Screen
from randomness import Randomness
import time


class GateToGods:
    def __init__(self, mapname: str, seed: int, log_filename: str):
        self.maps = []
        self.colours = Colours()
        self.player = Player(-1, -1, "@", 5, 40, 5, 5)
        self.maps.append(Map(mapname, self.player))
        self.current_level = self.maps[0]
        self.rng = Randomness(seed)
        self.brezel = Brezelheim(self.current_level)
        self.scr = Screen(21, 81)  # inits the size of the screen used to display the game
        self.msg_box = Messagebox(self.scr.len_x)
        self.keys = Input()  # inits the input keys
        self.log_filename = log_filename
        self.log_file = None

    def prepare_new_map(self):
        self.brezel.reset_brezelheim(self.current_level)
        self.current_level.build_map_colour(self.brezel, self.player, self.colours)

    def play(self):
        playing = True
        skip_npc_turn = False
        record = False

        if self.log_filename != "":
            self.log_file = open(self.log_filename, "w")
            record = True

        self.prepare_new_map()

        while playing:
            self.scr.print(record, self)
            pressed_key = input()

            playing, skip_npc_turn = self.player_turn(pressed_key, playing, skip_npc_turn)
            if playing:
                if not skip_npc_turn:
                    self.current_level.npc_actions(self.player, self.brezel, self.msg_box, self.colours, self.rng)
                else:
                    skip_npc_turn = False
                self.current_level.build_map_colour(self.brezel, self.player, self.colours)
                if not self.player.is_alive():
                    self.scr.print(record, gtg)
                    playing = False
                else:
                    pass

    def player_turn(self, pressed_key: str, playing: bool, skip_npc_turn: bool):
        if pressed_key == self.keys.exit_game:
            playing = False
        elif pressed_key == self.keys.open_door or pressed_key == self.keys.close_door:
            self.current_level.door_actions(pressed_key, self)
        elif self.player.move(pressed_key, self.keys, self.current_level) == -1:
            if not self.current_level.auto_toggle(self.player, self.keys, pressed_key, self.msg_box):
                self.player.attack(self.current_level.npcs, self.keys, pressed_key, self.msg_box, self.colours,
                                   self.rng)
        elif pressed_key == self.keys.enter_entrance or pressed_key == self.keys.enter_exit:
            entrance = self.current_level.find_entrance(self)
            if entrance is not None:
                entrance.enter(self)
            skip_npc_turn = True
        elif pressed_key == self.keys.toggle_beautiful_mode:
            self.colours.toggle_beautiful_colours()
            skip_npc_turn = True
        elif pressed_key == self.keys.show_coordinates:
            if not self.player.show_coordinates:
                self.player.show_coordinates = True
            else:
                self.player.show_coordinates = False
        return playing, skip_npc_turn


def interpret_parameters():
    filename = ""
    set_seed = time.time()
    save_replay = False
    play_replay = False
    for instance in range(len(sys.argv)):
        if sys.argv[instance] == "-log" or sys.argv[instance] == "-l":
            filename = sys.argv[instance + 1]
            save_replay = True
        elif sys.argv[instance] == "-view" or sys.argv[instance] == "-v":
            filename = sys.argv[instance + 1]
            play_replay = True
        elif sys.argv[instance] == "-seed" or sys.argv[instance] == "-s":
            try:
                set_seed = int(sys.argv[instance + 1])
            except ValueError:
                pass
    return save_replay, play_replay, filename, set_seed


def get_level_file_name():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        print("Geben Sie als ersten Parameter das Level an, das geöffnet werden soll.")
        exit(0)


if __name__ == '__main__':
    record, replay, replay_filename, seed = interpret_parameters()
    level_file_name = get_level_file_name()
    if not replay:
        gtg = GateToGods(level_file_name, seed, replay_filename)
        gtg.play()
    else:
        colours = Colours()
        r = Replay(replay_filename, colours)
        r.play_replay(Input(), colours)
