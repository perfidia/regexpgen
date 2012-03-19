# -*- coding: utf-8 -*-

'''
Created on Apr 27, 2011

@author: Bartosz Alchimowicz

Generowanie wyrażenie regularnego dla integers (-2, -1, 0, 1, 2, 3...).

Supported format:

FORMAT = '%d'
opis: zera wiodące są opcjonalne,
przykłady poprawne: 0, 1, 001, 012
przykłady niepoprawne: N/A

FORMAT = '%0d'
opis: zera wiodące niedowolone
przykłady poprawne: 0, 1
przykłady niepoprawne: 001, 012

FORMAT = '%0Xd'
opis: liczba zapisana przy pomocy X znaków, w przypadku liczb
      mniejszych od int('9'*X) należy liczbą poprzedzić zerami,
      zera wiodące są wymagane
przykłady poprawne dla %04d: 0001, 45678
przykłady niepoprawne dla %04d: 00011, 11
'''
import re
from misc import assertMinMax
from misc import digitsNum

def default(format, min, max):
    assertMinMax(min,max)
    if(min is not None):
        None
    return r'^-?[0-9]+$'


def no_leading_zeros(format, min, max):
    return r'^-?[1-9][0-9]*$'


def x_signs_leading_zeros(format, min, max):
    m = re.search('%0([0-9]+)d', format)
    param = m.group(1)
    return r'(^-?[0-9]{'+param+'}$)|(^-?[1-9][0-9]{'+param+',}$)'

def run(format, min, max):
    m = re.search('%0([0-9]+)d', format)
    if(m != None):
        generalFormat = '%0Xd'
    else:
        generalFormat = format 
    result = {
        '%d': default,
        '%0d': no_leading_zeros,
        '%0Xd': x_signs_leading_zeros,
    }.get(generalFormat, complex)(format, min, max)
    return result

# non-negative min/max only
def rawBounds(min,max,leadingZeros=True):
    assertMinMax(min, max)
    if(min>0): min -= 1;
    max += 1;
    minD = digitsNum(min)
    maxD = digitsNum(max)
    minS = str(min)
    maxS = str(max)
    res = list()
    for i in range(1,minD+1):
        curr = ""
        for j in range(0,minD-i):
            curr += minS[j]
        curr += "[%d-9]"%(int(minS[minD-i])+1)
        for j in range(minD-i+1, minD):
            curr += "[0-9]"
        res.append(curr)
    for i in range(minD+1,maxD):
        curr = "[1-9][0-9]{%d}"%(i-1)
        res.append(curr)
    for i in range(maxD-1,0,-1):
        curr = ""
        for j in range(0,maxD-i):
            curr += maxS[j]
        curr += "[0-%d]"%(int(maxS[maxD-i])-1)
        for j in range(maxD-i+1,maxD):
            curr += "[0-9]"
        res.append(curr)
    return "(" + ("|".join(res)) + ")"
