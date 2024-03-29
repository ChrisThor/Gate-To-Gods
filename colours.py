class Colours:
    def __init__(self):
        self.colours = dict()
        self.colours["clear_screen"] = "\033[2J"
        self.colours["jump_to_top"] = "\033[H"
        self.colours["grey"] = "\033[38;5;238m"
        self.colours["red"] = "\033[31m"
        self.colours["green"] = "\033[32m"
        self.colours["yellow"] = "\033[33m"
        self.colours["blue"] = "\033[34m"
        self.colours["magenta"] = "\033[35m"
        self.colours["cyan"] = "\033[36m"
        self.colours["white"] = "\033[37m"
        self.colours["default"] = "\033[0m"

    def get_colour(self, colour: str):
        if colour in self.colours:
            return self.colours[colour]
        return self.colours["default"]

    def reset(self):
        return self.get_colour("default")

    def clear(self):
        return self.get_colour("clear_screen")

    def jump_up(self):
        return self.get_colour("jump_to_top")

    def get_random_colour(self, rng, foreground: bool):
        if foreground:
            mode = 38
        else:
            mode = 48
        red = rng.randint(0, 255)
        green = rng.randint(0, 255)
        blue = rng.randint(0, 255)
        return f"\033[{mode};2;{red};{green};{blue}m"
