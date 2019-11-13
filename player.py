from entity import Entity


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
