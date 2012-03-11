'''
Created on Apr 27, 2011

@author: Bartosz Alchimowicz
'''
import unittest
import regexpgen
import re

class Test(unittest.TestCase):
	def testDefaultNoRangeRE(self):
		self.assertEquals(regexpgen.nnint("%d"), '[0-9]+')
		self.assertEquals(regexpgen.nnint("%0d"), '[1-9][0-9]*')
		self.assertEquals(regexpgen.nnint("%04d"), '(^[0-9]{4}$)|(^[1-9][0-9]{4,}$)')

	def testDefaultNoRangeMatch(self):
		self.assertEqual(re.match(regexpgen.nnint("%d"), "-2"), None)
		self.assertNotEqual(re.match(regexpgen.nnint("%d"), "04"), None)
		
		self.assertNotEqual(re.match(regexpgen.nnint("%0d"), "4"), None)
		self.assertEqual(re.match(regexpgen.nnint("%0d"), "04"), None)
		
		self.assertNotEqual(re.match(regexpgen.nnint("%04d"), "0001"), None)
		self.assertEqual(re.match(regexpgen.nnint("%04d"), "-45678"), None)
		self.assertEqual(re.match(regexpgen.nnint("%04d"), "00011"), None)
		self.assertEqual(re.match(regexpgen.nnint("%04d"), "11"), None)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
