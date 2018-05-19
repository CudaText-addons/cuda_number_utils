import string
from cudatext import *
from .romans import to_romans, from_romans

CHARS_ALL = string.digits + string.ascii_letters
CHARS_DIGITS = string.digits
CHARS_ROMAN = 'IVXLCDM' + 'IVXLCDM'.lower()


def is_roman(s):
    for ch in s:
        if not ch in CHARS_ROMAN:
            return False
    return True


def roman_conv(and_replace):

    carets = ed.get_carets()
    x, y, x1, y1 = carets[0]

    if y1>=0:
        msg_status('Romanize: Cannot work with selection')
        return

    line = ed.get_text_line(y)
    if not line or x>=len(line):
        msg_status('Romanize: Need a number')
        return

    if not line[x] in CHARS_ALL:
        msg_status('Romanize: Need a number')
        return

    n1 = x
    while n1>0 and line[n1-1] in CHARS_ALL: n1 -= 1

    n2 = x
    while n2<len(line) and line[n2] in CHARS_ALL: n2 += 1

    s_from = line[n1:n2]

    if s_from.isdigit():
        s_to = to_romans(int(s_from))
    elif is_roman(s_from):
        s_to = str(from_romans(s_from.upper()))
    else:
        msg_status('Romanize: incorrect number "%s"'%s_from)
        return

    if and_replace:
        ed.set_caret(n1, y)
        ed.replace(n1, y, n2, y, s_to)

    msg_status('Romanize: %s -> %s' % (s_from, s_to))
