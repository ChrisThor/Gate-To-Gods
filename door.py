class Door:
    def __init__(self, pos_y: int, pos_x: int, state: str):
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.state = state

    def interact_with_door(self, pressed_key, keys, msg, player, npcs):
        if pressed_key == keys.open_door and self.state == "closed":
            self.state = "open"
            msg.open_door()
            return 1
        elif pressed_key == keys.close_door:
            if self.pos_y != player.pos_y or self.pos_x != player.pos_x:
                allowed_to_close = True
                for npc in npcs:
                    if npc.confirm_pos(self.pos_y, self.pos_x):
                        allowed_to_close = False
                        break

                if allowed_to_close:
                    self.state = "closed"
                    msg.close_door()
                    return 1
                else:
                    msg.cannot_close_door()
            else:
                msg.cannot_close_door()
        return 0

    def confirm_pos(self, pos_y, pos_x):
        if self.pos_y == pos_y and self.pos_x == pos_x:
            return True
        else:
            return False


def door_actions(pressed_key, player, keys, msg, level):
    result = -1
    for y in range(player.pos_y - 1, player.pos_y + 2):
        for x in range(player.pos_x - 1, player.pos_x + 2):
            for door in level.doors:
                if door.confirm_pos(y, x) and not x == y == 0:
                    result += door.interact_with_door(pressed_key, keys, msg, player, level.npcs)
    return result


def auto_toggle(player, keys, pressed_key, msg, level):
    pos_y, pos_x = keys.get_direction_value(pressed_key, player.pos_y, player.pos_x)
    for door in level.doors:
        if door.confirm_pos(pos_y, pos_x) and door.state == "closed":
            door.interact_with_door(keys.open_door, keys, msg, player, level.npcs)
            return True
    return False
