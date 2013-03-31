# -*- coding: utf-8 -*-

'''
Set of functions to generate regular expressions from a pattern similar to printf function.
'''

import builder
import re
#import mdate, mtime, mdatetime

def nnint(frmt, minV = None, maxV = None, matchStartEnd = True):
	"""Generate regular expression for a non negative integer.

	:param frmt: frmt similar to C printf function
	:param minV: optional minimum value
	:param maxV: optional maximum value
	:param matchStartEnd: True if ^ at the beginning and $ at the ending of regexp are required

	:return: regular expression for a given frmt
	Generowanie wyrażenie regularnego dla non-negative integers (0, 1, 2, 3...).

	Supported frmt:

	frmt jak dla interger
	"""
	
	b = builder.RegexBuilder()
	return b.createNNIntegerRegex(frmt, minV, maxV)

def integer(frmt, minV = None, maxV = None, matchStartEnd = True):
	"""Generate regular expression for an integer.

	:param frmt: frmt similar to C printf function
	:param minV: optional minimum value
	:param maxV: optional maximum value
	:param matchStartEnd: True if ^ at the beginning and $ at the ending of regexp are required

	:return: regular expression for a given frmt
	Generowanie wyrażenie regularnego dla integers (-2, -1, 0, 1, 2, 3...).

	Supported frmt:

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
	
	b = builder.RegexBuilder()
	return b.createIntegerRegex(frmt, minV, maxV)

def real(format, min = None, max = None, matchStartEnd = True):
	'''
	Generowanie wyrażenie regularnego dla liczba rzeczywistych.

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

	b = builder.RegexBuilder()
	return  b.createRealRegex(format, min, max)

def concatenate(concatenationList):
	result = ""
	for element in concatenationList:
		if len(element) == 1:
			result += element[0]
		elif len(element) == 4:
			if element[0] == "int":
				b = builder.RegexBuilder()
				result += b.createIntegerRegex(element[1], int(element[2]), int(element[3])).replace("^", "")
			elif element[0] == "real":
				result += b.createRealRegex(element[1], int(element[2]), int(element[3])).replace("^", "")
			else:
				raise ValueError("Bad input")
		else:
			raise ValueError("Bad input")
	return "^({0})$".format(result.replace("^", "").replace("$", ""))

#def date(format, min = None, max = None, timezone = None, matchStartEnd = True):
#	return startEndMatcher(mdate.run(format, min, max, timezone), matchStartEnd)
#
#def time(format, min = None, max = None, timezone = None, matchStartEnd = True):
#	return startEndMatcher(mtime.run(format, min, max, timezone), matchStartEnd)
#
#def datetime(format, date_min = None, date_max = None, time_min = None, time_max = None, timezone = None, matchStartEnd = True):
#	return startEndMatcher(mdatetime.run(format, date_min, date_max, time_min, time_max, timezone), matchStartEnd)
