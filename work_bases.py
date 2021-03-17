import datetime
import os
import re

import cudatext_keys as keys

from enum import Enum

from cudatext import *
from cudax_lib import int_to_html_color, html_color_to_int

from cudax_lib import get_translation
_ = get_translation(__file__)  # I18N


def log(s):
    # Change conditional to True to log messages in a Debug process
    if False:
        plugin = os.path.basename(os.path.dirname(__file__))
        now = datetime.datetime.now()
        print(now.strftime("%H:%M:%S ") + plugin + ': ' + str(s))
    pass

# Index for number bases in radiogroup
class Base(Enum):
    decimal = 0
    binary = 1
    octal = 2
    hexadecimal = 3
    html = 4

class BaseConverter():

    def __init__(self):
        self.tick = 150
        self.title = _('Number Base Converter')
        self.carets = None
        self.msgs = {}
        self.controls = []
        self.h_dlg = self.init_form()
        self.form_msg = ''
        self.suffixes = ['0b', '0o', '0x', '#']

    def showDialog(self):
        dlg_proc(self.h_dlg, DLG_SHOW_NONMODAL)

    def init_form(self):
        # w = 400 -- too small for translations (fm)
        w = 500
        h = dlg_proc(0, DLG_CREATE)
        dlg_proc(h, DLG_PROP_SET, prop={
            'cap': self.title,
            'w': w,
            'h': 195,
            'border': DBORDER_TOOL,
            'topmost': True,
            'keypreview': True,
            'on_key_down': self.form_key_down,
            'on_show': self.form_show,
            'on_hide': self.form_hide,
            'on_mouse_enter': self.mouse_move,
            })

        p = 6

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
            'y': p,
            'w': 130,
            'h': 130,
            'act': True,
            'en': False,
            'items': _('Decimal\tBinary\tOctal\tHexadecimal\tHTML color'),
            'val': 0,
            'on_mouse_enter': self.mouse_move,
            })
        self.n_rg_base = n
        self.msgs[n] = _('Select with click or using Up-Down keys.')
        self.controls.append(n)

        n = dlg_proc(h, DLG_CTL_ADD, 'check')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'keep_carets',
            'a_l': None,
            'a_t': ('bases', '['),
            'a_r': ('', ']'),
            'a_b': None,
            'sp_t': 3*p,
            'sp_r': p,
            'cap': _('Keep selections after conversion'),
            'en': False,
            'val': True,
            'on_mouse_enter': self.mouse_move,
            })
        self.n_chk_keep_carets = n
        self.msgs[n] = _('If checked, selections will be kept after conversion.')
        self.controls.append(n)

        n = dlg_proc(h, DLG_CTL_ADD, 'button')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'convert',
            'w': 100,
            'a_l': None,
            'a_t': ('bases', ']'),
            'a_r': ('keep_carets', ']'),
            'a_b': None,
            'sp_r': p,
            'cap': _('Convert'),
            'hint': _('Convert numbers in selections to chosen base'),
            'en': False,
            'on_change': self.btn_convert_click,
            'on_mouse_enter': self.mouse_move,
            })
        self.n_btn_convert = n
        self.msgs[n] = _('Starts the conversion process.')
        self.controls.append(n)

        return h

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
            for id in self.controls:
                self.set_prop(id, 'en', True)

        self.upd_sb_text(self.form_msg)

    def form_hide(self, id_dlg, id_ctl, data='', info=''):
        ed.focus()
        dlg_proc(self.h_dlg, DLG_HIDE)

    def btn_convert_click(self, id_dlg, id_ctl, data='', info=''):
        carets = []

        keep = int(dlg_proc(self.h_dlg, DLG_CTL_PROP_GET,
                           index=self.n_chk_keep_carets)['val'])

        opt = int(dlg_proc(self.h_dlg, DLG_CTL_PROP_GET,
                           index=self.n_rg_base)['val'])

        one = self.carets[0]

        #Clean carets
        ed.set_caret(*one[:2], id=CARET_SET_ONE)

        for caret in self.carets:
            try:
                text = ed.get_text_substr(*caret).strip()
                res = self.get_suffix_number(text)

                if not res:
                    raise ValueError('Not found a correct base in caret')

                suffix, number = res

                new = old = -1

                try:
                    if suffix in self.suffixes[:3]:
                        # 0b, 0o or 0x
                        base = self.get_base(suffix)
                        old = int(number, base)
                    elif not suffix:
                        # Decimal value
                        old = int(number)
                    elif suffix == self.suffixes[3]:
                        # Use cudax_lib funtions
                        old = html_color_to_int(text)
                    else:
                        old = None

                    if not old:
                        raise ValueError('%s is a non valid number' % text)

                    new = old

                except Exception as e:
                    raise ValueError('The number "%s" is not valid with base %s' %
                                     (number, suffix))

                if opt == Base.binary.value and suffix != self.suffixes[0]:
                    try:
                        new = bin(old)
                    except Exception as e:
                        raise ValueError('%s cannot convert to Binary.' %
                                         str(old))

                if opt == Base.octal.value and suffix != self.suffixes[1]:
                    try:
                        new = oct(old)
                    except Exception as e:
                        raise ValueError('%s cannot convert to Octal.' %
                                         str(old))

                if opt == Base.hexadecimal.value and suffix != self.suffixes[2]:
                    try:
                        new = hex(old)
                    except Exception as e:
                        raise ValueError('%s cannot convert to Hexadecimal.' %
                                         str(old))

                if opt == Base.html.value and suffix != self.suffixes[3]:
                    try:
                        new = int_to_html_color(old)
                    except Exception as e:
                        raise ValueError('%s cannot convert to Hexadecimal.' %
                                         str(old))

                continue_dec = opt == Base.decimal.value and suffix

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

    def get_suffix_number(self, text):
        bases = '|'.join(self.suffixes)
        pattern = r'\A(?P<suffix>' + bases + r')?(?P<number>.+)'

        match = re.search(pattern, text)
        if not match:
            return

        suffix = match.group('suffix') if match.group('suffix') else None
        number = match.group('number') if match.group('number') else None

        return suffix, number

    def get_base(self, suffix):
        if suffix == self.suffixes[0]:
            return 2

        if suffix == self.suffixes[1]:
            return 8

        if suffix == self.suffixes[2]:
            return 16

        return None

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
                x2, y2 = x1, y1
                continue

            if (y1, x1) > (y2, x2):
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            if (y2 - y1) > 0:
                self.form_msg = _('Multi-line is not allowed.')
                return False

            new_carets.append((x1, y1, x2, y2))

        if not new_carets:
            self.form_msg = _('Make text selection(s) first.')
            return False
        else:
            self.form_msg = _('%d carets to process. Not valid numbers will be skipped.') % len(new_carets)
            self.carets = new_carets
            return True