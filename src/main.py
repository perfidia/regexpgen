'''
Created on Apr 27, 2011

@authors: Joanna Binczewska, Dawid Kowalski
'''

import regexpgen

print regexpgen.nnint("%04d", 71, 2319)
print regexpgen.integer("%0d", -521, 132)
print regexpgen.real("%lf", -12.7, 23.5)
print regexpgen.ip(100, 105, 250, 255, 122, 122, 0, 240)
print regexpgen.real("%lf", -100.0, 100.0)
print regexpgen.real("%lf", 0.0, 10.1)