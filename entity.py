class Entity:
    def __init__(self, entity_id, pos_y, pos_x, symbol, range_of_vision, hp, minimum_damage, maximum_damage):
        self.entity_id = entity_id
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

    def change_hp(self, gtg, difference):
        self.hp -= difference
        if self.hp <= 0 and self.alive:
            self.hp = 0
            self.kill(gtg)

    def kill(self, gtg):
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
