'''
Created on 19-03-2012

@author: Michzimny
'''

def assertMinMax(min,max):
    if(min>max):
        raise Exception("Invalid parameters (min>max)")

def digitsNum(number):
    if(number is None):
        return None
    elif((number >= 0) and (number <= 9)):
        return 1
    else:
        return digitsNum(number // 10) + 1
