'''
Created on Mar 16, 2012

@author: Bartosz Alchimowicz
'''
import unittest
import regexpgen
import re

class Test(unittest.TestCase):
	def testStartEnd(self):
		pattern = r"%Y-%m-%d"

		self.assertEqual(regexpgen.date(pattern),
						 regexpgen.date(pattern, matchStartEnd = True))

		self.assertEqual(regexpgen.date(pattern, matchStartEnd = True)[0], '^')
		self.assertEqual(regexpgen.date(pattern, matchStartEnd = True)[-1], '$')

		self.assertNotEqual(regexpgen.date(pattern, matchStartEnd = False)[0], '^')
		self.assertNotEqual(regexpgen.date(pattern, matchStartEnd = False)[-1], '$')

	def testDefaultDash(self):
		regexp = regexpgen.time(r"%Y-%m-%d")
		print regexp

		for i in ["%d-%d-%d" % (y, m, d) for y in xrange(1999, 2020) for m in xrange(0, 12 + 1) for d in xrange(0, 29) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in ["%04d-%02d-%02d" % (y, m, d) for y in xrange(1999, 2020) for m in xrange(0, 12 + 1) for d in xrange(0, 29) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

	def testDefaultDot(self):
		regexp = regexpgen.time(r"%Y.%m.%d")
		print regexp

		for i in ["%d.%d.%d" % (y, m, d) for y in xrange(1999, 2020) for m in xrange(0, 12 + 1) for d in xrange(0, 29) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in ["%04d.%02d.%02d" % (y, m, d) for y in xrange(1999, 2020) for m in xrange(0, 12 + 1) for d in xrange(0, 29) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
