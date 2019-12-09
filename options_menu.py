from language import LanguageManagement
from box import Box
import os


class OptionsMenu:
    def __init__(self, language: LanguageManagement):
        headline = language.texts.get("option_headline")
        options = [language.texts.get("option_change_language"), language.texts.get("option_change_screen"),
                   language.texts.get("option_go_back")]
        self.display_box = Box(content=headline, box_width=25, options=options)

    def enter_menu(self, gtg):
        jump_position = "\033[" + str(gtg.scr.len_y + 8) + ";0H"
        selected_option = ""
        while selected_option != gtg.language.texts.get("option_go_back"):
            gtg.scr.print(False, gtg)
            selected_option = self.display_box.access_options(gtg)
            if selected_option == gtg.language.texts.get("option_change_language"):
                options = os.listdir(os.getcwd() + "/data/lang")
                new_file = Box(content=gtg.language.texts.get("option_new_file"),
                               box_width=len(gtg.language.texts.get("option_new_file")),
                               options=options,
                               colour=gtg.colours.get_random_colour(gtg.rng, True))\
                    .access_options(gtg)
                gtg.configurations["language_file"] = new_file
            elif selected_option == gtg.language.texts.get("option_change_screen"):
                Box(content=gtg.language.texts.get("option_new_screen"),
                    box_width=len(gtg.language.texts.get("option_new_screen")),
                    colour=gtg.colours.get_random_colour(gtg.rng, True))\
                    .print_box(gtg.scr)
                new_dimensions = input(jump_position + "> ")
                buffer = new_dimensions.split(":")
                gtg.scr.change_size(int(buffer[0]), int(buffer[1]))
                gtg.configurations["screen_height"] = buffer[0]
                gtg.configurations["screen_width"] = buffer[1]
        configurations = open("data/config.txt", "w")
        for key in gtg.configurations:
            configurations.write(str(key) + "=" + str(gtg.configurations[key]) + "\n")
        configurations.close()
