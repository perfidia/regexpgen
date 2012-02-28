# -*- coding: utf-8 -*-

'''
Created on Apr 27, 2011

@author: Bartosz Alchimowicz

Parametry:
format - format danych zgodny z poleceniem printf w C
min - wartość minimalna, domyślna wartość: None
max - wartość maksymalna, domyślna wartość: None
'''

import minteger, mreal, mdate, mtime, mdatetime, mnnint

def nnint(format, min = None, max = None):
	return mnnint.run(format, min, max)

def integer(format, min = None, max = None):
	return minteger.run(format, min, max)

def real(format, min = None, max = None):
	return mreal.run(format, min, max)

def date(format, min = None, max = None, timezone = None):
	return mdate.run(format, min, max, timezone)

def time(format, min = None, max = None, timezone = None):
	return mtime.run(format, min, max, timezone)

def datetime(format, date_min = None, date_max = None, time_min = None, time_max = None, timezone = None):
	return mdatetime.run(format, date_min, date_max, time_min, time_max, timezone)
