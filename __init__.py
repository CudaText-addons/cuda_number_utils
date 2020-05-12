from .work_insert_num import *
from .work_carets_num import *
from .work_romans import *
from .work_num2words import *
from .work_num2ruwords import *
from .work_bases import BaseConverter

class Command:
    def dlg_insert_numbers(self):
        dialog_insert_numbers()

    def dlg_carets_num(self):
        dialog_carets_num()

    def dlg_base_converter(self):
        bc = BaseConverter()
        bc.showDialog()

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

    def num2ru_new_tab(self):
        num2ru_new_tab()
    def num2ru_replace(self):
        num2ru_replace()
    def num2ru_rubles_new_tab(self):
        num2ru_rubles_new_tab()
    def num2ru_rubles_replace(self):
        num2ru_rubles_replace()
