# -*- coding: utf-8 -*-

'''
Created on Apr 27, 2011

@author: Bartosz Alchimowicz

Generowanie wyrażenie regularnego dla non-negative integers (0, 1, 2, 3...).

Supported format:

format jak dla interger
'''

import minteger

def run(format, min, max):
	f = minteger.run(format, min, max)
	return f.replace("-?", "")
