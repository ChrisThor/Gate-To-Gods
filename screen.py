import sys


class Screen:
    def __init__(self, len_y, len_x):
        self.len_y = len_y
        self.len_x = len_x
        self.separator = self.set_separator(len_x)
        self.doors = []
        self.npcs = []
        self.entrances = []
        self.content = ""

    def build_screen(self, gtg):
        self.doors = gtg.current_level.doors.copy()
        self.npcs = gtg.current_level.npcs.copy()
        self.entrances = gtg.current_level.entrances_and_exits.copy()

        self.content = gtg.colours.jump_up()
        self.content += gtg.player.print_hp(gtg.colours, self)

        for y_pixel in range(self.len_y):
            for x_pixel in range(self.len_x):
                pos_y = gtg.player.pos_y - int(self.len_y / 2) + y_pixel
                pos_x = gtg.player.pos_x - int(self.len_x / 2) + x_pixel

                if pos_y < 0 or pos_x < 0 or pos_y >= gtg.current_level.len_y or pos_x >= gtg.current_level.len_x:
                    self.content += " "
                else:
                    try:
                        if gtg.current_level.discovered[pos_y][pos_x]:
                            self.content += gtg.current_level.colours[pos_y][pos_x]
                            if gtg.player.pos_y == pos_y and gtg.player.pos_x == pos_x:
                                self.content += gtg.player.symbol
                            else:
                                if self.find_npc(pos_x, pos_y, True):
                                    continue
                                if self.find_npc(pos_x, pos_y, False):
                                    continue
                                if self.find_door(pos_x, pos_y):
                                    continue
                                if self.find_entrance(pos_y, pos_x):
                                    continue
                                self.content += gtg.current_level.level_objects[pos_y][pos_x]
                        else:
                            self.content += " "
                    except IndexError:
                        self.content += "!"
            self.content += "\n"
        self.content += gtg.colours.get_colour("white")
        self.content += self.get_separator()
        self.content += self.get_ground_information(gtg)
        self.content += gtg.msg_box.get_msgbox()
        return self.content

    def find_entrance(self, pos_y, pos_x):
        for entrance in self.entrances:
            if entrance.pos_y == pos_y and entrance.pos_x == pos_x:
                self.content += entrance.symbol
                self.entrances.remove(entrance)
                return True
        return False

    def find_door(self, pos_x, pos_y):
        for door in self.doors:
            if pos_y == door.pos_y and pos_x == door.pos_x:
                if door.state == "closed":
                    self.content += "+"
                else:
                    self.content += "'"
                self.doors.remove(door)
                return True
        return False

    def find_npc(self, pos_x, pos_y, npc_alive):
        for npc in self.npcs:
            if pos_y == npc.pos_y and pos_x == npc.pos_x:
                if npc_alive and npc.alive:
                    self.content += npc.symbol
                    self.npcs.remove(npc)
                elif not npc_alive and not npc.alive:
                    self.content += "%"
                    self.npcs.remove(npc)
                else:
                    continue
                return True
        return False

    def get_ground_information(self, gtg):
        dead_npcs = []
        for npc in gtg.current_level.npcs:
            if npc.confirm_pos(gtg.player.pos_y, gtg.player.pos_x) and not npc.alive:
                dead_npcs.append(npc)
        if len(dead_npcs) == 0:
            return "".ljust(self.len_x) + "\n"
        if len(dead_npcs) == 1:
            return gtg.language.texts.get("knocked_out_npc", gtg.language.undefined)\
                .replace("(NPC_NAME)", dead_npcs[0].name).ljust(self.len_x) + "\n"
        else:
            return gtg.language.texts.get("knocked_out_npcs", gtg.language.undefined).ljust(self.len_x) + "\n"

    def get_separator(self) -> str:
        return self.separator

    def set_separator(self, length: int):
        separator = ""
        for i in range(length):
            separator += "-"
        return separator + "\n"

    def print(self, record, gtg):
        screen = self.build_screen(gtg)
        if record:
            gtg.log_file.write(screen)
        print(screen)
