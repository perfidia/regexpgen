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

def run(frmt, minV, maxV):
	assertMinMax(minV, maxV)
	if(maxV is not None) and (maxV < 0):
		raise Exception("Invalid parameters (max<0)")

	b = builder.RegexBuilder()
	return b.CreateNNIntegerRegex(frmt, minV, maxV)