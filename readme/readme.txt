plugin for CudaText.
it is several plugins merged, which give commands to work with numbers.

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



author: Alexey (CudaText)
license: MIT
