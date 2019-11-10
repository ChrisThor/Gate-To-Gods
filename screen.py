import sys


class Screen:
    def __init__(self, len_y, len_x):
        self.len_y = len_y
        self.len_x = len_x

    def print_screen(self, gtg, reciever):
        reciever.write(gtg.colours.jump_up())
        gtg.player.print_hp(reciever, gtg.colours, self)

        for y_pixel in range(self.len_y):
            for x_pixel in range(self.len_x):
                pos_y = gtg.player.pos_y - int(self.len_y / 2) + y_pixel
                pos_x = gtg.player.pos_x - int(self.len_x / 2) + x_pixel

                if pos_y < 0 or pos_x < 0 or pos_y >= gtg.current_level.len_y or pos_x >= gtg.current_level.len_x:
                    reciever.write(" ")
                else:
                    try:
                        if gtg.current_level.discovered[pos_y][pos_x]:
                            reciever.write(gtg.current_level.colours[pos_y][pos_x])
                            if gtg.player.pos_y == pos_y and gtg.player.pos_x == pos_x:
                                reciever.write(gtg.player.symbol)
                            else:
                                continue_for_loop = self.find_npc(gtg, pos_x, pos_y, reciever)
                                if continue_for_loop:
                                    continue
                                continue_for_loop = self.find_door(gtg, pos_x, pos_y, reciever)
                                if continue_for_loop:
                                    continue
                                continue_for_loop = self.find_entrance(gtg, pos_y, pos_x, reciever)
                                if continue_for_loop:
                                    continue
                                reciever.write(gtg.current_level.level_objects[pos_y][pos_x])
                        else:
                            reciever.write(" ")
                    except IndexError:
                        reciever.write("!")
            reciever.write("\n")
        gtg.msg_box.print_msgbox(reciever, gtg.colours, self)

    def find_entrance(self, gtg, pos_y, pos_x, reciever):
        for entrance in gtg.current_level.entrances_and_exits:
            if entrance.pos_y == pos_y and entrance.pos_x == pos_x:
                reciever.write(entrance.symbol)
                return True
        return False

    def find_door(self, gtg, pos_x, pos_y, reciever):
        for door in gtg.current_level.doors:
            if pos_y == door.pos_y and pos_x == door.pos_x:
                if door.state == "closed":
                    reciever.write("+")
                else:
                    reciever.write("'")
                return True
        return False

    def find_npc(self, gtg, pos_x, pos_y, reciever):
        for npc in gtg.current_level.npcs:
            if pos_y == npc.pos_y and pos_x == npc.pos_x:
                if npc.alive and gtg.current_level.visible_to_player[pos_y][pos_x]:
                    reciever.write(npc.symbol)
                    return True
        return False

    def print_separator(self, reciever):
        for i in range(self.len_x):
            reciever.write("-")
        reciever.write("\n")

    def print(self, record, gtg):
        if record:
            self.print_screen(gtg, gtg.log_file)
        self.print_screen(gtg, sys.stdout)
