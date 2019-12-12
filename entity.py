import status_effects


class Entity:
    def __init__(self, entity_id, pos_y, pos_x, symbol, range_of_vision, hp, minimum_damage, maximum_damage, effects):
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
        self.effects_on_entity = []
        self.afflicting_on_hit = effects

    def reduce_hp(self, gtg, difference):
        self.hp -= difference
        if self.hp <= 0 and self.alive:
            self.hp = 0
            self.kill(gtg)

    def add_hp(self, added_hp: int):
        self.hp += added_hp
        if self.hp > self.max_hp:
            self.hp = self.max_hp

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

    def apply_status_effect_on_entity(self, entity, gtg) -> bool:
        applied = False
        for effect in self.afflicting_on_hit:
            allowed_to_apply = True
            for enitiy_effect in entity.effects_on_entity:
                if enitiy_effect.effect_id == effect:
                    # print("HAB DICH GEFUNDEN!" + enitiy_effect.name)
                    allowed_to_apply = False
                    break
            if not allowed_to_apply:
                break
            # print(effect)
            status_effects.create_effect(gtg.all_status_effects[effect], entity)
            applied = True
        return applied

