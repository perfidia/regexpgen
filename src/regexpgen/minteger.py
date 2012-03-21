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
from regexpgen.misc import assertMinMax, rawBounds, minimum, maximum
import re

def default(format, min, max):
    if((min is None) and (max is None)):
        return r'^-?[0-9]+$'
    assertMinMax(min, max)
    res = list()
    inminusL = min
    if(inminusL is not None): inminusL = -min;
    inminusR = -minimum(0,max)
    inplusL = maximum(0,min)
    inplusR = max
    if(min is None)or(min <= 0):
        for el in rawBounds(inminusR, inminusL):
            res.append("-0*" + el)
    if(max is None)or(max >= 0):
        for el in rawBounds(inplusL, inplusR):
            res.append("0*" + el)
    return '^(' + "|".join(res) + ')$'


def no_leading_zeros(format, min, max):
    if((min is None) and (max is None)):
        return r'^(-?0|-?[1-9][0-9]*)$'
    assertMinMax(min, max)
    res = list()
    inminusL = min
    if(inminusL is not None): inminusL = -min;
    inminusR = -minimum(0,max)
    inplusL = maximum(0,min)
    inplusR = max
    if(min is None)or(min <= 0):
        for el in rawBounds(inminusR, inminusL):
            res.append("-" + el)
    if(max is None)or(max >= 0):
        for el in rawBounds(inplusL, inplusR):
            res.append(el)
    return '^(' + "|".join(res) + ')$'


def x_signs_leading_zeros(format, min, max):
    m = re.search('%0([0-9]+)d', format)
    param = int(m.group(1))
    if((min is None) and (max is None)):
        return r'^(-?[0-9]{%d}|-?[1-9][0-9]{%d,})$'%(param,param-1)
    assertMinMax(min, max)
    res = list()
    inminusL = min
    if(inminusL is not None): inminusL = -min;
    inminusR = -minimum(0,max)
    inplusL = maximum(0,min)
    inplusR = max
    if(min is None)or(min <= 0):
        for el in rawBounds(inminusR, inminusL, param):
            res.append("-" + el)
    if(max is None)or(max >= 0):
        for el in rawBounds(inplusL, inplusR, param):
            res.append(el)
    return '^(' + "|".join(res) + ')$'

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
    }.get(generalFormat)(format, min, max)
    return result
