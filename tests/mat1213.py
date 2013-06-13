'''
Created on Mar 30, 2013

@author: Bartosz Alchimowicz
'''

import unittest
import re
import regexpgen
import itertools

class Test(unittest.TestCase):
	def testPhase1Stage1(self):
		# 06 March 2013: nnint %d %0d %0Xd
		func = regexpgen.nnint

		self.assertRaises(ValueError, func, "%d",   'a', 'a')
		self.assertRaises(ValueError, func, "%0d",  'b', 'b')
		self.assertRaises(ValueError, func, "%03d", 'c', 'c')

		self.assertRaises(ValueError, func, "%0d", 21.1, 132)
		self.assertRaises(ValueError, func, "%0d", 21, 132.1)
		self.assertRaises(ValueError, func, "%0d", 21.1, 132.1)

		self.assertRaises(ValueError, func, "%lf")
		self.assertRaises(ValueError, func, "% d")
		self.assertRaises(ValueError, func, "%dddd")
		self.assertRaises(ValueError, func, "")

		self.assertRaises(ValueError, func, None) # ISSUE 5
		self.assertRaises(ValueError, func, None, None, None) # ISSUE 5

		self.assertTrue (re.match(func("%d", None), "12"))
		self.assertTrue (re.match(func("%d", None, 10), "10"))
		self.assertFalse(re.match(func("%d", None, 10), "11"))
		self.assertFalse(re.match(func("%d", 1, None), "-1"))
		self.assertFalse(re.match(func("%d", 1, None), "0"))
		self.assertTrue (re.match(func("%d", 1, None), "1"))
		self.assertTrue (re.match(func("%d", None, None), "0"))
		self.assertFalse(re.match(func("%d", None, None), "-1"))

		self.assertFalse(re.match(func("%d"), "-100"))
		self.assertFalse(re.match(func("%d"), "-1"))
		self.assertTrue (re.match(func("%d"), "0"))
		self.assertTrue (re.match(func("%d"), "1"))
		self.assertTrue (re.match(func("%d"), "100"))

		self.assertTrue (re.match(func("%d",   0, 100), "0"))
		self.assertTrue (re.match(func("%d",   0, 100), "1"))
		self.assertTrue (re.match(func("%d",   0, 100), "50"))
		self.assertTrue (re.match(func("%d",   0, 100), "99"))
		self.assertTrue (re.match(func("%d",   0, 100), "100"))
		self.assertTrue (re.match(func("%d",   0, 100), "00"))
		self.assertTrue (re.match(func("%d",   0, 100), "01"))
		self.assertTrue (re.match(func("%d",   0, 100), "050"))
		self.assertTrue (re.match(func("%d",   0, 100), "099"))
		self.assertTrue (re.match(func("%d",   0, 100), "0100"))
		self.assertFalse(re.match(func("%d",   0, 100), "-20"))
		self.assertFalse(re.match(func("%d",   0, 100), "-1"))
		self.assertFalse(re.match(func("%d",   0, 100), "101"))
		self.assertFalse(re.match(func("%d",   0, 100), "1010"))

		self.assertTrue (re.match(func("%0d",  0, 100), "0"))
		self.assertTrue (re.match(func("%0d",  0, 100), "1"))
		self.assertTrue (re.match(func("%0d",  0, 100), "50"))
		self.assertTrue (re.match(func("%0d",  0, 100), "99"))
		self.assertTrue (re.match(func("%0d",  0, 100), "100"))
		self.assertFalse(re.match(func("%0d",  0, 100), "00"))
		self.assertFalse(re.match(func("%0d",  0, 100), "01"))
		self.assertFalse(re.match(func("%0d",  0, 100), "050"))
		self.assertFalse(re.match(func("%0d",  0, 100), "099"))
		self.assertFalse(re.match(func("%0d",  0, 100), "0100"))
		self.assertFalse(re.match(func("%0d",  0, 100), "-20"))
		self.assertFalse(re.match(func("%0d",  0, 100), "-1"))
		self.assertFalse(re.match(func("%0d",  0, 100), "101"))
		self.assertFalse(re.match(func("%0d",  0, 100), "1010"))

		self.assertTrue (re.match(func("%03d", 0, 100), "000"))
		self.assertTrue (re.match(func("%03d", 0, 100), "001"))
		self.assertTrue (re.match(func("%03d", 0, 100), "050"))
		self.assertTrue (re.match(func("%03d", 0, 100), "099"))
		self.assertTrue (re.match(func("%03d", 0, 100), "100"))
		self.assertFalse(re.match(func("%03d", 0, 100), "0000"))
		self.assertFalse(re.match(func("%03d", 0, 100), "0001"))
		self.assertFalse(re.match(func("%03d", 0, 100), "00050"))
		self.assertFalse(re.match(func("%03d", 0, 100), "00099"))
		self.assertFalse(re.match(func("%03d", 0, 100), "00100"))
		self.assertFalse(re.match(func("%03d", 0, 100), "-20"))
		self.assertFalse(re.match(func("%03d", 0, 100), "-1"))
		self.assertFalse(re.match(func("%03d", 0, 100), "101"))
		self.assertFalse(re.match(func("%03d", 0, 100), "1010"))

		self.assertTrue(func("%d",   0,   10000))
		self.assertTrue(func("%d",   100, 10000))
		self.assertTrue(func("%0d",  0,   10000))
		self.assertTrue(func("%0d",  100, 10000))
		self.assertTrue(func("%03d", 0,   10000))
		self.assertTrue(func("%03d", 100, 10000))

	def testPhase1Stage2(self):
		# 13 March 2013: integer %d %0d %0Xd
		func = regexpgen.integer

		self.assertRaises(ValueError, func, "%d",   'a', 'a')
		self.assertRaises(ValueError, func, "%0d",  'b', 'b')
		self.assertRaises(ValueError, func, "%03d", 'c', 'c')

		self.assertRaises(ValueError, func, "%0d", 21.1, 132)
		self.assertRaises(ValueError, func, "%0d", 21, 132.1)
		self.assertRaises(ValueError, func, "%0d", 21.1, 132.1)

		self.assertRaises(ValueError, func, "%lf")
		self.assertRaises(ValueError, func, "% d")
		self.assertRaises(ValueError, func, "%dddd")
		self.assertRaises(ValueError, func, "%ad")
		self.assertRaises(ValueError, func, "")

		self.assertRaises(ValueError, func, None) # ISSUE 5
		self.assertRaises(ValueError, func, None, None, None) # ISSUE 5

		self.assertTrue (re.match(func("%d", None), "-1"))
		self.assertTrue (re.match(func("%d", None), "0"))
		self.assertTrue (re.match(func("%d", None), "1"))
		self.assertTrue (re.match(func("%d", None, 10), "-10"))
		self.assertTrue (re.match(func("%d", None, 10), "10"))
		self.assertFalse(re.match(func("%d", None, 10), "11"))
		self.assertFalse(re.match(func("%d", 1, None), "0"))
		self.assertTrue (re.match(func("%d", 1, None), "1"))
		self.assertTrue (re.match(func("%d", 1, None), "10"))
		self.assertTrue (re.match(func("%d", None, None), "-10"))
		self.assertTrue (re.match(func("%d", None, None), "10"))

		self.assertTrue(re.match(func("%d"), "-100"))
		self.assertTrue(re.match(func("%d"), "-1"))
		self.assertTrue(re.match(func("%d"), "0"))
		self.assertTrue(re.match(func("%d"), "1"))
		self.assertTrue(re.match(func("%d"), "100"))

		self.assertTrue (re.match(func("%d",   0, 100), "0"))
		self.assertTrue (re.match(func("%d",   0, 100), "1"))
		self.assertTrue (re.match(func("%d",   0, 100), "50"))
		self.assertTrue (re.match(func("%d",   0, 100), "99"))
		self.assertTrue (re.match(func("%d",   0, 100), "100"))
		self.assertTrue (re.match(func("%d",   0, 100), "00"))
		self.assertTrue (re.match(func("%d",   0, 100), "01"))
		self.assertTrue (re.match(func("%d",   0, 100), "050"))
		self.assertTrue (re.match(func("%d",   0, 100), "099"))
		self.assertTrue (re.match(func("%d",   0, 100), "0100"))
		self.assertFalse(re.match(func("%d",   0, 100), "-20"))
		self.assertFalse(re.match(func("%d",   0, 100), "-1"))
		self.assertFalse(re.match(func("%d",   0, 100), "101"))
		self.assertFalse(re.match(func("%d",   0, 100), "1010"))

		self.assertTrue (re.match(func("%0d",  0, 100), "0"))
		self.assertTrue (re.match(func("%0d",  0, 100), "1"))
		self.assertTrue (re.match(func("%0d",  0, 100), "50"))
		self.assertTrue (re.match(func("%0d",  0, 100), "99"))
		self.assertTrue (re.match(func("%0d",  0, 100), "100"))
		self.assertFalse(re.match(func("%0d",  0, 100), "00"))
		self.assertFalse(re.match(func("%0d",  0, 100), "01"))
		self.assertFalse(re.match(func("%0d",  0, 100), "050"))
		self.assertFalse(re.match(func("%0d",  0, 100), "099"))
		self.assertFalse(re.match(func("%0d",  0, 100), "0100"))
		self.assertFalse(re.match(func("%0d",  0, 100), "-20"))
		self.assertFalse(re.match(func("%0d",  0, 100), "-1"))
		self.assertFalse(re.match(func("%0d",  0, 100), "101"))
		self.assertFalse(re.match(func("%0d",  0, 100), "1010"))

		self.assertTrue (re.match(func("%03d", 0, 100), "000"))
		self.assertTrue (re.match(func("%03d", 0, 100), "001"))
		self.assertTrue (re.match(func("%03d", 0, 100), "050"))
		self.assertTrue (re.match(func("%03d", 0, 100), "099"))
		self.assertTrue (re.match(func("%03d", 0, 100), "100"))
		self.assertFalse(re.match(func("%03d", 0, 100), "0000"))
		self.assertFalse(re.match(func("%03d", 0, 100), "0001"))
		self.assertFalse(re.match(func("%03d", 0, 100), "00050"))
		self.assertFalse(re.match(func("%03d", 0, 100), "00099"))
		self.assertFalse(re.match(func("%03d", 0, 100), "00100"))
		self.assertFalse(re.match(func("%03d", 0, 100), "-20"))
		self.assertFalse(re.match(func("%03d", 0, 100), "-1"))
		self.assertFalse(re.match(func("%03d", 0, 100), "101"))
		self.assertFalse(re.match(func("%03d", 0, 100), "1010"))

		self.assertTrue (re.match(func("%d",   -100, 10), "0"))
		self.assertTrue (re.match(func("%d",   -100, 10), "1"))
		self.assertFalse(re.match(func("%d",   -100, 10), "50"))
		self.assertFalse(re.match(func("%d",   -100, 10), "99"))
		self.assertFalse(re.match(func("%d",   -100, 10), "100"))
		self.assertTrue (re.match(func("%d",   -100, 10), "00"))
		self.assertTrue (re.match(func("%d",   -100, 10), "01"))
		self.assertFalse(re.match(func("%d",   -100, 10), "050"))
		self.assertFalse(re.match(func("%d",   -100, 10), "099"))
		self.assertFalse(re.match(func("%d",   -100, 10), "0100"))
		self.assertTrue (re.match(func("%d",   -100, 10), "-20"))
		self.assertTrue (re.match(func("%d",   -100, 10), "-1"))
		self.assertFalse(re.match(func("%d",   -100, 10), "101"))
		self.assertFalse(re.match(func("%d",   -100, 10), "1010"))

		self.assertTrue (re.match(func("%0d",  -100, 10), "0"))
		self.assertTrue (re.match(func("%0d",  -100, 10), "1"))
		self.assertFalse(re.match(func("%0d",  -100, 10), "50"))
		self.assertFalse(re.match(func("%0d",  -100, 10), "99"))
		self.assertFalse(re.match(func("%0d",  -100, 10), "100"))
		self.assertFalse(re.match(func("%0d",  -100, 10), "00"))
		self.assertFalse(re.match(func("%0d",  -100, 10), "01"))
		self.assertFalse(re.match(func("%0d",  -100, 10), "050"))
		self.assertFalse(re.match(func("%0d",  -100, 10), "099"))
		self.assertFalse(re.match(func("%0d",  -100, 10), "0100"))
		self.assertTrue (re.match(func("%0d",  -100, 10), "-20"))
		self.assertTrue (re.match(func("%0d",  -100, 10), "-1"))
		self.assertFalse(re.match(func("%0d",  -100, 10), "101"))
		self.assertFalse(re.match(func("%0d",  -100, 10), "1010"))

		self.assertTrue (re.match(func("%03d", -100, 10), "000"))
		self.assertTrue (re.match(func("%03d", -100, 10), "001"))
		self.assertTrue (re.match(func("%03d", -100, 10), "010"))
		self.assertFalse(re.match(func("%03d", -100, 10), "011"))
		self.assertFalse(re.match(func("%03d", -100, 10), "050"))
		self.assertFalse(re.match(func("%03d", -100, 10), "099"))
		self.assertFalse(re.match(func("%03d", -100, 10), "100"))
		self.assertFalse(re.match(func("%03d", -100, 10), "0000"))
		self.assertFalse(re.match(func("%03d", -100, 10), "0001"))
		self.assertFalse(re.match(func("%03d", -100, 10), "00050"))
		self.assertFalse(re.match(func("%03d", -100, 10), "00099"))
		self.assertFalse(re.match(func("%03d", -100, 10), "00100"))
		self.assertTrue (re.match(func("%03d", -100, 10), "-020"))
		self.assertTrue (re.match(func("%03d", -100, 10), "-001"))
		self.assertTrue (re.match(func("%03d", -100, 10), "-100"))
		self.assertFalse(re.match(func("%03d", -100, 10), "-20"))
		self.assertFalse(re.match(func("%03d", -100, 10), "-1"))
		self.assertFalse(re.match(func("%03d", -100, 10), "101"))
		self.assertFalse(re.match(func("%03d", -100, 10), "-101"))
		self.assertFalse(re.match(func("%03d", -100, 10), "1010"))

		self.assertTrue(func("%d",   0,   10000))
		self.assertTrue(func("%d",   100, 10000))
		self.assertTrue(func("%0d",  0,   10000))
		self.assertTrue(func("%0d",  100, 10000))
		self.assertTrue(func("%03d", 0,   10000))
		self.assertTrue(func("%03d", 100, 10000))

		self.assertTrue (re.match(func("%d", 1, 1000),  "0999"))
		self.assertTrue (re.match(func('%0d', 1, 1000),  "999"))
		self.assertTrue (re.match(func('%04d', 0, 1000), "0101"))
		self.assertTrue (re.match(func("%0d", -521, 132), "-521"))
		self.assertFalse(re.match(func("%d", 1, 1000),  ""))
		self.assertFalse(re.match(func('%0d', 1, 1000),  ""))
		self.assertFalse(re.match(func('%04d', 0, 1000), ""))
		self.assertFalse(re.match(func("%0d", -521, 132), ""))
		self.assertFalse(re.match(func("%d", 100, 120), ""))
		self.assertTrue (re.match(func("%d", 100, 120), "0100"))
		self.assertFalse(re.match(func("%d", -100, 120), ""))
		self.assertTrue (re.match(func("%d", -16298, 11423), "-000"))
		self.assertFalse(re.match(func("%0d", -16298, 11423), "-000"))
		self.assertTrue (re.match(func("%04d", -16298, 11423), "0001"))
		self.assertRaises(ValueError, func, "%d", -1000.3, 1000)

	def testPhase1Stage3(self):
		# 20 March 2013: real %lf and %0lf
		func = regexpgen.real

		self.assertRaises(ValueError, func, "%lf", 'a', 'a')
		self.assertRaises(ValueError, func, "%lf", 10, 10)

		self.assertRaises(ValueError, func, None) # ISSUE 5
		self.assertRaises(ValueError, func, None, None)
		self.assertRaises(ValueError, func, None, None, None) # ISSUE 5

		self.assertTrue (re.match(func("%lf", None), "10.01"))
		self.assertTrue (re.match(func("%lf", None), "-10.01987"))
		self.assertFalse(re.match(func("%lf", None), "10.0.0"))
		self.assertTrue (re.match(func("%lf", None, 13.0), "12.999"))
		self.assertTrue (re.match(func("%lf", None, 13.0), "13.000"))
		self.assertFalse(re.match(func("%lf", None, 13.0), "13.001"))
		self.assertTrue (re.match(func("%lf", 11.999), "11.9999"))
		self.assertTrue (re.match(func("%lf", 11.999, None), "11.9999"))
		self.assertTrue (re.match(func("%lf", 12.0, None), "12.000"))
		self.assertTrue (re.match(func("%lf", 12.0, None), "12.001"))
		self.assertTrue (re.match(func("%lf", None, None), "-0000.0001"))

		self.assertTrue (re.match(func("%lf", -12.7, 23.5), "-0000.0001"))
		self.assertTrue (re.match(func("%lf", -100.0, 100.0), "0.0"))
		self.assertTrue (re.match(func("%lf", 0.0, 10.1), "0000.0000"))
		self.assertTrue (re.match(func("%lf", -0.01, 1.5), "1.5")) # ISSUE 6
		self.assertFalse(re.match(func("%lf", -0.01, 1.5), "1.51"))
		self.assertTrue (re.match(func("%lf", -0.01, 1.512), "1.5"))
		self.assertTrue (re.match(func("%lf", -0.01, 1.512), "1.512"))
		self.assertFalse(re.match(func("%lf", -0.01, 1.512), "1.5121"))
		self.assertTrue (re.match(func("%lf", -0.01, 1.50), "1.5"))
		self.assertTrue (re.match(func("%lf", -102.0, 100.0), "100.0"))

		self.assertFalse(re.match(func("%lf", 88.7653193745, 88.920716654), "88.0"))
		self.assertTrue (re.match(func("%lf", 88.7653193745, 88.920716654), "88.9")) # ISSUE 14
		self.assertTrue (re.match(func("%lf", 88.7653193745, 88.920716654), "88.92")) # ISSUE 14
		self.assertTrue (re.match(func("%lf", 88.7653193745, 88.920716654), "88.920")) # ISSUE 14
		self.assertTrue (re.match(func("%lf", 88.7653193745, 88.920716654), "88.9207")) # ISSUE 14
		self.assertTrue (re.match(func("%lf", 88.7653193745, 88.920716654), "88.92071")) # ISSUE 14
		self.assertTrue (re.match(func("%lf", 88.7653193745, 88.920716654), "88.920716")) # ISSUE 14
		self.assertTrue (re.match(func("%lf", 88.7653193745, 88.920716654), "88.9207166")) # ISSUE 14
		self.assertTrue (re.match(func("%lf", 88.7653193745, 88.920716654), "88.92071665")) # ISSUE 14
		self.assertTrue (re.match(func("%lf", 88.7653193745, 88.920716654), "88.920716654"))
		self.assertTrue (re.match(func("%lf", 88.7653193745, 88.920716654), "88.9207166540"))
		self.assertTrue (re.match(func("%lf", 88.7653193745, 88.920716654), "88.92071665400"))

		self.assertFalse(re.match(regexpgen.real("%0lf", 0.0, 10.11), "010.11"))

	def testPhase2Stage1(self):
		# 27 March 2013: real %0.Ylf and %.Ylf
		func = regexpgen.real

		self.assertRaises(ValueError, func, "%.1lf", 'a', 'a')
		self.assertRaises(ValueError, func, "%2.2lf", 'b', 'b')
		self.assertRaises(ValueError, func, "%.1lf", 10, 10)
		self.assertRaises(ValueError, func, "%0.2lf", 'b', 'b')
		self.assertRaises(ValueError, func, "%0.2lf", 13, -13)

		self.assertTrue (re.match(func("%0.2lf", -12.7, 23.5), "-9.99"))
		self.assertFalse(re.match(func("%0.2lf", -12.7, 23.5), "-9.99999"))
		self.assertTrue (re.match(func("%0.2lf", -12.7, 23.5), "23.10"))
		self.assertTrue (re.match(func("%0.1lf", -100.0, 100.0), "-100.0"))
		self.assertTrue (re.match(func("%0.1lf", -100.0, 100.0), "100.0"))
		self.assertFalse(re.match(func("%0.1lf", -100.0, 100.0), "-100.00"))
		self.assertFalse(re.match(func("%0.1lf", -100.0, 100.0), "100.00"))
		self.assertTrue (re.match(func("%0.2lf", 0.0, 10.11), "10.11"))
		self.assertFalse(re.match(func("%0.2lf", 0.0, 10.11), "10.111"))
		self.assertFalse(re.match(func("%0.2lf", 0.0, 10.11), "0010.10"))

		self.assertTrue (re.match(func("%.2lf"), "0.11"))
		self.assertTrue (re.match(func("%.2lf"), "11111.11"))
		self.assertTrue (re.match(func("%.2lf"), "-123.11"))
		self.assertTrue (re.match(func("%.2lf", 0.0, 10.11), "0.11"))
		self.assertTrue (re.match(func("%.2lf", 0.0, 10.11), "10.11"))
		self.assertFalse(re.match(func("%.2lf", 0.0, 10.11), "10.111"))
		self.assertFalse(re.match(func("%.2lf", 0.0, 10.11), "10.12"))
		self.assertFalse(re.match(func("%.2lf", 0.0, 10.11), "0.111"))
		self.assertFalse(re.match(func("%.2lf", 0.0, 10.11), "111.11"))
		self.assertFalse(re.match(func("%.2lf", 0.0, 10.11), "-0.111"))

		self.assertTrue (re.match(regexpgen.concatenate([
				('int', "%d", 100, 105),
				('\.',),
				('int', "%d", 250, 255),
				('\.',),
				('int', "%d", 122, 122),
				('\.',),
				('int', "%d", 0, 240)
		]), "100.250.122.10"))

	def testPhase2Stage2(self):
		# move validation to RegexBuilder
		from regexpgen.builder import RegexpBuilder
		r = RegexpBuilder()
		self.assertRaises(ValueError, r.createIntegerRegex, "%d", 'a', 'a')

		self.assertRaises(ValueError, regexpgen.nnint, 1111) # ISSUE 12
		self.assertRaises(ValueError, regexpgen.integer, 1111) # ISSUE 12
		self.assertRaises(ValueError, regexpgen.real, 1111) # ISSUE 12
		self.assertFalse(re.match(regexpgen.real("%lf"), "000-22.0")) # ISSUE 13

		# 03 April 2013: real %X.Ylf

		func = regexpgen.real

		self.assertRaises(ValueError, func, "%2.2lf", 13, -13)
		self.assertRaises(ValueError, func, "%2.2lf", None, -13)
		self.assertRaises(ValueError, func, "%2.2lf", 13, None)
		self.assertTrue (re.match(func("%2.2lf", 0.0, 10.11), "10.11"))
		self.assertTrue (re.match(func("%2.2lf", 0.0, 10.11), "00010.11"))
		self.assertFalse(re.match(func("%0lf", 0.0, 10.11), "00010.11"))
		self.assertTrue (re.match(func("%0lf", 0.0, 10.11), "10.110"))
		self.assertFalse(re.match(func("%0lf", 0.0, 10.11), "10.110001"))

	def testPhase2Stage3(self):
		# 10 April 2013: real %0X.Ylf

		func = regexpgen.real

		self.assertTrue  (re.match(func("%06.3lf", 5.456, 98.123), "05.456"))
		self.assertFalse (re.match(func("%06.3lf", 5.456, 98.123), "5.456"))
		self.assertTrue  (re.match(func("%05.2lf", 0.0, 10.11), "10.00"))
		self.assertTrue  (re.match(func("%05.2lf", 0.0, 10.11), "10.11"))
		self.assertRaises(ValueError, func, "%02.2lf", 0.0, 10.11)
		self.assertTrue  (re.match(func("%010.2lf", 0.0, 100.11), "0000010.00"))
		self.assertRaises(ValueError, func, "%00.2lf")
		self.assertTrue  (re.match(func("%010.2lf"), "0000010.00"))
		self.assertFalse (re.match(func("%010.2lf"), "11.6"))
		self.assertFalse (re.match(func("%012.10lf"), "1.6"))
		self.assertTrue  (re.match(func("%016.10lf"), "00001.0123456789"))
		self.assertTrue  (re.match(func("%016.10lf"), "15600001.0123456789"))
		self.assertFalse (re.match(func("%016.10lf"), "15600001.0123456"))
		self.assertTrue  (re.match(func("%016.10lf", 10.0, 20.0), "00015.0123456789"))
		self.assertFalse (re.match(func("%016.10lf", 10.0, 20.0), "000015.0123456789"))

	def testPhase3Stage1(self):
		# 18 April 2013: time

		func = regexpgen.time

		self.assertRaises(ValueError, func, None)
		self.assertRaises(ValueError, func, None, None)
		self.assertRaises(ValueError, func, None, None, None)

		self.assertFalse (re.match(func("%H:%M"), "24:23"))

		self.assertRaises(ValueError, func, "%H:%M", "12:24", "24:59")
		self.assertRaises(ValueError, func, "%H:%M", "-00:24", "12:59")
		self.assertRaises(ValueError, func, "%H:%M", "adsfa", "14:59")
		self.assertRaises(ValueError, func, "%I:%M", "1:12", "11:59")

		self.assertRaises(ValueError, func, "%I?%M?%p", "12:24am", "5:59 pm")

		self.assertFalse (re.match(func("%I %M %p", "01 24 pm", "05 59 pm"), "01 23 pm"))
		self.assertTrue  (re.match(func("%I %M %p", "01 24 pm", "05 59 pm"), "01 24 pm"))
		self.assertTrue  (re.match(func("%I %M %p", "01 24 pm", "05 59 pm"), "02 19 pm"))
		self.assertFalse (re.match(func("%I %M %p", "01 24 pm", "05 59 pm"), "02 99 pm"))
		self.assertTrue  (re.match(func("%I %M %p", "01 24 pm", "05 59 pm"), "05 59 pm"))
		self.assertFalse (re.match(func("%I %M %p", "01 24 pm", "05 59 pm"), "06 00 pm"))
		self.assertFalse (re.match(func("%I %M %p", "01 24 pm", "05 59 pm"), "01 50 am"))

		self.assertFalse (re.match(func("%H:%M", "12:24", "17:59"), "12:23"))
		self.assertTrue  (re.match(func("%H:%M", "12:24", "17:59"), "12:24"))
		self.assertTrue  (re.match(func("%H:%M", "12:24", "17:59"), "17:59"))
		self.assertTrue  (re.match(func("%H:%M", "12:24", "17:59"), "12:24"))
		self.assertFalse (re.match(func("%H:%M", "12:24", "17:59"), "18:00"))

		self.assertTrue  (re.match(func("%H:%M", maxV="17:59"), "00:00"))
		self.assertTrue  (re.match(func("%H:%M", maxV="17:59"), "12:00"))

		self.assertFalse (re.match(func("%H[%M]%S", "12[24]12", "17[59]25"), "12[24]11"))
		self.assertTrue  (re.match(func("%H[%M]%S", "12[24]12", "17[59]25"), "12[24]12"))
		self.assertTrue  (re.match(func("%H[%M]%S", "12[24]12", "17[59]25"), "17[59]25"))
		self.assertTrue  (re.match(func("%H[%M]%S", "12[24]12", "17[59]25"), "12[24]12"))
		self.assertFalse (re.match(func("%H[%M]%S", "12[24]12", "17[59]25"), "17[59]26"))

		h = func("%H")
		for i in xrange(0, 24):
			self.assertTrue  (re.match(h, "%02d" % i))

		self.assertFalse (re.match(h, ""))
		self.assertFalse (re.match(h, "25"))

		m = func("%M")
		for i in xrange(0, 60):
			self.assertTrue  (re.match(m, "%02d" % i))

		s = func("%S")
		for i in xrange(0, 60):
			self.assertTrue  (re.match(s, "%02d" % i))

		self.assertFalse (re.match(h, "a"))
		self.assertFalse (re.match(m, "b"))
		self.assertFalse (re.match(s, "c"))
		self.assertFalse (re.match(h, "-1"))
		self.assertFalse (re.match(m, "-2"))
		self.assertFalse (re.match(s, "3-"))

		hm = func("%H{}%M")

		for i in itertools.product(range(0, 24), range(0, 60)):
			self.assertTrue  (re.match(hm, "%02d{}%02d" % i))

		self.assertFalse (re.match(hm, "24{}60"))

		hm = func("%H{}%Mpp%S")

		for i in itertools.product(range(0, 24), range(0, 60), range(0, 60)):
			self.assertTrue  (re.match(hm, "%02d{}%02dpp%02d" % i))

		self.assertFalse (re.match(hm, "24{}60456789"))

