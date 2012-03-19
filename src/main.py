'''
Created on Apr 27, 2011

@author: Bartosz Alchimowicz
'''

import regexpgen

print regexpgen.integer("%d")
print regexpgen.integer("%d", -5, 1)
print regexpgen.integer("%d", 126, 12234)
print regexpgen.misc.rawBounds(0, 100)

