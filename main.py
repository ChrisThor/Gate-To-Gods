import sys
from colours import Colours
from map import Map
from keys_and_input import Input
from brezelheim import Brezelheim
from default_entity import DefaultEntity
from replay import Replay
from messagebox import Messagebox
from screen import Screen
from language import LanguageManagement
from options_menu import OptionsMenu
from random import Random
import status_effects
import readchar
import input_delay
import time


class GateToGods:
    def __init__(self, seed: int, log_filename: str):
        """
        Initializes the game
        :param seed:
        :param log_filename:
        """
        self.maps = []
        self.default_entities = []
        self.user_input = ""
        self.configurations = read_configuration_file()
        self.language = LanguageManagement(self.configurations.get("language_file"))
        self.options = OptionsMenu(self)
        mapname = get_level_file_name(self.language)
        self.read_units_dat()
        self.colours = Colours()
        self.player = self.set_entity("Player", -1, -1)
        self.maps.append(Map(mapname, self))
        self.current_level = self.maps[0]
        self.rng = Random(seed)
        self.all_status_effects = status_effects.set_effect_values(status_effects.read_status_effects_dat(self))
        self.brezelheim = Brezelheim(self.current_level)
        self.scr = Screen(self.configurations.get("screen_height"), self.configurations.get("screen_width"))
        self.msg_box = Messagebox(self.scr.len_x)
        self.keys = Input()  # inits the input keys
        self.log_filename = log_filename
        self.log_file = None

    def read_units_dat(self):
        """
        This function opens and reads the "units.dat" file, which contains all information regarding entities.
        Exits the game if a definition is wrong or incomplete.
        :return: Nothing
        """
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
                effects = {}
                accuracy = 1.0
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
                            if "/" in lines[line]:
                                minimum_damage = int(lines[line].split("(")[1].split("/")[0])
                                maximum_damage = int(lines[line].split("/")[1].split(")")[0])
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
                    elif "effects" in lines[line]:
                        line += 1
                        while line < len(lines) and "-" in lines[line]:
                            effect = lines[line].split("-")[1].replace("\n", "")
                            while effect[0] == " ":
                                effect = effect[1:]
                            effects[effect] = {"effect_id": effect}
                            line += 1
                        line -= 1
                    elif "accuracy" in lines[line]:
                        try:
                            accuracy = float(lines[line].split(":")[1])
                        except ValueError:
                            print(self.language.texts.get("unitsdat_number_error", self.language.undefined)
                                  .replace("(LINE)", str(line)).replace("(NOT_A_NUMBER)", lines[line].split(":")[1]))
                            valid_units_file = False
                    line += 1
                if name == "" or hp == -1 or minimum_damage == -1 == maximum_damage or range_of_vision == -1:
                    print(self.language.texts.get("unitsdat_incomplete_definition", self.language.undefined)
                          .replace("(ENTITY_ID)", entity_id))
                    exit(-1)
                else:
                    self.default_entities.append(DefaultEntity(entity_id, name, range_of_vision, hp, minimum_damage,
                                                               maximum_damage, aggression, effects, accuracy))
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
        """
        Creates an entity based on their ID and a given position.
        :param entity_id:   ID of the entity, defined in "units.dat"
        :param pos_y:       y-coordinate of the entity
        :param pos_x:       x-coordinate of the entity
        :return:            The entity that is created or None if the entity is not defined in "units.dat"
        """
        for entity in self.default_entities:
            if entity.entity_id == entity_id:
                return entity.create(pos_y, pos_x)
        return None

    def prepare_new_map(self):
        """
        When starting the game, it is required to calculate the colours before the main loop is entered.
        :return: Nothing
        """
        self.brezelheim.reset_brezelheim(self.current_level)
        self.current_level.build_map_colour(self)

    def play(self):
        """
        This method handles the main loop of the game, including procession of player input and everything else.
        :return:
        """
        playing = True
        skip_npc_turn = False
        record = False
        last_input_time = time.time()

        if self.log_filename != "":
            self.log_file = open(self.log_filename, "w")
            record = True

        self.prepare_new_map()
        print(self.colours.clear())

        while playing:
            self.scr.print(record, self)
            status_effects.remove_status_effects(self)

            input_delay.apply_delay(self.configurations["input_delay"], last_input_time)
            last_input_time = time.time()
            self.user_input = readchar.readkey()
            # try:
            #     self.user_input = input()[0]
            # except IndexError:
            #     self.user_input = " "

            playing, skip_npc_turn = self.player_turn(playing, skip_npc_turn)
            if playing:
                if not skip_npc_turn:
                    self.current_level.npc_actions(self)
                    status_effects.apply_status_effects(self)
                else:
                    skip_npc_turn = False
                self.current_level.build_map_colour(self)
                if not self.player.is_alive():
                    self.scr.print(record, self)
                    playing = False
                else:
                    pass

    def player_turn(self, playing: bool, skip_npc_turn: bool):
        """
        Selects an action based on the player's input
        :param playing:
        :param skip_npc_turn:
        :return:
        """
        if self.user_input == self.keys.exit_game:
            playing = False
        elif self.user_input == self.keys.open_door or self.user_input == self.keys.close_door:
            self.current_level.door_actions(self, self.user_input)
        elif self.player.move(self.user_input, self.keys, self.current_level) == -1:
            if not self.current_level.auto_toggle(self, self.user_input):
                self.player.attack(self, self.user_input)
        elif self.user_input == self.keys.enter_entrance or self.user_input == self.keys.enter_exit:
            entrance = self.current_level.find_entrance(self)
            if entrance is not None:
                entrance.enter(self)
            skip_npc_turn = True
        elif self.user_input == self.keys.show_coordinates:
            if not self.player.show_coordinates:
                self.player.show_coordinates = True
            else:
                self.player.show_coordinates = False
        elif self.user_input == self.keys.options:
            self.options.enter_menu(self)
            skip_npc_turn = True
        return playing, skip_npc_turn


