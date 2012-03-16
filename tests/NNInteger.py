'''
Created on Mar 16, 2012

@author: Bartosz Alchimowicz
'''
import unittest
import regexpgen
import re

class Test(unittest.TestCase):
	def testStartEnd(self):
		self.assertEqual(regexpgen.nnint("%d"),
						 regexpgen.nnint("%d", matchStartEnd = True))

		self.assertEqual(regexpgen.nnint("%d", matchStartEnd = True)[0], '^')
		self.assertEqual(regexpgen.nnint("%d", matchStartEnd = True)[-1], '$')

		self.assertNotEqual(regexpgen.nnint("%d", matchStartEnd = False)[0], '^')
		self.assertNotEqual(regexpgen.nnint("%d", matchStartEnd = False)[-1], '$')

	def testDefault(self):
		regexp = regexpgen.nnint("%d")
		print regexp

		for i in [ i for i in xrange(0, 65000) ]:
			print "check", i
			self.assertNotEqual(re.match(regexp, str(i)), None)

		for i in [ i for i in xrange(-65000, 0 + 1) ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

		for i in [ 'a', 1.1, -0.8 ]:
			print "check", i
			self.assertEqual(re.match(regexp, str(i)), None)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()