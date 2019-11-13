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
            message.fill(self.width, False)
            messages.append(message)
        return messages

    def update_messagebox(self, colour_mode):
        if self.message_count != 5:
            self.message_count += 1
        else:
            for slot in range(4):
                self.messages[slot] = self.messages[slot + 1]

        skip = False

        self.new_message.fill(self.width, colour_mode)
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

    def attack_npc(self, damage, npc, colours):
        new_hp = npc.hp - damage
        if new_hp < 0:
            new_hp = 0

        if colours.beautiful_colours:
            message = "Du greifst " + colours.get_colour("yellow") + npc.name + colours.get_colour("white") + " mit " \
                      + colours.get_colour("red") + str(damage) + colours.get_colour("white") + " Schaden an. " + \
                      colours.get_colour("yellow") + npc.name + colours.get_colour("white") + " hat " + \
                      colours.get_colour("red") + str(new_hp) + colours.get_colour("white") + " Lebenspunkte übrig."
            self.new_message = Message(message, 2 * len(colours.get_colour("yellow")) + 4 *
                                       len(colours.get_colour("white")) + 2 * len(colours.get_colour("red")))
        else:
            self.new_message = Message("Du greifst " + npc.name + " mit " + str(damage) + " Schaden an. " + npc.name +
                                       " hat " + str(new_hp) + " Lebenspunkte übrig.")
        self.update_messagebox(colours.beautiful_colours)

    def attack_player(self, player, npc, damage, colours):
        if colours.beautiful_colours:
            message = colours.get_colour("yellow") + npc.name + colours.get_colour("white") + \
                               " greift dich an. Du verlierst " + colours.get_colour("red") + \
                               str(damage) + colours.get_colour("white") + " von " + colours.get_colour("red") + \
                               str(player.hp) + colours.get_colour("white") + " Lebenspunkten."
            self.new_message = Message(message, len(colours.get_colour("yellow")) + 3 *
                                       len(colours.get_colour("white")) + 2 * len(colours.get_colour("red")))
        else:
            self.new_message = Message(npc.name + " greift dich an. Du verlierst " + str(damage) + " von " +
                                       str(player.hp) + " Lebenspunkten.")
        self.update_messagebox(colours.beautiful_colours)

    def npc_death(self, colours, npc):
        if colours.beautiful_colours:
            message = colours.get_colour("cyan") + npc.name + " sackt bewusstlos zusammen." + \
                               colours.get_colour("white")
            self.new_message = Message(message, len(colours.get_colour("cyan")) +
                                       len(colours.get_colour("white")))
        else:
            self.new_message = Message(npc.name + " sackt bewusstlos zusammen.")
        self.update_messagebox(colours.beautiful_colours)

    def player_death(self, colours):
        if colours.beautiful_colours:
            message = colours.get_colour("red") + "Du wurdest überwältigt." + colours.get_colour("white")
            self.new_message = Message(message, len(colours.get_colour("red")) + len(colours.get_colour("white")))
        else:
            self.new_message = Message("Du wurdest überwältigt.")
        self.update_messagebox(colours.beautiful_colours)

    def cannot_close_door(self):
        self.new_message = Message("Die Türe kann nicht geschlossen werden.")
        self.update_messagebox(False)

    def close_door(self):
        self.new_message = Message("Du schließt eine Tür.")
        self.update_messagebox(False)

    def open_door(self):
        self.new_message = Message("Du öffnest eine Tür.")
        self.update_messagebox(False)
