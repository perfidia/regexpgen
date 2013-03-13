'''
Created on Mar 15, 2012

@author: Bartosz Alchimowicz
'''

import unittest
import regexpgen
import re
import random
import math

class Test(unittest.TestCase):
#	def testStartEnd(self):
#		pattern = r"%d"
#
#		self.assertEqual(regexpgen.integer(pattern),
#						 regexpgen.integer(pattern, matchStartEnd = True))
#
#		self.assertEqual(regexpgen.integer(pattern, matchStartEnd = True)[0], '^')
#		self.assertEqual(regexpgen.integer(pattern, matchStartEnd = True)[-1], '$')
#
#		self.assertNotEqual(regexpgen.integer(pattern, matchStartEnd = False)[0], '^')
#		self.assertNotEqual(regexpgen.integer(pattern, matchStartEnd = False)[-1], '$')
#
#	def testDefault(self):
#		regexp = regexpgen.integer(r"%d")
#		print regexp
#
#		for i in [ i for i in xrange(-100, 10) ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "01", "00", "0012310" ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ 'a', 1.1, -0.8 ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#	def testNoLeadingZeros(self):
#		regexp = regexpgen.integer(r"%0d")
#		print regexp
#
#		for i in [ 0 ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "00", "01", "06" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#	def testFourDigits(self):
#		regexp = regexpgen.integer(r"%04d")
#		print regexp
#
#		for i in [ "0000", "-1000", "1000000" ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "1", "0", "a" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#	def testTwoDigits(self):
#		regexp = regexpgen.integer(r"%02d")
#		print regexp
#
#		for i in [ "00", "01", "-10", "-77", "1000000" ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "1", "0", "a" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#	def testRangePositive(self):
#		regexp = regexpgen.integer(r"%d", 0, 267)
#		print regexp
#
#		for i in [ "0", "-0" ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ i for i in xrange(0, 267 + 1) ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "-1", "268", "269" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#	def testRangeAll(self):
#		regexp = regexpgen.integer(r"%d", -351, 765)
#		print regexp
#
#		for i in [ "0", "-0" ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ i for i in xrange(-351, 765 + 1) ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "-766", "-765", "-352", "766", "1000", "1234" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#	def testRangeNoLeadingZeros(self):
#		regexp = regexpgen.integer(r"%0d", -1000, 1000)
#		print regexp
#
#		for i in [ "0", "-0" ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, i), None)
#
#		for i in [ i for i in xrange(-1000, 1000 + 1) ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "-1002", "-1001", "1001", "1002", "a", "01", "-01", "017", "-018" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#	def testRangeFourDigits(self):
#		regexp = regexpgen.integer(r"%04d", -123, 9871)
#		print regexp
#
#		for i in [ "0", "-0" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#		for i in [ i for i in xrange(-123, 999 + 1) ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "-9871", "-0125", "-0124", "9872", "9873", "45678" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#	def testRangeWithZero(self):
#		regexp = regexpgen.integer(r"%04d", -1, 9000)
#		print regexp
#
#		for i in [ "0", "-0" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#		for i in [ i for i in xrange(-1, 999 + 1) ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "0000", "-0001", "0023", "0123" ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "-0003", "-0002", "9001", "9002", "9873", "45678" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#	def testMin(self):
#		regexp = regexpgen.integer(r"%d", 0)
#		print regexp
#
#		for i in [ "0", "-0" ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ i for i in xrange(0, 65000) ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "01", "001", "00019" ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ i for i in xrange(-65000, 0) ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "-001", "-0001112" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#	def testMinWithoutZeros(self):
#		regexp = regexpgen.integer(r"%0d", -351)
#		print regexp
#
#		for i in [ "0", "-0" ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ i for i in xrange(-65000, -351 ) ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#		for i in [ i for i in xrange(-351, 65000) ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "a", "-00100", "-06578" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#	def testMinWithZeros(self):
#		regexp = regexpgen.integer(r"%04d", min = 100)
#		print regexp
#
#		for i in [ "0", "-0" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "%04d" % i for i in xrange(-65000 , 99 + 1) ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "a", "-1", "22", "01", "010", "-010", "0099" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "12345","0101" ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#	def testMax(self):
#		regexp = regexpgen.integer(r"%d", max = 100)
#		print regexp
#
#		for i in [ "0", "-0" ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, i), None)
#
#		for i in [ i for i in xrange(-65000, 100 + 1) ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ i for i in xrange(100 + 1, 65000) ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "01", "001", "00019", "-0001112" ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#	def testMaxWithoutZeros(self):
#		regexp = regexpgen.integer(r"%0d", max = 100)
#		print regexp
#
#		for i in [ "0", "-0" ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ i for i in xrange(-65000, 100 + 1) ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "-0123", "01", "001", "00019", "-0001112" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#		for i in [ i for i in xrange(100 + 1 , 65000) ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#	def testMaxWithZeros(self):
#		regexp = regexpgen.integer(r"%04d", max = 100)
#		print regexp
#
#		for i in [ "0", "-0" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "%04d" % i for i in xrange(-9000 , -1000 + 1) ]:
#			print "check", i
#			self.assertNotEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "000001", "0000010", "000019", "01", "001" ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
#		for i in [ "%04d" % i for i in xrange(100 + 1 , 65000) ]:
#			print "check", i
#			self.assertEqual(re.match(regexp, str(i)), None)
#
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
			self._runTest3(scale, False, False);
			self._runTest3(scale, False, True);
			self._runTest3(scale, True, False);
			self._runTest3(scale, True, True);
			print i

	def _runTest1(self, scale, setMin, setMax):
		min = random.randint(-1*(10**scale), 10**scale)
		max = random.randint(min, min + 5**scale) #zeby testowalo tez np -100 do -10

		format = "%d"
		regexp = regexpgen.integer(format, min if setMin else None, max if setMax else None)
		info = lambda value: self.__getInfo__(value, regexp, format, min if setMin else None, max if setMax else None)

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

 		if (setMin):
 		 	for i in xrange(rangeLeft, min - 1):
			 	self.assertFalse(re.match(regexp, str(i)), info(str(i)))
		for i in xrange(min, max):
			if i >= 0:
				a = "0" + str(i); b = "00" + str(i); c = "000" + str(i); d = "0000" + str(i);
			else:
				a = "-0" + str(-i); b = "-00" + str(-i); c = "-000" + str(-i); d = "-0000" + str(-i);
			self.assertTrue(re.match(regexp, str(i)), info(str(i)))
			self.assertTrue(re.match(regexp, a), info(a))
			self.assertTrue(re.match(regexp, b), info(b))
			self.assertTrue(re.match(regexp, c), info(c))
			self.assertTrue(re.match(regexp, d), info(d))
		if (setMax):
			for i in xrange(max+1, rangeRight):
				self.assertFalse(re.search(regexp, str(i)), info(str(i)))

	def _runTest2(self, scale, setMin, setMax):
		min = random.randint(-1*(10**scale), 10**scale)
		max = random.randint(min, min + 5**scale) #zeby testowalo tez np -100 do -10
		#print (str(min) + "  " +str(max))
		format = "%0d"
		regexp = regexpgen.integer(format, min if setMin else None, max if setMax else None)
		info = lambda value: self.__getInfo__(value, regexp, format, min if setMin else None, max if setMax else None)

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

 		if (setMin):
 		 	for i in xrange(rangeLeft, min - 1):
			 	self.assertFalse(re.match(regexp, str(i)), info(str(i)))
		for i in xrange(min, max):
			if i >= 0:
				a = "0" + str(i); b = "00" + str(i); c = "000" + str(i); d = "0000" + str(i);
			else:
				a = "-0" + str(-i); b = "-00" + str(-i); c = "-000" + str(-i); d = "-0000" + str(-i);
			self.assertTrue(re.match(regexp, str(i)), info(str(i)))
			self.assertFalse(re.match(regexp, a), info(a))
			self.assertFalse(re.match(regexp, b), info(b))
			self.assertFalse(re.match(regexp, c), info(c))
			self.assertFalse(re.match(regexp, d), info(d))
		if (setMax):
			for i in xrange(max+1, rangeRight):
				self.assertFalse(re.search(regexp, str(i)), info(str(i)))

	def _runTest3(self, scale, setMin, setMax):
		getZeros = lambda x: (scale - len(str(x)))*"0"
		min = random.randint(-1*(10**scale), 10**scale)
		max = random.randint(min, min + 5**scale) #zeby testowalo tez np -100 do -10
