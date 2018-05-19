# Code from: https://github.com/GCTsalamagkakis/Romanize
# Copyright (c) 2018 George-Chris Tsalamagkakis 
# License: MIT

CHARS = [
	(1000, 'M'),
	(900, 'CM'),
	(500, 'D'),
	(400, 'CD'),
	(100, 'C'),
	(90, 'XC'),
	(50, 'L'),
	(40, 'XL'),
	(10, 'X'),
	(9, 'IX'),
	(5, 'V'),
	(4, 'IV'),
	(1, 'I')
	]


def from_romans(str):

	i = 0
	decimal = 0
	while i < len(str):
		for number, symbol in CHARS:
			if str[i] == symbol or str[i].upper() == symbol:
				symbol1 = number
		if i+1 < len(str):
			for number, symbol in CHARS:
				if str[i+1] == symbol or str[i+1].upper() == symbol:
					symbol2 = number
			if symbol1 >= symbol2:
				decimal += symbol1
				i += 1
			else:
				decimal += symbol2 - symbol1
				i += 2
		else:
			decimal += symbol1
			i += 1
	return decimal

def to_romans(decimal):

	roman = ""
	for number, symbol in CHARS:
		while decimal >= number:
			roman += symbol
			decimal -= number
	return roman

