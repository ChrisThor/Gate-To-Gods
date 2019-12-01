class Word:
    def __init__(self, content: str, colour_codes: list):
        self.content = content
        self.colour_codes = colour_codes
        self.length = len(self.content)
        for colour_code in colour_codes:
            self.length -= len(colour_code)