#		print (str(min) + "  " +str(max))
		format = "%0{0}d".format(scale)
		regexp = regexpgen.integer(format, min if setMin else None, max if setMax else None)
		info = lambda value: self.__getInfo__(value, regexp, format, min if setMin else None, max if setMax else None)

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

		if (setMin):
			for i in xrange(rangeLeft, min - 1):
				if i < 0:
					a = "-" + getZeros(int(math.fabs(i))) + str(int(math.fabs(i)))
				else:
					a = getZeros(int(math.fabs(i))) + str(i)
				self.assertFalse(re.match(regexp, str(i)), info(str(i)))
				self.assertFalse(re.match(regexp, a), info(a))
		for i in xrange(min, max):
			if (len(str(i)) > scale):
				break
			zeros = getZeros(int(math.fabs(i)))
			if i < 0:
				a = "-" + zeros + str(int(math.fabs(i)))
				b = "-" + zeros + "0" + str(int(math.fabs(i)))
			else:
				a = zeros + str(i); b = zeros + "0" + str(i)
			self.assertTrue(re.match(regexp, a), info(a))
			self.assertFalse(re.match(regexp, b), info(b))
			if (len(zeros) > 0):
				if i < 0:
					c = "-" + zeros[:-1] + str(int(math.fabs(i))) #cuts last zero
				else:
					c = zeros[:-1] + str(i) #cuts last zero
				self.assertFalse(re.match(regexp, c), info(c))
		if (setMax):
			for i in xrange(max+1, rangeRight):
				if i < 0:
					a = "-" + getZeros(int(math.fabs(i))) + str(int(math.fabs(i)))
				else:
					a = getZeros(int(math.fabs(i))) + str(i)
				self.assertFalse(re.match(regexp, str(i)), info(str(i)))
				self.assertFalse(re.match(regexp, a), info(a))

	def __getInfo__(self, i, regexp, format, min, max):
		return "Failed! Number: {0}, min: {1}, max: {2}, format: {3}, regexp: {4}".format(i, str(min), str(max), format, regexp)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
