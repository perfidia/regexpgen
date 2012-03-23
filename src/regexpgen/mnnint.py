# -*- coding: utf-8 -*-

'''
Created on Apr 27, 2011

@author: Bartosz Alchimowicz

Generowanie wyrażenie regularnego dla non-negative integers (0, 1, 2, 3...).

Supported format:

format jak dla interger
'''

import minteger
from regexpgen.misc import assertMinMax

def run(format, min, max):
	assertMinMax(min, max)
	if(max is not None) and (max < 0):
		raise Exception("Invalid parameters (max<0)")
	if(min is None) or (min < 0):
		min = 0;
	f = minteger.run(format, min, max)
	f = f.replace("-0","0")
	return f
