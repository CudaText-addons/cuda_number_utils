import datetime
import os

import cudatext_keys as keys

from enum import Enum
from cudatext import *

def log(s):
    # Change conditional to True to log messages in a Debug process
    if False:
        plugin = os.path.basename(os.path.dirname(__file__))
        now = datetime.datetime.now()
        print(now.strftime("%H:%M:%S ") + plugin + ': ' + str(s))
    pass

# Index for number bases in radiogroup
class Base(Enum):
    binary = 0
    octal = 1
    decimal = 2
    hexadecimal = 3

class BaseConverter():

    def __init__(self):
        self.tick = 150
        self.title = 'Number Base Converter'
        self.opt = -1
        self.carets = None
        self.msgs = {}
        self.controls = []
        self.h_dlg = self.init_form()
        self.form_msg = ''

    def showDialog(self):
        dlg_proc(self.h_dlg, DLG_SHOW_NONMODAL)

    def init_form(self):
        w = 370
        h = dlg_proc(0, DLG_CREATE)
        dlg_proc(h, DLG_PROP_SET, prop={
            'cap': self.title,
            'w': w,
            'h': 170,
            'border': DBORDER_TOOL,
            'topmost': True,
            'keypreview': True,
            'on_key_down': self.form_key_down,
            'on_show': self.form_show,
            'on_hide': self.form_hide,
            'on_mouse_enter': self.mouse_move,
            })

        x = p = 6
        y = 10

        n = dlg_proc(h, DLG_CTL_ADD, 'statusbar')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'sb',
            'h': 28,
            'align': ALIGN_BOTTOM,
            })

        self.sb_tag = 1
        self.sb_id = dlg_proc(h, DLG_CTL_HANDLE, index=n)
        statusbar_proc(self.sb_id, STATUSBAR_ADD_CELL, tag=self.sb_tag)
        statusbar_proc(self.sb_id, STATUSBAR_SET_CELL_SIZE, tag=self.sb_tag,
                       value=w + 2)

        n = dlg_proc(h, DLG_CTL_ADD, 'radiogroup')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'bases',
            'x': p,
            'y': 0,
            'w': 130,
            'act': True,
            'en': False,
            'items': 'Binary\tOctal\tDecimal\tHexadecimal',
            'val': 0,
            # 'on_change': self.rg_change,
            'on_mouse_enter': self.mouse_move,
            })
        self.n_rg_base = n
        self.msgs[n] = 'Select with click or using Up-Down keys.'
        self.controls.append(n)

        n = dlg_proc(h, DLG_CTL_ADD, 'check')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'html_format',
            'cap': 'Use HTML format',
            'hint': 'The final hexadecimal values can be used in HTML/CSS as colors',
            'a_l': ('', '['),
            'a_t': ('bases', ']'),
            'a_r': None,
            'a_b': None,
            'sp_l': 5*p,
            'sp_t': p,
            'en': False,
            'on_mouse_enter': self.mouse_move,
            })
        self.n_chk_html = n
        self.msgs[n] = 'In Hexadecimal replace 0x with #.'

        n = dlg_proc(h, DLG_CTL_ADD, 'check')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'keep_carets',
            'w': 80,
            'x': 170,
            'y': 20,
            'cap': 'Preserve carets after conversion',
            'hint': 'Keep carets after conversion',
            'en': False,
            'val': True,
            'on_mouse_enter': self.mouse_move,
            })
        self.n_chk_keep_carets = n
        self.msgs[n] = 'If is ON the selections will keep after conversion.'
        self.controls.append(n)

        n = dlg_proc(h, DLG_CTL_ADD, 'button_ex')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'convert',
            'w': 80,
            'a_l': None,
            'a_t': None,
            'a_r': ('keep_carets', ']'),
            'a_b': ('bases', ']'),
            'sp_r': p,
            'cap': 'Convert',
            'hint': 'Convert carets to selected base number.',
            'en': False,
            'on_change': self.btn_convert_click,
            'on_mouse_enter': self.mouse_move,
            })
        self.n_btn_convert = n
        self.msgs[n] = 'Starts the conversion process.'
        self.controls.append(n)

        return h

    def timer_update(self, tag='', info=''):
        # log('Timer Update')
        opt = int(dlg_proc(self.h_dlg, DLG_CTL_PROP_GET,
                           index=self.n_rg_base)['val'])
        if self.opt == opt:
            return

        self.opt = opt

        if self.opt == Base.hexadecimal.value:
            enable = True
        else:
            enable = False

        self.set_prop(self.n_chk_html, 'en', enable)

    def upd_sb_text(self, text):
        statusbar_proc(self.sb_id, STATUSBAR_SET_CELL_TEXT, tag=self.sb_tag,
                       value=text)

    def set_prop(self, id, prop, value):
        dlg_proc(self.h_dlg, DLG_CTL_PROP_SET, index=id, prop={prop: value})

    def form_key_down(self, id_dlg, id_ctl, data='', info=''):

        # Enter
        if id_ctl == keys.VK_ENTER and (data == ''):
            self.btn_convert_click(id_dlg, self.n_btn_convert)
            self.form_hide(id_dlg, id_ctl, data, info)
            return True

        # Escape: Go to editor
        if (id_ctl == keys.VK_ESCAPE) and (data == ''):
            self.form_hide(id_dlg, id_ctl, data, info)
            return True

    def form_show(self, id_dlg, id_ctl, data='', info=''):
        if self.validate_carets():
            timer_proc(TIMER_START, self.timer_update, self.tick, tag='')

            for id in self.controls:
                self.set_prop(id, 'en', True)

        self.upd_sb_text(self.form_msg)

    def form_hide(self, id_dlg, id_ctl, data='', info=''):
        ed.focus()
        timer_proc(TIMER_STOP, self.timer_update, 0)
        dlg_proc(self.h_dlg, DLG_HIDE)

    def btn_convert_click(self, id_dlg, id_ctl, data='', info=''):
        timer_proc(TIMER_STOP, self.timer_update, 0)
        carets = []

        keep = int(dlg_proc(self.h_dlg, DLG_CTL_PROP_GET,
                           index=self.n_chk_keep_carets)['val'])

        html = int(dlg_proc(self.h_dlg, DLG_CTL_PROP_GET,
                           index=self.n_chk_html)['val'])

        one = self.carets[0]

        #Clean carets
        ed.set_caret(*one[:2], id=CARET_SET_ONE)

        for caret in self.carets:
            try:
                text = ed.get_text_substr(*caret).strip()
                base = self.get_base(text)

                if not base:
                    raise ValueError('Not found a correct base in caret')

                try:
                    new = old = int(text, base)
                except Exception as e:
                    raise ValueError('The number "%s" is not valid with base %d' %
                                     (text, base))

                if self.opt == Base.binary.value and base != 2:
                    try:
                        new = bin(old)
                    except Exception as e:
                        raise ValueError('%s cannot convert to Binary.' %
                                         str(old))

                if self.opt == Base.octal.value and base != 8:
                    try:
                        new = oct(old)
                    except Exception as e:
                        raise ValueError('%s cannot convert to Octal.' %
                                         str(old))

                if self.opt == Base.hexadecimal.value and base != 16:
                    try:
                        new = hex(old)
                        if html:
                            new = new.replace('0x', '#').upper()
                    except Exception as e:
                        raise ValueError('%s cannot convert to Hexadecimal.' %
                                         str(old))

                continue_dec = self.opt == Base.decimal.value and base != 10

                new = str(new)
                old = str(old)

                if new != old or continue_dec:
                    # Do the replace
                    ed.replace(*caret, new)
                    x1, y1, x2, y2 = caret
                    carets.append((x1, y1, x1 + len(new), y2))
                else:
                    carets.append(caret)

            except ValueError as e:
                log(e)
                carets.append(caret)
                continue

        if keep:
            for caret in carets:
                ed.set_caret(*caret, CARET_ADD)

        self.form_hide(id_dlg, id_ctl, data, info)

    def get_base(self, text):
        suffix = text[:2]
        number = text[2:]

        if suffix == '0b':
            return 2
        if suffix == '0o':
            return 8
        if suffix == '0x':
            return 16
        if text.isdigit():
            return 10

        return

    def rg_change(self, id_dlg, id_ctl, data='', info=''):
        # TODO: Waiting for API change to reach on_change events.
        pass

    def mouse_move(self, id_dlg, id_ctl, data='', info=''):
        if id_ctl in self.msgs:
            self.upd_sb_text(self.msgs[id_ctl])
        else:
            self.upd_sb_text(self.form_msg)

    def validate_carets(self):
        carets = ed.get_carets()
        new_carets = []

        self.form_msg = ''
        for caret in carets:
            x1, y1, x2, y2 = caret

            if (x2, y2) == (-1, -1):
                x2 = x1
                y2 = y1
                continue

            if (y1, x1) > (y2, x2):
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            if (y2 - y1) > 0:
                self.form_msg = 'Multi-line is not allowed.'
                return False

            new_carets.append((x1, y1, x2, y2))

        if not len(new_carets):
            self.form_msg = 'Do at least one selection.'
            return False
        else:
            self.form_msg = '%d carets to process. Non valid numbers will be skipped.' % len(new_carets)
            self.carets = new_carets
            return True