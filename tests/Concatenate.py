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

    def testDefault(self):
        regexp = regexpgen.concatenate([
        ('int', "%d", 100, 105),
        ('\.',),
        ('int', "%d", 250, 255),
        ('\.',),
        ('int', "%d", 122, 122),
        ('\.',),
        ('int', "%d", 0, 240)
        ])

        self.assertTrue(re.match(regexp, "100.250.122.1"))
        self.assertFalse(re.match(regexp, "111.117.111.1"))
        
        regexp = regexpgen.concatenate([
        ('int', "%d", 100, 105),
        ('\-',),
        ('real', "%lf")
        ])

        self.assertTrue(re.match(regexp, "100-22.5"))
        self.assertFalse(re.match(regexp, "22.5-100"))
        
        regexp = regexpgen.concatenate([
        ('date', "%m/%d"),
        (' ',),
        ('time', "%H:%M")
        ])

        self.assertTrue(re.match(regexp, "02/25 22:13"))
        self.assertFalse(re.match(regexp, "22.5-100"))
        
        regexp = regexpgen.concatenate([
        ('date', "%m/%d"),
        (' - ',),
        ('date', "%m/%d")
        ])

        self.assertTrue(re.match(regexp, "02/25 - 02/27"))
        self.assertFalse(re.match(regexp, "32/25 - 32/25"))
         
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
