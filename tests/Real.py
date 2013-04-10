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
        self.__testForShorterReal()
        self.__testForWrongFormat()
        self.__testForWrongInput()
        self.__testForBoundaryReal()

        random.seed(0)

        for a in xrange(0, 3):
            for i in xrange(0, 1100):
                for j in [True, False]:
                    for k in [True, False]:
                        scale = len(self.__str(i))
                        self.__runTest1(scale, False, False, j, k)
                        self.__runTest1(scale, False, True, j, k)
                        self.__runTest1(scale, True, False, j, k)
                        self.__runTest1(scale, True, True, j, k)
                        self.__runTest2(scale, False, False, j, k)
                        self.__runTest2(scale, False, True, j, k)
                        self.__runTest2(scale, True, False, j, k)
                        self.__runTest2(scale, True, True, j, k)
                        self.__runTest3(scale, False, False, j, k)
                        self.__runTest3(scale, False, True, j, k)
                        self.__runTest3(scale, True, False, j, k)
                        self.__runTest3(scale, True, True, j, k)
                        self.__runTest4(scale, False, False, j, k)
                        self.__runTest4(scale, False, True, j, k)
                        self.__runTest4(scale, True, False, j, k)
                        self.__runTest4(scale, True, True, j, k)
                        self.__runTest5(scale, False, False, j, k)
                        self.__runTest5(scale, False, True, j, k)
                        self.__runTest5(scale, True, False, j, k)
                        self.__runTest5(scale, True, True, j, k)
                        self.__runTest6(scale, False, False, j, k)
                        self.__runTest6(scale, False, True, j, k)
                        self.__runTest6(scale, True, False, j, k)
                        self.__runTest6(scale, True, True, j, k)
                print a,i

    def __runTest1(self, scale, setMin, setMax, useInt, stepInt):

        if stepInt:
            step = random.randint(1,3)
        else:
            step = random.uniform(0.5, 1.5)

        min = random.uniform(-1*(10**scale), 10**scale) if not useInt else random.randint(-1*(10**scale), 10**scale)
        max = random.uniform(min, min + 5**scale) if not useInt else random.randint(min, min + 5**scale)
        min = float(min)
        max = float(max)

        format = "%lf"
        regexp = regexpgen.real(format, min if setMin else None, max if setMax else None)
        info = lambda value: self.__getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

        (rangeLeft, rangeRight) = self.__getRanges(min, max)

        i = rangeLeft
        if setMin:
            self.assertTrue(re.search(regexp, self.__str(min)), info(self.__str(min)))
            while float(self.__str(i)) < float(self.__str(min)):
                self.assertFalse(re.match(regexp, self.__str(i)), info(self.__str(i)))
                i = i + step
        while float(self.__str(i)) <= float(self.__str(max)):
            if i >= 0:
                a = "0" + self.__str(i); b = "00" + self.__str(i); c = "000" + self.__str(i); d = "0000" + self.__str(i);
            else:
                a = "-0" + self.__str(-i); b = "-00" + self.__str(-i); c = "-000" + self.__str(-i); d = "-0000" + self.__str(-i);
            self.assertTrue(re.match(regexp, self.__str(i)), info(self.__str(i)))
            self.assertTrue(re.match(regexp, a), info(a))
            self.assertTrue(re.match(regexp, b), info(b))
            self.assertTrue(re.match(regexp, c), info(c))
            self.assertTrue(re.match(regexp, d), info(d))
            i = i + step
        if setMax:
            self.assertTrue(re.search(regexp, self.__str(max)), info(self.__str(max)))
            while i <= rangeRight:
                self.assertFalse(re.search(regexp, self.__str(i)), info(self.__str(i)))
                i = i + step

        if setMax and float(max) > 0:
            splitted = self.__str(max).split(".")
            if len(splitted[1]) > 1:
                test = splitted[0] + "." + splitted[1][:-1]
                test = float(test)
                self.assertTrue(re.match(regexp, self.__str(test)), info(self.__str(test)))

    def __runTest2(self, scale, setMin, setMax, useInt, stepInt):

        if useInt:
            step = random.randint(1,3)
        else:
            step = random.uniform(0.5, 1.5)

        min = random.uniform(-1*(10**scale), 10**scale) if not useInt else random.randint(-1*(10**scale), 10**scale)
        max = random.uniform(min, min + 5**scale) if not useInt else random.randint(min, min + 5**scale)
        min = float(min)
        max = float(max)

        format = "%0lf"
        regexp = regexpgen.real(format, min if setMin else None, max if setMax else None)
        info = lambda value: self.__getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

        (rangeLeft, rangeRight) = self.__getRanges(min, max)

        i = rangeLeft
        if setMin:
            self.assertTrue(re.search(regexp, self.__str(min)), info(self.__str(min)))
            while float(self.__str(i)) < float(self.__str(min)):
                self.assertFalse(re.match(regexp, self.__str(i)), info(self.__str(i)))
                i = i + step
        while float(self.__str(i)) <= float(self.__str(max)):
            if i >= 0:
                a = "0" + self.__str(i); b = "00" + self.__str(i); c = "000" + self.__str(i); d = "0000" + self.__str(i);
            else:
                a = "-0" + self.__str(-i); b = "-00" + self.__str(-i); c = "-000" + self.__str(-i); d = "-0000" + self.__str(-i);
            self.assertTrue(re.match(regexp, self.__str(i)), info(self.__str(i)))

            self.assertFalse(re.match(regexp, a), info(a))
            self.assertFalse(re.match(regexp, b), info(b))
            self.assertFalse(re.match(regexp, c), info(c))
            self.assertFalse(re.match(regexp, d), info(d))
            i = i + step
        if setMax:
            self.assertTrue(re.search(regexp, self.__str(max)), info(self.__str(max)))
            while i <= rangeRight:
                self.assertFalse(re.search(regexp, self.__str(i)), info(self.__str(i)))
                i = i + step

        if setMax and float(max) > 0:
            splitted = self.__str(max).split(".")
            if len(splitted[1]) > 1:
                test = splitted[0] + "." + splitted[1][:-1]
                test = float(test)
                self.assertTrue(re.match(regexp, self.__str(test)), info(self.__str(test)))

    def __runTest3(self, scale, setMin, setMax, useInt, stepInt):
        if useInt:
            step = random.randint(1,3)
        else:
            step = random.uniform(0.5, 1.5)

        min = random.uniform(-1*(10**scale), 10**scale) if not useInt else random.randint(-1*(10**scale), 10**scale)
        max = random.uniform(min, min + 5**scale) if not useInt else random.randint(min, min + 5**scale)
        format = "%0.{0}lf".format(scale)
        min = float(self.__sliceFloat(float(min), scale))
        max = float(self.__sliceFloat(float(max), scale))
        regexp = regexpgen.real(format, min if setMin else None, max if setMax else None)
        info = lambda value: self.__getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

        (rangeLeft, rangeRight) = self.__getRanges(min, max)

        i = rangeLeft
        if setMin:
            while float(self.__str(i)) < float(self.__str(min)) - step:
                x = self.__sliceFloat(i, scale - 1 if scale > 1 else 0)
                y = self.__sliceFloat(i, scale)
                z = self.__sliceFloat(i, scale + 1)
                if scale > 1:
                    self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))
                self.assertFalse(re.match(regexp, self.__str(y)), info(self.__str(y)))
                self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
                i = i + step
            i = i + step
        while float(self.__str(i)) <= float(self.__str(max)):
            if i >= 0:
                a = "0" + self.__str(i); b = "00" + self.__str(i); c = "000" + self.__str(i); d = "0000" + self.__str(i);
            else:
                a = "-0" + self.__str(-i); b = "-00" + self.__str(-i); c = "-000" + self.__str(-i); d = "-0000" + self.__str(-i);

            x = self.__sliceFloat(i, scale - 1 if scale > 1 else 0)
            y = self.__sliceFloat(i, scale)
            z = self.__sliceFloat(i, scale + 1)

            self.assertTrue(re.match(regexp, self.__str(y)), info(self.__str(y)))
            self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
            self.assertFalse(re.match(regexp, a), info(a))
            self.assertFalse(re.match(regexp, b), info(b))
            self.assertFalse(re.match(regexp, c), info(c))
            self.assertFalse(re.match(regexp, d), info(d))
            i = i + step
        if setMax:
            i = i + step
            while i <= rangeRight:
                x = self.__sliceFloat(i, scale - 1 if scale > 0 else 0)
                y = self.__sliceFloat(i, scale)
                z = self.__sliceFloat(i, scale + 1)
                if scale > 1:
                    self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))
                self.assertFalse(re.match(regexp, self.__str(y)), info(self.__str(y)))
                self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
                i = i + step

    def __runTest4(self, scale, setMin, setMax, useInt, stepInt):
        if useInt:
            step = random.randint(1,3)
        else:
            step = random.uniform(0.5, 1.5)

        min = random.uniform(-1*(10**scale), 10**scale) if not useInt else random.randint(-1*(10**scale), 10**scale)
        max = random.uniform(min, min + 5**scale) if not useInt else random.randint(min, min + 5**scale)
        format = "%.{0}lf".format(scale)
        min = float(self.__sliceFloat(float(min), scale))
        max = float(self.__sliceFloat(float(max), scale))
        regexp = regexpgen.real(format, min if setMin else None, max if setMax else None)
        info = lambda value: self.__getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

        (rangeLeft, rangeRight) = self.__getRanges(min, max)

        i = rangeLeft
        if setMin:
            while float(self.__str(i)) < float(self.__str(min)) - step:
                x = self.__sliceFloat(i, scale - 1 if scale > 0 else 0)
                y = self.__sliceFloat(i, scale)
                z = self.__sliceFloat(i, scale + 1)
                if scale > 1:
                    self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))
                self.assertFalse(re.match(regexp, self.__str(y)), info(self.__str(y)))
                self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
                i = i + step
            i = i + step
        while float(self.__str(i)) <= float(self.__str(max)):
            if i >= 0:
                a = "0" + self.__str(i); b = "00" + self.__str(i); c = "000" + self.__str(i); d = "0000" + self.__str(i);
            else:
                a = "-0" + self.__str(-i); b = "-00" + self.__str(-i); c = "-000" + self.__str(-i); d = "-0000" + self.__str(-i);

            x = self.__sliceFloat(i, scale - 1 if scale > 1 else 0)
            y = self.__sliceFloat(i, scale)
            z = self.__sliceFloat(i, scale + 1)
            a = self.__sliceFloat(a, scale)
            b = self.__sliceFloat(b, scale)
            c = self.__sliceFloat(c, scale)
            d = self.__sliceFloat(d, scale)
            aa = self.__sliceFloat(a, scale + 1)
            bb = self.__sliceFloat(b, scale + 1)
            cc = self.__sliceFloat(c, scale + 1)
            dd = self.__sliceFloat(d, scale + 1)

            self.assertTrue(re.match(regexp, self.__str(y)), info(self.__str(y)))
            if scale > 2:
                self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))

            self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
            self.assertTrue(re.match(regexp, a), info(a))
            self.assertTrue(re.match(regexp, b), info(b))
            self.assertTrue(re.match(regexp, c), info(c))
            self.assertTrue(re.match(regexp, d), info(d))
            self.assertFalse(re.match(regexp, aa), info(aa))
            self.assertFalse(re.match(regexp, bb), info(bb))
            self.assertFalse(re.match(regexp, cc), info(cc))
            self.assertFalse(re.match(regexp, dd), info(dd))
            i = i + step
        if setMax:
            i = i + step
            while i <= rangeRight:
                x = self.__sliceFloat(i, scale - 1 if scale > 0 else 0)
                y = self.__sliceFloat(i, scale)
                z = self.__sliceFloat(i, scale + 1)
                if scale > 1:
                    self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))
                self.assertFalse(re.match(regexp, self.__str(y)), info(self.__str(y)))
                self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
                i = i + step

    def __runTest5(self, scale, setMin, setMax, useInt, stepInt):
        if useInt:
            step = random.randint(1,3)
        else:
            step = random.uniform(0.5, 1.5)

        min = random.uniform(-1*(10**scale), 10**scale) if not useInt else random.randint(-1*(10**scale), 10**scale)
        max = random.uniform(min, min + 5**scale) if not useInt else random.randint(min, min + 5**scale)
        format = "%{0}.{1}lf".format(scale + 2, scale)
        min = float(self.__sliceFloat(float(min), scale))
        max = float(self.__sliceFloat(float(max), scale))
        regexp = regexpgen.real(format, min if setMin else None, max if setMax else None)
        info = lambda value: self.__getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

        (rangeLeft, rangeRight) = self.__getRanges(min, max)

        i = rangeLeft
        if setMin:
            while float(self.__str(i)) < float(self.__str(min)) - step:
                x = self.__sliceFloat(i, scale - 1 if scale > 0 else 0)
                y = self.__sliceFloat(i, scale)
                z = self.__sliceFloat(i, scale + 1)
                if scale > 1:
                    self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))
                self.assertFalse(re.match(regexp, self.__str(y)), info(self.__str(y)))
                self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
                i = i + step
            i = i + step
        while float(self.__str(i)) <= float(self.__str(max)):
            if i >= 0:
                a = "0" + self.__str(i); b = "00" + self.__str(i); c = "000" + self.__str(i); d = "0000" + self.__str(i);
            else:
                a = "-0" + self.__str(-i); b = "-00" + self.__str(-i); c = "-000" + self.__str(-i); d = "-0000" + self.__str(-i);

            x = self.__sliceFloat(i, scale - 1 if scale > 1 else 0)
            y = self.__sliceFloat(i, scale)
            z = self.__sliceFloat(i, scale + 1)
            a = self.__sliceFloat(a, scale)
            b = self.__sliceFloat(b, scale)
            c = self.__sliceFloat(c, scale)
            d = self.__sliceFloat(d, scale)
            aa = self.__sliceFloat(a, scale + 1)
            bb = self.__sliceFloat(b, scale + 1)
            cc = self.__sliceFloat(c, scale + 1)
            dd = self.__sliceFloat(d, scale + 1)

            self.assertTrue(re.match(regexp, self.__str(y)), info(self.__str(y)))
            if scale > 2:
                self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))

            self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
            self.assertTrue(re.match(regexp, a), info(a))
            self.assertTrue(re.match(regexp, b), info(b))
            self.assertTrue(re.match(regexp, c), info(c))
            self.assertTrue(re.match(regexp, d), info(d))
            self.assertFalse(re.match(regexp, aa), info(aa))
            self.assertFalse(re.match(regexp, bb), info(bb))
            self.assertFalse(re.match(regexp, cc), info(cc))
            self.assertFalse(re.match(regexp, dd), info(dd))
            i = i + step
        if setMax:
            i = i + step
            while i <= rangeRight:
                x = self.__sliceFloat(i, scale - 1 if scale > 0 else 0)
                y = self.__sliceFloat(i, scale)
                z = self.__sliceFloat(i, scale + 1)
                if scale > 1:
                    self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))
                self.assertFalse(re.match(regexp, self.__str(y)), info(self.__str(y)))
                self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
                i = i + step


    def __runTest6(self, scale, setMin, setMax, useInt, stepInt):
        if useInt:
            step = random.randint(1,3)
        else:
            step = random.uniform(0.5, 1.5)
        scaleR = scale
        scaleI = scale + 1
        min = random.uniform(-1*(10**scale), 10**scale) if not useInt else random.randint(-1*(10**scale), 10**scale)
        max = random.uniform(min, min + 5**scale) if not useInt else random.randint(min, min + 5**scale)
        format = "%0{0}.{1}lf".format(scaleI + 1, scaleR) # +1 because dot is included
        min = float(self.__sliceFloat(float(min), scaleR))
        max = float(self.__sliceFloat(float(max), scaleR))
        scaleI = scaleI - scaleR
        min = float(self.__sliceFloatIntPart(float(min), scaleI))
        max = float(self.__sliceFloatIntPart(float(max), scaleI))
        regexp = regexpgen.real(format, min if setMin else None, max if setMax else None)
        info = lambda value: self.__getInfo(value, regexp, format, min if setMin else None, max if setMax else None)

        (rangeLeft, rangeRight) = self.__getRanges(min, max)

        i = rangeLeft
        if setMin:
            while float(self.__str(i)) < float(self.__str(min)) - step:
                x = self.__sliceFloat(i, scaleR - 1 if scaleR > 0 else 0)
                y = self.__sliceFloat(i, scaleR)
                z = self.__sliceFloat(i, scaleR + 1)

                x = self.__sliceFloatIntPart(x, scaleI)
                y = self.__sliceFloatIntPart(y, scaleI)
                z = self.__sliceFloatIntPart(z, scaleI)

                if scale > 1:
                    self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))
                self.assertFalse(re.match(regexp, self.__str(y)), info(self.__str(y)))
                self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
                i = i + step
            i = i + step
            
        while float(self.__str(i)) <= float(self.__str(max)):

            x = self.__sliceFloat(i, scaleR - 1 if scaleR > 1 else 0)
            y = self.__sliceFloat(i, scaleR)
            z = self.__sliceFloat(i, scaleR + 1)

            x = self.__sliceFloatIntPart(x, scaleI)
            y = self.__sliceFloatIntPart(y, scaleI)
            z = self.__sliceFloatIntPart(z, scaleI)

            self.assertTrue(re.match(regexp, self.__str(y)), info(self.__str(y)))
            if scale > 2:
                self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))
            self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))

            x = self.__sliceFloat(i, scaleR)
            y = self.__sliceFloat(i, scaleR)
            z = self.__sliceFloat(i, scaleR)

            if not setMin and not setMax:
                x = self.__sliceFloatIntPart(x, scaleI - 1 if scaleI > 1 else 0)
                y = self.__sliceFloatIntPart(y, scaleI)
                z = self.__sliceFloatIntPart(z, scaleI + 1, "1")

                self.assertTrue(re.match(regexp, self.__str(y)), info(self.__str(y)))
                if scaleI > 2:
                    self.assertTrue(re.match(regexp, self.__str(x)), info(self.__str(x)))
                if i > 0:
                    self.assertTrue(re.match(regexp, self.__str(z)), info(self.__str(z)))

            if setMin and not setMax:
                x = self.__sliceFloatIntPart(x, scaleI - 1 if scaleI > 1 else 0)
                y = self.__sliceFloatIntPart(y, scaleI)
                z = self.__sliceFloatIntPart(z, scaleI + 1, "1")

                self.assertTrue(re.match(regexp, self.__str(y)), info(self.__str(y)))
                if scaleI > 2:
                    self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))
                if i > 0:
                    self.assertTrue(re.match(regexp, self.__str(z)), info(self.__str(z)))

            if setMax and not setMin:
                x = self.__sliceFloatIntPart(x, scaleI - 1 if scaleI > 1 else 0)
                y = self.__sliceFloatIntPart(y, scaleI)
                z = self.__sliceFloatIntPart(z, scaleI + 1, "1")

                self.assertTrue(re.match(regexp, self.__str(y)), info(self.__str(y)))
                if scaleI > 2:
                    self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))
                if i < 0:
                    self.assertTrue(re.match(regexp, self.__str(z)), info(self.__str(z)))

            if setMax and setMin:
                x = self.__sliceFloatIntPart(x, scaleI - 1 if scaleI > 1 else 0)
                y = self.__sliceFloatIntPart(y, scaleI)

                self.assertTrue(re.match(regexp, self.__str(y)), info(self.__str(y)))
                if scaleI > 2:
                    self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))
            i = i + step
            
        if setMax:
            i = i + step
            while i <= rangeRight:
                x = self.__sliceFloat(i, scaleR - 1 if scaleR > 0 else 0)
                y = self.__sliceFloat(i, scaleR)
                z = self.__sliceFloat(i, scaleR + 1)
                x = self.__sliceFloatIntPart(x, scaleI - 1 if scaleI > 0 else 0)
                y = self.__sliceFloatIntPart(y, scaleI)
                z = self.__sliceFloatIntPart(z, scaleI + 1)
                if scale > 1:
                    self.assertFalse(re.match(regexp, self.__str(x)), info(self.__str(x)))
                self.assertFalse(re.match(regexp, self.__str(y)), info(self.__str(y)))
                self.assertFalse(re.match(regexp, self.__str(z)), info(self.__str(z)))
                i = i + step

    def __sliceFloat(self, f, scale):
        splitted = self.__str(f).split(".")

        if len(splitted[1]) > scale:
            x = splitted[1][0:scale]
        elif len(splitted[1]) < scale:
            x = "0"*(scale -len(splitted[1])) + splitted[1]
        else:
            x = splitted[1]

        if x == "":
            return float(splitted[0])

        return splitted[0] + "." + x

    def __sliceFloatIntPart(self, f, scale, add = "0"):
        splitted = self.__str(f).split(".")

        if str(f).find("-") >= 0:
            minus = "-"
            splitted[0] = splitted[0][1:]
        else:
            minus = ""

        if len(splitted[0]) < scale:
            if minus == "":
                x = add * (scale - len(splitted[0])) + splitted[0]
            else:
                x = splitted[0]
        else:
            x = splitted[0]

        return  minus + x + "." + splitted[1]

    def __getRanges(self, min, max):
        min = float(min)
        max = float(max)
        if min < 0 and max < 0:
            rangeLeft = min*2
            rangeRight = -min*2
        if min < 0 and max > 0:
            rangeLeft = min*2
            rangeRight = max*2
        if min > 0 and max > 0:
            rangeLeft = -max*2
            rangeRight = max*2
        if min == 0 and max != 0:
            rangeLeft = -max*2
            rangeRight = max*2
        if max == 0 and min != 0:
            rangeLeft = min*2
            rangeRight = -min*2
        if max == 0 and min == 0:
            rangeLeft = -100.0
            rangeRight = 100.0
        return (rangeLeft, rangeRight)

    def __getInfo(self, i, regexp, format, min, max):
        return "Failed! Number: {0}, min: {1}, max: {2}, format: {3}, regexp: {4}".format(i, self.__str(min), self.__str(max), format, regexp)

    def __str(self, x):
        if x != None and str(x).count("e") > 0:
            return "{:f}".format(float(x))
        else:
            return str(x)

    def __testForWrongFormat(self):
        self.assertRaises(ValueError, regexpgen.real,"%0d", -100.0, 1000.0)
        self.assertRaises(ValueError, regexpgen.real,"%d", 100.0, 1000.0)
        self.assertRaises(ValueError, regexpgen.real,"aaaaaaaaa", None, 1000.0)
        self.assertRaises(ValueError, regexpgen.real, "%0.2lf", None, 1000)
        self.assertRaises(ValueError, regexpgen.real, None, None, 1000)
        self.assertRaises(ValueError, regexpgen.real, 123)
        self.assertRaises(ValueError, regexpgen.real, 12.3)

    def __testForWrongInput(self):
        self.assertRaises(ValueError, regexpgen.real,"%lf", -100, 1000)
        self.assertRaises(ValueError, regexpgen.real,"%0lf", 100, 1000)
        self.assertRaises(ValueError, regexpgen.real,"%lf", None, 10000)
        self.assertRaises(ValueError, regexpgen.real,"%0.2lf", None, 10000)
        self.assertRaises(ValueError, regexpgen.real,"%.2lf", None, 1000)
        self.assertRaises(ValueError, regexpgen.real, "%lf", "123", 123)
        self.assertRaises(ValueError, regexpgen.real, "%lf", 123, "123")

    def __testForShorterReal(self):
        x = regexpgen.real("%lf", 7.009, 7.698)
        self.assertTrue(re.match(x, "7.69")) # powinno byc match

        x = regexpgen.real("%lf", 7.09, 7.98)
        self.assertTrue(re.match(x, "7.69")) # powinno byc match

        x = regexpgen.real("%lf", None, 0.02)
        self.assertFalse(re.match(x, "0.04")) # powinno byc None

        x = regexpgen.real("%lf", -25.2691864655, -25.0697582645)
        self.assertFalse(re.match(x, "-25.8042065349")) # powinno byc None

        x = regexpgen.real("%lf", 6.063, 9.493)
        self.assertTrue(re.match(x, "9.49")) # powinno byc match

        x = regexpgen.real("%lf", 15.07, None)
        self.assertTrue(re.match(x, "15.3")) # powinno byc match

        x = regexpgen.real("%lf", None, 0.4)
        self.assertFalse(re.match(x, "0.8")) # powinno byc None

        x = regexpgen.real("%lf", None, 14.00)
        self.assertTrue(re.match(x, "0.519")) # powinno byc match

        x = regexpgen.real("%lf", 40.822, 46.202)
        self.assertFalse(re.match(x, "46.21")) # powinno byc None

        x = regexpgen.real("%lf", 0.97, 1.04)
        self.assertFalse(re.match(x, "0.9")) # powinno byc None

        x = regexpgen.real("%lf", None, 13.077)
        self.assertFalse(re.match(x, "13.088")) # powinno byc None

        x = regexpgen.real("%lf", None, 13.93)
        self.assertTrue(re.match(x, "13.9")) # powinno byc match

        x = regexpgen.real("%lf", -6.1, -3.3)
        self.assertFalse(re.match(x, "-6.8")) # powinno byc None

        self.assertFalse(re.match(regexpgen.real("%lf", 88.7653193745, 88.920716654), "88.0"))
        self.assertTrue(re.match(regexpgen.real("%lf", 88.7653193745, 88.920716654), "88.9"))
        self.assertTrue(re.match(regexpgen.real("%lf", 88.7653193745, 88.920716654), "88.92"))
        self.assertTrue(re.match(regexpgen.real("%lf", 88.7653193745, 88.920716654), "88.920"))
        self.assertTrue(re.match(regexpgen.real("%lf", 88.7653193745, 88.920716654), "88.9207"))
        self.assertTrue(re.match(regexpgen.real("%lf", 88.7653193745, 88.920716654), "88.92071"))
        self.assertTrue(re.match(regexpgen.real("%lf", 88.7653193745, 88.920716654), "88.920716"))
        self.assertTrue(re.match(regexpgen.real("%lf", 88.7653193745, 88.920716654), "88.9207166"))
        self.assertTrue(re.match(regexpgen.real("%lf", 88.7653193745, 88.920716654), "88.92071665"))        

    def __testForBoundaryReal(self):
        self.assertTrue(re.match(regexpgen.real("%03.1lf", 5.1, None), "8.9"))
        self.assertTrue(re.match(regexpgen.real("%03.1lf", 5.1, None), "88.9"))
        self.assertTrue(re.match(regexpgen.real("%03.1lf", -5.1, None), "-4.9"))
        self.assertTrue(re.match(regexpgen.real("%03.1lf", -5.1, None), "55.9"))
        self.assertFalse(re.match(regexpgen.real("%03.1lf", -5.1, None), "-55.1"))
        self.assertTrue(re.match(regexpgen.real("%04.1lf", 5.9, None), "05.9"))
        self.assertFalse(re.match(regexpgen.real("%05.1lf", 5.9, None), "05.9"))
        self.assertTrue(re.match(regexpgen.real("%06.2lf", 5.9, None), "005.90"))
        self.assertFalse(re.match(regexpgen.real("%04.2lf", 5.9, None), "3335.9"))
        self.assertFalse(re.match(regexpgen.real("%05.1lf", -5.9, None), "-05.9"))
        self.assertTrue(re.match(regexpgen.real("%06.2lf", -5.9, None), "-005.90"))

        self.assertTrue(re.match(regexpgen.real("%03.1lf",None, 5.1), "4.9"))
        self.assertTrue(re.match(regexpgen.real("%03.1lf",None, 5.1), "-88.9"))
        self.assertTrue(re.match(regexpgen.real("%03.1lf",None, -5.1), "-5.9"))
        self.assertTrue(re.match(regexpgen.real("%03.1lf",None, -5.1), "-55.9"))
        self.assertFalse(re.match(regexpgen.real("%03.1lf",None, -5.1), "55.1"))
        self.assertTrue(re.match(regexpgen.real("%04.1lf",None, 5.9), "05.9"))
        self.assertFalse(re.match(regexpgen.real("%05.1lf",None, 5.9), "05.9"))
        self.assertTrue(re.match(regexpgen.real("%06.2lf",None, 5.9), "005.90"))
        self.assertFalse(re.match(regexpgen.real("%06.2lf",None, 5.9), "05.90"))
        self.assertFalse(re.match(regexpgen.real("%04.2lf",None, 5.9), "3335.91"))
        self.assertFalse(re.match(regexpgen.real("%05.1lf",None, -5.9), "-05.9"))
        self.assertTrue(re.match(regexpgen.real("%06.2lf",None, -5.9), "-005.90"))
        self.assertFalse(re.match(regexpgen.real("%03.1lf",None, -9.1), "99.1"))
        self.assertTrue(re.match(regexpgen.real("%04.1lf",None, 9.9), "09.9"))
        self.assertFalse(re.match(regexpgen.real("%05.1lf",None, 9.9), "09.9"))
        self.assertTrue(re.match(regexpgen.real("%06.2lf",None, 9.9), "009.90"))

        self.assertTrue(re.match(regexpgen.real("%03.1lf",3.1, 5.1), "4.9"))
        self.assertTrue(re.match(regexpgen.real("%03.1lf",-7.3, 5.1), "-6.9"))
        self.assertTrue(re.match(regexpgen.real("%03.1lf",-8.9, -5.1), "-5.9"))
        self.assertFalse(re.match(regexpgen.real("%03.1lf",-5.1, -5.0), "55.1"))
        self.assertTrue(re.match(regexpgen.real("%04.1lf",4.1, 5.9), "05.9"))
        self.assertFalse(re.match(regexpgen.real("%05.1lf",1.0, 5.9), "05.9"))
        self.assertTrue(re.match(regexpgen.real("%06.2lf",1.0, 5.9), "005.90"))
        self.assertFalse(re.match(regexpgen.real("%06.2lf",1.2, 5.9), "05.90"))
        self.assertFalse(re.match(regexpgen.real("%04.2lf",2.8, 5.9), "3335.91"))
        self.assertFalse(re.match(regexpgen.real("%05.1lf",-22.8, -5.9), "-05.9"))
        self.assertTrue(re.match(regexpgen.real("%06.2lf",-22.8, -5.9), "-005.90"))
        self.assertFalse(re.match(regexpgen.real("%03.1lf",-9.3, -9.1), "99.1"))
        self.assertTrue(re.match(regexpgen.real("%04.1lf",1.2, 9.9), "09.9"))
        self.assertFalse(re.match(regexpgen.real("%05.1lf",1.2, 9.9), "09.9"))
        self.assertTrue(re.match(regexpgen.real("%06.2lf",1.2, 9.9), "009.90"))
        
        self.assertFalse(re.match(regexpgen.real("%06.4lf", 1.3399, 9.9434), "009.9044"))
        self.assertTrue(re.match(regexpgen.real("%08.4lf", 1.3399, 9.9434), "009.9044"))
        self.assertTrue(re.match(regexpgen.real("%03.1lf", None, -3.0), "-12.0"))
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
