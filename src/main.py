'''
Created on Apr 27, 2011

@authors: Joanna Binczewska, Dawid Kowalski
'''

import regexpgen
import re

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

x = regexpgen.real("%lf", 6.063, 9.493)
print x
print re.match(x, "9.49") # powinno byc match

x = regexpgen.real("%lf", 15.07, None)
print x
print re.match(x, "15.3") # powinno byc match

x = regexpgen.real("%lf", None, 0.4)
print x
print re.match(x, "0.8") # powinno byc None

x = regexpgen.real("%lf", None, 14.00)
print x
print re.match(x, "0.519") # powinno byc match

x = regexpgen.real("%lf", 40.822, 46.202)
print x
print re.match(x, "46.21") # powinno byc None

x = regexpgen.real("%lf", 0.97, 1.04)
print x
print re.match(x, "0.9") # powinno byc None

print regexpgen.integer("%02d", 1, 7)
y = regexpgen.real("%lf", None, 13.077)
print y
print re.match(y, "13.088") # powinno byc None

z = regexpgen.real("%lf", None, 13.93)
print z
print re.match(z, "13.9") # powinno byc match

x = regexpgen.real("%lf", -6.1, -3.3)
print x
print re.match(x, "-6.8") # powinno byc None

#^(0*(40\.822|40(\.((8[3-9]|9)|(82[2-9]|8[3-9]|9))[0-9]*)|(4[1-4]|45)\.[0-9]+|46(\.((1|2)|(0[1-9]|1|20)|(00|01|0[2-9]|10|1[1-9]|20[0-1]))[0-9]*)|46\.2020*))$





