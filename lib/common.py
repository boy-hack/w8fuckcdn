# common functions

import sys
from console_width import getTerminalSize

console_width = getTerminalSize()[0] - 2

def print_msg(msg=None, left_align=True, line_feed=False):
    if left_align:
        sys.stdout.write('\r' + msg + ' ' * (console_width - len(msg)))
    else:  # right align
        sys.stdout.write('\r' + ' ' * (console_width - len(msg)) + msg)
    if line_feed:
        sys.stdout.write('\n')
    sys.stdout.flush()