'''
Created on Apr 27, 2011

@authors: Joanna Binczewska, Dawid Kowalski
'''

import regexpgen
import re 

# print regexpgen.nnint("%04d", 71, 2319)
# print regexpgen.integer("%0d", -521, 132)
# print regexpgen.real("%lf", -12.7, 23.5)
# print regexpgen.real("%lf", -100.0, 100.0)
# print regexpgen.real("%lf", 0.0, 10.1)
# print regexpgen.concatenate([
# 		('int', "%d", 100, 105),
# 		('\.',),
# 		('int', "%d", 250, 255),
# 		('\.',),
# 		('int', "%d", 122, 122),
# 		('\.',),
# 		('int', "%d", 0, 240)
# ])

x = regexpgen.time("%I:%M (%P)", "10:44 (AM)", "10:21 (PM)")
print x
print re.match(x, "10:45 (AM)")
print re.match(x, "10:59 (AM)") 
print re.match(x, "09:45 (PM)")
print re.match(x, "06:45 (PM)")
print "a" 
print re.match(x, "13:43")
print re.match(x, "10:22 (PM)")
print re.match(x, "11:22 (PM)")