def interpret_parameters():
    """
    This function reads additional parameters.

    Currently possible are the following parameters:
        - "-log" or "-l": This parameter activates logging of the screen. A following parameter is required, which
                          contains the filename in which the log will be saved.
        - "-view" or "-v": This parameter will read the log file (next parameter).
        - "-seed" or "-s": This parameter sets a seed for the Random Number Generator. Using the same seed will always
                           lead to the same results.
    :return:
    """
    filename = ""
    set_seed = time.time()
    save_replay = False
    play_replay = False
    for parameter_number in range(len(sys.argv)):
        if sys.argv[parameter_number] == "-log" or sys.argv[parameter_number] == "-l":
            filename = sys.argv[parameter_number + 1]
            save_replay = True
        elif sys.argv[parameter_number] == "-view" or sys.argv[parameter_number] == "-v":
            filename = sys.argv[parameter_number + 1]
            play_replay = True
        elif sys.argv[parameter_number] == "-seed" or sys.argv[parameter_number] == "-s":
            try:
                set_seed = int(sys.argv[parameter_number + 1])
            except ValueError:
                pass
    return save_replay, play_replay, filename, set_seed


def get_level_file_name(language):
    """
    The first parameter is required to be the level that will be loaded while entering the game. This function extracts
    that parameter and returns it.
    :param language:    The language object of the game. Is used here to display an error message.
    :return:
    """
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        print(language.texts.get("no_level_parameter", language.undefined))
        exit(-1)


def read_configuration_file() -> dict:
    """
    This function requires the file "config.txt" in the folder "data".
    It contains the following information:
        - The language file that will be loaded.
          Default: "language_file=en_en.txt"
        - The screen height is used to define the height of the area in which the level will be displayed.
          Default: "screen_height=21"
        - The screen width is used to define the width of the area in which the level will be displayed.
          Default: "screen_width=81"
        - The input delay is used to make movement slower and more predictable. It defines the minimum period of time
          (in seconds) that is required to pass until the next input will be read.
          Default: "input_delay=0.1625"

    :return:
    """
    config = None
    error_text = "Error in \"config.txt\": Please check the line containing "
    configurations = {}
    try:
        config = open("data/config.txt", "r")
    except FileNotFoundError:
        print("\"config.txt\" could not be found.")
        exit(-1)
    lines = config.readlines()
    config.close()
    for line in lines:
        if "language_file" in line:
            try:
                configurations["language_file"] = line.split("=")[1].replace("\n", "")
            except IndexError:
                print(f"{error_text}\"language_file\"")
                exit(-1)
        elif "screen_height" in line:
            try:
                configurations["screen_height"] = int(line.split("=")[1])
            except ValueError or IndexError:
                print(f"{error_text}\"screen_height\"")
                exit(-1)
        elif "screen_width" in line:
            try:
                configurations["screen_width"] = int(line.split("=")[1])
            except ValueError or IndexError:
                print(f"{error_text}\"screen_width\"")
                exit(-1)
        elif "input_delay" in line:
            try:
                configurations["input_delay"] = float(line.split("=")[1])
            except ValueError or IndexError:
                print(f"{error_text}\"input_delay\"")
                exit(-1)

    if len(configurations) < 4:
        print("config.txt is incomplete.")
        exit(-1)
    return configurations


if __name__ == '__main__':
    record, replay, replay_filename, seed = interpret_parameters()
    if not replay:
        gtg = GateToGods(seed, replay_filename)
        gtg.play()
    else:
        colours = Colours()
        r = Replay(replay_filename, colours)
        r.play_replay(Input(), colours)
