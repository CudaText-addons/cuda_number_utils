from cudatext import *
from .romans import to_romans

from cudax_lib import get_translation
_ = get_translation(__file__)  # I18N


def _format_int(num, n_len, fmt):
    if fmt in ('d', 'x', 'o'):
        s = '%0'+str(n_len)+fmt
        return s % num
    if fmt=='r':
        return to_romans(num)


def dialog_carets_num():

    carets = ed.get_carets()
    if len(carets)<2:
        msg_status(_('Place several carets first'))
        return

    s = dlg_input_ex(6, _('Carets Numbering'),
      _('Starting number:'), '1',
      _('Increment (can be <0):'), '1',
      _('Digits:'), '1',
      _('Text before numbers:'), '',
      _('Text after numbers:'), '',
      _('Base: d=dec, x=hex, o=octal, r=romans'), 'd',
      )
    if not s: return

    try:
        n_start = int(s[0])
    except:
        msg_box(_('Incorrect number entered: ')+s[0], MB_OK)
        return

    try:
        n_inc = int(s[1])
    except:
        msg_box(_('Incorrect number entered: ')+s[1], MB_OK)
        return

    try:
        n_len = int(s[2])
    except:
        msg_box(_('Incorrect number entered: ')+s[2], MB_OK)
        return

    text_before = s[3]
    text_after = s[4]
    n_base = s[5]

    if not n_base in ('d', 'x', 'o', 'r'):
        msg_box(_('Incorrect base value entered'), MB_OK)
        return

    ed.lock()
    for i in range(len(carets)-1, -1, -1):
        caret = carets[i]
        num = n_start + n_inc*i
        s_num = _format_int(num, n_len, n_base)
        text = text_before + s_num.upper() + text_after
        ed.insert(caret[0], caret[1], text)
    ed.unlock()

    msg_status(_('Inserted %d numbers') % len(carets))
