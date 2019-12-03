import msvcrt


special_keys = {
    b'H': "KEY_ARROW_UP",
    b'K': "KEY_ARROW_LEFT",
    b'P': "KEY_ARROW_DOWN",
    b'M': "KEY_ARROW_RIGHT",
    b'S': "KEY_DELETE",
    b'O': "KEY_END",
    b'Q': "KEY_PAGE_DOWN",
    b'R': "KEY_INSERT",
    b'G': "KEY_HOME",
    b'I': "KEY_PAGE_UP",
    b';': "KEY_F1",
    b'<': "KEY_F2",
    b'=': "KEY_F3",
    b'>': "KEY_F4",
    b'?': "KEY_F5",
    b'@': "KEY_F6",
    b'A': "KEY_F7",
    b'B': "KEY_F8",
    b'C': "KEY_F9",
    b'D': "KEY_F10",
    b'\x85': "KEY_F11",
    b'\x86': "KEY_F12"
}


special_chars = {
    b'\x1b': "KEY_ESCAPE",
    b'\r': "KEY_ENTER",
    b'\x08': "KEY_BACKSPACE",
    b'\t': "KEY_TAB",
    b'\x81': "ü",
    b'\x94': "ö",
    b'\x84': "ä",
    b'\x9a': "Ü",
    b'\x99': "Ö",
    b'\x8e': "Ä",
    b'\xe1': "ß",
    # cannot support the big "ẞ" that is entered by SHIFT+ALTGR+ß
    # That combination returns the same value as SHIFT+ß, which results in "?"
    b'\xef': "´",
    b'\x82': "é",
    b'\x8a': "è",
    b'\x88': "ê",
    b'\x90': "É",
    b'\xd4': "È",
    b'\xd2': "Ê",
    b'\xa0': "á",
    b'\x85': "à",
    b'\x83': "â",
    b'\xb5': "Á",
    b'\xb7': "À",
    b'\xb6': "Â",
    b'\xa1': "í",
    b'\x8d': "ì",
    b'\x8c': "î",
    b'\xd6': "Í",
    b'\xde': "Ì",
    b'\xd7': "Î",
    b'\xa2': "ó",
    b'\x95': "ò",
    b'\x93': "ô",
    # b'\xe0': "Ó",  # Not supported due to arrow keys producing the same code
    b'\xe3': "Ò",
    b'\xe2': "Ô",
    b'\xa3': "ú",
    b'\x97': "ù",
    b'\x96': "û",
    b'\xe9': "Ú",
    b'\xeb': "Ù",
    b'\xea': "Û",
    b'\xec': "ý",
    b'\xed': "Ý",
    b'\xfd': "²",
    b'\xfc': "³",
    b'\xf8': "°"
}


def read_keyboard():
    user_input = msvcrt.getch()
    # print(user_input)

    if user_input == b'\xe0':
        user_input = msvcrt.getch()
        if user_input in special_keys:
            return special_keys[user_input]
    elif user_input == b'\x03':
        raise KeyboardInterrupt("CTRL+C closes the program")
    elif user_input == b'\x00':
        user_input = msvcrt.getch()
        if user_input in special_keys:
            return special_keys[user_input]
    elif user_input in special_chars:
        return special_chars[user_input]
    else:
        try:
            return user_input.decode("utf-8")
        except UnicodeDecodeError:
            pass
    return "None"