#	def testPhase3Stage2(self):
#		def gen_date(from_Y = 1970, from_m = 1, from_d = 1):
#			Y = from_Y
#
#			for m in xrange(from_m, 13):
#				if m == 2:
#					if (Y % 4 == 0 and Y % 100 != 0) or (Y % 400 == 0):
#						if Y == from_Y and m == from_m:
#							for d in xrange(from_d, 30):
#								yield (Y, m, d)
#						else:
#							for d in xrange(1, 30):
#								yield (Y, m, d)
#					else:
#						if Y == from_Y and m == from_m:
#							for d in xrange(from_d, 29):
#								yield (Y, m, d)
#						else:
#							for d in xrange(1, 29):
#								yield (Y, m, d)
#				elif m in [1, 3, 5, 7, 8, 10, 12]:
#					if Y == from_Y and m == from_m:
#						for d in xrange(from_d, 32):
#							yield (Y, m, d)
#					else:
#						for d in xrange(1, 32):
#							yield (Y, m, d)
#				else:
#					if Y == from_Y and m == from_m:
#						for d in xrange(from_d, 31):
#							yield (Y, m, d)
#					else:
#						for d in xrange(1, 31):
#							yield (Y, m, d)
#
#			for Y, m in itertools.product(xrange(from_Y + 1, 2100), xrange(1, 13)):
#				if m == 2:
#					if (Y % 4 == 0 and Y % 100 != 0) or (Y % 400 == 0):
#						for d in xrange(1, 30):
#							yield (Y, m, d)
#					else:
#						for d in xrange(1, 29):
#							yield (Y, m, d)
#				elif m in [1, 3, 5, 7, 8, 10, 12]:
#					for d in xrange(1, 32):
#						yield (Y, m, d)
#				else:
#					for d in xrange(1, 31):
#						yield (Y, m, d)
#
#		# 24 April 2013: date
#
#		func = regexpgen.date
#
#		self.assertRaises(ValueError, func, None)
#		self.assertRaises(ValueError, func, None, None)
#		self.assertRaises(ValueError, func, None, None, None)
#
#		y = func("%Y")
#		for i in xrange(1970, 2100):
#			self.assertTrue  (re.match(y, "%d" % i))
#
#		for i in [1, 12, 999, 1410, 1969, 2100, 2101]:
#			self.assertFalse (re.match(y, "%d" % i))
#
#		for i in ['', 'a']:
#			self.assertFalse (re.match(y, "%s" % i))
#
#		d = func("%d")
#		for i in xrange(1, 32):
#			self.assertTrue  (re.match(d, "%02d" % i))
#
#		for i in [-1, 0, 32, 100]:
#			self.assertFalse (re.match(d, "%02d" % i))
#
#		for i in ['', 'a']:
#			self.assertFalse (re.match(d, "%s" % i))
#
#		m = func("%m")
#		for i in xrange(1, 13):
#			self.assertTrue  (re.match(m, "%02d" % i))
#
#		for i in [-1, 0, 13, 14, 100]:
#			self.assertFalse (re.match(m, "%02d" % i))
#
#		for i in ['', 'm']:
#			self.assertFalse (re.match(m, "%s" % i))
#
#		self.assertFalse(re.match(func("%Y-%m-%d"), "%04d-%02d-%s" % (2010, 1, '--')))
#		self.assertFalse(re.match(func("%y-%m-%d"), "%02d-%02d-%s" % (10, 1, '-')))
#
#		###########
#
#		conf = [
#				(func("%Y-%m-%d"), func("%y-%m-%d"), "%04d-%02d-%02d", "%02d-%02d-%02d"),
#				(func("%Y+%m+%d"), func("%y+%m+%d"), "%04d+%02d+%02d", "%02d+%02d+%02d"),
#				(func("%Y %m %d"), func("%y %m %d"), "%04d %02d %02d", "%02d %02d %02d"),
#				(func("%Y la %m ka %d"), func("%y la %m ka %d"), "%04d la %02d ka %02d", "%02d la %02d ka %02d"),
#		]
#
#		for regexp_Ymd, regexp_ymd, fmt_Ymd, fmt_ymd in conf:
#			for Y, m in itertools.product(xrange(1970, 2100), xrange(1, 13)):
#				#print "(%4d, %02d, %02d)" % (Y, m, 0), y
#
#				y = Y - 2000 if Y >= 2000 else None
#
#				self.assertFalse(re.match(regexp_ymd, fmt_Ymd % (Y, m, 0))) # ISSUE #21
#
#				if m == 2:
#					if (Y % 4 == 0 and Y % 100 != 0) or (Y % 400 == 0):
#						for d in xrange(1, 30):
#							#print "(%4d, %02d, %02d)" % (Y, m, d), y
#							self.assertTrue(re.match(regexp_Ymd, fmt_Ymd % (Y, m, d)))
#
#							if y: self.assertTrue(re.match(regexp_ymd, fmt_ymd % (y, m, d))) # ISSUE 22
#
#						self.assertFalse(re.match(regexp_Ymd, fmt_Ymd % (Y, m, 31)))
#						if y: self.assertFalse(re.match(regexp_ymd, fmt_ymd % (y, m, 31))) # ISSUE 22
#					else:
#						for d in xrange(1, 29):
#							#print "(%4d, %02d, %02d)" % (Y, m, d), y
#							self.assertTrue(re.match(regexp_Ymd, fmt_Ymd % (Y, m, d)))
#							if y: self.assertTrue(re.match(regexp_ymd, fmt_ymd % (y, m, d))) # ISSUE 22
#
#						self.assertFalse(re.match(regexp_Ymd, fmt_Ymd % (Y, m, 29)))
#						self.assertFalse(re.match(regexp_Ymd, fmt_Ymd % (Y, m, 30)))
#						if y: self.assertFalse(re.match(regexp_ymd, fmt_ymd % (y, m, 29)))
#						if y: self.assertFalse(re.match(regexp_ymd, fmt_ymd % (y, m, 30)))
#				elif m in [1, 3, 5, 7, 8, 10, 12]:
#					for d in xrange(1, 32):
#						# (1971, 01, 31), (1971, 03, 31), (1971, 05, 31),
#						# (1971, 07, 31), (1971, 8, 31), (1971, 10, 31),
#						# (1971, 12, 31) - ISSUE #19
#						#print "(%4d, %02d, %02d)" % (Y, m, d), y
#						self.assertTrue(re.match(regexp_Ymd, fmt_Ymd % (Y, m, d)))
#
#						if y: self.assertTrue(re.match(regexp_ymd, fmt_ymd % (y, m, d)))  # ISSUE 22
#				else:
#					for d in xrange(1, 31):
#						#print "(%4d, %02d, %02d)" % (Y, m, d), y
#						self.assertTrue(re.match(regexp_Ymd, fmt_Ymd % (Y, m, d)))
#						if y: self.assertTrue(re.match(regexp_ymd, fmt_ymd % (y, m, d))) # ISSUE 22
#
#					self.assertFalse(re.match(regexp_Ymd, fmt_Ymd % (Y, m, 31)))
#					if y: self.assertFalse(re.match(regexp_ymd, fmt_ymd % (y, m, 31)))
#
#				self.assertFalse(re.match(regexp_Ymd, fmt_Ymd % (Y, m, 32)))
#				if y: self.assertFalse(re.match(regexp_ymd, fmt_ymd % (y, m, 32)))
#
#			self.assertFalse(re.match(regexp_Ymd, fmt_Ymd % (2100, 1, 31)))
#			self.assertFalse(re.match(regexp_ymd, fmt_ymd % (100, 1, 31)))
#
#		##########
#
#		conf = [
#				(func("%m-%Y-%d"), func("%m-%y-%d"), "%02d-%04d-%02d", "%02d-%02d-%02d"),
#				(func("%m+%Y+%d"), func("%m+%y+%d"), "%02d+%04d+%02d", "%02d+%02d+%02d"),
#				(func("%m %Y %d"), func("%m %y %d"), "%02d %04d %02d", "%02d %02d %02d"),
#				(func("%m la %Y ka %d"), func("%m la %y ka %d"), "%02d la %04d ka %02d", "%02d la %02d ka %02d"),
#		]
#
#		for regexp_Ymd, regexp_ymd, fmt_Ymd, fmt_ymd in conf:
#			for Y, m in itertools.product(xrange(1970, 2100), xrange(1, 13)):
#				#print "(%4d, %02d, %02d)" % (Y, m, 0), y
#
#				y = Y - 2000 if Y >= 2000 else None
#
#				self.assertFalse(re.match(regexp_ymd, fmt_Ymd % (m, Y, 0))) # ISSUE #21
#
#				if m == 2:
#					if (Y % 4 == 0 and Y % 100 != 0) or (Y % 400 == 0):
#						for d in xrange(1, 30):
#							#print "(%4d, %02d, %02d)" % (Y, m, d), y
#							self.assertTrue(re.match(regexp_Ymd, fmt_Ymd % (m, Y, d)))
#
#							if y: self.assertTrue(re.match(regexp_ymd, fmt_ymd % (m, y, d))) # ISSUE 22
#
#						self.assertFalse(re.match(regexp_Ymd, fmt_Ymd % (m, Y, 31)))
#						if y: self.assertFalse(re.match(regexp_ymd, fmt_ymd % (m, y, 31))) # ISSUE 22
#					else:
#						for d in xrange(1, 29):
#							#print "(%4d, %02d, %02d)" % (Y, m, d), y
#							self.assertTrue(re.match(regexp_Ymd, fmt_Ymd % (m, Y, d)))
#							if y: self.assertTrue(re.match(regexp_ymd, fmt_ymd % (m, y, d))) # ISSUE 22
#
#						self.assertFalse(re.match(regexp_Ymd, fmt_Ymd % (m, Y, 29)))
#						self.assertFalse(re.match(regexp_Ymd, fmt_Ymd % (m, Y, 30)))
#						if y: self.assertFalse(re.match(regexp_ymd, fmt_ymd % (m, y, 29)))
#						if y: self.assertFalse(re.match(regexp_ymd, fmt_ymd % (m, y, 30)))
#				elif m in [1, 3, 5, 7, 8, 10, 12]:
#					for d in xrange(1, 32):
#						# (1971, 01, 31), (1971, 03, 31), (1971, 05, 31),
#						# (1971, 07, 31), (1971, 8, 31), (1971, 10, 31),
#						# (1971, 12, 31) - ISSUE #19
#						#print "(%4d, %02d, %02d)" % (Y, m, d), y
#						self.assertTrue(re.match(regexp_Ymd, fmt_Ymd % (m, Y, d)))
#
#						if y: self.assertTrue(re.match(regexp_ymd, fmt_ymd % (m, y, d)))  # ISSUE 22
#				else:
#					for d in xrange(1, 31):
#						#print "(%4d, %02d, %02d)" % (Y, m, d), y
#						self.assertTrue(re.match(regexp_Ymd, fmt_Ymd % (m, Y, d)))
#						if y: self.assertTrue(re.match(regexp_ymd, fmt_ymd % (m, y, d))) # ISSUE 22
#
#					self.assertFalse(re.match(regexp_Ymd, fmt_Ymd % (m, Y, 31)))
#					if y: self.assertFalse(re.match(regexp_ymd, fmt_ymd % (m, y, 31)))
#
#				self.assertFalse(re.match(regexp_Ymd, fmt_Ymd % (m, Y, 32)))
#				if y: self.assertFalse(re.match(regexp_ymd, fmt_ymd % (m, y, 32)))
#
#			self.assertFalse(re.match(regexp_Ymd, fmt_Ymd % (1, 2100, 31)))
#			self.assertFalse(re.match(regexp_ymd, fmt_ymd % (1, 100, 31)))
#
#		##############
#
#		regexp_Ym = func("%Y-%m")
#		fmt_Ym = "%04d-%02d"
#
#		self.assertFalse(re.match(regexp_Ym, fmt_Ym % (1969, 1)))
#		self.assertFalse(re.match(regexp_Ym, fmt_Ym % (1970, 0)))
#		self.assertFalse(re.match(regexp_Ym, fmt_Ym % (1970, 13)))
#
#		for Y, m in itertools.product(xrange(1970, 2100), xrange(1, 13)):
#			self.assertTrue(re.match(regexp_Ym, fmt_Ym % (Y, m)))
#
#		self.assertFalse(re.match(regexp_Ym, fmt_Ym % (2100, 1)))
#		self.assertFalse(re.match(regexp_Ym, fmt_Ym % (2100, 0)))
#		self.assertFalse(re.match(regexp_Ym, fmt_Ym % (2100, 13)))
#
#		# range
#
#		for i in xrange(1970, 2100):
#			for j in xrange(i, 2100):
#				regexp = func("%Y", str(i), str(j))
#
#				self.assertFalse(re.match(regexp, "0"))
#
#				for k in xrange(i, j):
#					self.assertTrue(re.match(regexp, str(k)))
#
#				self.assertFalse(re.match(regexp, str(j + 1)))
#
#		for i in xrange(1, 13):
#			for j in xrange(i, 13):
#				regexp = func("%m", "%02d" % i, "%02d" % j)
#
#				self.assertFalse(re.match(regexp, "00"))
#
#				for k in xrange(i, j):
#					self.assertTrue(re.match(regexp, "%02d" % k))
#
#				self.assertFalse(re.match(regexp, "%02d" % (j + 1)))
#
#		for i in xrange(1, 32):
#			for j in xrange(i, 32):
#				regexp = func("%d", "%02d" % i, "%02d" % j)
#
#				self.assertFalse(re.match(regexp, "00"))
#
#				for k in xrange(i, j):
#					self.assertTrue(re.match(regexp, "%02d" % k))
#
#				self.assertFalse(re.match(regexp, "%02d" % (j + 1)))

	def testPhase3Stage3(self):
		# 8 May 2013: auto-detection, concatenate

		# concatenate

		self.assertTrue (re.match(regexpgen.concatenate([
				('int', "%d", 100, 105),
				('\.',),
				('int', "%d", 250, 255),
				('\.',),
				('int', "%d", 122, 122),
				('\.',),
				('int', "%d", 0, 240)
		]), "100.250.122.10"))

		self.assertFalse(re.match(regexpgen.concatenate([
				('int', "%d", 100, 105),
				('\.',),
				('int', "%d", 250, 255),
				('\.',),
				('int', "%d", 122, 122),
				('\.',),
				('int', "%d", 0, 240)
		]), "99.250.122.10"))

		self.assertTrue(re.match(regexpgen.concatenate([
				('int', "%04d", 99, 105),
				('\.',),
				('int', "%d", 250, 255),
				('\.',),
				('int', "%d", 122, 122),
				('\.',),
				('int', "%d", 0, 240)
		]), "0099.250.122.10"))

		self.assertFalse(re.match(regexpgen.concatenate([
				('int', "%04d", 99, 105),
				('\.',),
				('int', "%d", 250, 255),
				('\.',),
				('int', "%d", 122, 122),
				('\.',),
				('int', "%d", 0, 240)
		]), "99.250.122.10"))

		# auto
		self.assertTrue  (re.match(regexpgen.auto("%d", 1, None), "1"))
		self.assertTrue  (re.match(regexpgen.auto("%03d", 0, 100), "099"))
		self.assertFalse (re.match(regexpgen.auto("%lf", -0.01, 1.5), "1.51"))
		self.assertFalse (re.match(regexpgen.auto("%0.1lf", -100.0, 100.0), "-100.00"))
		self.assertTrue  (re.match(regexpgen.auto("%016.10lf"), "15600001.0123456789"))
		self.assertFalse (re.match(regexpgen.auto("%H:%M"), "24:23"))
		self.assertRaises(ValueError, regexpgen.auto, "%I?%M?%p", "12:24am", "5:59 pm")

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
