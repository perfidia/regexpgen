'''
Created on Apr 27, 2011

@author: Bartosz Alchimowicz
'''
import unittest
import regexpgen
import re

class Test(unittest.TestCase):
	def testDefaultNoRangeRE(self):
		self.assertEquals(
				regexpgen.nnint("%d"),
				'[0-9]+'
		)

	def testDefaultNoRangeMatch(self):
		self.assertNotEqual(re.match(regexpgen.nnint("%d"), "2"), None)
		self.assertNotEqual(re.match(regexpgen.nnint("%d"), "200"), None)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
