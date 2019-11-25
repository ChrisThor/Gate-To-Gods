class Colours:
    def __init__(self):
        self.clear_screen = "\033[2J"
        self.jump_to_top = "\033[H"
        self.grey = "\033[38;2;100;100;100m"
        self.red = "\033[31m"
        self.green = "\033[32m"
        self.yellow = "\033[33m"
        self.blue = "\033[34m"
        self.magenta = "\033[35m"
        self.cyan = "\033[36m"
        self.white = "\033[37m"
        self.default = "\033[0m"

    def get_colour(self, colour: str):
        if colour == "grey":
            return self.grey
        elif colour == "red":
            return self.red
        elif colour == "green":
            return self.green
        elif colour == "blue":
            return self.blue
        elif colour == "yellow":
            return self.yellow
        elif colour == "cyan":
            return self.cyan
        elif colour == "white":
            return self.white
        else:
            return self.default

    def reset(self):
        return self.default

    def clear(self):
        return self.clear_screen

    def jump_up(self):
        return self.jump_to_top
