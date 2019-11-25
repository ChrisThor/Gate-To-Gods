class Input:
    def __init__(self):
        self.move_left_0 = "a"
        self.move_left_1 = "4"
        self.move_up_0 = "w"
        self.move_up_1 = "8"
        self.move_right_0 = "d"
        self.move_right_1 = "6"
        self.move_down_0 = "s"
        self.move_down_1 = "2"
        self.move_up_right = "9"
        self.move_up_left = "7"
        self.move_down_right = "3"
        self.move_down_left = "1"
        self.exit_game = "x"
        self.open_door = "o"
        self.close_door = "c"
        self.next_slide = "n"
        self.previous_slide = "p"
        self.enter_exit = "<"
        self.enter_entrance = ">"
        self.show_coordinates = "#"

    def get_direction_value(self, pressed_key: str, pos_y: int, pos_x: int):
        if pressed_key == self.move_left_0 or pressed_key == self.move_left_1:
            return pos_y, pos_x - 1
        elif pressed_key == self.move_up_0 or pressed_key == self.move_up_1:
            return pos_y - 1, pos_x
        elif pressed_key == self.move_right_0 or pressed_key == self.move_right_1:
            return pos_y, pos_x + 1
        elif pressed_key == self.move_down_0 or pressed_key == self.move_down_1:
            return pos_y + 1, pos_x
        elif pressed_key == self.move_down_left:
            return pos_y + 1, pos_x - 1
        elif pressed_key == self.move_down_right:
            return pos_y + 1, pos_x + 1
        elif pressed_key == self.move_up_left:
            return pos_y - 1, pos_x - 1
        elif pressed_key == self.move_up_right:
            return pos_y - 1, pos_x + 1
        else:
            return pos_y, pos_x
