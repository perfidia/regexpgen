'''
Created on Apr 27, 2011

@author: Bartosz Alchimowicz
'''

import regexpgen

print regexpgen.nnint("%04d", 71, 2319)
print regexpgen.integer("%0d", -521, 132)
print regexpgen.real("%lf", -12.325454, 23.0132443)
print regexpgen.ip(100, 105, 250, 255, 122, 122, 0, 240)