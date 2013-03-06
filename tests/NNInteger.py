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

	def testDefault(self):
		random.seed(0);
		for i in xrange(0, 10000):
			scale = len(str(i))
			self.__runTest1__(scale, False, False);
			self.__runTest1__(scale, False, True);
			self.__runTest1__(scale, True, False);
			self.__runTest1__(scale, True, True);
			self.__runTest2__(scale, False, False);
			self.__runTest2__(scale, False, True);
			self.__runTest2__(scale, True, False);
			self.__runTest2__(scale, True, True);
			self.__runTest3__(scale, False, False);
			self.__runTest3__(scale, False, True);
			self.__runTest3__(scale, True, False);
			self.__runTest3__(scale, True, True);
			print i

	def __runTest1__(self, scale, setMin, setMax):
		min = random.randint(0, 10**scale) if setMin else 0
		max = random.randint(min, min + 10**scale)
		format = "%d"
		regexp = regexpgen.nnint(format, min if setMin else None, max if setMax else None)
		info = lambda value: self.__getInfo__(value, regexp, format, min if setMin else None, max if setMax else None)
		for i in xrange(-max * 2, -1):
			self.assertFalse(re.match(regexp, str(i)), info(str(i)))
		for i in xrange(0, min - 1):
			self.assertFalse(re.match(regexp, str(i)), info(str(i)))
		for i in xrange(min, max):
			a = "0" + str(i); b = "00" + str(i); c = "000" + str(i); d = "0000" + str(i);
			self.assertTrue(re.match(regexp, str(i)), info(str(i)))
			self.assertTrue(re.match(regexp, a), info(a))
			self.assertTrue(re.match(regexp, b), info(b))
			self.assertTrue(re.match(regexp, c), info(c))
			self.assertTrue(re.match(regexp, d), info(d))
		if (setMax):
			for i in xrange(max+1, max * 2):
				self.assertFalse(re.search(regexp, str(i)), info(str(i)))

	def __runTest2__(self, scale, setMin, setMax):
		min = random.randint(0, 10**scale) if setMin else 0
		max = random.randint(min, min + 10**scale)
		format = "%0d"
		regexp = regexpgen.nnint(format, min if setMin else None, max if setMax else None)
		info = lambda value: self.__getInfo__(value, regexp, format, min if setMin else None, max if setMax else None)
		for i in xrange(-max * 2, -1):
			self.assertFalse(re.match(regexp, str(i)), info(str(i)))
		for i in xrange(0, min - 1):
			self.assertFalse(re.match(regexp, str(i)), info(str(i)))
		for i in xrange(min, max):
			a = "0" + str(i); b = "00" + str(i); c = "000" + str(i); d = "0000" + str(i);
			self.assertTrue(re.match(regexp, str(i)), info(str(i)))
			self.assertFalse(re.match(regexp, a), info(a))
			self.assertFalse(re.match(regexp, b), info(b))
			self.assertFalse(re.match(regexp, c), info(c))
			self.assertFalse(re.match(regexp, d), info(d))
		if (setMax):
			for i in xrange(max+1, max * 2):
				self.assertFalse(re.match(regexp, str(i)), info(str(i)))

	def __runTest3__(self, scale, setMin, setMax):
		getZeros = lambda x: (scale - len(str(x)))*"0"
		min = random.randint(0, 10**scale) if setMin else 0
		max = random.randint(min, min + 10**scale)
		format = "%0{0}d".format(scale)
		regexp = regexpgen.nnint(format, min if setMin else None, max if setMax else None)
		info = lambda value: self.__getInfo__(value, regexp, format, min if setMin else None, max if setMax else None)
		for i in xrange(-max * 2, -1):
			a = "-" + getZeros(i) + str(math.fabs(i));
			self.assertFalse(re.match(regexp, str(i)), info(str(i)))
			self.assertFalse(re.match(regexp, a), info(a))
		for i in xrange(0, min - 1):
			a = getZeros(i) + str(i);
			self.assertFalse(re.match(regexp, str(i)), info(str(i)))
			self.assertFalse(re.match(regexp, a), info(a))
		for i in xrange(min, max):
			if (len(str(i)) > scale):
				break
			zeros = getZeros(i)
			a = zeros + str(i); b = zeros + "0" + str(i);
			self.assertTrue(re.match(regexp, a), info(a))
			self.assertFalse(re.match(regexp, b), info(b))
			if (len(zeros) > 0):
				c = zeros[:-1] + str(i) #cuts last zero
				self.assertFalse(re.match(regexp, c), info(c))
		if (setMax):
			for i in xrange(max+1, max * 2):
				a = getZeros(i) + str(i)
				self.assertFalse(re.match(regexp, str(i)), info(str(i)))
				self.assertFalse(re.match(regexp, a), info(a))

	def __getInfo__(self, i, regexp, format, min, max):
		return "Failed! Number: {0}, min: {1}, max: {2}, format: {3}, regexp: {4}".format(i, str(min), str(max), format, regexp)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()