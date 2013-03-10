# -*- coding: utf-8 -*-

'''
Created on Apr 27, 2011

@author: Bartosz Alchimowicz

Generowanie wyrażenie regularnego dla non-negative integers (0, 1, 2, 3...).

Supported format:

format jak dla interger
'''

import builder
from regexpgen.misc import assertMinMax

def run(format, min, max, startEndMatcher):
	assertMinMax(min, max)
	if(max is not None) and (max < 0):
		raise Exception("Invalid parameters (max<0)")

	b = builder.RegexBuilder()
	return b.CreateNNIntegerRegex(format, min, max)