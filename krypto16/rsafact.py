# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 11:52:42 2016

@author: flac
@title: RSA factor - Kattis
"""

import sys
import random

# Euclidean algorithm
def gcd(a, b):
        r = 1
        while(r != 0):
            r = a - (a/b)*b
            a = b
            b = r            
        return a
        
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

# Decomposition a number   
# Return (r, s) such as ed-1 = 2^s * r
def decomp(e,d): 
    a = e*d - 1
    s = 0
    while(a & 1 == 0):
        s = s + 1
        a = a >> 1
    return s,a

# Return the a good factorization 
def rsafact(n, e, d):
    s, r = decomp(e,d)
    w = random.randrange(1,n)
    a = rsaguess(n,s,r,w)
    c = 1
    while(a == 0 or a == n):
        w = random.randrange(1,n)
        a = rsaguess(n,s,r,w)
        c = c + 1
    return min(a, n/a), max(a, n/a)

# Try to make a factorization
# (It's a probabilistic algo)
def rsaguess(n,s,r,w):
    x = gcd(w,n)
    if(x > 1 and x < n):
        return x
    v = modexp(w,r,n)
    if v%n == 1:
        return 0
    while(v%n != 1):
        v0 = v
        v *= v
        v = v % n
    if v0%n == -1:
        return 0
    else:
        return gcd(v0+1,n)

        
# Main part of the program
line = sys.stdin.readline()
while line:
    vals = [int(a) for a in line.split()]
    p,q = rsafact(vals[0], vals[1], vals[2])
    print(str(p)+ " " + str(q))
    line = sys.stdin.readline()
