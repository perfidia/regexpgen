'''
Created on Apr 27, 2011

@authors: Joanna Binczewska, Dawid Kowalski
'''

import regexpgen
import re

print (re.match(regexpgen.real("%lf", 11.999), "11.9999"))
#print regexpgen.nnint("%04d", 71, 2319)
#print regexpgen.integer("%0d", -521, 132)
#print regexpgen.real("%lf", -12.7, 23.5)
#print regexpgen.real("%lf", -100.0, 100.0)
#print regexpgen.real("%lf", 0.0, 10.1)
#print regexpgen.concatenate([
#		('int', "%d", 100, 105),
#		('\.',),
#		('int', "%d", 250, 255),
#		('\.',),
#		('int', "%d", 122, 122),
#		('\.',),
#		('int', "%d", 0, 240)
#]




