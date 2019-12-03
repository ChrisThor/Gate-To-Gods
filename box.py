import word_wrap
import word
from screen import Screen


class Box:
    def __init__(self, content, box_width: int):
        if isinstance(content, str):
            content = word.convert_text_to_list(content)
        self.width: int = box_width
        self.lines: list = word_wrap.wrap(content, box_width)
        self.height: int = len(self.lines)
        self.y_offset = 2
        self.horizontal_line: str = ""
        self.set_horizontal_line()

    def set_horizontal_line(self):
        for i in range(self.width + 2):
            self.horizontal_line += "═"

    def print_horizontal_line(self, position_y: int, position_x: int, start: str, end: str):
        jump_position = "\033[" + str(position_y) + ";" + str(position_x) + "H"
        print(jump_position + start + self.horizontal_line + end, end="")

    def print_content(self, position_y: int, position_x: int, scr: Screen):
        for line_number in range(self.height):
            jump_position = "\033[" + str(position_y + line_number) + ";" + str(position_x) + "H"
            print(jump_position + "║ " + self.lines[line_number] + " ║", end="")

    def print_box(self, scr: Screen):
        start_pos_x: int = int(scr.len_x / 2) - int(self.width / 2) - 1
        start_pos_y: int = int(scr.len_y / 2) - int(self.height / 2) + self.y_offset
        self.print_horizontal_line(start_pos_y, start_pos_x, "╔", "╗")
        self.print_content(start_pos_y + 1, start_pos_x, scr)
        self.print_horizontal_line(start_pos_y + self.height + 1, start_pos_x, "╚", "╝")
