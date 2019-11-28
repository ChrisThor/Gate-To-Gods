import sys
from colours import Colours
from map import Map
from keys_and_input import Input
from brezelheim import Brezelheim
from default_entity import DefaultEntity
from replay import Replay
from messagebox import Messagebox
from screen import Screen
from randomness import Randomness
from language import LanguageManagement
import time


class GateToGods:
    def __init__(self, seed: int, log_filename: str):
        self.maps = []
        self.default_entities = []
        self.language = LanguageManagement()
        mapname = get_level_file_name(self.language)
        self.read_units_dat()
        self.colours = Colours()
        self.player = self.set_entity("Player", -1, -1)
        self.maps.append(Map(mapname, self))
        self.current_level = self.maps[0]
        self.rng = Randomness(seed)
        self.brezelheim = Brezelheim(self.current_level)
        self.scr = Screen(21, 81)  # inits the size of the screen used to display the game
        self.msg_box = Messagebox(self.scr.len_x)
        self.keys = Input()  # inits the input keys
        self.log_filename = log_filename
        self.log_file = None

    def read_units_dat(self):
        try:
            units_file = open("data/units.dat", "r")
            valid_units_file = True
            player_defined = False

            lines = units_file.readlines()
            units_file.close()
            line = 0
            while line < len(lines):
                entity_id = lines[line].split(":")[0]
                if "Player" in entity_id:
                    player_defined = True
                name = ""
                hp = -1
                minimum_damage = -1
                maximum_damage = -1
                range_of_vision = -1
                aggression = False
                line += 1
                while line < len(lines) and lines[line][0] == " ":
                    if "healthPoints" in lines[line]:
                        try:
                            hp = int(lines[line].split(":")[1])
                        except ValueError:
                            print(self.language.texts.get("unitsdat_number_error", self.language.undefined)
                                  .replace("(LINE)", str(line)).replace("(NOT_A_NUMBER)", lines[line].split(":")[1]))
                            valid_units_file = False
                    elif "damage" in lines[line]:
                        try:
                            if "-" in lines[line]:
                                minimum_damage = int(lines[line].split("(")[1].split("-")[0])
                                maximum_damage = int(lines[line].split("-")[1].split(")")[0])
                            else:
                                minimum_damage = int(lines[line].split("(")[1].split(")")[0])
                                maximum_damage = minimum_damage
                        except ValueError:
                            print(self.language.texts.get("unitsdat_damage_error", self.language.undefined)
                                  .replace("(LINE)", str(line)))
                            valid_units_file = False
                    elif "fieldOfVision" in lines[line]:
                        try:
                            range_of_vision = int(lines[line].split(":")[1])
                        except ValueError:
                            print(self.language.texts.get("unitsdat_number_error", self.language.undefined)
                                  .replace("(LINE)", str(line)).replace("(NOT_A_NUMBER)", lines[line].split(":")[1]))
                            valid_units_file = False
                    elif "hostile" in lines[line]:
                        if "false" in lines[line] or "False" in lines[line]:
                            aggression = False
                        elif "true" in lines[line] or "True" in lines[line]:
                            aggression = True
                    elif "name" in lines[line]:
                        if entity_id in self.language.texts:
                            name = self.language.texts.get(entity_id)
                        else:
                            name = lines[line].split(":")[1].replace("\n", "")
                            while name[0] == " ":
                                name = name[1:]     # if a blank is in front of a name, it gets removed
                    line += 1
                if name == "" or hp == -1 or minimum_damage == -1 == maximum_damage or range_of_vision == -1:
                    print(self.language.texts.get("unitsdat_incomplete_definition", self.language.undefined)
                          .replace("(ENTITY_ID)"), entity_id)
                    exit(-1)
                else:
                    self.default_entities.append(DefaultEntity(entity_id, name, range_of_vision, hp, minimum_damage,
                                                               maximum_damage, aggression))
                    if line >= len(lines):
                        break
            if not player_defined:
                print(self.language.texts.get("unitsdat_player_not_defined", self.language.undefined))
                exit(-1)
            if not valid_units_file:
                exit(-1)
        except FileNotFoundError:
            print(self.language.texts.get("unitsdat_not_found", self.language.undefined))
            exit(-1)

    def set_entity(self, entity_id, pos_y, pos_x):
        for entity in self.default_entities:
            if entity.id == entity_id:
                return entity.create(pos_y, pos_x)
        return None

    def prepare_new_map(self):
        self.brezelheim.reset_brezelheim(self.current_level)
        self.current_level.build_map_colour(self.brezelheim, self.player, self.colours)

    def play(self):
        playing = True
        skip_npc_turn = False
        record = False

        if self.log_filename != "":
            self.log_file = open(self.log_filename, "w")
            record = True

        self.prepare_new_map()
        print(self.colours.clear())

        while playing:
            self.scr.print(record, self)
            pressed_key = input()

            playing, skip_npc_turn = self.player_turn(pressed_key, playing, skip_npc_turn)
            if playing:
                if not skip_npc_turn:
                    self.current_level.npc_actions(self)
                else:
                    skip_npc_turn = False
                self.current_level.build_map_colour(self.brezelheim, self.player, self.colours)
                if not self.player.is_alive():
                    self.scr.print(record, self)
                    playing = False
                else:
                    pass

    def player_turn(self, pressed_key: str, playing: bool, skip_npc_turn: bool):
        if pressed_key == self.keys.exit_game:
            playing = False
        elif pressed_key == self.keys.open_door or pressed_key == self.keys.close_door:
            self.current_level.door_actions(self, pressed_key)
        elif self.player.move(pressed_key, self.keys, self.current_level) == -1:
            if not self.current_level.auto_toggle(self, pressed_key):
                self.player.attack(self, pressed_key)
        elif pressed_key == self.keys.enter_entrance or pressed_key == self.keys.enter_exit:
            entrance = self.current_level.find_entrance(self)
            if entrance is not None:
                entrance.enter(self)
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


def get_level_file_name(language):
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        print(language.texts.get("no_level_parameter", language.undefined))
        exit(0)


if __name__ == '__main__':
    record, replay, replay_filename, seed = interpret_parameters()
    if not replay:
        gtg = GateToGods(seed, replay_filename)
        gtg.play()
    else:
        colours = Colours()
        r = Replay(replay_filename, colours)
        r.play_replay(Input(), colours)
