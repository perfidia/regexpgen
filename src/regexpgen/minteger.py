# -*- coding: utf-8 -*-

'''
Created on Apr 27, 2011

@author: Bartosz Alchimowicz

Generowanie wyrażenie regularnego dla integers (-2, -1, 0, 1, 2, 3...).

Supported format:

FORMAT = '%d'
opis: zera wiodące są opcjonalne,
przykłady poprawne: 0, 1, 001, 012
przykłady niepoprawne: N/A

FORMAT = '%0d'
opis: zera wiodące niedowolone
przykłady poprawne: 0, 1
przykłady niepoprawne: 001, 012

FORMAT = '%0Xd'
opis: liczba zapisana przy pomocy X znaków, w przypadku liczb
      mniejszych od int('9'*X) należy liczbą poprzedzić zerami,
      zera wiodące są wymagane
przykłady poprawne dla %04d: 0001, 45678
przykłady niepoprawne dla %04d: 00011, 11
'''

def default(format, min, max):
	return r'(-)?[0-9]+'

def no_leading_zeros(format, min, max):
	return r'(-)?[1-9][0-9]*'

def run(format, min, max):
	result = {
		'%d': default,
		'%0d': no_leading_zeros,
	}.get(format, complex)(format, min, max)

	return result
