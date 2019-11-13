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
