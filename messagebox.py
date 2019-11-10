class Messagebox:
    def __init__(self):
        self.messages = self.init_slots()
        self.message_count = 0
        self.new_message = ""

    def init_slots(self):
        return ["", "", "", "", ""]

    def fill_message(self, message, length):
        return message.ljust(length)

    def update_messagebox(self):
        if self.message_count != 5:
            self.message_count += 1
        else:
            for slot in range(4):
                self.messages[slot] = self.messages[slot + 1]

        skip = False

        for message in range(5):
            if self.messages[message] == "":
                self.messages[message] = self.fill_message(self.new_message, 81)
                skip = True
                break
        if not skip:
            self.messages[4] = self.fill_message(self.new_message, 81)

    def print_msgbox(self, reciever, colours, scr):
        reciever.write(colours.get_colour("white"))
        scr.print_separator(reciever)
        for msg in self.messages:
            reciever.write(msg + "\n")

    def attack_npc(self, damage, npc, colours):
        new_hp = npc.hp - damage
        if new_hp < 0:
            new_hp = 0

        if colours.beautiful_colours:
            self.new_message = "Du greifst " + colours.get_colour("yellow") + npc.name + colours.get_colour("white") + \
                               " mit " + colours.get_colour("red") + str(damage) + colours.get_colour("white") \
                               + " Schaden an. " + colours.get_colour("yellow") + npc.name + colours.get_colour("white") \
                               + " hat " + colours.get_colour("red") + str(new_hp) + \
                               colours.get_colour("white") + " Lebenspunkte übrig."
        else:
            self.new_message = "Du greifst " + npc.name + " mit " + str(damage) + " Schaden an. " + npc.name + " hat " + \
                               str(new_hp) + " Lebenspunkte übrig."
        self.update_messagebox()

    def attack_player(self, player, npc, damage, colours):
        if colours.beautiful_colours:
            self.new_message = colours.get_colour("yellow") + npc.name + colours.get_colour("white") + \
                               " greift dich an. Du verlierst " + colours.get_colour("red") + \
                               str(damage) + colours.get_colour("white") + " von " + colours.get_colour("red") + \
                               str(player.hp) + colours.get_colour("white") + " Lebenspunkten."
        else:
            self.new_message = npc.name + " greift dich an. Du verlierst " + str(damage) + " von " + str(player.hp) \
                               + " Lebenspunkten."
        self.update_messagebox()

    def npc_death(self, colours, npc):
        if colours.beautiful_colours:
            self.new_message = colours.get_colour("cyan") + npc.name + " sackt bewusstlos zusammen." + \
                               colours.get_colour("white")
        else:
            self.new_message = npc.name + " sackt bewusstlos zusammen."
        self.update_messagebox()

    def player_death(self, colours):
        if colours.beautiful_colours:
            self.new_message = colours.get_colour("red") + "Du wurdest überwältigt." + colours.get_colour("white")
        else:
            self.new_message = "Du wurdest überwältigt."
        self.update_messagebox()

    def cannot_close_door(self):
        self.new_message = "Die Türe kann nicht geschlossen werden."
        self.update_messagebox()

    def close_door(self):
        self.new_message = "Du schließt eine Tür."
        self.update_messagebox()

    def open_door(self):
        self.new_message = "Du öffnest eine Tür."
        self.update_messagebox()
