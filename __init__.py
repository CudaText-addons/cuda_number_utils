from cudatext import *
from .work_romans import *
from .work_insert_numbers import *

class Command:
    def dec_roman_show(self):
        roman_conv(False)

    def dec_roman_replace(self):
        roman_conv(True)

    def dlg_insert_numbers(self):
        dialog_insert_numbers()
