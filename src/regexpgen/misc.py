'''
Created on 19-03-2012

@author: Michzimny
'''

def assertMinMax(min,max):
    if((min is not None) and (max is not None) and (min>max)):
        raise Exception("Invalid parameters (min>max)")

def digitsNum(number):
    if(number is None):
        return None
    elif((number >= 0) and (number <= 9)):
        return 1
    else:
        return digitsNum(number // 10) + 1

def minimum(a,b):
    return min(a,b)
def maximum(a,b):
    return max(a,b)

# non-negative min/max only
def rawBounds(min,max,leadingZeros=True):
    assertMinMax(min, max)
    res = list()
    if((min is None) or (min == 0)): 
        min = 0;
        res.append("0")
    elif(min>0): 
        min -= 1;
    if(max is not None): max += 1;
    minD = digitsNum(min)
    maxD = digitsNum(max)
    minS = str(min)
    maxS = str(max)
    q = diffLastChars(minS, maxS)
    for i in range(1,minD+1):
        if((q > 0) and (i >= q)): break
        curr = ""
        for j in range(0,minD-i):
            curr += minS[j]
        curr += "[%d-9]"%(int(minS[minD-i])+1)
        for j in range(minD-i+1, minD):
            curr += "[0-9]"
        res.append(curr)
    if(max is None):
        res.append("[1-9][0-9]{%d,}"%(minD))
    else:
        for i in range(minD+1,maxD):
            curr = "[1-9][0-9]{%d}"%(i-1)
            res.append(curr)
        for i in range(maxD-1,0,-1):
            if((q > 0) and (i >= q)): continue
            curr = ""
            for j in range(0,maxD-i):
                curr += maxS[j]
            curr += "[0-%d]"%(int(maxS[maxD-i])-1)
            for j in range(maxD-i+1,maxD):
                curr += "[0-9]"
            res.append(curr)
    
    if(q == 1): # <==> res is empty
        curr = ""
        for i in range(0,minD-1):
            curr += minS[i]
        curr += "[%d-%d]"%(int(minS[minD-1])+1,int(maxS[minD-1])-1)
        res.append(curr)
    
    return "(" + ("|".join(res)) + ")"

# returns the number of the different characters in both strings, checking from the end
# e.g. diffLastChars("asadfaw","qwtdfqe") == 2
def diffLastChars(s1,s2):
    if(len(s1)!=len(s2)):
        return 0
    for i in range(len(s1)-1,-1,-1):
        if(s1[i]==s2[i]):
            return len(s1)-i-1
    return len(s1)
