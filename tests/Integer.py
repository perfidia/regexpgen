'''
Created on Mar 15, 2012

@author: Bartosz Alchimowicz
'''
import unittest
import regexpgen
import re

class Test(unittest.TestCase):
	def testStartEnd(self):
		self.assertEqual(regexpgen.integer("%d"),
						 regexpgen.integer("%d", matchStartEnd = True))

		self.assertEqual(regexpgen.integer("%d", matchStartEnd = True)[0], '^')
		self.assertEqual(regexpgen.integer("%d", matchStartEnd = True)[-1], '$')

		self.assertNotEqual(regexpgen.integer("%d", matchStartEnd = True)[0], '^')
		self.assertNotEqual(regexpgen.integer("%d", matchStartEnd = True)[-1], '$')

	def testDefault(self):
		regexp = regexpgen.integer("%d")
		print regexp

		for i in [ i for i in xrange(-100, 10) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ "01", "00", "0012310" ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

		for i in [ 'a', 1.1, -0.8 ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

	def testNoLeadingZeros(self):
		regexp = regexpgen.integer("%0d")
		print regexp

		for i in [ 0 ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ "00", "01", "06" ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

	def testFourDigits(self):
		regexp = regexpgen.integer("%4d")
		print regexp

		for i in [ "0000", "-1000", "1000000" ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ "1", "0", "a" ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

	def testTwoDigits(self):
		regexp = regexpgen.integer("%2d")
		print regexp

		for i in [ "00", "01", "-10", "-77", "1000000" ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ "1", "0", "a" ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

	def testRangePositive(self):
		regexp = regexpgen.integer("%d", 0, 267)
		print regexp

		for i in [ "0", "-0" ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ i for i in xrange(0, 267 + 1) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ "-1", "268", "269" ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

	def testRangeAll(self):
		regexp = regexpgen.integer("%d", -351, 765)
		print regexp

		for i in [ "0", "-0" ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ i for i in xrange(-351, 765 + 1) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ "-766", "-765", "-352", "766", "1000", "1234" ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

	def testRangeNoLeadingZeros(self):
		regexp = regexpgen.integer("%0d", -1000, 1000)
		print regexp

		for i in [ "0", "-0" ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ i for i in xrange(-1000, 1000 + 1) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ "-1002", "-1001", "1001", "1002", "a", "01", "-01", "017", "-018" ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

	def testRangeFourDigits(self):
		regexp = regexpgen.integer("%4d", -123, 9871)
		print regexp

		for i in [ "0", "-0" ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ i for i in xrange(-123, 9871 + 1) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ "a", "-9871", "-125", "-124", "9872", "9873", "45678" ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

	def testRangeWithZero(self):
		regexp = regexpgen.integer("%04d", -1, 9000)
		print regexp

		for i in [ "0", "-0" ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ i for i in xrange(-1, 9000 + 1) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ "0000", "-0001", "0023", "0123" ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ "a", "-3", "-2", "9001", "9002", "09873", "45678" ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

	def testMin(self):
		regexp = regexpgen.integer("%d", 0)
		print regexp

		for i in [ "0", "-0" ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ i for i in xrange(0, 65000) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ "01", "001", "00019" ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ i for i in xrange(-65000, 0) ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

		for i in [ "-001", "-0001112" ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

	def testMinWithoutZeros(self):
		regexp = regexpgen.integer("%0d", -351)
		print regexp

		for i in [ "0", "-0" ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ i for i in xrange(-65000, -351 + 1 ) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ i for i in xrange(-351 + 1, 65000) ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

		for i in [ "a", "-00100", "-06578" ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

	def testMinWithZeros(self):
		regexp = regexpgen.integer("%04d", min = 100)
		print regexp

		for i in [ "0", "-0" ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ "%04d" % i for i in xrange(-65000 , 100 + 1) ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

		for i in [ "a", "-1", "22", "01", "010", "-010" ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

	def testMax(self):
		regexp = regexpgen.integer("%d", max = 100)
		print regexp

		for i in [ "0", "-0" ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ i for i in xrange(-65000, 100 + 1) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ i for i in xrange(100 + 1, 65000) ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

		for i in [ "01", "001", "00019", "-0001112" ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

	def testMaxWithoutZeros(self):
		regexp = regexpgen.integer("%0d", max = 100)
		print regexp

		for i in [ "0", "-0" ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ i for i in xrange(-65000, 100 + 1) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ "-0123", "01", "001", "00019", "-0001112" ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

		for i in [ i for i in xrange(100 + 1 , 65000) ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

	def testMaxWithZeros(self):
		regexp = regexpgen.integer("%04d", max = 100)
		print regexp

		for i in [ "0", "-0" ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ "%04d" % i for i in xrange(-65000 , 100 + 1) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ "000001", "0000010", "000019", "01", "001" ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

		for i in [ "%04d" % i for i in xrange(100 + 1 , 65000) ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
