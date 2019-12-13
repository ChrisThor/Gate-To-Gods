class StatusEffect:
    def __init__(self, effect_id, effect_name, entity, duration, min_tick, max_tick, cooldown):
        entity.effects_on_entity.append(self)
        self.effect_name = effect_name
        self.enitiy = entity
        self.effect_id = effect_id
        self.duration = duration
        self.min_tick = min_tick
        self.max_tick = max_tick
        self.tick = 0
        self.cooldown = cooldown
        self.show_effect = True

    def reduce_duration(self) -> bool:
        if self.duration > 0:
            self.duration -= 1
            return True
        return False

    def reduce_cooldown(self) -> bool:
        if self.cooldown > 0:
            self.cooldown -= 1
            return True
        return False

    def extend_duration_by(self, duration: int):
        self.duration += duration

    def do_tick(self, gtg) -> bool:
        if self.reduce_duration():
            if self.tick == 0:
                self.set_tick(gtg)
                return True
            else:
                self.tick -= 1
        elif self.reduce_cooldown():
            if self.show_effect:
                self.show_effect = False
                self.reverse()
        return False

    def set_tick(self, gtg):
        self.tick = gtg.rng.randint(self.min_tick, self.max_tick)

    def reverse(self):
        pass


def remove_effect_from_entity(entity, effect: StatusEffect):
    # effect.reverse()
    entity.effects_on_entity.remove(effect)


class HealingEffect(StatusEffect):
    def __init__(self, effect_id, effect_name, entity, duration, min_tick, max_tick, min_hp_gain, max_hp_gain,
                 cooldown):
        StatusEffect.__init__(self, effect_id, effect_name, entity, duration, min_tick, max_tick, cooldown)
        self.min_hp_gain = min_hp_gain
        self.max_hp_gain = max_hp_gain

    def apply(self, gtg, entity):
        if self.do_tick(gtg):
            entity.add_hp(gtg.rng.randint(self.min_hp_gain, self.max_hp_gain))


class DamageBoostEffect(StatusEffect):
    def __init__(self, effect_id, effect_name, entity, duration, min_boost, max_boost, cooldown):
        super().__init__(effect_id, effect_name, entity, duration, 0, 0, cooldown)
        self.min_boost = min_boost
        self.max_boost = max_boost
        self.original_min_damage = entity.minimum_damage
        self.original_max_damage = entity.maximum_damage

    def apply(self, gtg, entity):
        if self.do_tick(gtg):
            if self.enitiy.minimum_damage != self.min_boost + self.original_min_damage and \
                    self.enitiy.maximum_damage != self.max_boost + self.original_max_damage:
                self.enitiy.minimum_damage = self.original_min_damage + self.min_boost
                self.enitiy.maximum_damage = self.original_max_damage + self.max_boost

    def reverse(self):
        self.enitiy.minimum_damage = self.original_min_damage
        self.enitiy.maximum_damage = self.original_max_damage


class InvincibilityEffect(StatusEffect):
    def __init__(self, effect_id, effect_name, entity, duration, cooldown):
        super().__init__(effect_id, effect_name, entity, duration, 0, 0, cooldown)

    def apply(self, gtg, entity):
        if self.do_tick(gtg):
            if not self.enitiy.invincible:
                self.enitiy.invincible = True

    def reverse(self):
        self.enitiy.invincible = False


class InvisibilityEffect(StatusEffect):
    def __init__(self, effect_id, effect_name, entity, duration, cooldown):
        super().__init__(effect_id, effect_name, entity, duration, 0, 0, cooldown)

    def apply(self, gtg, entity):
        if self.do_tick(gtg):
            if not self.enitiy.invisible:
                self.enitiy.invisible = True

    def reverse(self):
        self.enitiy.invisible = False


def set_values(effect_args: dict, attribute_name: str, new_attribute: str) -> dict:
    if "-" in str(effect_args[attribute_name]):
        effect_args[f"min_{new_attribute}"] = int(effect_args[attribute_name].split("-")[0])
        effect_args[f"max_{new_attribute}"] = int(effect_args[attribute_name].split("-")[1])
    else:
        effect_args[f"min_{new_attribute}"] = effect_args[attribute_name]
        effect_args[f"max_{new_attribute}"] = effect_args[attribute_name]
    del effect_args[attribute_name]
    return effect_args


