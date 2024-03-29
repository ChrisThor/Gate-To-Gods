from entity import Entity
import calculate_chance


class Player(Entity):
    def __init__(self, entity_id, pos_y, pos_x, symbol, range_of_vision, hp, minimum_damage, maximum_damage, effects, accuracy):
        super().__init__(entity_id, pos_y, pos_x, symbol, range_of_vision, hp, minimum_damage, maximum_damage, effects, accuracy)
        self.has_moved = False

    def print_hp(self, colours, scr):
        if self.hp < 20:
            colour = colours.get_colour("red")
        else:
            colour = colours.get_colour("white")

        receiver = ""
        if self.show_coordinates:
            receiver += "\tX: " + str(self.pos_x) + " Y: " + str(self.pos_y).ljust(4, " ")
        else:
            receiver += f"{colour}HP: {str(self.hp).rjust(len(str(self.max_hp)))}/{self.max_hp}".ljust(scr.len_x)
        receiver += "\n" + colours.get_colour("white")
        receiver += scr.get_separator()
        return receiver

    def move(self, key, keys, level):
        pos_y, pos_x = keys.get_direction_value(key, self.pos_y, self.pos_x)

        if pos_y == self.pos_y and pos_x == self.pos_x:
            self.has_moved = False
            return 1
        elif level.is_walkable(pos_y, pos_x):
            self.has_moved = True   # To detect, when to disable "hit_py_player" attribute of npc
            self.pos_y = pos_y
            self.pos_x = pos_x
            return 0
        else:
            self.has_moved = False
            return -1

    def kill(self, gtg):
        self.alive = False
        gtg.msg_box.player_death(gtg)

    def attack(self, gtg, pressed_key):
        pos_y, pos_x = gtg.keys.get_direction_value(pressed_key, self.pos_y, self.pos_x)
        for npc in gtg.current_level.npcs:
            if npc.pos_y == pos_y and npc.pos_x == pos_x and npc.is_alive():
                if not npc.invincible:
                    if calculate_chance.calculate_chance(gtg.rng, self.accuracy):
                        damage = gtg.rng.randint(self.minimum_damage, self.maximum_damage)
                        gtg.msg_box.attack_npc(gtg, damage, npc)
                        npc.reduce_hp(gtg, damage)
                        npc.hit_by_player = True
                        self.apply_status_effect_on_entity(npc, gtg)
                    else:
                        gtg.msg_box.player_missed_npc(gtg, npc)
                else:
                    pass    # TODO: NPC is invincible message
