from box import Box
import os


class OptionsMenu:
    def __init__(self, gtg):
        headline = gtg.language.texts.get("option_headline")
        options = [gtg.language.texts.get("option_change_language"), gtg.language.texts.get("option_change_screen"),
                   gtg.language.texts.get("option_go_back")]
        self.display_box = Box(content=headline, box_width=25, options=options)
        self.change_language_box = Box(content=gtg.language.texts.get("option_new_file"),
                               box_width=len(gtg.language.texts.get("option_new_file")),
                               options=os.listdir(os.getcwd() + "/data/lang"))

    def enter_menu(self, gtg):
        jump_position = "\033[" + str(gtg.scr.len_y + 8) + ";0H"
        selected_option = ""
        self.display_box.active_option = 0
        while selected_option != gtg.language.texts.get("option_go_back"):
            gtg.scr.print(False, gtg)
            selected_option = self.display_box.access_options(gtg)
            if selected_option == gtg.language.texts.get("option_change_language"):
                self.change_language(gtg)
            elif selected_option == gtg.language.texts.get("option_change_screen"):
                self.change_screen_dimensions(gtg, jump_position)
        configurations = open("data/config.txt", "w")
        for key in gtg.configurations:
            configurations.write(str(key) + "=" + str(gtg.configurations[key]) + "\n")
        configurations.close()

    def change_screen_dimensions(self, gtg, jump_position):
        Box(content=gtg.language.texts.get("option_new_screen"),
            box_width=len(gtg.language.texts.get("option_new_screen")),
            colour=gtg.colours.get_random_colour(gtg.rng, True)) \
            .print_box(gtg.scr)
        new_dimensions = input(jump_position + "> ")
        buffer = new_dimensions.split(":")
        gtg.scr.change_size(int(buffer[0]), int(buffer[1]))
        gtg.configurations["screen_height"] = buffer[0]
        gtg.configurations["screen_width"] = buffer[1]

    def change_language(self, gtg):
        self.change_language_box.colour = gtg.colours.get_random_colour(gtg.rng, True)
        for language_file in range(self.change_language_box.amount_options):
            if gtg.configurations["language_file"] == self.change_language_box.options[language_file].text:
                self.change_language_box.active_option = language_file
        new_file = self.change_language_box.access_options(gtg)
        gtg.configurations["language_file"] = new_file
