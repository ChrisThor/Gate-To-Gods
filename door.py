class Door:
    def __init__(self, pos_y: int, pos_x: int, state: str):
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.state = state

    def interact_with_door(self, gtg, pressed_key):
        if pressed_key == gtg.keys.open_door and self.state == "closed":
            self.state = "open"
            gtg.msg_box.open_door(gtg)
            return 1
        elif pressed_key == gtg.keys.close_door and self.state == "open":
            if self.pos_y != gtg.player.pos_y or self.pos_x != gtg.player.pos_x:
                allowed_to_close = True
                for npc in gtg.current_level.npcs:
                    if npc.confirm_pos(self.pos_y, self.pos_x):
                        allowed_to_close = False
                        break

                if allowed_to_close:
                    self.state = "closed"
                    gtg.msg_box.close_door(gtg)
                    return 1
                else:
                    gtg.msg_box.cannot_close_door(gtg)
            else:
                gtg.msg_box.cannot_close_door(gtg)
        return 0

    def confirm_pos(self, pos_y, pos_x):
        if self.pos_y == pos_y and self.pos_x == pos_x:
            return True
        else:
            return False
