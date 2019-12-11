# -*- coding: utf-8 -*-
# Initially taken from:
# http://code.activestate.com/recipes/134892/#c9
# Thanks to Stephen Chappell

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

import msvcrt
import sys


win_encoding = 'mbcs'


XE0_OR_00 = '\x00\xe0'


def readchar(blocking=False):
    "Get a single character on Windows."

    while msvcrt.kbhit():
        msvcrt.getch()
    ch = msvcrt.getch()
    # print('ch={}, type(ch)={}'.format(ch, type(ch)))
    # while ch.decode(win_encoding) in unicode('\x00\xe0', win_encoding):
    while ch.decode(win_encoding) in XE0_OR_00:
        # print('found x00 or xe0')
        msvcrt.getch()
        ch = msvcrt.getch()

    return (
        ch
        if sys.version_info.major > 2
        else ch.decode(encoding=win_encoding)
    )