def set_effect_values(effects: dict) -> dict:
    for effect_id in effects:
        if effects[effect_id]["type"] == "HealingEffect":
            effects[effect_id] = set_values(effects[effect_id], "hp_gain", "hp_gain")
            effects[effect_id] = set_values(effects[effect_id], "cooldown", "cooldown")
            effects[effect_id] = set_values(effects[effect_id], "tick", "tick")
        elif effects[effect_id]["type"] == "DamageBoostEffect":
            effects[effect_id] = set_values(effects[effect_id], "damage_boost", "boost")
            effects[effect_id] = set_values(effects[effect_id], "cooldown", "cooldown")
        elif effects[effect_id]["type"] == "Invincibility" or effects[effect_id]["type"] == "Invisibility":
            effects[effect_id] = set_values(effects[effect_id], "cooldown", "cooldown")
    return effects


def create_effect(effect_args: dict, afflicted_entity, gtg):
    if effect_args["type"] == "HealingEffect":
        HealingEffect(effect_id=effect_args["effect_id"],
                      effect_name=effect_args["name"],
                      entity=afflicted_entity,
                      duration=effect_args["duration"],
                      min_tick=effect_args["min_tick"],
                      max_tick=effect_args["max_tick"],
                      min_hp_gain=effect_args["min_hp_gain"],
                      max_hp_gain=effect_args["max_hp_gain"],
                      cooldown=gtg.rng.randint(effect_args["min_cooldown"], effect_args["max_cooldown"]))
    elif effect_args["type"] == "DamageBoostEffect":
        DamageBoostEffect(effect_id=effect_args["effect_id"],
                          effect_name=effect_args["name"],
                          entity=afflicted_entity,
                          duration=effect_args["duration"],
                          min_boost=effect_args["min_boost"],
                          max_boost=effect_args["max_boost"],
                          cooldown=gtg.rng.randint(effect_args["min_cooldown"], effect_args["max_cooldown"]))
    elif effect_args["type"] == "Invincibility":
        InvincibilityEffect(effect_id=effect_args["effect_id"],
                            effect_name=effect_args["name"],
                            entity=afflicted_entity,
                            duration=effect_args["duration"],
                            cooldown=gtg.rng.randint(effect_args["min_cooldown"], effect_args["max_cooldown"]))
    elif effect_args["type"] == "Invisibility":
        InvisibilityEffect(effect_id=effect_args["effect_id"],
                           effect_name=effect_args["name"],
                           entity=afflicted_entity,
                           duration=effect_args["duration"],
                           cooldown=gtg.rng.randint(effect_args["min_cooldown"], effect_args["max_cooldown"]))


def apply_status_effects(gtg):
    for effect in gtg.player.effects_on_entity:
        effect.apply(gtg, gtg.player)
    for npc in gtg.current_level.npcs:
        for effect in npc.effects_on_entity:
            effect.apply(gtg, npc)


def remove_status_effects(gtg):
    for effect in gtg.player.effects_on_entity:
        if effect.duration <= 0 and effect.cooldown <= 0:
            remove_effect_from_entity(gtg.player, effect)
    for npc in gtg.current_level.npcs:
        for effect in npc.effects_on_entity:
            if effect.duration <= 0 and effect.cooldown <= 0:
                remove_effect_from_entity(npc, effect)


def read_status_effects_dat(gtg):
    file = None
    try:
        file = open("data/status_effects.dat", "r")
    except FileNotFoundError:
        exit(-1)
    lines = file.readlines()
    file.close()

    line = 0
    effect_templates = {}
    while line < len(lines):
        effect_properties = {"effect_id": lines[line].split(":")[0]}

        line += 1
        while line < len(lines) and lines[line][0] == " ":
            split_line = lines[line].split(":")
            effect_property = split_line[1].replace("\n", "")
            if "name" in split_line[0]:
                if effect_properties["effect_id"] in gtg.language.texts:
                    effect_property = gtg.language.texts[effect_properties["effect_id"]]
            while effect_property[0] == " ":
                effect_property = effect_property[1:]
            try:
                effect_property = int(effect_property)
            except ValueError:
                pass

            effect_properties[split_line[0].replace(" ", "")] = effect_property
            line += 1
        effect_templates[effect_properties["effect_id"]] = effect_properties
    return effect_templates


def is_sorted_by_duration(effects):
    try:
        highest_value = effects[0].duration
        for effect_number in range(0, len(effects)):
            if effects[effect_number].duration > highest_value:
                return False
            else:
                highest_value = effects[effect_number].duration
    except IndexError:
        pass
    return True


def sort_by_duration(effects):
    while not is_sorted_by_duration(effects):
        for effect_number in range(1, len(effects)):
            if effects[effect_number].duration > effects[effect_number - 1].duration:
                buffer = effects[effect_number]
                effects[effect_number] = effects[effect_number - 1]
                effects[effect_number - 1] = buffer
    return effects
