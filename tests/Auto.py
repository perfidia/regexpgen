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
        regexp = regexpgen.auto("%0d")
        self.assertTrue(re.match(regexp, "-2345"))
        self.assertFalse(re.match(regexp, "0045"))

        regexp = regexpgen.auto("%d")
        self.assertTrue(re.match(regexp, "-002345"))
        self.assertFalse(re.match(regexp, "0045.7"))

        regexp = regexpgen.auto("%05d")
        self.assertTrue(re.match(regexp, "-02345"))
        self.assertFalse(re.match(regexp, "0457"))

    def testForReal(self):
        regexp = regexpgen.auto("%lf")
        self.assertTrue(re.match(regexp, "-2.5"))
        self.assertFalse(re.match(regexp, "0045"))

        regexp = regexpgen.auto("%0lf")
        self.assertTrue(re.match(regexp, "45.7"))
        self.assertFalse(re.match(regexp, "0045.7"))

        regexp = regexpgen.auto("%05.2lf")
        self.assertTrue(re.match(regexp, "-22.45"))
        self.assertFalse(re.match(regexp, "2.3"))

    def testForTime(self):
        regexp = regexpgen.auto("%H")
        self.assertTrue(re.match(regexp, "00"))
        self.assertFalse(re.match(regexp, "67"))

        regexp = regexpgen.auto("%H:%M")
        self.assertTrue(re.match(regexp, "22:45"))
        self.assertFalse(re.match(regexp, "2.3"))

        regexp = regexpgen.auto("%I:%M %P")
        self.assertTrue(re.match(regexp, "02:45 PM"))
        self.assertFalse(re.match(regexp, "22:34 pm"))

    def testForDate(self):
        regexp = regexpgen.auto("%Y")
        self.assertTrue(re.match(regexp, "1990"))
        self.assertFalse(re.match(regexp, "-67.3"))

        regexp = regexpgen.auto("%d/%m/%Y")
        self.assertTrue(re.match(regexp, "22/10/2010"))
        self.assertFalse(re.match(regexp, "2.3"))

        regexp = regexpgen.auto("%m-%d")
        self.assertTrue(re.match(regexp, "02-12"))
        self.assertFalse(re.match(regexp, "22-34"))

    def testForBadFormat(self):
        self.assertRaises(ValueError, regexpgen.auto, "%0d %d", 100.6757, 100)
        self.assertRaises(ValueError, regexpgen.auto, "%d:%H", 100.6757, 100)
        self.assertRaises(ValueError, regexpgen.auto, "%lf %03d", 100.6757, 100)
        self.assertRaises(ValueError, regexpgen.auto, "%lf %m", 100.6757, 100)
        self.assertRaises(ValueError, regexpgen.auto, "%m-%M", 100.6757, 100)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
