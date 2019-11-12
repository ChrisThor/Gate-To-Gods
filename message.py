class Message:
    def __init__(self, content="", colour_code_length=0):
        self.content = content
        self.colour_code_length = colour_code_length
        self.length = len(content)

    def fill(self, width, colour_mode):
        if colour_mode:
            self.content = self.content.ljust(width + self.colour_code_length, " ")
        else:
            self.content = self.content.ljust(width, " ")
