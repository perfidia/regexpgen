'''
Created on Apr 27, 2011

@author: Bartosz Alchimowicz
'''

import regexpgen

#print regexpgen.integer("%d")
#print regexpgen.integer("%d", -5, 1)
#print regexpgen.integer("%d", 126, 12234)
#print regexpgen.misc.rawBounds(0, 100)
#print regexpgen.integer(r"%d", 0)
#print regexpgen.misc.rawBounds(0, 257)
#print regexpgen.misc.rawBounds(0, 100, 4)
print regexpgen.misc.rawBounds(101, None, 4)
regexp = regexpgen.integer(r"%04d", min = 100)
print regexp