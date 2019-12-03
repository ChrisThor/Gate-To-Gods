from word import Word


def wrap(text: list, limit: int, ignore=0) -> list:
    new_text = []
    line_length = 0
    line = ""

    for word in text:
        if line_length + word.length > limit:
            if "\n" in word.content:
                new_text.append(line.ljust(limit))
                new_text.append(word.content.replace("\n", "").ljust(limit))
                line = ""
                line_length = 0
            else:
                new_text.append(line[:-1].ljust(limit))
                line = word.content + " "
                line_length = word.length + 1
        elif "\n" in word.content:
            new_text.append((line + word.content.replace("\n", "")).ljust(limit))
            line = ""
            line_length = 0
        else:
            line += word.content + " "
            line_length += word.length + 1
    new_text.append(line[:-1].ljust(limit))
    return new_text
