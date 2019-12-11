from box import Box
import readchar
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
        self.change_screen_box = Box(content=gtg.language.texts.get("option_new_screen"),
                                     box_width=27)

    def enter_menu(self, gtg):
        selected_option = ""
        self.display_box.active_option = 0
        while selected_option != gtg.language.texts.get("option_go_back"):
            gtg.scr.print(False, gtg)
            selected_option = self.display_box.access_options(gtg)
            if selected_option == gtg.language.texts.get("option_change_language"):
                self.change_language(gtg)
            elif selected_option == gtg.language.texts.get("option_change_screen"):
                self.change_screen_dimensions(gtg)
            elif selected_option == "":
                return None
        configurations = open("data/config.txt", "w")
        for key in gtg.configurations:
            configurations.write(str(key) + "=" + str(gtg.configurations[key]) + "\n")
        configurations.close()

    def change_screen_dimensions(self, gtg):
        key = ""
        len_y = gtg.scr.len_y
        len_x = gtg.scr.len_x
        original_y = len_y
        original_x = len_x
        lower_x_limit = 33
        lower_y_limit = 11
        self.change_screen_box.colour = gtg.colours.get_random_colour(gtg.rng, True)
        while key != "Enter" and key != "Escape":
            print(f"\033[H{gtg.language.texts.get('screen_height')}: {len_y} "
                  f"{gtg.language.texts.get('screen_width')}: {len_x}\t\t")
            self.print_screen_size_preview(gtg.scr.len_y, gtg.scr.len_x)
            self.change_screen_box.print_box(gtg.scr)
            key = readchar.readkey()

            if key == "Up":
                len_y -= 1
            elif key == "Down":
                len_y += 1
            elif key == "Left":
                len_x -= 1
            elif key == "Right":
                len_x += 1
            if len_y < lower_y_limit:
                len_y = lower_y_limit
            if len_x < lower_x_limit:
                len_x = lower_x_limit

            gtg.scr.change_size(len_y, len_x)
        # print(gtg.colours.clear())
        if key == "Escape":
            gtg.scr.change_size(original_y, original_x)
        else:
            gtg.configurations["screen_height"] = len_y
            gtg.configurations["screen_width"] = len_x

    def print_screen_size_preview(self, len_y: int, len_x: int):
        len_y -= 1
        y_offset = 3
        symbol = "*"
        print("\033[H")
        for i in range(len_y + y_offset):
            for j in range(len_x + 1):
                print(" ", end="")
            print()
        print(f"\033[{y_offset};0H{symbol}\033[{y_offset};{len_x}H{symbol}\033[{y_offset + len_y};0H{symbol}"
              f"\033[{y_offset + len_y};{len_x}H{symbol}")

    def change_language(self, gtg):
        self.change_language_box.colour = gtg.colours.get_random_colour(gtg.rng, True)
        for language_file in range(self.change_language_box.amount_options):
            if gtg.configurations["language_file"] == self.change_language_box.options[language_file].text:
                self.change_language_box.active_option = language_file
        new_file = self.change_language_box.access_options(gtg)
        if new_file != "":
            gtg.configurations["language_file"] = new_file
