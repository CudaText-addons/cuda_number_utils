from .work_insert_num import *
from .work_carets_num import *
from .work_romans import *

class Command:
    def dlg_insert_numbers(self):
        dialog_insert_numbers()
        
    def dlg_carets_num(self):
        dialog_carets_num()

    def dec_roman_show(self):
        roman_conv(False)

    def dec_roman_replace(self):
        roman_conv(True)
