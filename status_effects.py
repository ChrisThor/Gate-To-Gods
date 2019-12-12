class StatusEffect:
    def __init__(self, effect_id, effect_name, entity, duration: int, min_cooldown: int, max_cooldown):
        entity.effects_on_entity.append(self)
        self.effect_name = effect_name
        self.enitiy = entity
        self.effect_id = effect_id
        self.duration = duration
        self.min_cooldown = min_cooldown
        self.max_cooldown = max_cooldown
        self.cooldown = 0

    def reduce_duration(self) -> bool:
        if self.duration > 0:
            self.duration -= 1
            return True
        return False

    def extend_duration_by(self, duration: int):
        self.duration += duration

    def tick_cooldown(self, gtg) -> bool:
        if self.reduce_duration():
            if self.cooldown <= 0:
                self.set_cooldown(gtg)
                return True
            else:
                self.cooldown -= 1
        return False

    def set_cooldown(self, gtg):
        self.cooldown = gtg.rng.randint(self.min_cooldown, self.max_cooldown)


def remove_effect_from_entity(entity, effect: StatusEffect):
    entity.effects_on_entity.remove(effect)


class HealingEffect(StatusEffect):
    def __init__(self, effect_id, effect_name, entity, duration, min_cooldown, max_cooldown, min_hp_gain, max_hp_gain):
        StatusEffect.__init__(self, effect_id, effect_name, entity, duration, min_cooldown, max_cooldown)
        self.min_hp_gain = min_hp_gain
        self.max_hp_gain = max_hp_gain

    def apply(self, gtg, entity):
        if self.tick_cooldown(gtg):
            entity.add_hp(gtg.rng.randint(self.min_hp_gain, self.max_hp_gain))


def set_healing_effect_values(effect_args: dict) -> dict:
    for effect_id in effect_args:
        if "-" in str(effect_args[effect_id]["hp_gain"]):
            effect_args[effect_id]["min_hp_gain"] = int(effect_args[effect_id]["hp_gain"].split("-")[0])
            effect_args[effect_id]["max_hp_gain"] = int(effect_args[effect_id]["hp_gain"].split("-")[1])
        else:
            effect_args[effect_id]["min_hp_gain"] = effect_args[effect_id]["hp_gain"]
            effect_args[effect_id]["max_hp_gain"] = effect_args[effect_id]["hp_gain"]
        del effect_args[effect_id]["hp_gain"]

        if "-" in str(effect_args[effect_id]["cooldown"]):
            effect_args[effect_id]["min_cooldown"] = int(effect_args[effect_id]["cooldown"].split("-")[0])
            effect_args[effect_id]["max_cooldown"] = int(effect_args[effect_id]["cooldown"].split("-")[1])
        else:
            effect_args[effect_id]["min_cooldown"] = effect_args[effect_id]["cooldown"]
            effect_args[effect_id]["max_cooldown"] = effect_args[effect_id]["cooldown"]
        del effect_args[effect_id]["cooldown"]

    return effect_args


def create_effect(effect_args: dict, afflicted_entity):
    HealingEffect(effect_id=effect_args["effect_id"],
                  effect_name=effect_args["name"],
                  entity=afflicted_entity,
                  duration=effect_args["duration"],
                  min_cooldown=effect_args["min_cooldown"],
                  max_cooldown=effect_args["max_cooldown"],
                  min_hp_gain=effect_args["min_hp_gain"],
                  max_hp_gain=effect_args["max_hp_gain"])


def apply_status_effects(gtg):
    for effect in gtg.player.effects_on_entity:
        effect.apply(gtg, gtg.player)
    for npc in gtg.current_level.npcs:
        for effect in npc.effects_on_entity:
            effect.apply(gtg, npc)


def remove_status_effects(gtg):
    for effect in gtg.player.effects_on_entity:
        if effect.duration <= 0:
            remove_effect_from_entity(gtg.player, effect)
    for npc in gtg.current_level.npcs:
        for effect in npc.effects_on_entity:
            if effect.duration <= 0:
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
        for effect_number in range(1, len(effects)):
            if effects[effect_number].duration > highest_value:
                return False
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
