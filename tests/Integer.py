'''
Created on Mar 15, 2012

@authors: Joanna Binczewska, Dawid Kowalski
'''

import unittest
import regexpgen
import re
import random
import math

class Test(unittest.TestCase):

	def testDefault(self):
		random.seed(0);

		for i in xrange(0, 1100):
			scale = len(str(i))
			self.__runTest1(scale, False, False);
			self.__runTest1(scale, False, True);
			self.__runTest1(scale, True, False);
			self.__runTest1(scale, True, True);
			self.__runTest2(scale, False, False);
			self.__runTest2(scale, False, True);
			self.__runTest2(scale, True, False);
			self.__runTest2(scale, True, True);
			self.__runTest3(scale, False, False);
			self.__runTest3(scale, False, True);
			self.__runTest3(scale, True, False);
			self.__runTest3(scale, True, True);
			print i

	def __runTest1(self, scale, setMin, setMax):
		min = random.randint(-1*(10**scale), 10**scale)
		max = random.randint(min, min + 5**scale) #zeby testowalo tez np -100 do -10
		format = "%d"
		regexp = regexpgen.integer(format, min if setMin else None, max if setMax else None)
		info = lambda value: self.__getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

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

		if setMin:
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
		if setMax:
			for i in xrange(max+1, rangeRight):
				self.assertFalse(re.search(regexp, str(i)), info(str(i)))

	def __runTest2(self, scale, setMin, setMax):
		min = random.randint(-1*(10**scale), 10**scale)
		max = random.randint(min, min + 5**scale) #zeby testowalo tez np -100 do -10
		format = "%0d"
		regexp = regexpgen.integer(format, min if setMin else None, max if setMax else None)
		info = lambda value: self.__getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

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

		if setMin:
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
		if setMax:
			for i in xrange(max+1, rangeRight):
				self.assertFalse(re.search(regexp, str(i)), info(str(i)))

	def __runTest3(self, scale, setMin, setMax):
		getZeros = lambda x: (scale - len(str(x)))*"0"
		min = random.randint(-1*(10**scale), 10**scale)
		max = random.randint(min, min + 5**scale) #zeby testowalo tez np -100 do -10
		format = "%0{0}d".format(scale)
		regexp = regexpgen.integer(format, min if setMin else None, max if setMax else None)
		info = lambda value: self.__getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

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

		if setMin:
			for i in xrange(rangeLeft, min - 1):
				if i < 0:
					a = "-" + getZeros(int(math.fabs(i))) + str(int(math.fabs(i)))
				else:
					a = getZeros(int(math.fabs(i))) + str(i)
				self.assertFalse(re.match(regexp, str(i)), info(str(i)))
				self.assertFalse(re.match(regexp, a), info(a))
		for i in xrange(min, max):
			if len(str(i)) > scale:
				break
			zeros = getZeros(int(math.fabs(i)))
			if i < 0:
				a = "-" + zeros + str(int(math.fabs(i)))
				b = "-" + zeros + "0" + str(int(math.fabs(i)))
			else:
				a = zeros + str(i); b = zeros + "0" + str(i)
			self.assertTrue(re.match(regexp, a), info(a))
			self.assertFalse(re.match(regexp, b), info(b))
			if len(zeros) > 0:
				if i < 0:
					c = "-" + zeros[:-1] + str(int(math.fabs(i))) #cuts last zero
				else:
					c = zeros[:-1] + str(i) #cuts last zero
				self.assertFalse(re.match(regexp, c), info(c))
		if setMax:
			for i in xrange(max+1, rangeRight):
				if i < 0:
					a = "-" + getZeros(int(math.fabs(i))) + str(int(math.fabs(i)))
				else:
					a = getZeros(int(math.fabs(i))) + str(i)
				self.assertFalse(re.match(regexp, str(i)), info(str(i)))
				self.assertFalse(re.match(regexp, a), info(a))

	def __getInfo(self, i, regexp, format, min, max):
		return "Failed! Number: {0}, min: {1}, max: {2}, format: {3}, regexp: {4}".format(i, str(min), str(max), format, regexp)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
