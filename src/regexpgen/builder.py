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
		result = ""
		for alternative in self.alternatives:
			if alternative != []:
				m = re.match("^.+-+.+$", str(alternative))
				if len(alternative) == 1 and m == None:
					result += "0" * (self.zeros - len(str(alternative[0])))
				else:
					result += "0" * (self.zeros - len(alternative))
				for element in alternative:
					result += element
				result += "|"
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
		try:
			if minV is not None:
				if str(minV) != str(int(minV)):
					raise
			if maxV is not None:
				if str(maxV) != str(int(maxV)):
					raise
		except:
			raise ValueError("Bad input")
	
		if (frmt == None) or (frmt not in ["%d", "%0d"]) and not re.match("^%0[0-9]+d$", frmt):
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
		return b.createIntegerRegex(frmt, minV, maxV).replace("^", "").replace("$", "")

	def createRealRegex(self, frmt, minV, maxV):
		try:
			if minV is not None:
				float(minV)
			if maxV is not None:
				float(maxV)
		except:
			raise ValueError("Bad input: " + str(minV))
	
		if (minV is not None) and (maxV is not None) and (minV>maxV):
			raise ValueError("Invalid parameters (min>max)")
		if (frmt == None) or frmt not in ["%lf", "%0lf"] and not re.match("^%.[0-9]+lf$", frmt) and not re.match("^%0.[0-9]+lf$", frmt):
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

		#%0.Ylf zera wiodace niedozwolone lub '%X.Ylf'
		m = re.match('%0\.([0-9]+)lf', frmt)
		if m:
			digitsReal = int(m.group(1))

		m = re.match('%([1-9]+)\.([0-9]+)lf', frmt)
		if m:
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

		if digitsReal != None:
			if (minV != None and len(str(minV).split(".")[1]) > digitsReal) or (maxV != None and len(str(maxV).split(".")[1]) > digitsReal) or digitsReal == 0:
				raise ValueError("Bad input")

		if digitsReal == None:
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
				self.__addElement("-?([0-9]+(\.[0-9]+|0)?)")
			if frmt == "%0lf":
				self.__addElement("-?(([1-9][0-9]*|0)(\.[0-9]+)?)")
			if digitsReal != None:
				self.__addElement("-?{0}(([1-9][0-9]*|0)(\.{1})?)".format(zeros, endingReal))

			return "^({0})$".format(self.__buildRegEx())

		if minV is None and maxV is not None:
			if maxV < 0:
				minV = -maxV
				splitted = str(minV).split(".")
				maxV = "{0}.{1}".format("1" + len(splitted[0])*"0", len(splitted[1])*"0")# if digitsReal == None else digitsReal*"9")

				ans = self.calculateRealRegex(minV, maxV, digitsReal)
				minV = int(maxV.split(".")[0])
				ans2 = self.__executeIntegerCalculation("%0d", minV, None)
				if digitsReal == None:
					return r"^-({0}({1})|{0}({2})\.{3})$".format(zeros, ans, ans2, endingReal)
					#return "^(-({0}({1}))|{0}({2})(\.{3})?)$".format(zeros, ans, ans2, endingReal)
				else:
					return r"^-({0}({1})|{0}({2})\.{3})$".format(zeros, ans, ans2.replace("?", ""), endingReal)
			else:
				if digitsReal == None:
					result = "-(" + zeros + "([1-9][0-9]*|0)(\." + endingReal + ")?)"
					minV = 0
					ans = self.calculateRealRegex(minV, maxV, digitsReal)
					result += "|-?(" + zeros + "({0}))".format(ans)
				else:
					result = "-(" + zeros + "([1-9][0-9]*|0)(\." + endingReal + "))"
					minV = 0
					ans = self.calculateRealRegex(minV, maxV, digitsReal)
					result += "|-?(" + zeros + "({0}))".format(ans.replace("?", ""))
				return "^({0})$".format(result)

		if minV is not None and maxV is None:
			if minV <0:
				result = "-{0}({1})".format(zeros, self.calculateRealRegex(0, -minV, digitsReal))
				ans = self.__executeIntegerCalculation("%0d", 0, None)
				result += "|{0}({1})\.{2}".format(zeros, ans, endingReal)
				if digitsReal == None:
					return "^({0})$".format(result)
				else:
					return "^({0})$".format(result).replace("?", "")
			else:
				ans = "{0}".format(self.calculateRealRegex(minV, minV+1, digitsReal))
				ans2 = "{0}\.({1})".format(self.__executeIntegerCalculation("%0d", int(math.floor(minV + 1)), None), endingReal)
				if digitsReal == None:
					return "^({0}({1}|{2}))$".format(zeros, ans, ans2)
				else:
					return "^({0}({1}|{2}))$".format(zeros, ans, ans2).replace("?", "")

		if minV is not None and maxV is not None:
			if minV < 0 and maxV < 0:
				tempMinV = minV
				minV = -maxV
				maxV = -tempMinV
				if digitsReal == None:
					return "^-({0}({1}))$".format(zeros, self.calculateRealRegex(minV, maxV, digitsReal))
				else:
					return "^-({0}({1}))$".format(zeros, self.calculateRealRegex(minV, maxV, digitsReal)).replace("?", "")
			else:
				if minV <= 0 and maxV >= 0:
					if math.fabs(minV) < maxV:
						if digitsReal == None:
							result = "-?({0}({1}))".format(zeros,self.calculateRealRegex(0, -minV, digitsReal))
							result += "|{0}({1})".format(zeros,self.calculateRealRegex(-minV, maxV, digitsReal))
						else:
							result = "-?({0}({1}))".format(zeros,self.calculateRealRegex(0, -minV, digitsReal).replace("?", ""))
							result += "|{0}({1})".format(zeros,self.calculateRealRegex(-minV, maxV, digitsReal).replace("?", ""))
						return "^({0})$".format(result)
					else:
						if digitsReal == None:
							result = "-?({0}({1}))".format(zeros,self.calculateRealRegex(0, maxV, digitsReal))
							result += "|-{0}({1})".format(zeros,self.calculateRealRegex(maxV, -minV, digitsReal))
						else:
							result = "-?({0}({1}))".format(zeros,self.calculateRealRegex(0, maxV, digitsReal).replace("?", ""))
							result += "|-{0}({1})".format(zeros,self.calculateRealRegex(maxV, -minV, digitsReal).replace("?", ""))

						return "^({0})$".format(result)

				else:
					if digitsReal == None:
						return "^({0}({1}))$".format(zeros, self.calculateRealRegex(minV, maxV, digitsReal))
					else:
						return "^({0}({1}))$".format(zeros, self.calculateRealRegex(minV, maxV, digitsReal)).replace("?", "")

	def createNNIntegerRegex(self, frmt, minV, maxV):
		try:
			if minV is not None:
				if str(minV) != str(int(minV)):
					raise
			if maxV is not None:
				if str(maxV) != str(int(maxV)):
					raise
		except:
			raise ValueError("Bad input")
	
		if (frmt == None) or (frmt not in ["%d", "%0d"]) and not re.match("^%0[0-9]+d$", frmt):
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

	def calculateRealRegex(self, mi, ma, digits):
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

		while len(min) < len(str(max)) or len(min) < digits:
			min = min + "0"
		while len(str(min)) > len(max) or len(max) < digits:
			max = max + "0"

		if digits == None:
			format =  "%0" + str(len(max))+ "d"
		else:
			format =  "%0" + str(digits)+ "d"

		if miIntPart == maIntPart:
			if min == max:
				return "{0}\.{1}".format(miIntPart, min)
			x = self.__executeIntegerCalculation(format, int(min), int(max)-1)
			if digits == None:
				x = x.replace("[0-9]", "")
				return "{0}\.({1}[0-9]*|{2}0*)".format(miIntPart, x, max)
			else:
				return "{0}\.({1}|{2})".format(miIntPart, x, max)
		else:
			if digits == None:
				x = self.__executeIntegerCalculation(format, int(min), "9"*len(min)).replace("[0-9]", "")
			else:
				x = self.__executeIntegerCalculation(format, int(min), "9"*len(min))
			if int(max) != 0:
				if digits == None:
					y = self.__executeIntegerCalculation(format, 0, int(max) - 1).replace("[0-9]", "")
				else:
					y = self.__executeIntegerCalculation(format, 0, int(max) - 1)
			else:
				y = None

			if int(miIntPart) + 1 < int(maIntPart)-1:
				z = self.__executeIntegerCalculation("%0d", int(miIntPart) + 1, int(maIntPart)-1)
			else:
				z = str(int(miIntPart) + 1)

			if digits == None:
				ans = "{0}(\.{1}[0-9]*)".format(miIntPart, x)
				if int(miIntPart) + 1 <= int(maIntPart)-1:
					ans += "|{0}\.[0-9]+".format(z)
				if y != None:
					ans += "|{0}(\.{1}[0-9]*)".format(maIntPart, y)
				ans += "|{0}\.{1}0*".format(maIntPart, max)
			else:
				ans = "{0}\.({1})".format(miIntPart, x)
				if int(miIntPart) + 1 <= int(maIntPart)-1:
					ans += "|{0}\.[0-9]{{{1}}}".format(z, digits)
				if y != None:
					ans += "|{0}\.({1})".format(maIntPart, y)
				ans += "|{0}\.{1}".format(maIntPart, max)

			return ans



	def __buildPartRegEx(self):
		result = ""
		for alternative in self.alternatives:
			if alternative != []:
				m = re.match("^.+-+.+$", str(alternative))
				if len(alternative) == 1 and m == None:
					result += "0" * (self.zeros - len(str(alternative[0])))
				else:
					result += "0" * (self.zeros - len(alternative))
				for element in alternative:
					result += element
				result += "|"
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

			if self.__sameDigit("9", p[1]):
				lastIndex = l - 1
				left = str(p[0])

				while lastIndex >= 0:
					trailing = l - lastIndex - 1						#how many digits after current one
					nextNines = left[0:lastIndex][::-1]				 #reversed digits before current one
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
		if m == None:
			self.__addRange(ma, ma)
			self.__startNextAlternative()

	def __getSames(self, a, b):
		aS = str(a)
		bS = str(b)
		sames = ""
		for i in xrange(len(bS)):
			if bS[i] == aS[i]:
				sames += bS[i]
			else:
				break
		return sames
