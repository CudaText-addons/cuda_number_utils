from cudatext import *
from .romans import to_romans


def _format_int(num, n_len, fmt):
    if fmt in ('d', 'x', 'o'):
        s = '%0'+str(n_len)+fmt
        return (s%num).upper()
    if fmt=='r':
        return to_romans(num)


def dialog_insert_numbers():

    carets = ed.get_carets()
    if len(carets)!=1:
        msg_status('Cannot handle multi-carets')
        return

    x0, y0, x1, y1 = carets[0]
    use_sel = y1>=0
    if use_sel:
        if not ((y1>y0) or ((y1==y0) and (x1>x0))):
            x0, y0, x1, y1 = x1, y1, x0, y0

    text_info = 'Specified count of lines will be inserted' if not use_sel else 'Selected lines will be changed'

    id_prefix = 1
    id_startnum = 3
    id_digits = 5
    id_suffix = 7
    id_onlytext = 8
    id_skipempty = 9
    id_afterlead = 10
    id_repeat = 12
    id_base = 14
    id_ok = 16

    c1 = chr(1)
    res = dlg_custom('Insert Numbers', 600, 220, '\n'.join([]
      +[c1.join(['type=label', 'cap=&Prefix:', 'pos=6,6,200,0'])]
      +[c1.join(['type=edit', 'val=', 'pos=6,24,194,0'])]
      +[c1.join(['type=label', 'cap=Start &num:', 'pos=200,6,300,0'])]
      +[c1.join(['type=spinedit', 'val=1', 'props=-1000,1000000,1', 'pos=200,24,294,0'])]
      +[c1.join(['type=label', 'cap=&Digits:', 'pos=300,6,400,0'])]
      +[c1.join(['type=spinedit', 'val=1', 'props=1,20,1', 'pos=300,24,394,0'])]
      +[c1.join(['type=label', 'cap=&Suffix:', 'pos=400,6,600,0'])]
      +[c1.join(['type=edit', 'val=', 'pos=400,24,594,0'])]
      +[c1.join(['type=check', 'cap=&Use only prefix+suffix', 'pos=6,54,500,0'])]
      +[c1.join(['type=check', 'cap=Skip &empty lines', 'pos=6,80,500,0', 'val=1', 'en='+str(int(use_sel)) ])]
      +[c1.join(['type=check', 'cap=Insert &after leading spaces', 'pos=6,106,500,0', 'en='+str(int(use_sel)) ])]
      +[c1.join(['type=label', 'cap=&Repeat counter:', 'en='+str(int(not use_sel)), 'pos=6,130,100,0'])]
      +[c1.join(['type=spinedit', 'val=4', 'props=1,2000000,1', 'en='+str(int(not use_sel)), 'pos=6,150,100,0'])]
      +[c1.join(['type=label', 'cap=Number &base:', 'pos=200,130,400,0'])]
      +[c1.join(['type=combo_ro', 'items=Decimal\tHex\tOctal\tRomans', 'val=0', 'pos=200,150,300,0'])]
      +[c1.join(['type=label', 'cap='+text_info, 'pos=6,190,400,0'])]
      +[c1.join(['type=button', 'cap=&OK', 'props=1', 'pos=400,190,494,0'])]
      +[c1.join(['type=button', 'cap=Cancel', 'pos=500,190,594,0'])]
      ))
    if res is None: return

    (btn, text) = res
    if btn!=id_ok: return
    text = text.splitlines()

    s_prefix = text[id_prefix]
    n_startnum = int(text[id_startnum])
    n_digits = int(text[id_digits])
    s_suffix = text[id_suffix]
    n_repeat = int(text[id_repeat])
    b_onlytext = bool(int(text[id_onlytext]))
    b_skipempty = bool(int(text[id_skipempty]))
    b_afterlead = bool(int(text[id_afterlead]))
    n_base = int(text[id_base])

    text_repeat = 'repeat %d'%n_repeat if not use_sel else 'selection'
    text_onlytext = 'only text' if b_onlytext else ''
    s_format = ['d', 'x', 'o', 'r'][n_base]

    #print('Insert numbers: prefix "%s", start %d, digits %d, suffix "%s", %s, %s' % \
    #      (s_prefix, n_startnum, n_digits, s_suffix, text_repeat, text_onlytext))

    if use_sel:
        number = n_startnum
        for i in range(y0, y1+1):
            s_prev = ed.get_text_line(i)
            s_indent = ''

            if b_skipempty:
                if not s_prev.strip():
                    continue

            if b_afterlead:
                n = 0
                while n<len(s_prev) and s_prev[n] in (' ', '\t'): n += 1
                s_indent = s_prev[:n]
                s_prev = s_prev[n:]

            if b_onlytext:
                s = s_indent + s_prefix + s_prev + s_suffix
            else:
                s = s_indent + s_prefix + _format_int(number, n_digits, s_format) + s_suffix + s_prev
                number += 1
            ed.set_text_line(i, s)
    else:
        items = []
        for i in range(n_repeat):
            s = '' if b_onlytext else _format_int(n_startnum+i, n_digits, s_format)
            items += [s_prefix + s + s_suffix]
        items += ['']
        ed.insert(0, y0, '\n'.join(items))

    msg_status('Numbers inserted')
