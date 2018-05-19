plugin for CudaText.
merged several plugins, which give number-related commands.


Insert Numbers
--------------
dialog to insert numbers: from starting number, with increment (default 1), with prefix/suffix strings.
- only one caret allowed.
- if selection exists, then selected lines will be numbered, at line start.
- if no selection, then "repeat counter" field is enabled in dialog, numbers are inserted at start of caret's line.


Carets Numbering
----------------
works only with multi-carets, allows to insert increasing/decreasing numbers in positions of all multi-carets.
for example, you can insert:
- 00, 01, 02, 03...
- 0030, 0031, 0032...
- 100, 95, 90, 85...

gives dialog to input parameters:
- Starting number (default is 1)
- Increment (use value<0 to make decreasing numbers)
- Number of digits, ie width of numbers (if it's 3, numbers can be 001, 002, 003...)
- Text before numbers (prefix)
- Text after numbers (suffix)
- Base: 
  - "d": decimal format
  - "x": hex format
  - "o": octal format
  - "r": Roman notation


Romanize
--------
converts number (in the current editor under first caret) between decimal and Roman formats.
plugin reads an entire word at caret, and tries to convert it.

Roman numbers can have only digits: IVXLCDM, lowercase digits are allowed.
numbers<=0 are not supported.
result is not nice for numbers >=4000.

gives commands:
- Show: convert number between decimal/Roman, and show it in the statusbar
- Replace: the same, and replace number in the editor


Number to Words
---------------
converts number (under caret) into textual form, e.g.
- "10" -> "ten"
- "2030" -> "two thousand and thirty"
works with integer and floating numbers.
floating point can be "." and ",".

gives commands:
- read number under caret, put result to a new tab
- read number under caret, replace this number with result
- select language


Number to Words, Ru
-------------------
converts number (under caret) into Russian textual form, e.g.
- "10" -> "десять"
- "2030" -> "две тысячи тридцать"
works with integer and floating numbers.
floating point can be "." and ",".

gives commands:
- number to words, put to new tab
- number to words, replace
- roubles to words, put to new tab
- roubles to words, replace


author: Alexey (CudaText)
license: MIT
