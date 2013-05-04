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

    def testForInteger(self):
        regexp = regexpgen.getRegExp("%0d")
        self.assertTrue(re.match(regexp, "-2345"))
        self.assertFalse(re.match(regexp, "0045"))

        regexp = regexpgen.getRegExp("%d")
        self.assertTrue(re.match(regexp, "-002345"))
        self.assertFalse(re.match(regexp, "0045.7"))

        regexp = regexpgen.getRegExp("%05d")
        self.assertTrue(re.match(regexp, "-02345"))
        self.assertFalse(re.match(regexp, "0457"))

    def testForReal(self):
        regexp = regexpgen.getRegExp("%lf")
        self.assertTrue(re.match(regexp, "-2.5"))
        self.assertFalse(re.match(regexp, "0045"))

        regexp = regexpgen.getRegExp("%0lf")
        self.assertTrue(re.match(regexp, "45.7"))
        self.assertFalse(re.match(regexp, "0045.7"))

        regexp = regexpgen.getRegExp("%05.2lf")
        self.assertTrue(re.match(regexp, "-22.45"))
        self.assertFalse(re.match(regexp, "2.3"))

    def testForTime(self):
        regexp = regexpgen.getRegExp("%H")
        self.assertTrue(re.match(regexp, "00"))
        self.assertFalse(re.match(regexp, "67"))

        regexp = regexpgen.getRegExp("%H:%M")
        self.assertTrue(re.match(regexp, "22:45"))
        self.assertFalse(re.match(regexp, "2.3"))

        regexp = regexpgen.getRegExp("%I:%M %P")
        self.assertTrue(re.match(regexp, "02:45 PM"))
        self.assertFalse(re.match(regexp, "22:34 pm"))

    def testForDate(self):
        regexp = regexpgen.getRegExp("%Y")
        self.assertTrue(re.match(regexp, "1990"))
        self.assertFalse(re.match(regexp, "-67.3"))

        regexp = regexpgen.getRegExp("%d/%m/%Y")
        self.assertTrue(re.match(regexp, "22/10/2010"))
        self.assertFalse(re.match(regexp, "2.3"))

        regexp = regexpgen.getRegExp("%m-%d")
        self.assertTrue(re.match(regexp, "02-12"))
        self.assertFalse(re.match(regexp, "22-34"))
        
    def testForBadFormat(self):
        self.assertRaises(ValueError, regexpgen.getRegExp, "%0d %d", 100.6757, 100)
        self.assertRaises(ValueError, regexpgen.getRegExp, "%d:%H", 100.6757, 100)
        self.assertRaises(ValueError, regexpgen.getRegExp, "%lf %03d", 100.6757, 100)
        self.assertRaises(ValueError, regexpgen.getRegExp, "%lf %m", 100.6757, 100)
        self.assertRaises(ValueError, regexpgen.getRegExp, "%m-%M", 100.6757, 100)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
