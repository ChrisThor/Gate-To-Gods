from entity import Entity


class Player(Entity):
    def print_hp(self, colours, scr):
        if self.hp < 20:
            colour = colours.get_colour("red")
        else:
            colour = colours.get_colour("white")

        receiver = colour + "HP: " + str(self.hp).rjust(len(str(self.max_hp))) + "/" + str(self.max_hp)
        if self.show_coordinates:
            receiver += "\tX: " + str(self.pos_x) + " Y: " + str(self.pos_y).ljust(4, " ")
        receiver += "\n" + colours.get_colour("white")
        receiver += scr.get_separator()
        return receiver

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

    def kill(self, gtg):
        self.alive = False
        gtg.msg_box.player_death(gtg)

    def attack(self, gtg, pressed_key):
        pos_y, pos_x = gtg.keys.get_direction_value(pressed_key, self.pos_y, self.pos_x)
        for npc in gtg.current_level.npcs:
            if npc.pos_y == pos_y and npc.pos_x == pos_x and npc.is_alive():
                damage = gtg.rng.next_random_number(self.minimum_damage, self.maximum_damage)
                gtg.msg_box.attack_npc(gtg, damage, npc)
                npc.change_hp(gtg, damage)
