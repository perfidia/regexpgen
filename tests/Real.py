'''
Created on Mar 16, 2012

@author: Bartosz Alchimowicz
'''

import unittest
import regexpgen
import re
import random
import math

class Test(unittest.TestCase):
#	def testStartEnd(self):
#		pattern = r"%lf"
#
#		self.assertEqual(regexpgen.real(pattern),
#						 regexpgen.real(pattern, matchStartEnd = True))
#
#		self.assertEqual(regexpgen.real(pattern, matchStartEnd = True)[0], '^')
#		self.assertEqual(regexpgen.real(pattern, matchStartEnd = True)[-1], '$')
#
#		self.assertNotEqual(regexpgen.real(pattern, matchStartEnd = False)[0], '^')
#		self.assertNotEqual(regexpgen.real(pattern, matchStartEnd = False)[-1], '$')
#
#	def testDefault(self):
#		regexp = regexpgen.real(r"%lf")
#		print regexp
#
#		for i in [ i/100 for i in xrange(-65000, 65000) ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ i for i in xrange(-65000, 0 + 1) ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#		for i in [ 'a' ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)


	def frange(self, x, y, jump):
  		while x < y:
  			yield x
      		x += jump

	def testDefault(self):
		random.seed(3);
		for i in xrange(0, 1100):
			scale = len(str(i))
			self._runTest1(scale, False, False);
			self._runTest1(scale, False, True);
			self._runTest1(scale, True, False);
			self._runTest1(scale, True, True);
			self._runTest2(scale, False, False);
			self._runTest2(scale, False, True);
			self._runTest2(scale, True, False);
			self._runTest2(scale, True, True);
			print i

	def _runTest1(self, scale, setMin, setMax):
		min = random.uniform(-1*(10**scale), 10**scale)
		max = random.uniform(min, min + 5**scale) #zeby testowalo tez np -100 do -10

		format = "%lf"
		#print None, max
		regexp = regexpgen.real(format, min if setMin else None, max if setMax else None)
		info = lambda value: self._getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

		if min < 0 and max < 0:
			rangeLeft = min*2
			rangeRight = -min*2
		if min < 0 and max > 0:
			rangeLeft = min*2
			rangeRight = max*2
		if min > 0 and max > 0:
			rangeLeft = -max*2
			rangeRight = max*2
		if min == 0 and max != 0:
			rangeLeft = -max*2
			rangeRight = max*2
		if max == 0 and min != 0:
			rangeLeft = min*2
			rangeRight = -min*2
		if max == 0 and min == 0:
			rangeLeft = -100
			rangeRight = 100

 		rest = min - int(min)
 		rest = math.fabs(rest)
 		i = rangeLeft
 		if (setMin):
 		 	while i < min:
			 	self.assertFalse(re.match(regexp, str(i)), info(str(i)))
			 	i = i + 1.05
		while i <= max:
			if i >= 0:
				a = "0" + str(i); b = "00" + str(i); c = "000" + str(i); d = "0000" + str(i);
			else:
				a = "-0" + str(-i); b = "-00" + str(-i); c = "-000" + str(-i); d = "-0000" + str(-i);
			self.assertTrue(re.match(regexp, str(i)), info(str(i)))
			self.assertTrue(re.match(regexp, a), info(a))
			self.assertTrue(re.match(regexp, b), info(b))
			self.assertTrue(re.match(regexp, c), info(c))
			self.assertTrue(re.match(regexp, d), info(d))
			i = i + 1.05
		if (setMax):
			while i <= rangeRight:
				self.assertFalse(re.search(regexp, str(i)), info(str(i)))
				i = i + 1.05

	def _runTest2(self, scale, setMin, setMax):
		min = random.uniform(-1*(10**scale), 10**scale)
		max = random.uniform(min, min + 5**scale)
		format = "%0lf"
		regexp = regexpgen.real(format, min if setMin else None, max if setMax else None)
		info = lambda value: self._getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

		if min < 0 and max < 0:
			rangeLeft = min*2
			rangeRight = -min*2
		if min < 0 and max > 0:
			rangeLeft = min*2
			rangeRight = max*2
		if min > 0 and max > 0:
			rangeLeft = -max*2
			rangeRight = max*2
		if min == 0 and max != 0:
			rangeLeft = -max*2
			rangeRight = max*2
		if max == 0 and min != 0:
			rangeLeft = min*2
			rangeRight = -min*2
		if max == 0 and min == 0:
			rangeLeft = -100
			rangeRight = 100

 		rest = min - int(min)
 		rest = math.fabs(rest)
 		i = rangeLeft
 		if (setMin):
 		 	while i < min :
			 	self.assertFalse(re.match(regexp, str(i)), info(str(i)))
			 	i = i + 1.05
		while i <= max:
			#print int(min), int(max)
			if i >= 0:
				a = "0" + str(i); b = "00" + str(i); c = "000" + str(i); d = "0000" + str(i);
			else:
				a = "-0" + str(-i); b = "-00" + str(-i); c = "-000" + str(-i); d = "-0000" + str(-i);
			self.assertTrue(re.match(regexp, str(i)), info(str(i)))
			self.assertFalse(re.match(regexp, a), info(a))
			self.assertFalse(re.match(regexp, b), info(b))
			self.assertFalse(re.match(regexp, c), info(c))
			self.assertFalse(re.match(regexp, d), info(d))
			i = i + 1.05
		if (setMax):
			while i <= rangeRight:
				self.assertFalse(re.search(regexp, str(i)), info(str(i)))
				i = i + 1.05

	def _getInfo(self, i, regexp, format, min, max):
		return "Failed! Number: {0}, min: {1}, max: {2}, format: {3}, regexp: {4}".format(i, str(min), str(max), format, regexp)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
