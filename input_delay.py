import sys
import time

if sys.platform.startswith("linux"):
    import termios
elif sys.platform in ('win32', 'cygwin'):
    import msvcrt


def apply_delay(delay: float, last_input_time: float):
    difference = time.time() - last_input_time
    while difference < delay:
        if sys.platform.startswith("linux"):
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
        elif sys.platform in ('win32', 'cygwin'):
            while msvcrt.kbhit():
                msvcrt.getch()
        difference = time.time() - last_input_time
