from language import LanguageManagement
from box import Box


class OptionsMenu:
    def __init__(self, language: LanguageManagement):
        text = language.texts.get("option_headline") + "\n " + language.texts.get("option_change_language") + "\n " + \
            language.texts.get("option_change_screen") + "\n " + language.texts.get("option_go_back")
        self.display_box = Box(text, 25)

    def enter_menu(self, gtg):
        jump_position = "\033[" + str(gtg.scr.len_y + 8) + ";0H"
        selected_option = ""
        while selected_option != "3":
            gtg.scr.print(False, gtg)
            self.display_box.print_box(gtg.scr)
            selected_option = input(jump_position + "> ")[0]
            if selected_option == "1":
                Box(gtg.language.texts.get("option_new_file"),
                    len(gtg.language.texts.get("option_new_file"))).print_box(gtg.scr)
                new_file = input(jump_position + "> ")
                gtg.configurations["language_file"] = new_file

            elif selected_option == "2":
                Box(gtg.language.texts.get("option_new_screen"),
                    len(gtg.language.texts.get("option_new_screen"))).print_box(gtg.scr)
                new_dimensions = input(jump_position + "> ")
                buffer = new_dimensions.split(":")
                gtg.scr.change_size(int(buffer[0]), int(buffer[1]))
                gtg.configurations["screen_height"] = buffer[0]
                gtg.configurations["screen_width"] = buffer[1]
                print(gtg.colours.clear())
        configurations = open("data/config.txt", "w")
        for key in gtg.configurations:
            print(gtg.configurations[key])
            configurations.write(str(key) + "=" + str(gtg.configurations[key]) + "\n")
        configurations.close()