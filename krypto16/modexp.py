# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 15:48:09 2016

@author: flac
@title: Modular Exponentiation - Kattis
"""

import sys

# Return the binary decomposition of the number a
def toBin(a):
    tab = []
    while a != 0:
        tab.append(a & 1)
        a = a >> 1
    return list(reversed(tab))
        
# Compute a^e = r [n]
def modexp(a, e, n):
    if e == 0:
        return 1
    elif n == 0:
        return 0
    else:
        r = 1
        tab = toBin(e)
        for i in tab:
            r *= r
            r = r % n
            if i == 1:
                r *= a
                r = r % n
        return r                
                
# Main part of the program        
line = sys.stdin.readline()
while line:
    vals = [int(a) for a in line.split()]
    print modexp(vals[0], vals[1], vals[2])
    line = sys.stdin.readline()
