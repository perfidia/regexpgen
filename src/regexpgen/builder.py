# -*- coding: utf-8 -*-

'''
Created on March 5, 2013

@authors: Joanna Binczewska, Dawid Kowalski

Builder object for regular expressions.
'''

import re
import math

class RegexBuilder(object):
    def __init__(self):
        self.alternatives = [[]]
        self.currentIndex = 0
        self.zeros = 0
        self.format = ""
        self.base = ""
        self.setBase = True

    def __startNextAlternative(self):
        if len(self.alternatives[self.currentIndex]) == 0:
            return
        self.alternatives.append([])
        self.currentIndex = self.currentIndex + 1

    def __setNNRegExpBase(self):
        if self.format == "%0d":
            self.base = "{0}"
        if self.format == "%d":
            self.base = "0*({0})"
        m = re.match('%0([0-9]+)d', self.format)
        if m:
            self.base = "{0}"

    def __setRegExpBase(self):
        if self.format == "%0d":
            self.base = "^({0})$"
        if self.format == "%d":
            self.base = "^(0*({0}))$"
        m = re.match("%0([0-9]+)d", self.format)
        if m:
            self.base = "^({0})$"

    def __buildRegEx(self):
        result = []
        for alternative in self.alternatives:
            if alternative != []:
                m = re.match("^.+-+.+$", str(alternative))
                if len(alternative) == 1 and m is None:
                    result.append("0" * (self.zeros - len(str(alternative[0]))))
                else:
                    result.append("0" * (self.zeros - len(alternative)))
                for element in alternative:
                    result.append(element)
                result.append("|")
        result = "".join(result)
        return self.base.format(result[:-1])

    def __addRange(self, mi, ma):
        if mi == ma:
            r = str(mi)
        else:
            r = "[{0}-{1}]".format(str(mi), str(ma))
        self.alternatives[self.currentIndex].append(r)

    def __addElement(self, element):
        self.alternatives[self.currentIndex].append(str(element))

    def __sameDigit(self, digit, number):
        for d in str(number):
            if d != digit:
                return False
        return True

    def createIntegerRegex(self, frmt, minV, maxV):
        if minV != None and not (isinstance(minV, int) or isinstance(minV, long)):
            raise ValueError("Bad input")
        if maxV != None and not (isinstance(maxV, int) or isinstance(maxV, long)):
            raise ValueError("Bad input")

        if minV is not None:
            if str(minV) != str(int(minV)):
                raise ValueError("Bad input")
        if maxV is not None:
            if str(maxV) != str(int(maxV)):
                raise ValueError("Bad input")

        if (frmt is None) or (not isinstance(frmt, str)) or (frmt not in ["%d", "%0d"]) and not re.match("^%0[0-9]+d$", frmt):
            raise ValueError("Bad format")

        if (minV is not None) and (maxV is not None) and (minV>maxV):
            raise ValueError("Invalid parameters (minV>maxV)")

        if minV >= 0 and (maxV >= 0 or maxV is None):
            self.createNNIntegerRegex(frmt, minV, maxV)
            return "^({0})$".format(self.__buildRegEx())

        m = re.match('%0([0-9]+)d', frmt)
        if m:
            self.zeros = int(m.group(1))
        self.alternatives = [[]]
        self.currentIndex = 0
        self.base = "{0}"

        #%0Xd
        if self.zeros != 0 and minV is not None and maxV is None:
            maxV = int(self.zeros * "9")

        if self.zeros != 0 and minV is None and maxV is None:
            maxV = int(self.zeros * "9")

        #%d
        if frmt == "%d":
            self.base = "0*({0})"

        #%0d
        if minV is None and maxV is None:
            if frmt == "%d":
                self.__addElement("-?([0-9]+)")
            if frmt == "%0d":
                self.__addElement("-?([1-9][0-9]*|0)")
            return "^({0})$".format(self.__buildRegEx())

        if minV is None and maxV is not None:
            if maxV < 0:
                minV = -maxV
                maxV = None
                self.setBase = False
                self.createNNIntegerRegex(frmt, minV, maxV)
                return "^(-({0}))$".format(self.__buildRegEx())
            else:
                minV = 0
                self.__calculateRegex(minV, maxV)
                result = "-?({0})".format(self.__buildRegEx())
                minV = maxV + 1
                maxV = None
                self.createNNIntegerRegex(frmt, minV, maxV)
                result += "|-({0})".format(self.__buildRegEx())
                return "^({0})$".format(result)

        if minV is not None and maxV is None:
            maxV = -minV
            minV = 0
            self.__calculateRegex(minV, maxV)
            result = "-?({0})".format(self.__buildRegEx())
            minV = maxV + 1
            maxV = None
            self.createNNIntegerRegex(frmt, minV, maxV)
            result += "|{0}".format(self.__buildRegEx())
            return "^({0})$".format(result)

        if minV is not None and maxV is not None:
            if minV <= 0 and maxV <= 0:
                tempMinV = minV
                minV = -maxV
                maxV = -tempMinV
                self.__calculateRegex(minV, maxV)
                return "^-({0})$".format(self.__buildRegEx())
            else: #n-, n+
                if -minV < maxV:
                    mxV = maxV
                    maxV = -minV
                    minV = 0
                    self.__calculateRegex(minV, maxV)
                    result = "-?({0})".format(self.__buildRegEx())
                    minV = maxV + 1
                    maxV = mxV
                    self.__calculateRegex(minV, maxV)
                    result += "|{0}".format(self.__buildRegEx())
                    return "^({0})$".format(result)
                else:
                    mnV = minV
                    minV = 0
                    self.__calculateRegex(minV, maxV)
                    result = "-?({0})".format(self.__buildRegEx())
                    minV = maxV + 1
                    maxV = -mnV
                    if minV <= maxV:
                        self.__calculateRegex(minV, maxV)
                        result += "|-({0})".format(self.__buildRegEx())
                    return "^({0})$".format(result)

    def __executeIntegerCalculation(self, frmt, minV, maxV):
        b = RegexBuilder()
        minV = None if minV is None else int(minV)
        maxV = None if maxV is None else int(maxV)
        return b.createIntegerRegex(frmt, minV, maxV).replace("^", "").replace("$", "")

    def createRealRegex(self, frmt, minV, maxV):
        if minV != None and not isinstance(minV, float):
            raise ValueError("Bad input")
        if maxV != None and not isinstance(maxV, float):
            raise ValueError("Bad input")

        try:
            if minV is not None:
                float(minV)
            if maxV is not None:
                float(maxV)
        except:
            raise ValueError("Bad input: " + str(minV))

        if (minV is not None) and (maxV is not None) and (minV>maxV):
            raise ValueError("Invalid parameters (min>max)")
        if (frmt is None) or (not isinstance(frmt, str)) or frmt not in ["%lf", "%0lf"] and not re.match("^%\.[0-9]+lf$", frmt) and not re.match("^%0\.[0-9]+lf$", frmt) and not re.match("^%0[1-9][0-9]*\.[0-9]+lf$", frmt) and not re.match("^%[1-9][0-9]*\.[0-9]+lf$", frmt):
            raise ValueError("Bad format")
        if (minV is not None and re.match("^-?[0-9]+\.[0-9]+$", str(minV)) is None) or (maxV is not None and re.match("^-?[0-9]+\.[0-9]+$", str(maxV)) is None):
            raise ValueError("Invalid parameters - real expected")

        self.alternatives = [[]]
        self.currentIndex = 0
        self.base = "{0}"
        zeros = ""
        digitsReal = None
        digitsInt = None

        if frmt == "%lf":
            self.base = "0*({0})"
            zeros = "0*"

        #%0.Ylf zera wiodace niedozwolone
        m = re.match('%0\.([0-9]+)lf', frmt)
        if m:
            digitsReal = int(m.group(1))

        #%X.Ylf'
        m = re.match('%([1-9][0-9]*)\.([0-9]+)lf', frmt)
        if m:
            self.base = "{0}"
            zeros = "0*"
            digitsReal = int(m.group(2))

        #%.Ylf zera wiodace dozwolone
        m = re.match('%\.([0-9]+)lf', frmt)
        if m:
            self.base = "{0}"
            zeros = "0*"
            digitsReal = int(m.group(1))

        #%0X.Ylf
        m = re.match('%0([0-9]+)\.([0-9]+)lf', frmt)
        if m:
            digitsAll = int(m.group(1))
            digitsReal = int(m.group(2))

            if digitsAll > digitsReal:
                digitsAll = digitsReal - digitsAll - 1
            return self.__createRealRegexFor0XY(frmt, minV, maxV)

        if digitsReal != None:
            if (minV != None and len(str(minV).split(".")[1]) > digitsReal) or (maxV != None and len(str(maxV).split(".")[1]) > digitsReal) or digitsReal == 0:
                raise ValueError("Bad input")

        if digitsReal is None:
            endingReal = "[0-9]+"
        else:
            endingReal = "[0-9]{" + str(digitsReal) + "}" if digitsReal > 1 else "[0-9]"

        if digitsInt != None and minV is not None and maxV is None:
            maxV = int(digitsAll * "9")

        if digitsInt != None and minV is None and maxV is None:
            maxV = int(digitsAll * "9")

        #%0d
        if minV is None and maxV is None:
            if frmt == "%lf":
                ans = "-?" + zeros + "([0-9]+|0)\.[0-9]+"
            if frmt == "%0lf":
                ans = "-?" + zeros + "([1-9][0-9]*|0)\.[0-9]+"
            if digitsReal != None:
                ans = "-?{0}([1-9][0-9]*|0)(\.{1})".format(zeros, endingReal)

            return "^({0})$".format(ans)

        if minV is None and maxV is not None:
            if maxV < 0:
                minV = -maxV
                splitted = str(minV).split(".")
                maxV = "{0}.{1}".format("1" + len(splitted[0])*"0", len(splitted[1])*"0")# if digitsReal == None else digitsReal*"9")

                ans = self.__calculateRealRegex(minV, maxV, digitsReal)
                minV = int(maxV.split(".")[0])
                ans2 = self.__executeIntegerCalculation("%0d", minV, None)
                if digitsReal is None:
                    return r"^-({0}({1})|{0}({2})\.{3})$".format(zeros, ans, ans2, endingReal)
                    #return "^(-({0}({1}))|{0}({2})(\.{3})?)$".format(zeros, ans, ans2, endingReal)
                else:
                    return r"^-({0}({1})|{0}({2})\.{3})$".format(zeros, ans, ans2.replace("?", ""), endingReal)
            else:
                if digitsReal is None:
                    result = "-(" + zeros + "([1-9][0-9]*|0)(\." + endingReal + ")?)"
                    minV = 0
                    ans = self.__calculateRealRegex(minV, maxV, digitsReal)
                    result += "|-?(" + zeros + "({0}))".format(ans)
                else:
                    result = "-(" + zeros + "([1-9][0-9]*|0)(\." + endingReal + "))"
                    minV = 0
                    ans = self.__calculateRealRegex(minV, maxV, digitsReal)
                    result += "|-?(" + zeros + "({0}))".format(ans.replace("?", ""))
                return "^({0})$".format(result)

        if minV is not None and maxV is None:
            if minV <0:
                result = "-{0}({1})".format(zeros, self.__calculateRealRegex(0, -minV, digitsReal))
                ans = self.__executeIntegerCalculation("%0d", 0, None)
                result += "|{0}({1})\.{2}".format(zeros, ans, endingReal)
                if digitsReal is None:
                    return "^({0})$".format(result)
                else:
                    return "^({0})$".format(result).replace("?", "")
            else:
                ans = "{0}".format(self.__calculateRealRegex(minV, minV+1, digitsReal))
                ans2 = "{0}\.({1})".format(self.__executeIntegerCalculation("%0d", int(math.floor(minV + 1)), None), endingReal)
                if digitsReal is None:
                    return "^({0}({1}|{2}))$".format(zeros, ans, ans2)
                else:
                    return "^({0}({1}|{2}))$".format(zeros, ans, ans2).replace("?", "")

        if minV is not None and maxV is not None:
            if minV < 0 and maxV < 0:
                tempMinV = minV
                minV = -maxV
                maxV = -tempMinV
                if digitsReal is None:
                    return "^-({0}({1}))$".format(zeros, self.__calculateRealRegex(minV, maxV, digitsReal))
                else:
                    return "^-({0}({1}))$".format(zeros, self.__calculateRealRegex(minV, maxV, digitsReal)).replace("?", "")
            else:
                if minV <= 0 and maxV >= 0:
                    if math.fabs(minV) < maxV:
                        if digitsReal is None:
                            result = "-?({0}({1}))".format(zeros,self.__calculateRealRegex(0, -minV, digitsReal))
                            result += "|{0}({1})".format(zeros,self.__calculateRealRegex(-minV, maxV, digitsReal))
                        else:
                            result = "-?({0}({1}))".format(zeros,self.__calculateRealRegex(0, -minV, digitsReal).replace("?", ""))
                            result += "|{0}({1})".format(zeros,self.__calculateRealRegex(-minV, maxV, digitsReal).replace("?", ""))
                        return "^({0})$".format(result)
                    else:
                        if digitsReal is None:
                            result = "-?({0}({1}))".format(zeros,self.__calculateRealRegex(0, maxV, digitsReal))
                            result += "|-{0}({1})".format(zeros,self.__calculateRealRegex(maxV, -minV, digitsReal))
                        else:
                            result = "-?({0}({1}))".format(zeros,self.__calculateRealRegex(0, maxV, digitsReal).replace("?", ""))
                            result += "|-{0}({1})".format(zeros,self.__calculateRealRegex(maxV, -minV, digitsReal).replace("?", ""))

                        return "^({0})$".format(result)

                else:
                    if digitsReal is None:
                        return "^({0}({1}))$".format(zeros, self.__calculateRealRegex(minV, maxV, digitsReal))
                    else:
                        return "^({0}({1}))$".format(zeros, self.__calculateRealRegex(minV, maxV, digitsReal)).replace("?", "")

    def __createRealRegexFor0XY(self, frmt, minV, maxV):
        m = re.match('%0([0-9]+)\.([0-9]+)lf', frmt)
        if m:
            digitsAll = int(m.group(1))
            digitsReal = int(m.group(2))

        self.alternatives = [[]]
        self.currentIndex = 0
        self.base = "{0}"
        zeros = ""
        endingReal = "[0-9]{" + str(digitsReal) + "}" if digitsReal > 1 else "[0-9]"

        digitsInt = digitsAll - digitsReal - 1

        formatInt = "%0" + str(digitsInt) + "d"
        if minV is None and maxV is None:
            ans = self.createIntegerRegex(formatInt, None, None).replace("^", "").replace("$", "")
            return "^(({0})[0-9]*\.{1})$".format(ans, endingReal)

        if minV is not None and maxV is None:
            if minV <0:
                result = "-{0}({1})".format(zeros, self.__calculateRealRegex(0, -minV, digitsReal, formatInt))
                ans = self.__executeIntegerCalculation(formatInt, 0, None)
                result += "|{0}({1})[0-9]*\.{2}".format(zeros, ans, endingReal)
                return "^({0})$".format(result).replace("?", "")
            else:
                ans = "{0}".format(self.__calculateRealRegex(minV, minV+1, digitsReal, formatInt))
                ans = re.sub("\\\.", "[0-9]*\.", ans)
                if digitsInt < len(str(int(math.floor(minV + 1)))):
                    formatInt = "%0" + str(len(str(int(math.floor(minV + 1))))) + "d"
                ans2 = "{0}\.({1})".format(self.__executeIntegerCalculation(formatInt, int(math.floor(minV + 1)), None), endingReal)
                ans2 = re.sub("\\\.", "[0-9]*\.", ans2)
                ans3 = "{0}\.({1})".format(self.__executeIntegerCalculation("%0d", int("1" + "0"*len(str(int(math.floor(minV + 1))))), None), endingReal)
                ans3 = re.sub("\\\.", "[0-9]*\.", ans3)
                return "^({0}({1}|{2}|{3}))$".format(zeros, ans, ans2, ans3).replace("?", "")

        if minV is None and maxV is not None:
            if maxV < 0:
                minV = -maxV
                maxV = minV + 1
                ans = self.__calculateRealRegex(minV, maxV, digitsReal, formatInt)
                ans = re.sub("\\\.", "[0-9]*\.", ans)
                if digitsInt == 1:
                    ans2 = self.__executeIntegerCalculation("%0d", int(math.floor(maxV)), None)
                else:
                    ans2 = self.__executeIntegerCalculation(formatInt, int(math.floor(maxV)), None)
                if digitsReal is None:
                    return r"^-({0}|({1})[0-9]*\.{2})$".format(ans, ans2, endingReal)
                else:
                    return r"^-({0}|({1})[0-9]*\.{2})$".format(ans, ans2.replace("?", ""), endingReal)
            else:
                if digitsReal is None:
                    ans = self.__executeIntegerCalculation(formatInt, None, 0)
                    result = "("+ ans +")[0-9]*\." + endingReal
                    minV = 0
                    ans2 = self.__calculateRealRegex(minV, maxV, digitsReal, formatInt)
                    result += "|-?({0})".format(ans2)
                else:
                    ans = self.__executeIntegerCalculation(formatInt, None, 0)
                    result = "("+ ans +")[0-9]*\." + endingReal
                    minV = 0
                    ans2 = self.__calculateRealRegex(minV, maxV, digitsReal, formatInt)
                    result += "|-?({0})".format(ans2.replace("?", ""))
                return "^({0})$".format(result)

        if minV is not None and maxV is not None:
            if minV < 0 and maxV < 0:
                tempMinV = minV
                minV = -maxV
                maxV = -tempMinV
                if digitsReal is None:
                    return "^-({0}({1}))$".format(zeros, self.__calculateRealRegex(minV, maxV, digitsReal, formatInt))
                else:
                    return "^-({0}({1}))$".format(zeros, self.__calculateRealRegex(minV, maxV, digitsReal, formatInt)).replace("?", "")
            else:
                if minV <= 0 and maxV >= 0:
                    if math.fabs(minV) < maxV:
                        if digitsReal is None:
                            result = "-?({0}({1}))".format(zeros,self.__calculateRealRegex(0, -minV, digitsReal, formatInt))
                            result += "|{0}({1})".format(zeros,self.__calculateRealRegex(-minV, maxV, digitsReal, formatInt))
                        else:
                            result = "-?({0}({1}))".format(zeros,self.__calculateRealRegex(0, -minV, digitsReal, formatInt).replace("?", ""))
                            result += "|{0}({1})".format(zeros,self.__calculateRealRegex(-minV, maxV, digitsReal, formatInt).replace("?", ""))
                        return "^({0})$".format(result)
                    else:
                        if digitsReal is None:
                            result = "-?({0}({1}))".format(zeros,self.__calculateRealRegex(0, maxV, digitsReal, formatInt))
                            result += "|-{0}({1})".format(zeros,self.__calculateRealRegex(maxV, -minV, digitsReal, formatInt))
                        else:
                            result = "-?({0}({1}))".format(zeros,self.__calculateRealRegex(0, maxV, digitsReal, formatInt).replace("?", ""))
                            result += "|-{0}({1})".format(zeros,self.__calculateRealRegex(maxV, -minV, digitsReal, formatInt).replace("?", ""))

                        return "^({0})$".format(result)
                else:
                    if digitsReal is None:
                        return "^({0}({1}))$".format(zeros, self.__calculateRealRegex(minV, maxV, digitsReal, formatInt))
                    else:
                        return "^({0}({1}))$".format(zeros, self.__calculateRealRegex(minV, maxV, digitsReal, formatInt)).replace("?", "")

    def createNNIntegerRegex(self, frmt, minV, maxV):
        if minV != None and not (isinstance(minV, int) or isinstance(minV, long)):
            raise ValueError("Bad input")
        if maxV != None and not (isinstance(maxV, int) or isinstance(maxV, long)):
            raise ValueError("Bad input")

        if minV is not None:
            if str(minV) != str(int(minV)):
                raise ValueError("Bad input")
        if maxV is not None:
            if str(maxV) != str(int(maxV)):
                raise ValueError("Bad input")

        if (frmt is None) or (not isinstance(frmt, str)) or (frmt not in ["%d", "%0d"]) and not re.match("^%0[0-9]+d$", frmt):
            raise ValueError("Bad format")

        if (minV is not None) and (maxV is not None) and (minV>maxV):
            raise ValueError("Invalid parameters (minV>maxV)")
        if (minV is not None) and (minV < 0):
            raise ValueError("Invalid parameters (minV<0)")

        m = re.match('%0([0-9]+)d', frmt)
        if m:
            self.zeros = int(m.group(1))
        self.alternatives = [[]]
        self.currentIndex = 0
        self.format = frmt
        self.__setNNRegExpBase()

        #%d
        if frmt == "%d" and minV is None and maxV is not None:
            self.__addElement("0*")
            frmt = "%0d"

        if frmt == "%d" and minV is None and maxV is None:
            self.__addElement("[0-9]+")

        if frmt == "%d" and minV is not None and maxV is None:
            frmt = "%0d"

        if frmt == "%d" and minV is not None and maxV is not None:
            frmt = "%0d"

        #%0d
        if frmt == "%0d" and minV is None and maxV is None:
            if self.zeros == 0:
                self.__addElement("[1-9][0-9]*|0")
            else:
                multiple = "" if self.zeros == 1 else "{{{0}}}".format(str(self.zeros))
                self.__addElement("[0-9]{0}".format(multiple))
                self.zeros = 0

        if frmt == "%0d" and minV is not None and maxV is None:
            l = len(str(minV))
            ma = l * "9"
            self.__calculateRegex(minV, ma)
            self.__addRange(1, 9)
            self.__addElement("[0-9]{{{0}}}[0-9]*".format(str(l)))

        if frmt == "%0d" and minV is None and maxV is not None:
            minV = 0
            self.__calculateRegex(minV, maxV)

        if frmt == "%0d" and minV is not None and maxV is not None:
            self.__calculateRegex(minV, maxV)

        #%0Xd
        if self.zeros != 0 and minV is not None and maxV is None:
            maxV = self.zeros * "9"
            self.__calculateRegex(minV, maxV)

        if self.zeros != 0 and minV is None and maxV is None:
            minV = 0
            maxV = self.zeros * "9"
            self.__calculateRegex(minV, maxV)

        if self.zeros != 0 and minV is None and maxV is not None:
            minV = 0
            self.__calculateRegex(minV, maxV)

        if self.zeros != 0 and minV is not None and maxV is not None:
            self.__calculateRegex(minV, maxV)

        return "^({0})$".format(self.__buildRegEx())

    def __calculateRealRegex(self, mi, ma, digits, formatInt = "%0d"):
        if mi == 0.0:
            mi = 0.0
        if ma == 0.0:
            ma = 0.0
        groupMin = str(mi).split(".")
        groupMax = str(ma).split(".")

        if(len(groupMin) > 1):
            miIntPart = str(mi).split(".")[0]
            min = str(mi).split(".")[1]
        else:
            miIntPart = str(mi)
            min = "0"

        if(len(groupMax) > 1):
            maIntPart = str(ma).split(".")[0]
            max = str(ma).split(".")[1]
        else:
            maIntPart = str(ma)
            max = "0"

        maxBefore = max
        minBefore = min

        while len(min) < len(str(max)) or len(min) < digits:
            min = min + "0"
        while len(str(min)) > len(max) or len(max) < digits:
            max = max + "0"

        if digits is None:
            format =  "%0" + str(len(max))+ "d"
        else:
            format =  "%0" + str(digits)+ "d"

        remove = digits is None

        if miIntPart == maIntPart:
            if min == max:
                return "{0}\.{1}".format(self.__executeIntegerCalculation(formatInt, miIntPart, miIntPart), min)
            if digits is None:
                x = self.__generateAlternativesForReal(format, int(min), int(max) - 1, remove)
            else:
                x = self.__executeIntegerCalculation(format, int(min), int(max) - 1)
            if digits is None:
                #x = re.sub("\[0\-9\](?!\*)", "",x)
                return "{0}\.({1}|{2}0*)".format(self.__executeIntegerCalculation(formatInt, miIntPart, miIntPart), x, maxBefore)
            else:
                return "{0}\.({1}|{2})".format(self.__executeIntegerCalculation(formatInt, miIntPart, miIntPart), x, max)
        else:
            if digits is None:
                x =  self.__generateAlternativesForReal(format, int(min), "9"*len(min), remove)
            else:
                x = self.__executeIntegerCalculation(format, int(min), "9"*len(min))
            if int(max) != 0:
                if digits is None:
                    y = self.__generateAlternativesForReal(format, 0, int(max) - 1, remove)
                else:
                    y = self.__executeIntegerCalculation(format, 0, int(max) - 1)
            else:
                y = None

            if int(miIntPart) + 1 < int(maIntPart)-1:
                z = self.__executeIntegerCalculation(formatInt, int(miIntPart) + 1, int(maIntPart)-1)
            else:
                z = str(int(miIntPart) + 1)

            if digits is None:
                ans = "{0}\.{1}".format(self.__executeIntegerCalculation(formatInt, miIntPart, miIntPart), minBefore)
                ans += "|{0}(\.{1})".format(self.__executeIntegerCalculation(formatInt, miIntPart, miIntPart), x)
                if int(miIntPart) + 1 <= int(maIntPart)-1:
                    ans += "|{0}\.[0-9]+".format(z)
                if y != None:
                    ans += "|{0}(\.{1})".format(self.__executeIntegerCalculation(formatInt, maIntPart, maIntPart), y)
                ans += "|{0}\.{1}0*".format(self.__executeIntegerCalculation(formatInt, maIntPart, maIntPart), maxBefore)
            else:
                ans = "{0}\.({1})".format(self.__executeIntegerCalculation(formatInt, miIntPart, miIntPart), x)
                if int(miIntPart) + 1 <= int(maIntPart)-1:
                    ans += "|{0}\.[0-9]{{{1}}}".format(z, digits)
                if y != None:
                    ans += "|{0}\.({1})".format(self.__executeIntegerCalculation(formatInt, maIntPart, maIntPart), y)
                ans += "|{0}\.{1}".format(self.__executeIntegerCalculation(formatInt, maIntPart, maIntPart), max)

            return ans

    def __generateAlternativesForReal(self, format, min, max, remove):
        result = ["(",]
        if str(min) == str(max):
            result.append(str(max))

        m = re.match('%0([0-9]+)d', format)
        if m:
            digits = int(m.group(1))

        sub = len(str(max))
        if sub < digits:
            count = digits - sub
            while count != 0:
                result.append(count * "0" + "|")
                count -= 1

        temp = "0"*(digits - len(str(min))) + str(min)
        while temp[-1] == "0":
            temp = temp[:-1]
            if len(temp) == 0:
                break

        if len(temp) != 0:
            result.append(temp + "|")

        for i in xrange(len(str(max))):
            newMin = str(int(str("0"* (digits - len(str(min))) + str(min))[0:i + 1]) + 1)
            newMax = str(max)[0:i + 1]
            x = digits - (sub - 1 - i)
            if int(newMin) <= int(newMax):
                if i != len(str(max)) - 1:
                    a = self.__executeIntegerCalculation("%0" + str(x) + "d", int(newMin), int(newMax))
                    result.append(a + "|")
                else:
                    a = self.__executeIntegerCalculation("%0" + str(digits) + "d", int(str(min)[0:i + 1]), int(newMax))
                    result.append(a)

        result.append("[0-9]*)")
        return "".join(result)

    def __buildPartRegEx(self):
        result = []
        for alternative in self.alternatives:
            if alternative != []:
                m = re.match("^.+-+.+$", str(alternative))
                if len(alternative) == 1 and m is None:
                    result.append("0" * (self.zeros - len(str(alternative[0]))))
                else:
                    result.append("0" * (self.zeros - len(alternative)))
                for element in alternative:
                    result.append(element)
                result.append("|")
        result = "".join(result)
        return result[:-1]

    def __calculateRegex(self, mi, ma):
        if mi == ma:
            self.__addElement(mi)
            return

        minl = len(str(mi))
        maxl = len(str(ma))
        minV = []
        maxV = []

        for i in str(mi):
            minV.append(int(i))
        for i in str(ma):
            maxV.append(int(i))

        ranges = []
        frm = mi
        for i in xrange(minl, maxl + 1):
            to = 10**i - 1
            ranges.append((frm, to if to < int(ma) else ma))
            frm = to + 1

        resultRanges = []
        for p in ranges:
            l = len(str(p[0]))

            minV = []
            maxV = []
            for i in str(str(p[0])):
                minV.append(int(i))
            for i in str(str(p[1])):
                maxV.append(int(i))

            if self.__sameDigit("9", p[1]):
                lastIndex = l - 1
                left = str(p[0])

                while lastIndex >= 0:
                    trailing = l - lastIndex - 1                        #how many digits after current one
                    nextNines = left[0:lastIndex][::-1]                 #reversed digits before current one
                    i = 0
                    while i < len(nextNines) and nextNines[i] == '9':
                        i += 1
                    right = left[0:lastIndex] + '9' + '9'*trailing
                    resultRanges.append((left, right))
                    left = str(int(right) + 1)
                    lastIndex -= (1 + i)
            else:
                lastIndex = l - 1
                left = str(p[0])

                while lastIndex >= 0 and left[0] != str(ma)[0]:
                    if lastIndex == 0:
                        right = str(int(str(ma)[0])-1) + '9'*(l-1)
                        resultRanges.append((left, right))
                    else:
                        trailing = l - lastIndex - 1
                        nextNines = left[0:lastIndex][::-1]
                        i = 0
                        while i < len(nextNines) and nextNines[i] == '9':
                            i += 1
                        right = left[0:lastIndex] + '9' + '9'*trailing
                        resultRanges.append((left, right))
                        lastIndex -= (1 + i)
                    left = str(int(right) + 1)

                maxRange = str(ma)
                sames = self.__getSames(left, ma)

                left = left[len(sames):]
                right = maxRange[len(sames):]
                newMa = right

                lastIndex = len(left) - 1
                if not self.__sameDigit("0", str(left)):
                    while lastIndex >= 0 and (left[0] != newMa[0] or len(left) != len(newMa)):
                        if lastIndex == 0:
                            right = str(int(newMa[0])-1) + '9'*(len(newMa)-1)
                            resultRanges.append((sames + left, sames + right))
                        else:
                            trailing = len(left) - lastIndex - 1
                            nextNines = left[0:lastIndex][::-1]
                            i = 0
                            while i < len(nextNines) and nextNines[i] == '9':
                                i += 1
                            right = left[0:lastIndex] + '9' + '9'*trailing
                            resultRanges.append((sames + left, sames + right))
                            lastIndex -= (1 + i)
                        left = str(int(right) + 1)
                        diff = len(right) - len(left)
                        left = diff*"0" + left


                right = str(ranges[-1][0])
                while right != newMa:
                    right = ""
                    index = 0
                    for i in str(left):
                        rng = []
                        rng.append(sames + str(left))
                        if str(left)[index] == newMa[index]:
                            right = right + str(left)[index]
                            index = index + 1
                            if right == newMa:
                                rng.append(sames + right)
                                resultRanges.append(rng)
                        else:
                            if index + 1 == len(str(left)):
                                nextDigit = int(newMa[-1])
                            else:
                                nextDigit = int(newMa[index]) - 1
                            right = right + str(nextDigit)
                            while len(right) != len(str(left)):
                                right = right + "9"
                            rng.append(sames + right)
                            resultRanges.append(rng)
                            left = int(right) + 1
                            index = 0
                            if right == newMa:
                                break
                            right = ""

        for p in resultRanges:
            for i in xrange(0, len(str(p[0]))):
                left = str(p[0])[i]
                right = str(p[1])[i]
                self.__addRange(left, right)
            self.__startNextAlternative()

        newNumber = ma
        if self.zeros != 0 and len(str(ma)) != self.zeros:
            newNumber = (self.zeros - len(str(ma)))* "0" + str(ma)
        xeas = self.__buildRegEx()
        m = re.match("^(" + xeas + ")$", str(newNumber))
        if m is None:
            self.__addRange(ma, ma)
            self.__startNextAlternative()

    def __getSames(self, a, b):
        aS = str(a)
        bS = str(b)
        sames = []
        for i in xrange(len(bS)):
            if bS[i] == aS[i]:
                sames.append(bS[i])
            else:
                break
        return "".join(sames)

    def createTimeRegex(self, frmt, minT, maxT):
        return "^{0}$".format(self.__calcTimeRegex(frmt, minT, maxT))

    def __calcTimeRegex(self, frmt, minT, maxT):
        if (frmt is None or not isinstance(frmt, str)):
            raise ValueError("Bad input")
        if (minT is not None and not isinstance(minT, str)):
            raise ValueError("Bad input")
        if (maxT is not None and not isinstance(maxT, str)):
            raise ValueError("Bad input")

        for t in ["%H", "%I", "%M", "%p", "%P", "%S"]:
            if frmt.count(t) > 1:
                raise ValueError("Bad input")

        H, I, M, p, P, S = False, False, False, False, False, False
        if "%H" in frmt:
            H = True
        if "%I" in frmt:
            I = True
        if "%M" in frmt:
            M = True
        if "%p" in frmt:
            p = True
        if "%P" in frmt:
            P = True
        if "%S" in frmt:
            S = True

        if H and I:
            raise ValueError("Wrong format")
        if p and P:
            raise ValueError("Wrong format")
        if I and not p and not P:
            raise ValueError("Wrong format")
        if (H or I) and S and not M:
            raise ValueError("Wrong format")
        if H and (p or P):
            raise ValueError("Wrong format")
        if not H and not I and not M and not S:
            raise ValueError("Wrong format")

        frmtRegExp = re.escape(frmt).replace("\%", "%")

        if H:
            frmtRegExp = frmtRegExp.replace("%H", "(?P<H>[01][0-9]|2[0-3])")
        if I:
            frmtRegExp = frmtRegExp.replace("%I", "(?P<I>0[0-9]|1[0-2])")
        if M:
            frmtRegExp = frmtRegExp.replace("%M", "(?P<M>[0-5][0-9])")
        if S:
            frmtRegExp = frmtRegExp.replace("%S", "(?P<S>[0-5][0-9])")
        if p:
            frmtRegExp = frmtRegExp.replace("%p", "(?P<p>am|pm)")
        if P:
            frmtRegExp = frmtRegExp.replace("%P", "(?P<P>AM|PM)")

        f = re.escape(frmt).replace("\%", "%")

        le = lambda g: self.__le(m1, m2, g)
        eq = lambda g: self.__eq(m1, m2, g)
        g1 = lambda g: m1.group(g) if g == "p" or g == "P" else int(m1.group(g))
        g2 = lambda g: m2.group(g) if g == "p" or g == "P" else int(m2.group(g))
        gz1 = lambda g: ("0" + m1.group(g))[-2:]
        gz2 = lambda g: ("0" + m2.group(g))[-2:]
        reg = lambda a, b: self.__executeIntegerCalculation("%02d", a, b) if a != 0 or b != 59 else "[0-5][0-9]"
        fill = lambda l: self.__fillTimeRegex(f, l)
        res = lambda l: "|".join(filter(None, l))

        P = p or P
        Pname = "p" if p else "P" if P else None
        PnamePrc = "%" + str(Pname)
        
        if minT is None:
            minT = frmt
            if H:
                minT = minT.replace("%H", "00")
            if I:
                minT = minT.replace("%I", "00")
                if p:
                    minT = minT.replace("%p", "am")
                else:
                    minT = minT.replace("%P", "AM")
            if M:
                minT = minT.replace("%M", "00")
            if S:
                minT = minT.replace("%S", "00")
            if p:
                minT = minT.replace("%S", "00")

        if maxT is None:
            maxT = frmt
            if H:
                maxT = maxT.replace("%H", "23")
            if I:
                maxT = maxT.replace("%I", "11")
                if p:
                    maxT = maxT.replace("%p", "pm")
                else:
                    maxT = maxT.replace("%P", "PM")
            if M:
                maxT = maxT.replace("%M", "59")
            if S:
                maxT = maxT.replace("%S", "59")

        m1 = re.match(frmtRegExp, minT)
        m2 = re.match(frmtRegExp, maxT)

        if (m1 is None or m2 is None):
            raise ValueError("Bad input")

        if H:
            if not le("H"):
                raise ValueError("Bad input")
            if eq("H") and not le("M"):
                raise ValueError("Bad input")
            if eq("H") and eq("M") and not le("S"):
                raise ValueError("Bad input")
        elif I:
            if P:
                if eq(Pname) and not le("I") and g1("I") != 12:
                    raise ValueError("Bad input")
                if not le(Pname):
                    raise ValueError("Bad input")
                if (g1(Pname).lower() == "am" and (g1("I") < 0 or g1("I") > 11)):
                    raise ValueError("Bad input")
                if (g1(Pname).lower() == "pm" and (g1("I") < 1 or g1("I") > 12)):
                    raise ValueError("Bad input")
                if (g2(Pname).lower() == "am" and (g2("I") < 0 or g2("I") > 11)):
                    raise ValueError("Bad input")
                if (g2(Pname).lower() == "pm" and (g2("I") < 1 or g2("I") > 12)):
                    raise ValueError("Bad input")
        else:
            if M and not le("M"):
                raise ValueError("Bad input")
            if M and S and eq("M") and not le("S"):
                raise ValueError("Bad input")
            if not M and S and not le("S"):
                raise ValueError("Bad input")

        if H:
            if eq("H"):
                if M:
                    if eq("M"):
                        if S:
                            rS = reg(g1("S"), g2("S"))
                            return fill([("%H", gz1("H")), ("%M", gz1("M")), ("%S", rS)])
                        else:
                            return fill([("%H", gz1("H")), ("%M", gz1("M"))])
                    else:
                        if S:
                            rS1 = reg(g1("S"), 59)
                            rS2 = reg(0, 59)
                            rS3 = reg(0, g2("S"))
                            rM = reg(g1("M") + 1, g2("M") - 1) if g1("M") + 1 < g2("M") else None
                            return res([
                                         fill([("%H", gz1("H")), ("%M", gz1("M")), ("%S", rS1)]),
                                         fill([("%H", gz1("H")), ("%M", rM),       ("%S", rS2)]),
                                         fill([("%H", gz1("H")), ("%M", gz2("M")), ("%S", rS3)])
                                         ])
                        else:
                            rM = reg(g1("M"), g2("M"))
                            return fill([("%H", gz1("H")), ("%M", rM)]) #fill rH same
                else:
                    return fill([("%H", gz1("H"))])
            else:
                if M:
                    if S:
                        rS1 = reg(g1("S"), 59)
                        rS2 = reg(0, 59)
                        rS3 = reg(0, g2("S"))
                        rM1 = reg(g1("M") + 1, 59)
                        rM2 = reg(0, 59)
                        rM3 = reg(0, g2("M") - 1)
                        rI2 = reg(g1("H") + 1, g2("H") - 1) if g1("H") + 1 < g2("H") else None
                        return res([
                                     fill([("%H", gz1("H")), ("%M", gz1("M")), ("%S", rS1)]),
                                     fill([("%H", gz1("H")), ("%M", rM1),      ("%S", rS2)]),
                                     fill([("%H", rI2),      ("%M", rM2),      ("%S", rS2)]),
                                     fill([("%H", gz2("H")), ("%M", rM3),      ("%S", rS2)]),
                                     fill([("%H", gz2("H")), ("%M", gz2("M")), ("%S", rS3)])
                                     ])
                    else:
                        rM1 = reg(g1("M"), 59)
                        rM2 = reg(0, 59)
                        rM3 = reg(0, g2("M"))
                        rI = reg(g1("H") + 1, g2("H") - 1) if g1("H") + 1 < g2("H") else None
                        return res([
                                     fill([("%H", gz1("H")), ("%M", rM1)]),
                                     fill([("%H", rI),       ("%M", rM2)]),
                                     fill([("%H", gz2("H")), ("%M", rM3)])
                                     ])
                else:
                    rH = reg(g1("H"), g2("H"))
                    return fill([("%H", rH)])
        elif I:
            if eq(Pname):
                if eq("I"):
                    if M:
                        if eq("M"):
                            if S:
                                rS = reg(g1("S"), g2("S"))
                                return fill([(PnamePrc, g1(Pname)), ("%I", gz1("I")), ("%M", gz1("M")), ("%S", rS)])
                            else:
                                return fill([(PnamePrc, g1(Pname)), ("%I", gz1("I")), ("%M", gz1("M"))])
                        else:
                            if S:
                                rS1 = reg(g1("S"), 59)
                                rS2 = reg(0, 59)
                                rS3 = reg(0, g2("S"))
                                rM = reg(g1("M") + 1, g2("M") - 1) if g1("M") + 1 < g2("M") else None
                                return res([
                                             fill([(PnamePrc, g1(Pname)), ("%I", gz1("I")), ("%M", gz1("M")), ("%S", rS1)]),
                                             fill([(PnamePrc, g1(Pname)), ("%I", gz1("I")), ("%M", rM),       ("%S", rS2)]),
                                             fill([(PnamePrc, g1(Pname)), ("%I", gz1("I")), ("%M", gz2("M")), ("%S", rS3)])
                                             ])
                            else:
                                rM1 = reg(g1("M"), 59)
                                rM2 = reg(0, 59)
                                rM3 = reg(0, g2("M"))
                                rI2 = reg(g1("I") + 1, g2("I") - 1) if g1("I") + 1 < g2("I") else None
                                return res([
                                             fill([(PnamePrc, g1(Pname)), ("%I", gz1("I")), ("%M", rM1)]),
                                             fill([(PnamePrc, g1(Pname)), ("%I", rI2),      ("%M", rM2)]),
                                             fill([(PnamePrc, g1(Pname)), ("%I", gz2("I")), ("%M", rM3)])
                                             ])
                    else:
                        return fill([(PnamePrc, g1(Pname)), ("%I", gz1("I"))])
                else:
                    if M:
                        if S:
                            rS1 = reg(g1("S"), 59)
                            rS2 = reg(0, 59)
                            rS3 = reg(0, g2("S"))
                            rM1 = reg(g1("M") + 1, 59)
                            rM2 = reg(0, 59)
                            rM3 = reg(0, g2("M") - 1)
                            if g1(Pname).lower() == "pm" and g1("I") == 12:
                                rI2 = reg(1, g2("I") - 1) if g2("I") != 1 else None
                            else:
                                rI2 = reg(g1("I") + 1, g2("I") - 1) if g1("I") + 1 < g2("I") else None
                            return res([
                                         fill([(PnamePrc, g1(Pname)),("%I", gz1("I")), ("%M", gz1("M")), ("%S", rS1)]),
                                         fill([(PnamePrc, g1(Pname)),("%I", gz1("I")), ("%M", rM1),      ("%S", rS2)]),
                                         fill([(PnamePrc, g1(Pname)),("%I", rI2),      ("%M", rM2),      ("%S", rS2)]),
                                         fill([(PnamePrc, g1(Pname)),("%I", gz2("I")), ("%M", rM3),      ("%S", rS2)]),
                                         fill([(PnamePrc, g1(Pname)),("%I", gz2("I")), ("%M", gz2("M")), ("%S", rS3)])
                                         ])
                        else:
                            rM1 = reg(g1("M"), 59)
                            rM2 = reg(0, 59)
                            rM3 = reg(0, g2("M"))
                            if g1(Pname).lower() == "pm" and g1("I") == 12:
                                rI2 = reg(1, g2("I") - 1) if g2("I") != 1 else None
                            else:
                                rI2 = reg(g1("I") + 1, g2("I") - 1) if g1("I") + 1 < g2("I") else None
                            
                                
                            return res([
                                         fill([(PnamePrc, g1(Pname)), ("%I", gz1("I")), ("%M", rM1)]),
                                         fill([(PnamePrc, g1(Pname)), ("%I", rI2),      ("%M", rM2)]),
                                         fill([(PnamePrc, g1(Pname)), ("%I", gz2("I")), ("%M", rM3)])
                                         ])
                    else:
                        return fill([(PnamePrc, g1(Pname)), ("%I", gz1("I"))])
            else:
                if M:
                    if S:
                        rS1 = reg(g1("S"), 59)
                        rS2 = reg(0, 59)
                        rS3 = reg(0, g2("S"))
                        rM1 = reg(g1("M"), 59)
                        rM2 = reg(0, 59)
                        rM3 = reg(0, g2("M") - 1)
                        rI0 = reg(g1("I") + 1, 11)
                        rI1 = "(" + reg(12, 12) + (("|" + reg(1, g2("I") - 1)) if g2("I") != 1 else "") + ")"
                        rI1 = rI1 if g2("I") != 12 else None

                        return res([
                                   fill([(PnamePrc, g1(Pname)), ("%I", gz1("I")), ("%M", gz1("M")), ("%S", rS1)]),
                                   fill([(PnamePrc, g1(Pname)), ("%I", gz1("I")), ("%M", rM1),      ("%S", rS2)]),
                                   fill([(PnamePrc, g1(Pname)), ("%I", rI0),      ("%M", rM2),      ("%S", rS2)]),
                                   fill([(PnamePrc, g2(Pname)), ("%I", rI1),      ("%M", rM2),      ("%S", rS2)]),
                                   fill([(PnamePrc, g2(Pname)), ("%I", gz2("I")), ("%M", rM3),      ("%S", rS2)]),
                                   fill([(PnamePrc, g2(Pname)), ("%I", gz2("I")), ("%M", gz2("M")), ("%S", rS3)])
                                   ])
                    else:
                        rM1 = reg(g1("M"), 59)
                        rM2 = reg(0, 59)
                        rM3 = reg(0, g2("M"))
                        rI0 = reg(g1("I") + 1, 11)
                        rI1 = "(" + reg(12, 12) + (("|" + reg(1, g2("I") - 1)) if g2("I") != 1 else "") + ")"
                        rI1 = rI1 if g2("I") != 12 else None
                        return res([
                                   fill([(PnamePrc, g1(Pname)), ("%I", gz1("I")), ("%M", rM1)]),
                                   fill([(PnamePrc, g1(Pname)), ("%I", rI0),      ("%M", rM2)]),
                                   fill([(PnamePrc, g2(Pname)), ("%I", rI1),      ("%M", rM2)]),
                                   fill([(PnamePrc, g2(Pname)), ("%I", gz2("I")), ("%M", rM3)])
                                   ])
                else:
                    rI1 = reg(g1("I"), 11)
                    rI2 = "(" + reg(12, 12) + (("|" + reg(1, g2("I") - 1)) if g2("I") != 1 else "") + ")"
                    rI2 = rI2 if g2("I") != 12 else None
                    return res([
                               fill([(PnamePrc, g1(Pname)), ("%I", rI1)]),
                               fill([(PnamePrc, g2(Pname)), ("%I", rI2)])
                               ])
        else:
            if M and S:
                if eq("M"):
                    rS = reg(g1("S"), g2("S"))
                    return fill([("%M", gz1("M")), ("%S", rS)])
                else:
                    rS1 = reg(g1("S"), 59)
                    rS2 = reg(0, 59)
                    rS3 = reg(0, g2("S"))
                    rM = reg(g1("M") + 1, g2("M") - 1) if g1("M") + 1 < g2("M") else None
                    return res([
                                fill([("%M", gz1("M")), ("%S", rS1)]),
                                fill([("%M", rM),       ("%S", rS2)]),
                                fill([("%M", gz2("M")), ("%S", rS3)])
                                ])
            if M:
                rM = reg(g1("M"), g2("M"))
                return fill([("%M", rM)])
            elif S:
                rS = reg(g1("S"), g2("S"))
                return fill([("%S", rS)])

    def __fillTimeRegex(self, frmt, l):
        for e in l:
            if e[1] is None:
                return None
            frmt = frmt.replace(e[0], str(e[1]))
        return frmt

    def __le(self, m1, m2, g):
        if g == "P" or g == "p":
            return m1.group(g).lower() == "am" or m2.group(g).lower() == "pm"

        if g == "I":
            if m1.group(g) == 12:
                return True
            elif m2.group(g) == 12:
                return m1.group(g) == 12

        return int(m1.group(g)) <= int(m2.group(g))

    def __eq(self, m1, m2, g):
        if g == "P" or g == "p":
            return m1.group(g) == m2.group(g)
        return int(m1.group(g)) == int(m2.group(g))
