import word_wrap
import word
import keyboard_input
from screen import Screen


class Box:
    def __init__(self, content, box_width: int, options=[], colour="\033[0m", abortable=True):
        if isinstance(content, str):
            content = word.convert_text_to_list(content)
        self.colour = colour
        self.width: int = box_width
        self.abortable = abortable
        self.options: list = self.set_options(options)
        self.lines: list = word_wrap.wrap(content, box_width)
        self.height_content: int = len(self.lines)
        self.height_options: int = 0
        for option in self.options:
            for line in option.formatted_text:
                self.height_options += 1
        self.amount_options = len(options)
        self.height: int = self.height_content + self.height_options
        self.y_offset = 2
        self.horizontal_line: str = ""
        self.active_option = 0
        self.set_horizontal_line()

    def set_options(self, options: list):
        option_list = []
        for option in options:
            option_list.append(Option(option, self.width))
        return option_list

    def set_horizontal_line(self):
        for i in range(self.width + 2):
            self.horizontal_line += "═"

    def print_horizontal_line(self, position_y: int, position_x: int, start: str, end: str):
        jump_position = "\033[" + str(position_y) + ";" + str(position_x) + "H"
        print(jump_position + start + self.horizontal_line + end, end="")

    def print_content(self, position_y: int, position_x: int, scr: Screen):
        line_number = 0
        line_offset = 0
        for line_number in range(self.height_content):
            jump_position = "\033[" + str(position_y + line_number) + ";" + str(position_x) + "H"
            print(jump_position + "║ " + self.lines[line_number] + " ║", end="")
        new_y = 1 + position_y + line_number
        for option_number in range(self.amount_options):
            line_offset += self.options[option_number].print_option(new_y, option_number, line_offset, position_x,
                                                                    self.colour)

    def print_box(self, scr: Screen):
        start_pos_x: int = int(scr.len_x / 2) - int(self.width / 2) - 1
        start_pos_y: int = int(scr.len_y / 2) - int(self.height / 2) + self.y_offset
        print(self.colour)
        self.print_horizontal_line(start_pos_y, start_pos_x, "╔", "╗")
        self.print_content(start_pos_y + 1, start_pos_x, scr)
        self.print_horizontal_line(start_pos_y + self.height + 1, start_pos_x, "╚", "╝")
        print("\033[0m")  # it only works with this statement, don't ask

    def access_options(self, gtg) -> str:
        pressed_key = ""
        while pressed_key != "KEY_ENTER":
            self.deactivate_options()
            self.options[self.active_option].toggle()
            self.print_box(gtg.scr)
            pressed_key = keyboard_input.read_keyboard()
            if pressed_key == "KEY_ARROW_UP":
                if self.active_option != 0:
                    self.active_option -= 1
            elif pressed_key == "KEY_ARROW_DOWN":
                if self.active_option < len(self.options) - 1:
                    self.active_option += 1
            elif self.abortable and pressed_key == "KEY_ESCAPE":
                return ""
        return self.options[self.active_option].text

    def deactivate_options(self):
        for option in self.options:
            option.active = False


class Option:
    def __init__(self, text: str, width: int):
        self.swap_colour: str = "\033[7m"
        self.text: str = text
        self.formatted_text: list = word_wrap.wrap(word.convert_text_to_list(text), width)
        self.active: bool = False

    def print_option(self, position_y: int, option_number: int, line_offset: int, position_x, colour: str):
        line_offset -= 1
        for line in range(len(self.formatted_text)):
            line_offset += 1
            jump_position = f"\033[{position_y + option_number + line_offset};{position_x}H"
            if self.active:
                print(f"{jump_position}║ {self.swap_colour}{self.formatted_text[line]}\033[0m{colour} ║")
            else:
                print(f"{jump_position}║ {self.formatted_text[line]} ║")
        return line_offset

    def toggle(self):
        if self.active:
            self.active = False
        else:
            self.active = True
