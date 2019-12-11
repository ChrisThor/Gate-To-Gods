class Word:
    def __init__(self, content: str, colour_codes: list):
        self.content = content
        self.colour_codes = colour_codes
        self.length = len(self.content)
        for colour_code in colour_codes:
            self.length -= len(colour_code)
        if "\n" in content:
            self.length -= 1


def convert_text_to_list(text: str) -> list:
    list_of_words = []
    buffer = text.split(" ")
    for word in buffer:
        list_of_words.append(Word(word, []))
    return list_of_words
