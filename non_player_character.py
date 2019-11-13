from entity import Entity


class NonPlayerCharacter(Entity):
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
