'''
Created on Mar 16, 2012

@author: Bartosz Alchimowicz
'''

import unittest
import regexpgen
import re
import itertools

class Test(unittest.TestCase):

#
#	def testDefaultColon(self):
#		regexp = regexpgen.time(r"%H:%M")
#		print regexp
#
#		for i in ["%2d:%2d" % (H, M) for H in xrange(0, 24) for M in xrange(0, 60) ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in ["%02d:%02d" % (H, M) for H in xrange(0, 24) for M in xrange(0, 60) ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#	def testDefaultDot(self):
#		regexp = regexpgen.time(r"%H.%M")
#		print regexp
#
#		for i in ["%2d.%2d" % (H, M) for H in xrange(0, 24) for M in xrange(0, 60) ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in ["%02d.%02d" % (H, M) for H in xrange(0, 24) for M in xrange(0, 60) ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
# %H    godzina (00..23)
# %I    godzina (00..12)
# %M    minuty (00..59)
# %p    AM lub PM ?
# %P    am lub pm ?
# %S    sekundy (00..59)

	def testDefault(self):
		regexp = regexpgen.time("%H")

		self.assertTrue(re.match(regexp, "01"))
		self.assertTrue(re.match(regexp, "10"))
		self.assertTrue(re.match(regexp, "00"))
		self.assertTrue(re.match(regexp, "23"))
		self.assertTrue(re.match(regexp, "17"))

		self.assertFalse(re.match(regexp, "1"))
		self.assertFalse(re.match(regexp, "33"))
		self.assertFalse(re.match(regexp, "24"))
		self.assertFalse(re.match(regexp, "99"))
		self.assertFalse(re.match(regexp, "-17"))
		
		for format in ["%M", "%S"]:
			regexp = regexpgen.time(format)
			self.assertTrue(re.match(regexp, "01"))
			self.assertTrue(re.match(regexp, "46"))
			self.assertTrue(re.match(regexp, "00"))
			self.assertTrue(re.match(regexp, "23"))
			self.assertTrue(re.match(regexp, "59"))
	
			self.assertFalse(re.match(regexp, "1"))
			self.assertFalse(re.match(regexp, "333"))
			self.assertFalse(re.match(regexp, "99"))
			self.assertFalse(re.match(regexp, "-17"))

		regexp = regexpgen.time("%H:%M")

		self.assertTrue(re.match(regexp, "01:00"))
		self.assertTrue(re.match(regexp, "00:00"))
		self.assertTrue(re.match(regexp, "00:05"))
		self.assertTrue(re.match(regexp, "23:59"))
		self.assertTrue(re.match(regexp, "17:34"))

		self.assertFalse(re.match(regexp, "1:12"))
		self.assertFalse(re.match(regexp, "33:12"))
		self.assertFalse(re.match(regexp, "23:67"))
		self.assertFalse(re.match(regexp, "99:00"))
		self.assertFalse(re.match(regexp, "-17:11"))

		regexp = regexpgen.time("%I:%M %p")

		self.assertTrue(re.match(regexp, "01:00 am"))
		self.assertTrue(re.match(regexp, "01:00 pm"))
		self.assertTrue(re.match(regexp, "09:45 pm"))
		self.assertTrue(re.match(regexp, "11:59 pm"))
		self.assertTrue(re.match(regexp, "00:00 am"))

		self.assertFalse(re.match(regexp, "1:00 am"))
		self.assertFalse(re.match(regexp, "01:0 am"))
		self.assertFalse(re.match(regexp, "12:00 am"))

		regexp = regexpgen.time("%I:%M:%S %p")

		self.assertTrue(re.match(regexp, "01:00:00 am"))
		self.assertTrue(re.match(regexp, "01:00:20 pm"))
		self.assertTrue(re.match(regexp, "09:45:59 pm"))
		self.assertTrue(re.match(regexp, "11:59:59 pm"))
		self.assertTrue(re.match(regexp, "00:00:00 am"))

		self.assertFalse(re.match(regexp, "1:00:00 am"))
		self.assertFalse(re.match(regexp, "01:0:00 am"))
		self.assertFalse(re.match(regexp, "12:00:00 am"))

	def testForWrongFormat(self):		
		self.assertRaises(ValueError, regexpgen.time, "%wwI:%M %P")
		self.assertRaises(ValueError,regexpgen.time, "%I:%I")
		self.assertRaises(ValueError,regexpgen.time, "%I:%M")
		self.assertRaises(ValueError,regexpgen.time, "%I:%H")
		self.assertRaises(ValueError,regexpgen.time, "%H:%S")
		self.assertRaises(ValueError,regexpgen.time, "%P")
		
	def testForWrongInput(self):	
		self.assertRaises(ValueError,regexpgen.time, "%H:%M", "01:00", "00:00")
		self.assertRaises(ValueError,regexpgen.time, "%I:%M %P", "01:00 am", "00:00 am")
		self.assertRaises(ValueError,regexpgen.time, "%H:%M", "01:00 pm", "00:00 am")
		self.assertRaises(ValueError,regexpgen.time, "%H:", "01", "00")
		self.assertRaises(ValueError,regexpgen.time, "%H:%M", "01:02", "01:00")
		self.assertRaises(ValueError,regexpgen.time, "%H:%M:%S", "01:00:02", "01:00:00")
		
	def testForMin(self):
		regexp = regexpgen.time("%H", "10", None)

		self.assertTrue(re.match(regexp, "10"))
		self.assertTrue(re.match(regexp, "17"))
		self.assertTrue(re.match(regexp, "23"))
		
		self.assertFalse(re.match(regexp, "00"))
		self.assertFalse(re.match(regexp, "01"))
		self.assertFalse(re.match(regexp, "08"))
		
		regexp = regexpgen.time("%S", "40", None)

		self.assertTrue(re.match(regexp, "56"))
		self.assertTrue(re.match(regexp, "40"))
		self.assertTrue(re.match(regexp, "59"))
		
		self.assertFalse(re.match(regexp, "39"))
		self.assertFalse(re.match(regexp, "01"))
		self.assertFalse(re.match(regexp, "08"))
		
		regexp = regexpgen.time("%H:%M", "12:13", None)
		
		self.assertTrue(re.match(regexp, "12:56"))
		self.assertTrue(re.match(regexp, "13:40"))
		self.assertTrue(re.match(regexp, "23:59"))
		
		self.assertFalse(re.match(regexp, "00:39"))
		self.assertFalse(re.match(regexp, "12:01"))
		self.assertFalse(re.match(regexp, "12:12"))
		
		regexp = regexpgen.time("%I:%M %P", "12:13 PM", None)
		
		self.assertTrue(re.match(regexp, "12:56 PM"))
		self.assertTrue(re.match(regexp, "01:40 PM"))
		self.assertTrue(re.match(regexp, "10:59 PM"))
		
		self.assertFalse(re.match(regexp, "00:39 AM"))
		self.assertFalse(re.match(regexp, "12:01 PM"))
		self.assertFalse(re.match(regexp, "12:12 PM"))


	def testForMax(self):
		regexp = regexpgen.time("%H", None, "10")

		self.assertFalse(re.match(regexp, "11"))
		self.assertFalse(re.match(regexp, "17"))
		self.assertFalse(re.match(regexp, "23"))
		
		self.assertTrue(re.match(regexp, "00"))
		self.assertTrue(re.match(regexp, "01"))
		self.assertTrue(re.match(regexp, "08"))
		
		regexp = regexpgen.time("%S", None, "40")

		self.assertFalse(re.match(regexp, "56"))
		self.assertFalse(re.match(regexp, "41"))
		self.assertFalse(re.match(regexp, "59"))
		
		self.assertTrue(re.match(regexp, "39"))
		self.assertTrue(re.match(regexp, "01"))
		self.assertTrue(re.match(regexp, "08"))
		
		regexp = regexpgen.time("%H:%M", None, "12:13")
		
		self.assertFalse(re.match(regexp, "12:56"))
		self.assertFalse(re.match(regexp, "13:40"))
		self.assertFalse(re.match(regexp, "23:59"))
		
		self.assertTrue(re.match(regexp, "00:39"))
		self.assertTrue(re.match(regexp, "12:01"))
		self.assertTrue(re.match(regexp, "12:12"))
		
		regexp = regexpgen.time("%I:%M %P", None, "12:13 PM")
		
		#self.assertFalse(re.match(regexp, "12:56 PM"))
		self.assertFalse(re.match(regexp, "01:40 PM"))
		self.assertFalse(re.match(regexp, "10:59 PM"))
		
		self.assertTrue(re.match(regexp, "00:39 AM"))
		self.assertTrue(re.match(regexp, "12:01 PM"))
		self.assertTrue(re.match(regexp, "12:12 PM"))
												




#		for sep in [".", "-", ":", " "]:
#			for parts in [	["%H", "%M", "%S"], ["%H", "%M"], ["%M", "%S"],
#							["%I", "%M", "%S"], ["%I", "%M"]
#							["%I", "%M", "%S", "%p"], ["%I", "%M", "%S", "%P"],
#							["%I", "%M", "%p"], ["%I", "%M", "%P"],
#							["%I", "%p"], ["%I", "%P"],
#							["%H"], ["%I"], ["%M"], ["%S"]]:
#
#				frmt = sep.join(parts)
#				hMin, hMax = None, None
#				mMin, mMax = 0, 59
#				sMin, sMax = 0, 59
#
#				if "%H" in parts:
#					hMin, hMax = 0, 23
#				if "%I" in parts:
#					hMin, hMax = 0, 11

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
