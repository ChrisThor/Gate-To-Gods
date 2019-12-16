from door import Door
from entrance import Entrance


class Map:
    def __init__(self, file, gtg):
        self.len_y = 0
        self.len_x = 0
        self.name = file
        self.walkable_level_objects = "."
        self.level_objects = []
        self.discovered = []
        self.visible_to_player = []
        self.colours = []
        self.doors = []
        self.npcs = []
        self.entrances_and_exits = []
        self.open_map(file, gtg)
        self.init_tile_visibility()

    def init_tile_visibility(self):
        """
        Creates a 2D-List corresponding to the size of the loaded level with "False" values.
        Only tiles with "True" are visible (discovered)
        :return: Nothing
        """
        for pos_y in range(self.len_y):
            discovered_x = []
            for pos_x in range(self.len_x):
                discovered_x.append(False)
            self.discovered.append(discovered_x)

    def reset_colours(self, colours):
        """
        Creates a new 2D-List containing the default colour "grey" of the level.
        :param colours:     The colours object of the game.
        :return:            Nothing
        """
        self.colours = []
        for pos_y in range(self.len_y):
            colours_x = []
            for pos_x in range(self.len_x):
                colours_x.append(colours.get_colour("grey"))
            self.colours.append(colours_x)

    def open_map(self, file, gtg):
        """
        This method loads a level from a file.
        :param file:    The file which contains the level.
        :param gtg:     The game object
        :return:
        """
        level_file = ""
        try:
            level_file = open(file, "r")
        except FileNotFoundError:
            print(gtg.language.texts.get("level_file_not_found", gtg.language.undefined).replace("(FILE)", file))
            exit(-1)

        loopstate = 0
        player_defined = False
        for line in level_file:
            if line == "---\n":
                loopstate = 1
            elif loopstate == 0:
                if "\n" in line:
                    line = line[:-1]
                self.level_objects.append(line)
                self.len_y += 1
                if len(line) > self.len_x:
                    self.len_x = len(line)
            elif loopstate == 1:
                parts = line.split("/")
                pos_y = int(parts[1].split(")")[0])
                pos_x = int(parts[0].split("(")[1])

                if line[0] == "U":
                    if "Player" in line:
                        player_defined = True
                        gtg.player.pos_y = pos_y
                        gtg.player.pos_x = pos_x
                    else:
                        entity_id = line.split(":")[2].replace("\n", "")
                        entity = gtg.set_entity(entity_id, pos_y, pos_x)
                        if entity is None:
                            print(gtg.language.texts.get("level_entity_not_defined", gtg.language.undefined)
                                  .replace("(ENTITY_ID)", entity_id))
                            exit(-1)
                        self.npcs.append(entity)
                elif "Door" in line:
                    self.doors.append(Door(pos_y, pos_x, "closed"))
                elif "Entrance" in line:
                    self.init_entrance(line, pos_x, pos_y, ">")
                elif "Exit" in line:
                    self.init_entrance(line, pos_x, pos_y, "<")
        if not player_defined and gtg.player.pos_x == -1 and gtg.player.pos_y == -1:
            print(gtg.language.texts.get("level_player_not_defined", gtg.language.undefined))
            exit(-1)
        level_file.close()

    def init_entrance(self, line, pos_x, pos_y, symbol):
        """
        Creates an entrance and saves the linked map in that entrance
        :param line:    the line inside the level file which contains the information for this entrance
        :param pos_x:   x-coordinate of the entrance
        :param pos_y:   y-coordinate of the entrance
        :param symbol:  the symbol which is shown at the position
        :return:        Nothing
        """
        map_name = line.split(":")[3]
        if "\n" in map_name:
            map_name = map_name[:-1]
        self.entrances_and_exits.append(Entrance(pos_y, pos_x, map_name, symbol))

    def find_entrance(self, gtg):
        """
        This method is used to find an entrance when the player has hit the key to enter an entrance.
        If there is an entrance at the position of the player, that entrance is returned.
        If there is not an entrance, None will be returned.
        :param gtg: The game object
        :return:    The Entrance
        """
        for entrance in self.entrances_and_exits:
            if entrance.pos_y == gtg.player.pos_y and entrance.pos_x == gtg.player.pos_x:
                return entrance
        return None

    def set_visible_to_player(self, brezelheim):
        """
        This method saves the area the player sees.
        :param brezelheim:  The brezelheim object of the game
        :return:            Nothing
        """
        self.visible_to_player = brezelheim.brezelheimable

    def build_map_colour(self, gtg):
        """
        This method handles the calculation of FOV of every entity and the colours in which the level will be shown.
        :param gtg: The game object
        :return:    Nothing
        """
        gtg.brezelheim.reset_brezelheim(self)
        self.reset_colours(gtg.colours)

        gtg.player.calculate_fov(gtg.brezelheim, self)
        self.set_visible_to_player(gtg.brezelheim)
        gtg.brezelheim.reset_brezelheim(self)

        self.calculate_npcs_fov(gtg.brezelheim)

        self.colour_level(gtg)

    def calculate_npcs_fov(self, brezelheim):
        """
        Calculates the FOV of every NPC on this level.
        :param brezelheim:  The brezelheim object of the game
        :return:            Nothing
        """
        for npc in self.npcs:
            if npc.is_alive:
                brezelheim.reset_brezelheim(self)
                npc.calculate_fov(brezelheim, self)
                npc.visible = brezelheim.brezelheimable

    def colour_level(self, gtg):
        """
        After all the FOV calculation, this method will set the colours for the current frame.
        :param gtg: The game object
        :return:    Nothing
        """
        for pos_y in range(self.len_y):
            for pos_x in range(self.len_x):
                if self.visible_to_player[pos_y][pos_x]:
                    self.discovered[pos_y][pos_x] = True
                    if not gtg.player.drugged:
                        self.colours[pos_y][pos_x] = gtg.colours.get_colour("white")

                        for npc in self.npcs:
                            if npc.is_alive() and not npc.invisible and \
                                    self.visible_to_player[npc.pos_y][npc.pos_x] and \
                                    gtg.brezelheim.check_distance(npc.pos_y - pos_y, npc.pos_x - pos_x, npc.range) and \
                                    npc.visible[pos_y][pos_x]:
                                self.colours[pos_y][pos_x] = gtg.colours.get_colour("yellow")
                    else:
                        self.colours[pos_y][pos_x] = gtg.colours.get_random_colour(gtg.rng, True)

    def is_walkable(self, pos_y, pos_x):
        """
        Checks if the targeted tile is walkable.
        :param pos_y:   y-coordinate of the targeted tile.
        :param pos_x:   x-coordinate of the targeted tile.
        :return:        True, if walkable
                        False, if not
        """
        if self.len_y > pos_y >= 0 and self.len_x > pos_x >= 0:
            try:
                if self.level_objects[pos_y][pos_x] in self.walkable_level_objects:
                    for door in self.doors:
                        if door.pos_y == pos_y and door.pos_x == pos_x and door.state == "closed":
                            return False
                    for npc in self.npcs:
                        if npc.pos_y == pos_y and npc.pos_x == pos_x and npc.is_alive():
                            return False
                    return True
                return False
            except IndexError:
                return False
        else:
            return False

    def is_visible(self, pos_y, pos_x):
        """
        Checks if the targeted tile can be seen through.
        :param pos_y:   y-coordinate of the targeted tile.
        :param pos_x:   x-coordinate of the targeted tile.
        :return:        True, if possible
                        False, if not
        """
        if self.len_y > pos_y >= 0 and self.len_x > pos_x >= 0:
            if self.level_objects[pos_y][pos_x] in self.walkable_level_objects:
                for door in self.doors:
                    if door.confirm_pos(pos_y, pos_x) and door.state == "closed":
                        return False
                return True
        return False

    def npc_actions(self, gtg):
        """
        Takes care of all the actions that all the NPCs on this map will perform.
        :param gtg:     The game object
        :return:        Nothing
        """
        for npc in self.npcs:
            if gtg.player.has_moved and npc.hit_by_player:
                npc.hit_by_player = False
            if npc.visible[gtg.player.pos_y][gtg.player.pos_x] and npc.is_alive() and gtg.player.is_alive():
                if gtg.brezelheim.check_distance(npc.pos_y - gtg.player.pos_y, npc.pos_x - gtg.player.pos_x, 1.5):
                    npc.attack_player(gtg)
                elif not gtg.player.invisible:
                    npc.move(gtg.player, self)

    def door_actions(self, gtg, pressed_key):
        """
        This function opens or closes all doors around the player.
        :param gtg:         The game object
        :param pressed_key: Open or close door command
        :return:
        """
        result = -1
        for y in range(gtg.player.pos_y - 1, gtg.player.pos_y + 2):
            for x in range(gtg.player.pos_x - 1, gtg.player.pos_x + 2):
                for door in self.doors:
                    if door.confirm_pos(y, x) and not x == y == 0:
                        result += door.interact_with_door(gtg, pressed_key)
        return result

    def auto_toggle(self, gtg, pressed_key):
        """
        If the player couldn't move, this method checks if there is a door that can be opened instead.
        :param gtg:         The game object
        :param pressed_key: The direction key
        :return:
        """
        pos_y, pos_x = gtg.keys.get_direction_value(pressed_key, gtg.player.pos_y, gtg.player.pos_x)
        for door in self.doors:
            if door.confirm_pos(pos_y, pos_x) and door.state == "closed":
                door.interact_with_door(gtg, gtg.keys.open_door)
                return True
        return False
