'''
Created on 19-03-2012

@author: Michzimny
'''
import unittest
import re
from regexpgen.misc import digitsNum, diffLastChars
from regexpgen.misc import rawBounds

class Test(unittest.TestCase):
    def testDigitsNum(self):
        self.assertEqual(digitsNum(0), 1)
        self.assertEqual(digitsNum(9), 1)
        self.assertEqual(digitsNum(10), 2)
        self.assertEqual(digitsNum(02345), 4)
        self.assertEqual(digitsNum(None), None)
        
    def testDiffLastChars(self):
        self.assertEqual(diffLastChars("12345","45445"), 0)
        self.assertEqual(diffLastChars("12345","45446"), 1)
    
    def testRawBounds(self):
        self.assertNotEqual(re.match("^"+rawBounds(28, 128)+"$", "32"), None)
        self.assertNotEqual(re.match("^"+rawBounds(28, 128)+"$", "101"), None)
