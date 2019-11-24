class LanguageManagement:
    def __init__(self):
        self.no_level_parameter = ""
        self.unitsdat_number_error = ""
        self.unitsdat_damage_error = ""
        self.unitsdat_player_not_defined = ""
        self.unitsdat_incomplete_definition = ""
        self.unitsdat_not_found = ""
        self.level_file_not_found = ""
        self.level_entity_not_defined = ""
        self.level_player_not_defined = ""
        self.attack_npc_message = ""
        self.attack_player_message = ""
        self.npc_death_message = ""
        self.player_death_message = ""
        self.cannot_close_door_message = ""
        self.close_door_message = ""
        self.open_door_message = ""
        self.read_language_file(self.get_language_file())

    def get_language_file(self):
        config = None
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
                    return line.split("=")[1].replace("\n", "")
                except IndexError:
                    print("\"config.txt\" is incorrect.")
                    exit(-1)

    def read_language_file(self, filename):
        language_file = None
        try:
            language_file = open("data/" + filename, "r")
        except FileNotFoundError:
            print("\"" + filename + "\" could not be found.")
            exit(-1)
        lines = language_file.readlines()
        language_file.close()
        for line in lines:
            if "no_level_parameter" in line:
                self.no_level_parameter = line.split("=")[1].replace("\n", "")
            elif "unitsdat_number_error" in line:
                self.unitsdat_number_error = line.split("=")[1].replace("\n", "")
            elif "unitsdat_damage_error" in line:
                self.unitsdat_damage_error = line.split("=")[1].replace("\n", "")
            elif "unitsdat_player_not_defined" in line:
                self.unitsdat_player_not_defined = line.split("=")[1].replace("\n", "")
            elif "unitsdat_incomplete_definition" in line:
                self.unitsdat_incomplete_definition = line.split("=")[1].replace("\n", "")
            elif "unitsdat_not_found" in line:
                self.unitsdat_not_found = line.split("=")[1].replace("\n", "")
            elif "level_file_not_found" in line:
                self.level_file_not_found = line.split("=")[1].replace("\n", "")
            elif "level_entity_not_defined" in line:
                self.level_entity_not_defined = line.split("=")[1].replace("\n", "")
            elif "level_player_not_defined" in line:
                self.level_player_not_defined = line.split("=")[1].replace("\n", "")
            elif "attack_npc_message" in line:
                self.attack_npc_message = line.split("=")[1].replace("\n", "")
            elif "attack_player_message" in line:
                self.attack_player_message = line.split("=")[1].replace("\n", "")
            elif "npc_death_message" in line:
                self.npc_death_message = line.split("=")[1].replace("\n", "")
            elif "player_death_message" in line:
                self.player_death_message = line.split("=")[1].replace("\n", "")
            elif "cannot_close_door_message" in line:
                self.cannot_close_door_message = line.split("=")[1].replace("\n", "")
            elif "close_door_message" in line:
                self.close_door_message = line.split("=")[1].replace("\n", "")
            elif "open_door_message" in line:
                self.open_door_message = line.split("=")[1].replace("\n", "")
