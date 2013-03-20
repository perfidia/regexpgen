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

    def StartNextAlternative(self):
        if (len(self.alternatives[self.currentIndex]) == 0):
            return;
        self.alternatives.append([])
        self.currentIndex = self.currentIndex + 1

    def SetNNRegExpBase(self):
        if self.format == "%0d":
            self.base = "{0}"
        if self.format == "%d":
            self.base = "0*({0})"
        m = re.match('%0([0-9]+)d', self.format)
        if m:
            self.base = "{0}"

    def SetRegExpBase(self):
        if self.format == "%0d":
            self.base = "^({0})$"
        if self.format == "%d":
            self.base = "^(0*({0}))$"
        m = re.match("%0([0-9]+)d", self.format)
        if m:
            self.base = "^({0})$"

    def BuildRegEx(self):
        result = ""
        for alternative in self.alternatives:
            if alternative != []:
                m = re.match("^.+-+.+$", str(alternative))
                if len(alternative) == 1 and m == None:
                    result += "0" * (self.zeros - len(str(alternative[0])))
                #    result += "0" * (self.zeros - len(alternative))
                else:
                    result += "0" * (self.zeros - len(alternative))
                for element in alternative:
                    result += element
                result += "|"
        return self.base.format(result[:-1]);

    def AddRange(self, mi, ma):
        if mi == ma:
            r = str(mi)
        else:
            r = "[{0}-{1}]".format(str(mi), str(ma))
        self.alternatives[self.currentIndex].append(r)

    def AddElement(self, element):
        self.alternatives[self.currentIndex].append(str(element))

    def sameDigit(self, digit, number):
        for d in str(number):
            if d != digit:
                return False
        return True

    def CreateIntegerRegex(self, frmt, minV, maxV):
        if minV >= 0 and (maxV >= 0 or maxV is None):
            self.CreateNNIntegerRegex(frmt, minV, maxV)
            return "^({0})$".format(self.BuildRegEx())
        m = re.match('%0([0-9]+)d', frmt)
        if (m):
            self.zeros = int(m.group(1))
        self.alternatives = [[]]
        self.currentIndex = 0;
        self.base = "{0}"

        #%0Xd
        if self.zeros != 0 and minV is not None and maxV is None:
            maxV = int(self.zeros * "9")
            #self.calculateRegex(minV, maxV)

        if self.zeros != 0 and minV is None and maxV is None:
#            minV = 0
            maxV = int(self.zeros * "9")
#            self.calculateRegex(minV, maxV)

#        if self.zeros != 0 and minV is None and maxV is not None:
#            minV = 0
#            self.calculateRegex(minV, maxV)

