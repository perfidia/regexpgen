'''
Created on Mar 16, 2012

@author: Bartosz Alchimowicz
'''
import unittest
import regexpgen
import re

class Test(unittest.TestCase):
	def testStartEnd(self):
		pattern = r"%lf"

		self.assertEqual(regexpgen.real(pattern),
						 regexpgen.real(pattern, matchStartEnd = True))

		self.assertEqual(regexpgen.real(pattern, matchStartEnd = True)[0], '^')
		self.assertEqual(regexpgen.real(pattern, matchStartEnd = True)[-1], '$')

		self.assertNotEqual(regexpgen.real(pattern, matchStartEnd = False)[0], '^')
		self.assertNotEqual(regexpgen.real(pattern, matchStartEnd = False)[-1], '$')

	def testDefault(self):
		regexp = regexpgen.real(r"%lf")
		print regexp

		for i in [ i/100 for i in xrange(-65000, 65000) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ i for i in xrange(-65000, 0 + 1) ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

		for i in [ 'a' ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
