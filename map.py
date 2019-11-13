import entities
import door
import entrance


class Map:
    def __init__(self, file, player):
        self.len_y = 0
        self.len_x = 0
        self.name = file
        self.walkable_level_objects = "."
        self.level_objects = []
        self.discovered = []
        self.visible_to_player = []
        self.visible_to_npc = []
        self.colours = []
        self.doors = []
        self.npcs = []
        self.entrances_and_exits = []
        self.open_map(file, player)
        self.init_tile_visibility()

    def init_tile_visibility(self):
        for pos_y in range(self.len_y):
            discovered_x = []
            for pos_x in range(self.len_x):
                discovered_x.append(False)
            self.discovered.append(discovered_x)

    def reset_colours(self, colours):
        self.colours = []
        for pos_y in range(self.len_y):
            colours_x = []
            for pos_x in range(self.len_x):
                colours_x.append(colours.get_colour("grey"))
            self.colours.append(colours_x)

    def open_map(self, file, player):
        level_file = ""
        try:
            level_file = open(file, "r")
        except FileNotFoundError:
            print("Die Datei \"" + file + "\" konnte nicht gefunden werden.")
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
                if "Player" in line:
                    player_defined = True
                    player.pos_y = pos_y
                    player.pos_x = pos_x
                elif "Person" in line:
                    self.npcs.append(entities.Person(pos_y, pos_x, "p", "Person", 3, 40, 10, 10))
                elif "Drunkard" in line:
                    self.npcs.append(entities.Person(pos_y, pos_x, "E", "Betrunkener", 5, 10, 1, 1))
                elif "PrairieDog" in line:
                    self.npcs.append(entities.Person(pos_y, pos_x, "E", "Präriehund", 4, 20, 1, 2))
                elif "Door" in line:
                    self.doors.append(door.Door(pos_y, pos_x, "closed"))
                elif "Entrance" in line:
                    self.init_entrance(line, pos_x, pos_y, ">")
                elif "Exit" in line:
                    self.init_entrance(line, pos_x, pos_y, "<")
        if not player_defined and player.pos_x == -1 and player.pos_y == -1:
            print("Es darf kein Level gestartet werden, in dem keine Spielerkoordinaten definiert sind.")
            exit(-1)
        level_file.close()

    def init_entrance(self, line, pos_x, pos_y, symbol):
        map_name = line.split(":")[3]
        if "\n" in map_name:
            map_name = map_name[:-1]
        self.entrances_and_exits.append(entrance.Entrance(pos_y, pos_x, map_name, symbol))

    def find_entrance(self, gtg):
        for entrance in self.entrances_and_exits:
            if entrance.pos_y == gtg.player.pos_y and entrance.pos_x == gtg.player.pos_x:
                return entrance
        return None

    def set_visible_to_player(self, brezel):
        self.visible_to_player = brezel.brezelheimable

    def set_visible_to_npc(self, brezel):
        self.visible_to_npc = brezel.brezelheimable

    def build_map_colour(self, brezel, player, colours):
        brezel.reset_brezelheim(self)
        self.reset_colours(colours)

        player.calculate_fov(brezel, self)
        self.set_visible_to_player(brezel)
        brezel.reset_brezelheim(self)

        self.calculate_npcs_fov(brezel)
        # self.set_visible_to_npc(brezel)

        self.colour_level(colours, brezel)

    def calculate_npcs_fov(self, brezelheim):
        for npc in self.npcs:
            if npc.is_alive:
                brezelheim.reset_brezelheim(self)
                npc.calculate_fov(brezelheim, self)
                npc.visible = brezelheim.brezelheimable

    def colour_level(self, colours, brezel):
        for pos_y in range(self.len_y):
            for pos_x in range(self.len_x):
                if self.visible_to_player[pos_y][pos_x]:
                    self.colours[pos_y][pos_x] = colours.get_colour("white")
                    self.discovered[pos_y][pos_x] = True

                    for npc in self.npcs:
                        if npc.is_alive() and self.visible_to_player[npc.pos_y][npc.pos_x] and \
                                brezel.check_distance(npc.pos_y - pos_y, npc.pos_x - pos_x, npc.range) and \
                                npc.visible[pos_y][pos_x]:
                            # brezel.draw_brezelheim(self, npc.pos_y, npc.pos_x, pos_y, pos_x, npc.range):
                            # self.colours[pos_y][pos_x] = colours.get_colour("green")
                            self.colours[pos_y][pos_x] = colours.get_colour("yellow")

    def find_object_on_level(self, objects, pos_y, pos_x):  # should be replaced or deleted
        counter = 0
        for o in objects:
            if o.confirm_pos(pos_y, pos_x):
                return counter
            counter += 1
        return -1

    def is_walkable(self, pos_y, pos_x):
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

    def is_visible(self, pos_y, pos_x):
        if pos_y < 0 or pos_x < 0 or pos_y >= self.len_y or pos_x >= self.len_x:
            return False
        elif self.level_objects[pos_y][pos_x] in self.walkable_level_objects:
            door = self.find_object_on_level(self.doors, pos_y, pos_x)
            walkable = False
            if door != -1 and self.doors[door].state == "open":
                walkable = True
            elif door == -1:
                walkable = True
            if walkable:
                return True
        return False

    def npc_actions(self, player, brezelheim, msg, colours, rng):
        for npc in self.npcs:
            if npc.visible[player.pos_y][player.pos_x] and npc.is_alive() and player.is_alive():
                if brezelheim.check_distance(npc.pos_y - player.pos_y, npc.pos_x - player.pos_x, 1.5):
                    npc.attack_player(player, msg, colours, rng)
                else:
                    npc.move(player, self)

    def door_actions(self, pressed_key, gtg):
        result = -1
        for y in range(gtg.player.pos_y - 1, gtg.player.pos_y + 2):
            for x in range(gtg.player.pos_x - 1, gtg.player.pos_x + 2):
                for door in self.doors:
                    if door.confirm_pos(y, x) and not x == y == 0:
                        result += door.interact_with_door(pressed_key, gtg.keys, gtg.msg_box, gtg.player,
                                                          self.npcs)
        return result

    def auto_toggle(self, player, keys, pressed_key, msg):
        pos_y, pos_x = keys.get_direction_value(pressed_key, player.pos_y, player.pos_x)
        for door in self.doors:
            if door.confirm_pos(pos_y, pos_x) and door.state == "closed":
                door.interact_with_door(keys.open_door, keys, msg, player, self.npcs)
                return True
        return False
