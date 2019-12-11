class LanguageManagement:
    def __init__(self, language_file: str):
        self.texts = {}
        self.undefined = "You tried to access a text or message that is not defined in your current language file."
        self.read_language_file(language_file)

    def read_language_file(self, filename: str):
        self.texts = {}
        language_file = None
        try:
            language_file = open("data/lang/" + filename, "r")
        except FileNotFoundError:
            print("\"" + filename + "\" could not be found.")
            exit(-1)
        lines = language_file.readlines()
        language_file.close()
        for line in lines:
            split_line = line.split("=")
            self.texts[split_line[0]] = split_line[1].replace("\n", "")
