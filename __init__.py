from .work_insert_num import *
from .work_carets_num import *
from .work_romans import *
from .work_num2words import *

class Command:
    def dlg_insert_numbers(self):
        dialog_insert_numbers()
        
    def dlg_carets_num(self):
        dialog_carets_num()

    def dec_roman_show(self):
        roman_conv(False)
    def dec_roman_replace(self):
        roman_conv(True)

    def num2word_new_tab(self):
        num2words_new_tab()
    def num2word_replace(self):
        num2words_replace()
    def num2word_langs(self):
        num2words_langs()
