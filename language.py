class LanguageManagement:
    def __init__(self):
        self.texts = {}
        self.undefined = "You tried to access a text or message that is not defined in your current language file."
        self.read_language_file(self.get_language_file())

    def get_language_file(self):
        config = None
        try:
            config = open("data/config.txt", "r")
        except FileNotFoundError:
            print("\"config.txt\" could not be found.")
            exit(-1)
        lines = config.readlines()
        config.close()
        for line in lines:
            if "language_file" in line:
                try:
                    return line.split("=")[1].replace("\n", "")
                except IndexError:
                    print("\"config.txt\" is incorrect.")
                    exit(-1)

    def read_language_file(self, filename):
        language_file = None
        try:
            language_file = open("data/" + filename, "r")
        except FileNotFoundError:
            print("\"" + filename + "\" could not be found.")
            exit(-1)
        lines = language_file.readlines()
        language_file.close()
        for line in lines:
            split_line = line.split("=")
            self.texts[split_line[0]] = split_line[1].replace("\n", "")
