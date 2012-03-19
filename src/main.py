'''
Created on Apr 27, 2011

@author: Bartosz Alchimowicz
'''

import regexpgen

print regexpgen.misc.rawBounds(127, 12891)
print regexpgen.misc.rawBounds(127, None)
print regexpgen.misc.rawBounds(None, 123)
print regexpgen.misc.rawBounds(None, None)
print regexpgen.misc.rawBounds(129, 131)
print regexpgen.misc.rawBounds(127, 128)
