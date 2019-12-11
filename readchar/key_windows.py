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

# common
LF = '\x0d'
CR = '\x0a'
ENTER = "Enter"
BACKSPACE = "Backspace"
SPACE = '\x20'
ESC = "Escape"
TAB = "Tab"

# CTRL
CTRL_A = "ControlA"
CTRL_B = "ControlB"
CTRL_C = "ControlC"
CTRL_D = "ControlD"
CTRL_E = "ControlE"
CTRL_F = "ControlF"
CTRL_Z = "ControlZ"

# ALT
ALT_A = '\x1b\x61'

# CTRL + ALT
CTRL_ALT_A = '\x1b\x01'

# cursors
UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"

CTRL_ALT_DELETE = '\x1b\x5b\x33\x5e'

# other
F1 = "F1"
F2 = "F2"
F3 = "F3"
F4 = "F4"
F5 = "F5"
F6 = "F6"
F7 = "F7"
F8 = "F8"
F9 = "F9"
F10 = "F10"
F11 = "F11"
F12 = "F12"

PAGE_UP = "PageUp"
PAGE_DOWN = "PageDown"
HOME = "Home"
END = "End"

INSERT = "Insert"
DELETE = "Delete"


ESCAPE_SEQUENCES = (
    ESC,
    ESC + '\x5b',
    ESC + '\x5b' + '\x31',
    ESC + '\x5b' + '\x32',
    ESC + '\x5b' + '\x33',
    ESC + '\x5b' + '\x35',
    ESC + '\x5b' + '\x36',
    ESC + '\x5b' + '\x31' + '\x35',
    ESC + '\x5b' + '\x31' + '\x36',
    ESC + '\x5b' + '\x31' + '\x37',
    ESC + '\x5b' + '\x31' + '\x38',
    ESC + '\x5b' + '\x31' + '\x39',
    ESC + '\x5b' + '\x32' + '\x30',
    ESC + '\x5b' + '\x32' + '\x31',
    ESC + '\x5b' + '\x32' + '\x32',
    ESC + '\x5b' + '\x32' + '\x33',
    ESC + '\x5b' + '\x32' + '\x34',
    ESC + '\x4f',
    ESC + ESC,
    ESC + ESC + '\x5b',
    ESC + ESC + '\x5b' + '\x32',
    ESC + ESC + '\x5b' + '\x33',
)
