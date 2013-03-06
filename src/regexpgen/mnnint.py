# -*- coding: utf-8 -*-

'''
Created on Apr 27, 2011

@author: Bartosz Alchimowicz

Generowanie wyrażenie regularnego dla non-negative integers (0, 1, 2, 3...).

Supported format:

format jak dla interger
'''

import builder
import re
from regexpgen.misc import assertMinMax

def run(format, min, max):
	assertMinMax(min, max)
	if(max is not None) and (max < 0):
		raise Exception("Invalid parameters (max<0)")

	b = builder.NNIntegerRegexBuilder()

	if format == "%0d":
		b.CreateNNIntegerRegex(format, min, max)
		return "^("+b.BuildRegEx()+")$"

	if format == "%d":
		b.CreateNNIntegerRegex(format, min, max)
		return "^(0*("+b.BuildRegEx()+"))$"

	if re.match('%0([0-9]+)d', format):
		m = re.search('%0([0-9]+)d', format)
		zeros = int(m.group(1))
		b.CreateNNIntegerRegex(format, min, max, zeros)
		return "^("+b.BuildRegEx()+")$"