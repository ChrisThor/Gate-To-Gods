class Replay:
    def __init__(self, filename, colours):
        self.slides = []
        self.read_replay_file(filename, colours)

    def read_replay_file(self, filename, colours):
        replay = ""
        try:
            replay = open(filename)
        except FileNotFoundError:
            print("Fehler beim Öffnen von \"" + filename + "\"")
            exit(64646)
        filecontent = replay.readlines()
        replay.close()

        line = []
        for lines in filecontent:
            if colours.jump_up() in lines and line != []:
                self.slides.append(line)
                line = [lines]
            else:
                line.append(lines)
        self.slides.append(line)

    def play_replay(self, keys, colours):
        position = 0
        command = ""
        while command != keys.exit_game:
            # print(colours.jump_up())
            for line in self.slides[position]:
                print(line, end='')
            command = input(colours.get_colour("white") + "Frame " + str(position + 1) + "/" + str(len(self.slides)) +
                            " (" + keys.next_slide + ": next, " + keys.previous_slide + ": previous): ")
            if command == keys.next_slide and position + 1 < len(self.slides):
                position += 1
            elif command == keys.previous_slide and position - 1 >= 0:
                position -= 1
