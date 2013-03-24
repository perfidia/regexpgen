'''
Created on Mar 16, 2012

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
		min = random.uniform(-1*(10**scale), 10**scale)
		max = random.uniform(min, min + 5**scale) #zeby testowalo tez np -100 do -10

		format = "%lf"
		regexp = regexpgen.real(format, min if setMin else None, max if setMax else None)
		info = lambda value: self.__getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

		(rangeLeft, rangeRight) = self.__getRanges(min, max)

		rest = min - int(min)
		rest = math.fabs(rest)
		i = rangeLeft
		if setMin:
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
		if setMax:
			while i <= rangeRight:
				self.assertFalse(re.search(regexp, str(i)), info(str(i)))
				i = i + 1.05

	def __runTest2(self, scale, setMin, setMax):
		min = random.uniform(-1*(10**scale), 10**scale)
		max = random.uniform(min, min + 5**scale)
		format = "%0lf"
		regexp = regexpgen.real(format, min if setMin else None, max if setMax else None)
		info = lambda value: self.__getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

		(rangeLeft, rangeRight) = self.__getRanges(min, max)

 		rest = min - int(min)
		rest = math.fabs(rest)
		i = rangeLeft
		if setMin:
			while i < min :
				self.assertFalse(re.match(regexp, str(i)), info(str(i)))
			 	i = i + 1.05
		while i <= max:
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
		if setMax:
			while i <= rangeRight:
				self.assertFalse(re.search(regexp, str(i)), info(str(i)))
				i = i + 1.05

	def __runTest3(self, scale, setMin, setMax):
		min = random.uniform(-1*(10**scale), 10**scale)
		max = random.uniform(min, min + 5**scale)
		format = "%0.{0}lf".format(scale)
		min = float(self.__sliceFloat(min, scale))
		max = float(self.__sliceFloat(max, scale))
		regexp = regexpgen.real(format, min if setMin else None, max if setMax else None)
		info = lambda value: self.__getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

		(rangeLeft, rangeRight) = self.__getRanges(min, max)

		i = rangeLeft
		if setMin:
			while i < min - 1.05:
				x = self.__sliceFloat(i, scale - 1 if scale > 0 else 0)
				y = self.__sliceFloat(i, scale)
				z = self.__sliceFloat(i, scale + 1)
				self.assertFalse(re.match(regexp, str(x)), info(str(x)))
				self.assertFalse(re.match(regexp, str(y)), info(str(y)))
				self.assertFalse(re.match(regexp, str(z)), info(str(z)))
			 	i = i + 1.05
			i = i + 1.05
		while i <= max:
			if i >= 0:
				a = "0" + str(i); b = "00" + str(i); c = "000" + str(i); d = "0000" + str(i);
			else:
				a = "-0" + str(-i); b = "-00" + str(-i); c = "-000" + str(-i); d = "-0000" + str(-i);

			x = self.__sliceFloat(i, scale - 1 if scale > 0 else 0)
			y = self.__sliceFloat(i, scale)
			z = self.__sliceFloat(i, scale + 1)

			self.assertTrue(re.match(regexp, str(y)), info(str(y)))
			#if (x != y):
			#	self.assertFalse(re.match(regexp, str(x)), info(str(x)))

			self.assertFalse(re.match(regexp, str(z)), info(str(z)))
			self.assertFalse(re.match(regexp, a), info(a))
			self.assertFalse(re.match(regexp, b), info(b))
			self.assertFalse(re.match(regexp, c), info(c))
			self.assertFalse(re.match(regexp, d), info(d))
			i = i + 1.05
		if setMax:
			i = i + 1.05
			while i <= rangeRight:
				x = self.__sliceFloat(i, scale - 1 if scale > 0 else 0)
				y = self.__sliceFloat(i, scale)
				z = self.__sliceFloat(i, scale + 1)
				self.assertFalse(re.match(regexp, str(x)), info(str(x)))
				self.assertFalse(re.match(regexp, str(y)), info(str(y)))
				self.assertFalse(re.match(regexp, str(z)), info(str(z)))
				i = i + 1.05

	def __sliceFloat(self, f, scale):
		splitted = str(f).split(".")

		if (len(splitted[1]) > scale):
			x = splitted[1][0:scale]
		elif (len(splitted[1]) < scale):
			x = splitted[1] + "0"*(scale -len(splitted[1]))
		else:
			x = splitted[1]

		if x == "":
			return splitted[0]

		return splitted[0] + "." + x

	def __getRanges(self, min, max):
		min = float(min)
		max = float(max)
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
		return (rangeLeft, rangeRight)

	def __getInfo(self, i, regexp, format, min, max):
		return "Failed! Number: {0}, min: {1}, max: {2}, format: {3}, regexp: {4}".format(i, str(min), str(max), format, regexp)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
