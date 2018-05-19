import os
import string
from cudatext import *
from .pytils import numeral
from .word_proc import *


def do_num_words(mode, rubles):
    x0, y0, nlen, text = get_word_info()
    if not text:
        msg_status('Place caret under number')
        return
                   
    try:            
        num = int(text)
    except:
        try:
            text = text.replace(',', '.')
            num = float(text)
        except:
            msg_status('Place caret under number')
            return

    if rubles:
        text = numeral.rubles(num)
    else:
        text = numeral.in_words(num)
    if not text: return

    if mode=='newtab':
        file_open('')
        ed.insert(0, 0, text)
    elif mode=='replace':
        ed.set_caret(x0, y0)
        ed.delete(x0, y0, x0+nlen, y0)
        ed.insert(x0, y0, text)
    else:
        raise Exception('Mode?')
            

def num2ru_new_tab():
    do_num_words('newtab', False)

def num2ru_replace():
    do_num_words('replace', False)

def num2ru_rubles_new_tab():
    do_num_words('newtab', True)

def num2ru_rubles_replace():
    do_num_words('replace', True)
