from message import Message


class Messagebox:
    def __init__(self, width):
        self.width = width
        self.messages = self.init_slots()
        self.message_count = 0
        self.new_message = Message()

    def init_slots(self):
        messages = []
        for i in range(5):
            message = Message()
            message.fill(self.width)
            messages.append(message)
        return messages

    def update_messagebox(self):
        if self.message_count != 5:
            self.message_count += 1
        else:
            for slot in range(4):
                self.messages[slot] = self.messages[slot + 1]

        skip = False

        self.new_message.fill(self.width)
        for slot in range(5):
            trimmed_message = self.messages[slot].content.replace(" ", "")
            if trimmed_message == "":
                del self.messages[slot]
                self.messages.insert(slot, self.new_message)
                skip = True
                break
        if not skip:
            self.messages[4] = self.new_message

    def print_msgbox(self, reciever, colours, scr):
        reciever.write(colours.get_colour("white"))
        scr.print_separator(reciever)
        for message in self.messages:
            reciever.write(message.content + "\n")

    def attack_npc(self, gtg, damage, npc):
        new_hp = npc.hp - damage
        if new_hp < 0:
            new_hp = 0
        message = gtg.language.texts.get("attack_npc_message", gtg.language.undefined)\
            .replace("(NPC_NAME)", gtg.colours.get_colour("yellow") + npc.name + gtg.colours.get_colour("white"))\
            .replace("(PLAYER_DAMAGE)", gtg.colours.get_colour("red") + str(damage) + gtg.colours.get_colour("white"))\
            .replace("(NPC_HP)", gtg.colours.get_colour("red") + str(new_hp) + gtg.colours.get_colour("white"))
        self.new_message = Message(message, 2 * len(gtg.colours.get_colour("yellow")) + 4 *
                                   len(gtg.colours.get_colour("white")) + 2 * len(gtg.colours.get_colour("red")))
        self.update_messagebox()

    def attack_player_m(self, gtg, npc, damage):
        message = gtg.language.texts.get("attack_player_message", gtg.language.undefined)\
            .replace("(NPC_NAME)", gtg.colours.get_colour("yellow") +
            npc.name + gtg.colours.get_colour("white")).replace("(NPC_DAMAGE)", gtg.colours.get_colour("red") +
            str(damage) + gtg.colours.get_colour("white")).replace("(PLAYER_HP)", gtg.colours.get_colour("red") +
            str(gtg.player.hp) + gtg.colours.get_colour("white"))
        self.new_message = Message(message, len(gtg.colours.get_colour("yellow")) + 3 *
                                   len(gtg.colours.get_colour("white")) + 2 * len(gtg.colours.get_colour("red")))
        self.update_messagebox()

    def npc_death(self, gtg, npc):
        message = gtg.colours.get_colour("cyan") + gtg.language.texts.get("npc_death_message", gtg.language.undefined)\
                  .replace("(NPC_NAME)", npc.name) + \
                  gtg.colours.get_colour("white")
        self.new_message = Message(message, len(gtg.colours.get_colour("cyan")) + len(gtg.colours.get_colour("white")))
        self.update_messagebox()

    def player_death(self, gtg):
        message = gtg.colours.get_colour("red") + \
                  gtg.language.texts.get("player_death_message", gtg.language.undefined) + \
                  gtg.colours.get_colour("white")
        self.new_message = Message(message, len(gtg.colours.get_colour("red")) + len(gtg.colours.get_colour("white")))
        self.update_messagebox()

    def cannot_close_door(self, gtg):
        self.new_message = Message(gtg.language.texts.get("cannot_close_door_message", gtg.language.undefined))
        self.update_messagebox()

    def close_door(self, gtg):
        self.new_message = Message(gtg.language.texts.get("close_door_message", gtg.language.undefined))
        self.update_messagebox()

    def open_door(self, gtg):
        self.new_message = Message(gtg.language.texts.get("open_door_message", gtg.language.undefined))
        self.update_messagebox()
