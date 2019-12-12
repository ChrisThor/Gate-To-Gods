from non_player_character import NonPlayerCharacter
from player import Player


class DefaultEntity:
    def __init__(self,
                 entity_id: str,
                 name: str,
                 range_of_vision: int,
                 hp: int,
                 minimum_damage: int,
                 maximum_damage: int,
                 aggressive: bool,
                 status_effects: dict):
        self.entity_id = entity_id
        self.name = name
        self.range_of_vision = range_of_vision
        self.hp = hp
        self.minimum_damage = minimum_damage
        self.maximum_damage = maximum_damage
        self.aggressive = aggressive
        self.afflicting_effects_on_hit = status_effects

    def create(self, pos_y, pos_x):
        if self.entity_id == "Player":
            return Player(self.entity_id, pos_y, pos_x, "@", self.range_of_vision, self.hp, self.minimum_damage, self.maximum_damage, self.afflicting_effects_on_hit)
        symbol = ""
        if self.aggressive:
            symbol = "E"
        else:
            symbol = "p"
        return NonPlayerCharacter(self.entity_id, pos_y, pos_x, symbol, self.aggressive, self.name, self.range_of_vision, self.hp, self.minimum_damage,
                                  self.maximum_damage, self.afflicting_effects_on_hit)
