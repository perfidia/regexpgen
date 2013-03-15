# -*- coding: utf-8 -*-

'''
Set of functions to generate regular expressions from a pattern similar to printf function.
'''

import minteger, mnnint, mreal#, mdate, mtime, mdatetime

def nnint(format, min = None, max = None, matchStartEnd = True):
	"""Generate regular expression for a non negative integer.

	:param format: format similar to C printf function
	:param min: optional minimum value
	:param max: optional maximum value
	:param matchStartEnd: True if ^ at the beginning and $ at the ending of regexp are required

	:return: regular expression for a given format
	"""

	return mnnint.run(format, min, max)

def integer(format, min = None, max = None, matchStartEnd = True):
	"""Generate regular expression for an integer.

	:param format: format similar to C printf function
	:param min: optional minimum value
	:param max: optional maximum value
	:param matchStartEnd: True if ^ at the beginning and $ at the ending of regexp are required

	:return: regular expression for a given format
	"""

	return minteger.run(format, min, max)

def real(format, min = None, max = None, matchStartEnd = True):
	return mreal.run(format, min, max)
#
#def date(format, min = None, max = None, timezone = None, matchStartEnd = True):
#	return startEndMatcher(mdate.run(format, min, max, timezone), matchStartEnd)
#
#def time(format, min = None, max = None, timezone = None, matchStartEnd = True):
#	return startEndMatcher(mtime.run(format, min, max, timezone), matchStartEnd)
#
#def datetime(format, date_min = None, date_max = None, time_min = None, time_max = None, timezone = None, matchStartEnd = True):
#	return startEndMatcher(mdatetime.run(format, date_min, date_max, time_min, time_max, timezone), matchStartEnd)

# put it somewhere else...
def startEndMatcher(re_str, matchStartEnd = True):
	if not matchStartEnd:
		re_str = re_str.replace("^",'')
		re_str = re_str.replace("$",'')

	return re_str