#        if self.zeros != 0 and minV is not None and maxV is not None:
#            self.calculateRegex(minV, maxV)

        #%d
        if frmt == "%d":
            self.base = "0*({0})"

        #%0d
        if minV is None and maxV is None:
            if frmt == "%d":
                self.AddElement("-?([0-9]+)")
            if frmt == "%0d":
                self.AddElement("-?([1-9][0-9]*|0)")
            return "^({0})$".format(self.BuildRegEx())

        if minV is None and maxV is not None:
            if maxV < 0:
                minV = -maxV
                maxV = None
                self.setBase = False
                self.CreateNNIntegerRegex(frmt, minV, maxV)
                return "^(-({0}))$".format(self.BuildRegEx())
            else:
                minV = 0
                self.calculateRegex(minV, maxV)
                result = "-?({0})".format(self.BuildRegEx())
                minV = maxV + 1
                maxV = None
                self.CreateNNIntegerRegex(frmt, minV, maxV)
                result += "|-({0})".format(self.BuildRegEx())
                return "^({0})$".format(result)

        if minV is not None and maxV is None:
            maxV = -minV
            minV = 0
            self.calculateRegex(minV, maxV)
            result = "-?({0})".format(self.BuildRegEx())
            minV = maxV + 1
            maxV = None
            self.CreateNNIntegerRegex(frmt, minV, maxV)
            result += "|{0}".format(self.BuildRegEx())
            return "^({0})$".format(result)

        if minV is not None and maxV is not None:
            if minV <= 0 and maxV <= 0:
                tempMinV = minV
                minV = -maxV
                maxV = -tempMinV
                self.calculateRegex(minV, maxV)
                return "^-({0})$".format(self.BuildRegEx())
            else: #n-, n+
                if (-minV < maxV):
                    mxV = maxV
                    maxV = -minV
                    minV = 0
                    self.calculateRegex(minV, maxV)
                    result = "-?({0})".format(self.BuildRegEx())
                    minV = maxV + 1
                    maxV = mxV
                    self.calculateRegex(minV, maxV)
                    result += "|{0}".format(self.BuildRegEx())
                    return "^({0})$".format(result)
                else:
                    mnV = minV
                    minV = 0
                    self.calculateRegex(minV, maxV)
                    result = "-?({0})".format(self.BuildRegEx())
                    minV = maxV + 1
                    maxV = -mnV
                    if minV <= maxV:
                        self.calculateRegex(minV, maxV)
                        result += "|-({0})".format(self.BuildRegEx())
                    return "^({0})$".format(result)


