'''
Created on Mar 16, 2012

@author: Bartosz Alchimowicz
'''

import unittest
import regexpgen
import re

class Test(unittest.TestCase):
	def testDefault(self):
		regexp = regexpgen.date("%Y")

		self.assertTrue(re.match(regexp, "1990"))
		self.assertTrue(re.match(regexp, "2099"))
		self.assertTrue(re.match(regexp, "1970"))
		self.assertTrue(re.match(regexp, "1983"))
		self.assertTrue(re.match(regexp, "2012"))

		self.assertFalse(re.match(regexp, "1"))
		self.assertFalse(re.match(regexp, "33"))
		self.assertFalse(re.match(regexp, "0024"))
		self.assertFalse(re.match(regexp, "99"))
		self.assertFalse(re.match(regexp, "-17"))
		self.assertFalse(re.match(regexp, "2100"))
		self.assertFalse(re.match(regexp, "1969"))

		regexp = regexpgen.date("%y")

		self.assertTrue(re.match(regexp, "90"))
		self.assertTrue(re.match(regexp, "99"))
		self.assertTrue(re.match(regexp, "70"))
		self.assertTrue(re.match(regexp, "83"))
		self.assertTrue(re.match(regexp, "02"))

		self.assertFalse(re.match(regexp, "1"))
		self.assertFalse(re.match(regexp, "335"))
		self.assertFalse(re.match(regexp, "0024"))
		self.assertFalse(re.match(regexp, "9"))
		self.assertFalse(re.match(regexp, "-17"))
		self.assertFalse(re.match(regexp, "1ss"))

		regexp = regexpgen.date("%m")

		self.assertTrue(re.match(regexp, "12"))
		self.assertTrue(re.match(regexp, "01"))
		self.assertTrue(re.match(regexp, "11"))
		self.assertTrue(re.match(regexp, "09"))

		self.assertFalse(re.match(regexp, "1"))
		self.assertFalse(re.match(regexp, "335"))
		self.assertFalse(re.match(regexp, "13"))
		self.assertFalse(re.match(regexp, "00"))
		self.assertFalse(re.match(regexp, "-17"))
		self.assertFalse(re.match(regexp, "1s"))

		regexp = regexpgen.date("%d")

		self.assertTrue(re.match(regexp, "12"))
		self.assertTrue(re.match(regexp, "01"))
		self.assertTrue(re.match(regexp, "31"))
		self.assertTrue(re.match(regexp, "28"))
		self.assertTrue(re.match(regexp, "09"))

		self.assertFalse(re.match(regexp, "1"))
		self.assertFalse(re.match(regexp, "335"))
		self.assertFalse(re.match(regexp, "99"))
		self.assertFalse(re.match(regexp, "00"))
		self.assertFalse(re.match(regexp, "-17"))
		self.assertFalse(re.match(regexp, "1ss"))

		regexp = regexpgen.date("%d-%m")
		
		self.assertTrue(re.match(regexp, "12-12"))
		self.assertTrue(re.match(regexp, "01-01"))
		self.assertTrue(re.match(regexp, "31-12"))
		self.assertTrue(re.match(regexp, "28-02"))
		self.assertTrue(re.match(regexp, "09-09"))

		self.assertFalse(re.match(regexp, "1-10"))
		self.assertFalse(re.match(regexp, "31-02"))
		self.assertFalse(re.match(regexp, "99-92"))
		self.assertFalse(re.match(regexp, "00-00"))
		self.assertFalse(re.match(regexp, "-17-00"))
		self.assertFalse(re.match(regexp, "1ss"))

		regexp = regexpgen.date("%Y-%m")

		self.assertTrue(re.match(regexp, "2012-12"))
		self.assertTrue(re.match(regexp, "2001-01"))
		self.assertTrue(re.match(regexp, "1991-12"))
		self.assertTrue(re.match(regexp, "2050-02"))
		self.assertTrue(re.match(regexp, "1999-09"))

		self.assertFalse(re.match(regexp, "1955-10"))
		self.assertFalse(re.match(regexp, "31-02"))
		self.assertFalse(re.match(regexp, "3099-92"))
		self.assertFalse(re.match(regexp, "0000-00"))
		self.assertFalse(re.match(regexp, "-1700-00"))
		self.assertFalse(re.match(regexp, "1sss-ss"))

		regexp = regexpgen.date("%Y-%m-%d")
		
		self.assertTrue(re.match(regexp, "2089-01-12"))
		self.assertTrue(re.match(regexp, "2087-12-13"))
		self.assertTrue(re.match(regexp, "2090-02-28"))
		self.assertTrue(re.match(regexp, "2088-09-30"))

		self.assertFalse(re.match(regexp, "1955-10-00"))
		self.assertFalse(re.match(regexp, "31-02-04"))
		self.assertFalse(re.match(regexp, "3099-92-19"))
		self.assertFalse(re.match(regexp, "0000-00-00"))
		self.assertFalse(re.match(regexp, "-1700-00-21"))
		self.assertFalse(re.match(regexp, "1sss-ss-45"))


	def testForMin(self):

		regexp = regexpgen.date("%Y", "1990")

		self.assertTrue(re.match(regexp, "1990"))
		self.assertTrue(re.match(regexp, "2099"))
		self.assertTrue(re.match(regexp, "1997"))

		self.assertFalse(re.match(regexp, "1989"))
		self.assertFalse(re.match(regexp, "1988"))
		self.assertFalse(re.match(regexp, "0024"))
		self.assertFalse(re.match(regexp, "1969"))

		regexp = regexpgen.date("%y" ,"85")

		self.assertTrue(re.match(regexp, "99"))
		self.assertTrue(re.match(regexp, "88"))
		self.assertTrue(re.match(regexp, "85"))
		self.assertTrue(re.match(regexp, "91"))

		self.assertFalse(re.match(regexp, "01"))
		self.assertFalse(re.match(regexp, "00"))
		self.assertFalse(re.match(regexp, "84"))
		self.assertFalse(re.match(regexp, "55"))

		regexp = regexpgen.date("%m", "06")

		self.assertTrue(re.match(regexp, "12"))
		self.assertTrue(re.match(regexp, "06"))
		self.assertTrue(re.match(regexp, "08"))
		self.assertTrue(re.match(regexp, "09"))

		self.assertFalse(re.match(regexp, "01"))
		self.assertFalse(re.match(regexp, "05"))
		self.assertFalse(re.match(regexp, "13"))
		self.assertFalse(re.match(regexp, "04"))

		regexp = regexpgen.date("%d", "13")

		self.assertTrue(re.match(regexp, "13"))
		self.assertTrue(re.match(regexp, "14"))
		self.assertTrue(re.match(regexp, "31"))
		self.assertTrue(re.match(regexp, "28"))

		self.assertFalse(re.match(regexp, "01"))
		self.assertFalse(re.match(regexp, "12"))
		self.assertFalse(re.match(regexp, "99"))
		self.assertFalse(re.match(regexp, "00"))

		regexp = regexpgen.date("%Y-%m-%d", "2072-12-01")

		self.assertTrue(re.match(regexp, "2072-12-01"))
		self.assertTrue(re.match(regexp, "2083-01-12"))
		self.assertTrue(re.match(regexp, "2090-02-28"))
		self.assertTrue(re.match(regexp, "2099-09-30"))

		self.assertFalse(re.match(regexp, "1972-12-01"))
		self.assertFalse(re.match(regexp, "2012-11-01"))
		self.assertFalse(re.match(regexp, "1995-10-01"))
		self.assertFalse(re.match(regexp, "1955-10-01"))

	def testForMax(self):
		regexp = regexpgen.date("%Y", None, "1990")

		self.assertFalse(re.match(regexp, "1991"))
		self.assertFalse(re.match(regexp, "2099"))
		self.assertFalse(re.match(regexp, "1997"))

		self.assertTrue(re.match(regexp, "1989"))
		self.assertTrue(re.match(regexp, "1990"))
		self.assertTrue(re.match(regexp, "1971"))

		regexp = regexpgen.date("%y" , None, "85")

		self.assertFalse(re.match(regexp, "99"))
		self.assertFalse(re.match(regexp, "88"))
		self.assertFalse(re.match(regexp, "86"))
		self.assertFalse(re.match(regexp, "91"))

		self.assertTrue(re.match(regexp, "01"))
		self.assertTrue(re.match(regexp, "85"))
		self.assertTrue(re.match(regexp, "84"))
		self.assertTrue(re.match(regexp, "55"))

		regexp = regexpgen.date("%m", None, "06")

		self.assertFalse(re.match(regexp, "12"))
		self.assertFalse(re.match(regexp, "07"))
		self.assertFalse(re.match(regexp, "08"))
		self.assertFalse(re.match(regexp, "09"))

		self.assertTrue(re.match(regexp, "01"))
		self.assertTrue(re.match(regexp, "05"))
		self.assertTrue(re.match(regexp, "06"))
		self.assertTrue(re.match(regexp, "04"))

		regexp = regexpgen.date("%d", None, "13")

		self.assertFalse(re.match(regexp, "14"))
		self.assertFalse(re.match(regexp, "15"))
		self.assertFalse(re.match(regexp, "31"))
		self.assertFalse(re.match(regexp, "28"))

		self.assertTrue(re.match(regexp, "01"))
		self.assertTrue(re.match(regexp, "12"))
		self.assertTrue(re.match(regexp, "13"))
		self.assertTrue(re.match(regexp, "07"))

		regexp = regexpgen.date("%Y-%m-%d", None, "1980-12-01")

		self.assertFalse(re.match(regexp, "2072-12-01"))
		self.assertFalse(re.match(regexp, "2083-01-12"))
		self.assertFalse(re.match(regexp, "2090-02-28"))
		self.assertFalse(re.match(regexp, "1980-12-02"))

		self.assertTrue(re.match(regexp, "1980-12-01"))
		self.assertTrue(re.match(regexp, "1980-11-02"))
		self.assertTrue(re.match(regexp, "1975-10-05"))
		self.assertTrue(re.match(regexp, "1977-10-21"))
		
		self.assertTrue(re.match(regexp, "1976-02-29"))
		self.assertFalse(re.match(regexp, "1977-02-29"))
		self.assertTrue(re.match(regexp, "1980-02-29"))
		
	def testForMinMax(self):
		regexp = regexpgen.date("%Y", "1990", "2000")

		self.assertTrue(re.match(regexp, "1990"))
		self.assertTrue(re.match(regexp, "2000"))
		self.assertTrue(re.match(regexp, "1997"))

		self.assertFalse(re.match(regexp, "1989"))
		self.assertFalse(re.match(regexp, "1988"))
		self.assertFalse(re.match(regexp, "2001"))
		self.assertFalse(re.match(regexp, "2011"))

		regexp = regexpgen.date("%y" ,"85", "95")

		self.assertTrue(re.match(regexp, "95"))
		self.assertTrue(re.match(regexp, "88"))
		self.assertTrue(re.match(regexp, "85"))
		self.assertTrue(re.match(regexp, "91"))

		self.assertFalse(re.match(regexp, "01"))
		self.assertFalse(re.match(regexp, "84"))
		self.assertFalse(re.match(regexp, "84"))
		self.assertFalse(re.match(regexp, "99"))

		regexp = regexpgen.date("%m", "06", "10")

		self.assertTrue(re.match(regexp, "10"))
		self.assertTrue(re.match(regexp, "06"))
		self.assertTrue(re.match(regexp, "08"))
		self.assertTrue(re.match(regexp, "09"))

		self.assertFalse(re.match(regexp, "11"))
		self.assertFalse(re.match(regexp, "05"))
		self.assertFalse(re.match(regexp, "13"))
		self.assertFalse(re.match(regexp, "04"))

		regexp = regexpgen.date("%d", "13", "20")

		self.assertTrue(re.match(regexp, "13"))
		self.assertTrue(re.match(regexp, "14"))
		self.assertTrue(re.match(regexp, "20"))
		self.assertTrue(re.match(regexp, "15"))

		self.assertFalse(re.match(regexp, "21"))
		self.assertFalse(re.match(regexp, "12"))
		self.assertFalse(re.match(regexp, "99"))
		self.assertFalse(re.match(regexp, "00"))

		regexp = regexpgen.date("%Y-%m-%d", "2072-12-01", "2085-12-01")

		self.assertTrue(re.match(regexp, "2072-12-01"))
		self.assertTrue(re.match(regexp, "2083-01-12"))
		self.assertTrue(re.match(regexp, "2073-02-28"))
		self.assertTrue(re.match(regexp, "2085-12-01"))

		self.assertFalse(re.match(regexp, "2085-12-02"))
		self.assertFalse(re.match(regexp, "2072-11-30"))
		self.assertFalse(re.match(regexp, "1995-10-01"))
		self.assertFalse(re.match(regexp, "1955-10-01"))
		
	def testForWrongFormat(self):
		self.assertRaises(ValueError, regexpgen.date, "%wd %ay")
		self.assertRaises(ValueError,regexpgen.date, "%Y:%y")
		self.assertRaises(ValueError,regexpgen.date, "%y:%d")
		self.assertRaises(ValueError,regexpgen.date, "%Y:%d")
		self.assertRaises(ValueError,regexpgen.date, "%P")

	def testForWrongInput(self):
		self.assertRaises(ValueError,regexpgen.time, "%d:%m", "01:00", "00:00")
		self.assertRaises(ValueError,regexpgen.time, "%Y-%m", "99-03", "1998-03")
		self.assertRaises(ValueError,regexpgen.time, "%m-%d", "13-02", "02-02")
		self.assertRaises(ValueError,regexpgen.time, "%m", "12", "02")
		self.assertRaises(ValueError,regexpgen.time, "%d", "00", "100")
		self.assertRaises(ValueError,regexpgen.time, "%Y/%m/%d", "1990-02/02", "1992/03-03")

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
