# -*- coding: utf-8 -*-

'''
Set of functions to generate regular expressions from a pattern similar to printf function.
'''

import builder
#import mdate, mtime, mdatetime

def nnint(format, min = None, max = None, matchStartEnd = True):
	"""Generate regular expression for a non negative integer.

	:param format: format similar to C printf function
	:param min: optional minimum value
	:param max: optional maximum value
	:param matchStartEnd: True if ^ at the beginning and $ at the ending of regexp are required

	:return: regular expression for a given format
	Generowanie wyrażenie regularnego dla non-negative integers (0, 1, 2, 3...).

	Supported format:

	format jak dla interger
	"""
	if (min is not None) and (max is not None) and (min>max):
		raise Exception("Invalid parameters (min>max)")
	if (max is not None) and (max < 0):
		raise Exception("Invalid parameters (max<0)")

	b = builder.RegexBuilder()
	return b.createNNIntegerRegex(format, min, max)

def integer(format, min = None, max = None, matchStartEnd = True):
	"""Generate regular expression for an integer.

	:param format: format similar to C printf function
	:param min: optional minimum value
	:param max: optional maximum value
	:param matchStartEnd: True if ^ at the beginning and $ at the ending of regexp are required

	:return: regular expression for a given format
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
	"""
	if (min is not None) and (max is not None) and (min>max):
		raise Exception("Invalid parameters (min>max)")

	b = builder.RegexBuilder()
	return b.createIntegerRegex(format, min, max)

def real(format, min = None, max = None, matchStartEnd = True):
	'''
	Generowanie wyrażenie regularnego dla liczba reczywistych.

	Supported format:

	FORMAT = '%lf'
	opis: zera wiodące są dozwolone,
	przykłady poprawne: 0.1, 1.32, 001.21, 012.123

	FORMAT = '%0lf'
	opis: zera wiodące są niedowolone
	przykłady poprawne: 22.1, 1.1
	przykłady niepoprawne: 001.2, 012.9

	FORMAT = '%0.Ylf'
	opis: zera wiodące są niedowolone, po przecinku można wprowadzić dokładnie Y cyfr
	przykłady poprawne: 22.1, 1.1
	przykłady niepoprawne: 001.2, 012.9

	FORMAT = '%.Ylf'
	opis: zera wiodące są opcjonalne, po przecinku można wprowadzić dokładnie Y cyfr
	przykłady poprawne: 022.1, 1.1, 001.2, 012.9

	FORMAT = '%X.Ylf'
	opis: X jest ignorowany (działa jak '%.Ylf')

	FORMAT = '%0X.Ylf'
	opis: zera wiodące są wymagane, liczba jest zapisana przy wykorzystaniu co najmniej X znaków (łącznie z kropoką),
	      po przecinku można wprowadzić dokładnie Y cyfr,
	      jeżeli liczba zaweira mniej niż X znaków to przestrzeń należy wypełnić zerami
	przykłady poprawne dla %5.2lf: 022.1, 32431.2, 012.9
	przykłady poprawne dla %5.2lf: 22.1, 111.122
	'''

	if (min is not None) and (max is not None) and (min>max):
		raise Exception("Invalid parameters (min>max)")
	if (format not in ["%lf", "%0lf"]):
		raise Exception("unsupported format")

	b = builder.RegexBuilder()
	return  b.createRealRegex(format, min, max)

def ip(min1 = 0, max1 = 255, min2 = 0, max2 = 255, min3 = 0, max3 = 255, min4 = 0, max4 = 255, separator = "\."):
	if min1 > max1 or min2 > max2 or min3 > max3 or min4 > max4:
		raise Exception("Invalid parameters (min > max)")
	if (min1 < 0 or min1 > 255 or min2 < 0 or min2 > 255 or min3 < 0 or min3 > 255 or min4 < 0 or min4 > 255):
		raise Exception("Invalid parameters (must be between o and 255)")

	ans = ""

	b = builder.RegexBuilder()
	ans += b.createNNIntegerRegex("%0d", min1, max1) + separator

	b = builder.RegexBuilder()
	ans += b.createNNIntegerRegex("%0d", min2, max2) + separator

	b = builder.RegexBuilder()
	ans += b.createNNIntegerRegex("%0d", min3, max3) + separator

	b = builder.RegexBuilder()
	ans += b.createNNIntegerRegex("%0d", min4, max4)

	return "^({0})$".format(ans.replace("^", "").replace("$", ""))

#def date(format, min = None, max = None, timezone = None, matchStartEnd = True):
#	return startEndMatcher(mdate.run(format, min, max, timezone), matchStartEnd)
#
#def time(format, min = None, max = None, timezone = None, matchStartEnd = True):
#	return startEndMatcher(mtime.run(format, min, max, timezone), matchStartEnd)
#
#def datetime(format, date_min = None, date_max = None, time_min = None, time_max = None, timezone = None, matchStartEnd = True):
#	return startEndMatcher(mdatetime.run(format, date_min, date_max, time_min, time_max, timezone), matchStartEnd)
