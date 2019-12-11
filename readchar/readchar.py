# -*- coding: utf-8 -*-
# This file is based on this gist:
# http://code.activestate.com/recipes/134892/
# So real authors are DannyYoo and company.

# Licenced under MIT-Licence:
"""Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
import sys


if sys.platform.startswith('linux'):
    from .readchar_linux import readchar
    from .key_linux import ANSI_SEQUENCES
elif sys.platform == 'darwin':
    from .readchar_linux import readchar
elif sys.platform in ('win32', 'cygwin'):
    import msvcrt
    from .readchar_windows import readchar
    from . import key_windows
else:
    raise NotImplemented('The platform %s is not supported yet' % sys.platform)


if sys.platform in ('win32', 'cygwin'):
    #
    # Windows uses scan codes for extended characters. The ordinal returned is
    # 256 * the scan code.  This dictionary translates scan codes to the
    # unicode sequences expected by readkey.
    #
    # for windows scan codes see:
    #   https://msdn.microsoft.com/en-us/library/aa299374
    #      or
    #   http://www.quadibloc.com/comp/scan.htm
    xlate_dict = {
        8: key_windows.BACKSPACE,
        9: key_windows.TAB,
        13: key_windows.ENTER,
        27: key_windows.ESC,
        15104: key_windows.F1,
        15360: key_windows.F2,
        15616: key_windows.F3,
        15872: key_windows.F4,
        16128: key_windows.F5,
        16384: key_windows.F6,
        16640: key_windows.F7,
        16896: key_windows.F8,
        17152: key_windows.F9,
        17408: key_windows.F10,
        22272: key_windows.F11,
        34528: key_windows.F12,

        7680: key_windows.ALT_A,

        # don't have table entries for...
        # CTRL_ALT_A, # Ctrl-Alt-A, etc.
        # CTRL_ALT_DELETE,
        # CTRL-F1

        21216: key_windows.INSERT,
        21472: key_windows.DELETE,
        18912: key_windows.PAGE_UP,
        20960: key_windows.PAGE_DOWN,
        18400: key_windows.HOME,
        20448: key_windows.END,

        18656: key_windows.UP,
        20704: key_windows.DOWN,
        19424: key_windows.LEFT,
        19936: key_windows.RIGHT,
    }

    def readkey(getchar_fn=None):
        # Get a single character on Windows. if an extended key is pressed, the
        # Windows scan code is translated into a the unicode sequences readchar
        # expects (see key_windows.py).
        while True:
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                a = ord(ch)
                # print(a)
                list_special_keys = [8, 9, 13, 27]
                if a == 0 or a == 224:
                    b = ord(msvcrt.getch())
                    x = a + (b * 256)
                    # print(x)

                    try:
                        return xlate_dict[x]
                    except KeyError:
                        return None
                    # return x
                    # This in unreachable, therefore not needed
                elif a in list_special_keys:
                    return xlate_dict[a]
                else:
                    return ch.decode()

else:
    def readkey(getchar_fn=None):
        getchar = getchar_fn or readchar
        c1 = getchar()
        if ord(c1) != 0x1b:
            try:
                return ANSI_SEQUENCES[c1]
            except KeyError:
                return c1
        c2 = getchar()
        if ord(c2) != 0x5B and ord(c2) != 0x4F:
            try:
                return ANSI_SEQUENCES[c1 + c2]
            except KeyError:
                return c1
        c3 = getchar()
        if ord(c3) != 0x31 and ord(c3) != 0x32 and ord(c3) != 0x33 and ord(c3) != 0x34 and ord(c3) != 0x35 and ord(c3) \
                != 0x36:
            try:
                return ANSI_SEQUENCES[c1 + c2 + c3]
            except KeyError:
                return c1
        c4 = getchar()
        if ord(c4) == 0x7E:
            try:
                return ANSI_SEQUENCES[c1 + c2 + c3 + c4]
            except KeyError:
                return c1
        c5 = getchar()
        return ANSI_SEQUENCES[c1 + c2 + c3 + c4 + c5]
