class Entity:
    def __init__(self, pos_y, pos_x, symbol, range_of_vision, hp, minimum_damage, maximum_damage):
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.symbol = symbol
        self.name = ""
        self.range = range_of_vision
        self.hp = hp
        self.max_hp = hp
        self.minimum_damage = minimum_damage
        self.maximum_damage = maximum_damage
        self.show_coordinates = False
        self.alive = True

    def change_hp(self, difference, msg, colours):
        self.hp -= difference
        if self.hp <= 0 and self.alive:
            self.hp = 0
            self.kill(msg, colours)

    def kill(self, msg, colours):
        self.alive = False

    def is_alive(self):
        return self.alive

    def calculate_fov(self, brezelheim, level):
        for i in range(-self.range, self.range + 1):
            brezelheim.draw_brezelheim(level, self.pos_y, self.pos_x, self.pos_y + i, self.pos_x - self.range,
                                       self.range)
            brezelheim.draw_brezelheim(level, self.pos_y, self.pos_x, self.pos_y + i, self.pos_x + self.range,
                                       self.range)
            brezelheim.draw_brezelheim(level, self.pos_y, self.pos_x, self.pos_y - self.range, self.pos_x + i,
                                       self.range)
            brezelheim.draw_brezelheim(level, self.pos_y, self.pos_x, self.pos_y + self.range, self.pos_x + i,
                                       self.range)


class Player(Entity):
    def print_hp(self, reciever, colours, scr):
        colour = ""
        if self.hp < 20:
            colour = colours.get_colour("red")
        else:
            colour = colours.get_colour("white")

        reciever.write(colour + "HP: " + str(self.hp).rjust(len(str(self.max_hp))) + "/" +
                       str(self.max_hp))
        if self.show_coordinates:
            reciever.write("\tX: " + str(self.pos_x) + " Y: " + str(self.pos_y).ljust(4, " "))
        reciever.write("\n" + colours.get_colour("white"))
        scr.print_separator(reciever)

    def move(self, key, keys, level):
        pos_y, pos_x = keys.get_direction_value(key, self.pos_y, self.pos_x)

        if pos_y == self.pos_y and pos_x == self.pos_x:
            return 1
        elif level.is_walkable(pos_y, pos_x):
            self.pos_y = pos_y
            self.pos_x = pos_x
            return 0
        else:
            return -1

    def kill(self, msg, colours):
        self.alive = False
        msg.player_death(colours)

    def attack(self, npcs, keys, pressed_key, msg, colours, rng):
        pos_y, pos_x = keys.get_direction_value(pressed_key, self.pos_y, self.pos_x)
        for npc in npcs:
            if npc.pos_y == pos_y and npc.pos_x == pos_x and npc.is_alive():
                damage = rng.next_random_number(self.minimum_damage, self.maximum_damage)
                msg.attack_npc(damage, npc, colours)
                npc.change_hp(damage, msg, colours)


class Person(Entity):
    def __init__(self, pos_y, pos_x, symbol, name, range_of_vision, hp, minimum_damage, maximum_damage):
        Entity.__init__(self, pos_y, pos_x, symbol, range_of_vision, hp, minimum_damage, maximum_damage)
        self.name = name
        if symbol == "E":
            self.aggressive = True
        elif symbol == "p":
            self.aggressive = False
        self.visible = []

    def kill(self, msg, colours):
        self.alive = False
        msg.npc_death(colours, self)

    def change_hp(self, difference, msg, colours):
        if not self.aggressive:
            self.aggressive = True
        self.hp -= difference
        if self.hp <= 0 and self.alive:
            self.hp = 0
            self.kill(msg, colours)

    def move(self, player, level):
        if self.is_alive() and self.aggressive:
            dy = player.pos_y - self.pos_y
            dx = player.pos_x - self.pos_x

            new_y = self.pos_y
            new_x = self.pos_x

            if dx == 0 or dy == 0:
                if abs(dx) >= abs(dy):
                    if dx > 0:
                        new_x += 1
                    else:
                        new_x -= 1
                else:
                    if dy > 0:
                        new_y += 1
                    else:
                        new_y -= 1
            else:
                if dx > 0:
                    new_x += 1
                else:
                    new_x -= 1
                if dy > 0:
                    new_y += 1
                else:
                    new_y -= 1

            if level.is_walkable(new_y, new_x):
                self.pos_y = new_y
                self.pos_x = new_x

    def attack_player(self, player, msg, colours, rng):
        if self.aggressive:
            damage = rng.next_random_number(self.minimum_damage, self.maximum_damage)
            if damage > player.hp:
                damage = player.hp
            msg.attack_player(player, self, damage, colours)
            player.change_hp(damage, msg, colours)

    def confirm_pos(self, pos_y, pos_x):
        if self.pos_y == pos_y and self.pos_x == pos_x:
            return True
        else:
            return False
