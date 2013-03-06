import re

class NNIntegerRegexBuilder(object):
    def __init__(self):
        self.alternatives = [[]]
        self.currentIndex = 0
        self.zeros = 0

    def StartNextAlternative(self):
        if (len(self.alternatives[self.currentIndex]) == 0):
            return;
        self.alternatives.append([])
        self.currentIndex = self.currentIndex + 1

    def BuildRegEx(self):
        result = ""
        for alternative in self.alternatives:
            if alternative != []:
                result += "0" * (self.zeros - len(alternative))
                for element in alternative:
                    result += element
                result += "|"
        return result[:-1];

    def AddRange(self, mi, ma):
        if mi == ma:
            r = str(mi)
        else:
            r = "[{0}-{1}]".format(str(mi), str(ma))
        self.alternatives[self.currentIndex].append(r)

    def AddElement(self, element):
        self.alternatives[self.currentIndex].append(str(element))

    def onlyNines(self, number):
        for digit in str(number):
            if digit != "9":
                return False
        return True

    def onlyZeros(self, number):
        for digit in str(number):
            if digit != "0":
                return False
        return True

    def CreateNNIntegerRegex(self, format, min, max, zeros = 0):
        self.zeros = zeros

        #%d
        if format == "%d" and min is None and max is not None:
            self.AddElement("0*")
            format = "%0d"

        if format == "%d" and min is None and max is None:
            self.AddElement("[0-9]+")

        if format == "%d" and min is not None and max is None:
            format = "%0d"

        if format == "%d" and min is not None and max is not None:
            format = "%0d"

        #%0d
        if format == "%0d" and min is None and max is None:
            if (zeros == 0):
                self.AddElement("[1-9][0-9]*|0")
            else:
                self.AddElement("[0-9]{" + str(zeros) + "}")
                self.zeros = 0

        if format == "%0d" and min is not None and max is None:
            l = len(str(min))
            ma = l * "9"
            self.calculateRegex(min, ma)
            self.AddRange(1, 9)
            self.AddElement("[0-9]{" + str(l) +"}[0-9]*")

        if format == "%0d" and min is None and max is not None:
            min = 0
            mi = 0
            self.calculateRegex(min, max)

        if format == "%0d" and min is not None and max is not None:
            self.calculateRegex(min, max)

        #%0Xd
        if re.match('%0([0-9]+)d', format) and min is not None and max is None:
            max = zeros * "9"
            self.calculateRegex(min, max)

        if re.match('%0([0-9]+)d', format) and min is None and max is None:
            min = 0
            max = zeros * "9"
            self.calculateRegex(min, max)

        if re.match('%0([0-9]+)d', format) and min is None and max is not None:
            min = 0
            self.calculateRegex(min, max)

        if re.match('%0([0-9]+)d', format) and min is not None and max is not None:
            self.calculateRegex(min, max)

    def calculateRegex(self, mi, ma):
        if (mi == ma):
            self.AddElement(mi)
            return

        minl = len(str(mi))
        maxl = len(str(ma))
        min = []
        max = []

        for i in str(mi):
            min.append(int(i))
        for i in str(ma):
            max.append(int(i))

        ranges = []
        frm = mi
        for i in xrange(minl, maxl + 1):
            to = 10**(i) - 1
            range = [frm]
            range.append(to if to < ma else ma)
            ranges.append(range)
            frm = to + 1

        resultRanges = []
        for p in ranges:
            if (len(ranges) == 1 and len(str(p[0])) == 1):#jezeli 1 cyfrowy przedzial jest jedynym to od razu mamy rozw
                resultRanges = ranges
                break

            l = len(str(p[0]))

            min = []
            max = []
            for i in str(str(p[0])):
                min.append(int(i))
            for i in str(str(p[1])):
                max.append(int(i))

            if p[0] == 10**(l-1) and p[1] == 10**l - 1:
                resultRanges.append((p[0], p[1]))
            else:
                if(self.onlyNines(p[1])):
                    lastIndex = l - 1
                    left = str(p[0])

                    while lastIndex >= 0:
                        trailing = l - lastIndex - 1
                        nextNines = left[0:lastIndex][::-1]
                        i = 0;
                        while (i < len(nextNines) and nextNines[i] == '9'):
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
                            while (i < len(nextNines) and nextNines[i] == '9'):
                                i += 1
                            right = left[0:lastIndex] + '9' + '9'*trailing
                            resultRanges.append((left, right))
                            lastIndex -= (1 + i)
                        left = str(int(right) + 1)

                    maxRange = str(ma)
                    sames = ""
                    for i in xrange(len(maxRange)):
                        if (maxRange[i] == left[i]):
                            sames += maxRange[i]
                        else:
                            break

                    left = left[len(sames):]
                    right = maxRange[len(sames):]
                    newMa = right

                    lastIndex = len(left) - 1
                    if (not self.onlyZeros(str(left))):
                        while lastIndex >= 0 and left[0] != newMa[0]:
                            if lastIndex == 0:
                                right = str(int(newMa[0])-1) + '9'*(len(left)-1)
                                resultRanges.append((sames + left, sames + right))
                            else:
                                trailing = len(left) - lastIndex - 1
                                nextNines = left[0:lastIndex][::-1]
                                i = 0;
                                while (i < len(nextNines) and nextNines[i] == '9'):
                                    i += 1
                                right = left[0:lastIndex] + '9' + '9'*trailing
                                resultRanges.append((sames + left, sames + right))
                                lastIndex -= (1 + i)
                            left = str(int(right) + 1)

                    right = str(ranges[-1][0])
                    while right != newMa:
                        right = ""
                        index = 0
                        for i in str(left):
                            range = []
                            range.append(sames + str(left))
                            if str(left)[index] == newMa[index]:
                                right = right + str(left)[index]
                                index = index + 1
                                if right == newMa:
                                    range.append(sames + right)
                                    resultRanges.append(range)

                            else:
                                if index + 1 == len(str(left)):
                                    nextDigit = int(newMa[-1])
                                else:
                                    nextDigit = int(newMa[index]) - 1
                                right = right + str(nextDigit)
                                while len(right) != len(str(left)):
                                    right = right + "9"
                                range.append(sames + right)
                                resultRanges.append(range)
                                left = int(right) + 1
                                index = 0
                                if right == newMa:
                                    break
                                else:
                                    right = ""

        for p in resultRanges:
            min = []
            max = []
            for i in str(p[0]):
                min.append(int(i))
            for i in str(p[1]):
                max.append(int(i))
            for i in xrange(0, len(min)):
                self.AddRange(min[i], max[i])
            self.StartNextAlternative()
