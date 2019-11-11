class Message:
    def __init__(self, content="", length=0):
        self.content = content
        if length == 0:
            self.length = len(content)
        else:
            self.length = length

    def fill(self, width):
        if len(self.content) > width:
            self.content = self.content.ljust(2 * width - self.length, " ")
        else:
            self.content = self.content.ljust(width, " ")
