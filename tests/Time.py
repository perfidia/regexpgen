'''
Created on Mar 16, 2012

@author: Bartosz Alchimowicz
'''
import unittest
import regexpgen
import re

class Test(unittest.TestCase):
	def testStartEnd(self):
		pattern = r"%H:%M"

		self.assertEqual(regexpgen.time(pattern),
						 regexpgen.time(pattern, matchStartEnd = True))

		self.assertEqual(regexpgen.time(pattern, matchStartEnd = True)[0], '^')
		self.assertEqual(regexpgen.time(pattern, matchStartEnd = True)[-1], '$')

		self.assertNotEqual(regexpgen.time(pattern, matchStartEnd = False)[0], '^')
		self.assertNotEqual(regexpgen.time(pattern, matchStartEnd = False)[-1], '$')

	def testDefaultColon(self):
		regexp = regexpgen.time(r"%H:%M")
		print regexp

		for i in ["%2d:%2d" % (H, M) for H in xrange(0, 24) for M in xrange(0, 60) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in ["%02d:%02d" % (H, M) for H in xrange(0, 24) for M in xrange(0, 60) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

	def testDefaultDot(self):
		regexp = regexpgen.time(r"%H.%M")
		print regexp

		for i in ["%2d.%2d" % (H, M) for H in xrange(0, 24) for M in xrange(0, 60) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in ["%02d.%02d" % (H, M) for H in xrange(0, 24) for M in xrange(0, 60) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
