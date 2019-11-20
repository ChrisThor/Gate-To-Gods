import map


class Entrance:
    def __init__(self, pos_y, pos_x, linked_map, symbol):
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.linked_map = linked_map
        self.symbol = symbol

    def enter(self, gtg):
        skip = False
        for level in gtg.maps:
            if level.name == self.linked_map:
                for entrance in level.entrances_and_exits:
                    if entrance.linked_map == gtg.current_level.name:
                        gtg.player.pos_y = entrance.pos_y
                        gtg.player.pos_x = entrance.pos_x
                        break
                gtg.current_level = level
                skip = True
                break
        if not skip:
            new_level = map.Map(self.linked_map, gtg)
            for entrance in new_level.entrances_and_exits:
                if entrance.linked_map == gtg.current_level.name:
                    gtg.player.pos_y = entrance.pos_y
                    gtg.player.pos_x = entrance.pos_x
                    break
            gtg.current_level = new_level
            gtg.maps.append(new_level)