#UWAGA
#calcRealRegex wydaje sie dzialac dobrze, ale to ponizej nie, nie mam juz dzisiaj sily, ale to co warto na pewno zrobic to zrobic jakas metode
#ktora bedzie tworzyla nowy obiekt buildera i wywolywala CreateRegexy, bo kazde wywolanie "zanieczyszcza" nam stan tego obiektu (inny base, alternatvies itd.
#poza tym trzeba przesledzic kazda sciezke (najlepiej rozpisac to) i bo tak jak wczesniej mielismy taka "metode proxy" (createNNinteger) to teraz nie mamy
#wiec jak chcemy dac np min=5, a max=None to trzeba recznie zrobic od 5 do 9 a potem do tego dopisac [1-9][0-9]+
#oprocz tego te uwagi ktore mielismy, czyli nazwy metod, zbedne pliki powywalac itd

    def executeIntegerCalculation(self, frmt, minV, maxV):
        b = RegexBuilder()
        return b.CreateIntegerRegex(frmt, minV, maxV).replace("^", "").replace("$", "")

    def CreateRealRegex(self, frmt, minV, maxV):
        self.alternatives = [[]]
        self.currentIndex = 0
        self.base = "{0}"
        zeros = ""
        if frmt == "%lf":
            self.base = "0*({0})"
            zeros = "0*"

        #%0d
        if minV is None and maxV is None:
            if frmt == "%lf":
                self.AddElement("-?([0-9]+(\.[0-9]+|0)?)")
            if frmt == "%0lf":
                self.AddElement("-?(([1-9][0-9]*|0)(\.[0-9]+)?)")
            return "^({0})$".format(self.BuildRegEx())

        if minV is None and maxV is not None:
            if maxV < 0:
                minV = -maxV
                splitted = str(minV).split(".")
                if len(splitted) > 1:
                    maxV = "{0}.{1}".format(len(splitted[0])*"9", len(splitted[1])*"9")
                else:
                    maxV = "9"*len(str(minV))
                ans = self.calculateRealRegex(minV, maxV)
                minV = int(maxV.split(".")[0]) + 1
                ans2 = self.executeIntegerCalculation("%0d", minV, None)
                return "^(-({0}({1})|{0}({2})\.[0-9]*))$".format(zeros, ans, ans2)
            else:
                result = "-(" + zeros + "([1-9][0-9]*|0)(\.[0-9]+)?|0)"
                minV = 0
                ans = self.calculateRealRegex(minV, maxV)
                result += "|-?(" + zeros + "({0}))".format(ans)
                return "^({0})$".format(result)

        if minV is not None and maxV is None:
            if minV <=0:
                result = "-{0}({1})".format(zeros, self.calculateRealRegex(0, -minV))
                ans = self.executeIntegerCalculation("%0d", 0, None)
                result += "|{0}({1})\.[0-9]+".format(zeros, ans)
                return "^({0})$".format(result)
            else:
                ans = "{0}".format(self.calculateRealRegex(minV, minV+1))
                ans2 = "{0}\.([0-9]+)".format(self.executeIntegerCalculation("%0d", int(math.floor(minV + 1)), None))
                return "^({0}({1}|{2}))$".format(zeros, ans, ans2)

        if minV is not None and maxV is not None:
            if minV <= 0 and maxV <= 0:
                tempMinV = minV
                minV = -maxV
                maxV = -tempMinV
                return "^-({0}({1}))$".format(zeros, self.calculateRealRegex(minV, maxV))
            else:
                if minV <= 0 and maxV >= 0:
                    if math.fabs(minV) < maxV:
                        result = "-?({0}({1}))".format(zeros,self.calculateRealRegex(0, -minV))
                        result += "|{0}({1})".format(zeros,self.calculateRealRegex(-minV, maxV))
                        return "^({0})$".format(result)
                    else:
                        result = "-?({0}({1}))".format(zeros,self.calculateRealRegex(0, maxV))
                        result += "|-{0}({1})".format(zeros,self.calculateRealRegex(maxV, -minV))
                        return "^({0}({1}))$".format(zeros, result)
                else:
                    return "^({0}({1}))$".format(zeros, self.calculateRealRegex(minV, maxV))

    def CreateNNIntegerRegex(self, frmt, minV, maxV):
        m = re.match('%0([0-9]+)d', frmt)
        if (m):
            self.zeros = int(m.group(1))
        self.alternatives = [[]]
        self.currentIndex = 0
        self.format = frmt
        self.SetNNRegExpBase();

        #%d
        if frmt == "%d" and minV is None and maxV is not None:
            self.AddElement("0*")
            frmt = "%0d"

        if frmt == "%d" and minV is None and maxV is None:
            self.AddElement("[0-9]+")

        if frmt == "%d" and minV is not None and maxV is None:
            frmt = "%0d"

        if frmt == "%d" and minV is not None and maxV is not None:
            frmt = "%0d"

        #%0d
        if frmt == "%0d" and minV is None and maxV is None:
            if (self.zeros == 0):
                self.AddElement("[1-9][0-9]*|0")
            else:
                multiple = "" if self.zeros == 1 else "{{{0}}}".format(str(self.zeros))
                self.AddElement("[0-9]{0}".format(multiple))
                self.zeros = 0

        if frmt == "%0d" and minV is not None and maxV is None:
            l = len(str(minV))
            ma = l * "9"
            self.calculateRegex(minV, ma)
            self.AddRange(1, 9)
            self.AddElement("[0-9]{{{0}}}[0-9]*".format(str(l)))

        if frmt == "%0d" and minV is None and maxV is not None:
            minV = 0
            self.calculateRegex(minV, maxV)

        if frmt == "%0d" and minV is not None and maxV is not None:
            self.calculateRegex(minV, maxV)

        #%0Xd
        if self.zeros != 0 and minV is not None and maxV is None:
            maxV = self.zeros * "9"
            self.calculateRegex(minV, maxV)

        if self.zeros != 0 and minV is None and maxV is None:
            minV = 0
            maxV = self.zeros * "9"
            self.calculateRegex(minV, maxV)

        if self.zeros != 0 and minV is None and maxV is not None:
            minV = 0
            self.calculateRegex(minV, maxV)

        if self.zeros != 0 and minV is not None and maxV is not None:
            self.calculateRegex(minV, maxV)

        return "^({0})$".format(self.BuildRegEx())

    def calculateRealRegex(self, mi, ma):
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

        while len(min) < len(str(max)):
            min = min + "0"
        while len(str(min)) > len(max):
            max = max + "0"

        format =  "%0" + str(len(max))+ "d"

        if miIntPart == maIntPart:
            #print format, min, str(int(max)-1)
            x = self.executeIntegerCalculation(format, int(min), int(max)-1)
            return "{0}\.({1}[0-9]*|{2}0*)?".format(miIntPart, x, max)
        else:
            x = self.executeIntegerCalculation(format, int(min), "9"*len(min)).replace("[0-9]", "")
            y = self.executeIntegerCalculation(format, 0, int(max) - 1).replace("[0-9]", "")
            if int(miIntPart) + 1 < int(maIntPart)-1:
                z = self.executeIntegerCalculation("%0d", int(miIntPart) + 1, int(maIntPart)-1)# tu inny format bo liczymy dla czsci cakowitych
            else:
                z = str(int(miIntPart) + 1)

            ans = "{0}(\.({1}[0-9]*))?".format(miIntPart, x)
            if int(miIntPart) + 1 <= int(maIntPart)-1:
                ans += "|{0}(\.[0-9]+)?".format(z)
            ans += "|{0}(\.({1}[0-9]*))?".format(maIntPart, y)
            ans += "|{0}(\.{1}0*)?".format(maIntPart, max)

            return ans;

    def BuildPartRegEx(self):
        result = ""
        for alternative in self.alternatives:
            if alternative != []:
                m = re.match("^.+-+.+$", str(alternative))
                if len(alternative) == 1 and m == None:
                    result += "0" * (self.zeros - len(str(alternative[0])))
                #    result += "0" * (self.zeros - len(alternative))
                else:
                    result += "0" * (self.zeros - len(alternative))
                for element in alternative:
                    result += element
                result += "|"
        return result[:-1];

    def calculateRegex(self, mi, ma):
        if mi == ma:
            self.AddElement(mi)
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
            ranges.append((frm, to if to < ma else ma))
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

            if self.sameDigit("9", p[1]):
                lastIndex = l - 1
                left = str(p[0])

                while lastIndex >= 0:
                    trailing = l - lastIndex - 1                        #how many digits after current one
                    nextNines = left[0:lastIndex][::-1]                 #reversed digits before current one
                    i = 0;
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
                        i = 0;
                        while i < len(nextNines) and nextNines[i] == '9':
                            i += 1
                        right = left[0:lastIndex] + '9' + '9'*trailing
                        resultRanges.append((left, right))
                        lastIndex -= (1 + i)
                    left = str(int(right) + 1)

                maxRange = str(ma)
                sames = self.GetSames(left, ma)

                left = left[len(sames):]
                right = maxRange[len(sames):]
                newMa = right

                lastIndex = len(left) - 1
                if not self.sameDigit("0", str(left)):
                    while lastIndex >= 0 and (left[0] != newMa[0] or len(left) != len(newMa)):
                        if lastIndex == 0:
                            right = str(int(newMa[0])-1) + '9'*(len(newMa)-1)
                            resultRanges.append((sames + left, sames + right))
                        else:
                            trailing = len(left) - lastIndex - 1
                            nextNines = left[0:lastIndex][::-1]
                            i = 0;
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
                self.AddRange(left, right)
            self.StartNextAlternative()

        newNumber = ma
        if self.zeros != 0 and len(str(ma)) != self.zeros:
            newNumber = (self.zeros - len(str(ma)))* "0" + str(ma)
        m = re.match("^(" + self.BuildRegEx() + ")$", str(newNumber))
        if m == None:
            self.AddRange(ma, ma)
            self.StartNextAlternative()

    def GetSames(self, a, b):
        aS = str(a)
        bS = str(b)
        sames = ""
        for i in xrange(len(bS)):
            if bS[i] == aS[i]:
                sames += bS[i]
            else:
                break
        return sames
