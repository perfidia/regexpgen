'''
Created on Apr 27, 2011

@author: Bartosz Alchimowicz
'''

import regexpgen
import re

#print regexpgen.nnint("%0d")
#print regexpgen.nnint("%04d", 71, 2319)
#print regexpgen.integer("%d", -5, 1)
#print regexpgen.nnint("%01d", )
b = regexpgen.builder.RegexBuilder()
#print b.calculateRealRegex(5.001, 5.312)
#print b.calculateRealRegex(5.0010, 5.312)
#print b.calculateRealRegex(5.1, 6.7)
#print b.calculateRealRegex(5.01, 6.7)
#print b.calculateRealRegex(5.23, 6.437)
#print b.calculateRealRegex(5.23, 6.4)
#print b.CreateIntegerRegex("%0d", None, 5)
print b.calculateRealRegex(0, 2.5)
#print re.match(b.CreateIntegerRegex("%0d", None, 5), "00")

#print regexpgen.integer("%03d", 1, 312)
#print regexpgen.integer("%03d", int("001"), "311")

#print regexpgen.integer("%07d", 432, 12234)
#print regexpgen.misc.rawBounds(0, 100)
#print regexpgen.integer(r"%d", 0)
#print regexpgen.misc.rawBounds(0, 257)
#print regexpgen.misc.rawBounds(0, 100, 4)
#print regexpgen.misc.rawBounds(101, None, 4)
#regexp = regexpgen.integer(r"%04d", min = 100)
#print regexp