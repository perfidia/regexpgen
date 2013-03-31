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
		self.__testForWrongFormat()
		self.__testForWrongInput()

		random.seed(0)

		for a in xrange(0, 3):
			for i in xrange(0, 1100):
				for j in [True, False]:
					for k in [True, False]:
						scale = len(self.__str(i))
						self.__runTest1(scale, False, False, j, k);
						self.__runTest1(scale, False, True, j, k);
						self.__runTest1(scale, True, False, j, k);
						self.__runTest1(scale, True, True, j, k);
						self.__runTest2(scale, False, False, j, k);
						self.__runTest2(scale, False, True, j, k);
						self.__runTest2(scale, True, False, j, k);
						self.__runTest2(scale, True, True, j, k);
						self.__runTest3(scale, False, False, j, k);
						self.__runTest3(scale, False, True, j, k);
						self.__runTest3(scale, True, False, j, k);
						self.__runTest3(scale, True, True, j, k);
						self.__runTest4(scale, False, False, j, k);
						self.__runTest4(scale, False, True, j, k);
						self.__runTest4(scale, True, False, j, k);
						self.__runTest4(scale, True, True, j, k);
				print a,i

	def __runTest1(self, scale, setMin, setMax, useInt, stepInt):

		if stepInt:
			step = random.randint(1,3)
		else:
			step = random.uniform(0.5, 1.5)

		min = random.uniform(-1*(10**scale), 10**scale) if not useInt else random.randint(-1*(10**scale), 10**scale)
		max = random.uniform(min, min + 5**scale) if not useInt else random.randint(min, min + 5**scale)
		min = float(min)
		max = float(max)

		format = "%lf"
		regexp = regexpgen.real(format, min if setMin else None, max if setMax else None)
		info = lambda value: self.__getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

		(rangeLeft, rangeRight) = self.__getRanges(min, max)

		i = rangeLeft
		if setMin:
			while float(self.__str(i)) < float(self.__str(min)):
				self.assertFalse(re.match(regexp, self.__str(i)), info(self.__str(i)))
				i = i + step
		while float(self.__str(i)) <= float(self.__str(max)):
			if i >= 0:
				a = "0" + self.__str(i); b = "00" + self.__str(i); c = "000" + self.__str(i); d = "0000" + self.__str(i);
			else:
				a = "-0" + self.__str(-i); b = "-00" + self.__str(-i); c = "-000" + self.__str(-i); d = "-0000" + self.__str(-i);
			self.assertTrue(re.match(regexp, self.__str(i)), info(self.__str(i)))
			self.assertTrue(re.match(regexp, a), info(a))
			self.assertTrue(re.match(regexp, b), info(b))
			self.assertTrue(re.match(regexp, c), info(c))
			self.assertTrue(re.match(regexp, d), info(d))
			i = i + step
		if setMax:
			while i <= rangeRight:
				self.assertFalse(re.search(regexp, self.__str(i)), info(self.__str(i)))
				i = i + step

	def __runTest2(self, scale, setMin, setMax, useInt, stepInt):

		if useInt:
			step = random.randint(1,3)
		else:
			step = random.uniform(0.5, 1.5)

		min = random.uniform(-1*(10**scale), 10**scale) if not useInt else random.randint(-1*(10**scale), 10**scale)
		max = random.uniform(min, min + 5**scale) if not useInt else random.randint(min, min + 5**scale)
		min = float(min)
		max = float(max)

		format = "%0lf"
		regexp = regexpgen.real(format, min if setMin else None, max if setMax else None)
		info = lambda value: self.__getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

		(rangeLeft, rangeRight) = self.__getRanges(min, max)

		i = rangeLeft
		if setMin:
			while float(self.__str(i)) < float(self.__str(min)):
				self.assertFalse(re.match(regexp, self.__str(i)), info(self.__str(i)))
				i = i + step
		while float(self.__str(i)) <= float(self.__str(max)):
			if i >= 0:
				a = "0" + self.__str(i); b = "00" + self.__str(i); c = "000" + self.__str(i); d = "0000" + self.__str(i);
			else:
				a = "-0" + self.__str(-i); b = "-00" + self.__str(-i); c = "-000" + self.__str(-i); d = "-0000" + self.__str(-i);
			self.assertTrue(re.match(regexp, self.__str(i)), info(self.__str(i)))
			self.assertFalse(re.match(regexp, a), info(a))
			self.assertFalse(re.match(regexp, b), info(b))
			self.assertFalse(re.match(regexp, c), info(c))
			self.assertFalse(re.match(regexp, d), info(d))
			i = i + step
		if setMax:
			while i <= rangeRight:
				self.assertFalse(re.search(regexp, self.__str(i)), info(self.__str(i)))
				i = i + step

	def __runTest3(self, scale, setMin, setMax, useInt, stepInt):
		if useInt:
			step = random.randint(1,3)
		else:
			step = random.uniform(0.5, 1.5)

		min = random.uniform(-1*(10**scale), 10**scale) if not useInt else random.randint(-1*(10**scale), 10**scale)
		max = random.uniform(min, min + 5**scale) if not useInt else random.randint(min, min + 5**scale)
		format = "%0.{0}lf".format(scale)
		min = float(self.__sliceFloat(float(min), scale))
		max = float(self.__sliceFloat(float(max), scale))
		regexp = regexpgen.real(format, min if setMin else None, max if setMax else None)
		info = lambda value: self.__getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

		(rangeLeft, rangeRight) = self.__getRanges(min, max)

		i = rangeLeft
		if setMin:
			while float(self.__str(i)) < float(self.__str(min)) - step:
				x = self.__sliceFloat(i, scale - 1 if scale > 1 else 0)
				y = self.__sliceFloat(i, scale)
				z = self.__sliceFloat(i, scale + 1)
				if scale > 1:
					self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))
				self.assertFalse(re.match(regexp, self.__str(y)), info(self.__str(y)))
				self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
				i = i + step
			i = i + step
		while float(self.__str(i)) <= float(self.__str(max)):
			if i >= 0:
				a = "0" + self.__str(i); b = "00" + self.__str(i); c = "000" + self.__str(i); d = "0000" + self.__str(i);
			else:
				a = "-0" + self.__str(-i); b = "-00" + self.__str(-i); c = "-000" + self.__str(-i); d = "-0000" + self.__str(-i);

			x = self.__sliceFloat(i, scale - 1 if scale > 1 else 0)
			y = self.__sliceFloat(i, scale)
			z = self.__sliceFloat(i, scale + 1)

			self.assertTrue(re.match(regexp, self.__str(y)), info(self.__str(y)))
			self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
			self.assertFalse(re.match(regexp, a), info(a))
			self.assertFalse(re.match(regexp, b), info(b))
			self.assertFalse(re.match(regexp, c), info(c))
			self.assertFalse(re.match(regexp, d), info(d))
			i = i + step
		if setMax:
			i = i + step
			while i <= rangeRight:
				x = self.__sliceFloat(i, scale - 1 if scale > 0 else 0)
				y = self.__sliceFloat(i, scale)
				z = self.__sliceFloat(i, scale + 1)
				if scale > 1:
					self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))
				self.assertFalse(re.match(regexp, self.__str(y)), info(self.__str(y)))
				self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
				i = i + step

	def __runTest4(self, scale, setMin, setMax, useInt, stepInt):
		if useInt:
			step = random.randint(1,3)
		else:
			step = random.uniform(0.5, 1.5)

		min = random.uniform(-1*(10**scale), 10**scale) if not useInt else random.randint(-1*(10**scale), 10**scale)
		max = random.uniform(min, min + 5**scale) if not useInt else random.randint(min, min + 5**scale)
		format = "%.{0}lf".format(scale)
		min = float(self.__sliceFloat(float(min), scale))
		max = float(self.__sliceFloat(float(max), scale))
		regexp = regexpgen.real(format, min if setMin else None, max if setMax else None)
		info = lambda value: self.__getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

		(rangeLeft, rangeRight) = self.__getRanges(min, max)

		i = rangeLeft
		if setMin:
			while float(self.__str(i)) < float(self.__str(min)) - step:
				x = self.__sliceFloat(i, scale - 1 if scale > 0 else 0)
				y = self.__sliceFloat(i, scale)
				z = self.__sliceFloat(i, scale + 1)
				if scale > 1:
					self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))
				self.assertFalse(re.match(regexp, self.__str(y)), info(self.__str(y)))
				self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
				i = i + step
			i = i + step
		while float(self.__str(i)) <= float(self.__str(max)):
			if i >= 0:
				a = "0" + self.__str(i); b = "00" + self.__str(i); c = "000" + self.__str(i); d = "0000" + self.__str(i);
			else:
				a = "-0" + self.__str(-i); b = "-00" + self.__str(-i); c = "-000" + self.__str(-i); d = "-0000" + self.__str(-i);

			x = self.__sliceFloat(i, scale - 1 if scale > 1 else 0)
			y = self.__sliceFloat(i, scale)
			z = self.__sliceFloat(i, scale + 1)
			a = self.__sliceFloat(a, scale)
			b = self.__sliceFloat(b, scale)
			c = self.__sliceFloat(c, scale)
			d = self.__sliceFloat(d, scale)
			aa = self.__sliceFloat(a, scale + 1)
			bb = self.__sliceFloat(b, scale + 1)
			cc = self.__sliceFloat(c, scale + 1)
			dd = self.__sliceFloat(d, scale + 1)

			self.assertTrue(re.match(regexp, self.__str(y)), info(self.__str(y)))
			if scale > 2:
				self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))

			self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
			self.assertTrue(re.match(regexp, a), info(a))
			self.assertTrue(re.match(regexp, b), info(b))
			self.assertTrue(re.match(regexp, c), info(c))
			self.assertTrue(re.match(regexp, d), info(d))
			self.assertFalse(re.match(regexp, aa), info(aa))
			self.assertFalse(re.match(regexp, bb), info(bb))
			self.assertFalse(re.match(regexp, cc), info(cc))
			self.assertFalse(re.match(regexp, dd), info(dd))
			i = i + step
		if setMax:
			i = i + step
			while i <= rangeRight:
				x = self.__sliceFloat(i, scale - 1 if scale > 0 else 0)
				y = self.__sliceFloat(i, scale)
				z = self.__sliceFloat(i, scale + 1)
				if scale > 1:
					self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))
				self.assertFalse(re.match(regexp, self.__str(y)), info(self.__str(y)))
				self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
				i = i + step

	def __sliceFloat(self, f, scale):
		splitted = self.__str(f).split(".")

		if len(splitted[1]) > scale:
			x = splitted[1][0:scale]
		elif len(splitted[1]) < scale:
			x = splitted[1] + "0"*(scale -len(splitted[1]))
		else:
			x = splitted[1]

		if x == "":
			return float(splitted[0])

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
			rangeLeft = -100.0
			rangeRight = 100.0
		return (rangeLeft, rangeRight)

	def __getInfo(self, i, regexp, format, min, max):
		return "Failed! Number: {0}, min: {1}, max: {2}, format: {3}, regexp: {4}".format(i, self.__str(min), self.__str(max), format, regexp)

	def __str(self, x):
		if x != None and str(x).count("e") > 0:
			return "{:f}".format(float(x))
		else:
			return str(x)

	def __testForWrongFormat(self):
		self.assertRaises(ValueError, regexpgen.real,"%0d", -100.0, 1000.0)
		self.assertRaises(ValueError, regexpgen.real,"%d", 100.0, 1000.0)
		self.assertRaises(ValueError, regexpgen.real,"aaaaaaaaa", None, 1000.0)
		self.assertRaises(ValueError, regexpgen.real, "%0.2lf", None, 1000)
		self.assertRaises(ValueError, regexpgen.real, None, None, 1000)

	def __testForWrongInput(self):
		self.assertRaises(ValueError, regexpgen.real,"%lf", -100, 1000)
		self.assertRaises(ValueError, regexpgen.real,"%0lf", 100, 1000)
		self.assertRaises(ValueError, regexpgen.real,"%lf", None, 10000)
		self.assertRaises(ValueError, regexpgen.real,"%0.2lf", None, 10000)
		self.assertRaises(ValueError, regexpgen.real,"%.2lf", None, 1000)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
