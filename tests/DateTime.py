'''
Created on Mar 16, 2012

@author: Bartosz Alchimowicz
'''

import unittest
import regexpgen
import re

class Test(unittest.TestCase):
	def testStartEnd(self):
		pattern= r"%Y-%m-%d %H:%M"

		self.assertEqual(regexpgen.datetime(pattern),
						 regexpgen.datetime(pattern, matchStartEnd = True))

		self.assertEqual(regexpgen.datetime(pattern, matchStartEnd = True)[0], '^')
		self.assertEqual(regexpgen.datetime(pattern, matchStartEnd = True)[-1], '$')

		self.assertNotEqual(regexpgen.datetime(pattern, matchStartEnd = False)[0], '^')
		self.assertNotEqual(regexpgen.datetime(pattern, matchStartEnd = False)[-1], '$')

	def testDefault(self):
		"""
		Warning: This test requires a lot of time.
		"""

		regexp = regexpgen.time(r"%Y-%m-%d %H:%M")
		print regexp

		for i in ["%d-%d-%d %d:%d" % (y, m, d, H, M) for y in xrange(2010, 2015) for m in xrange(0, 12 + 1) for d in xrange(0, 29) for H in xrange(0, 24) for M in xrange(0, 60) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in ["%0d-%0d-%0d %0d:%0d" % (y, m, d, H, M) for y in xrange(2010, 2015) for m in xrange(0, 12 + 1) for d in xrange(0, 29) for H in xrange(0, 24) for M in xrange(0, 60) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
