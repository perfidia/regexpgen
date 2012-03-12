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

def nnint(format, min = None, max = None, matchStartEnd = True):
	return startEndMatcher(mnnint.run(format, min, max), matchStartEnd)

def integer(format, min = None, max = None, matchStartEnd = True):
	return startEndMatcher(minteger.run(format, min, max), matchStartEnd)

def real(format, min = None, max = None, matchStartEnd = True):
	return startEndMatcher(mreal.run(format, min, max), matchStartEnd)

def date(format, min = None, max = None, timezone = None, matchStartEnd = True):
	return startEndMatcher(mdate.run(format, min, max, timezone), matchStartEnd)

def time(format, min = None, max = None, timezone = None, matchStartEnd = True):
	return startEndMatcher(mtime.run(format, min, max, timezone), matchStartEnd)

def datetime(format, date_min = None, date_max = None, time_min = None, time_max = None, timezone = None, matchStartEnd = True):
	return startEndMatcher(mdatetime.run(format, date_min, date_max, time_min, time_max, timezone), matchStartEnd)


def startEndMatcher(re_str, matchStartEnd = True):
	if(not matchStartEnd):
		re_str = re_str.replace("^",'')
		re_str = re_str.replace("$",'')
	return re_str
