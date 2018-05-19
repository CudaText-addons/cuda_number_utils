from cudatext import *
from .work_romans import *

class Command:
    def dec_roman_show(self):
        roman_conv(False)

    def dec_roman_replace(self):
        roman_conv(True)
