# -*- coding: utf-8 -*-
"""
Created on Tue May 17 11:26:54 2016

@author: flac
@title : Feldman Verifiable Secret Sharing - Kattis
"""

import sys;

# Convert the number a into binary
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

# Compute the modular inverse of a modulus p
def inv(a,p):
        b = p
        s1 = 1
        s2 = 0
        r = 0
        while(r != 1):
            q = a/b
            r = a%b
            st = s1 - q * s2
            s1 = s2
            s2 = st
            a = b
            b = r            
        return s2 % p          

# Check if each element of the list s can be a point of the polynomial
# Return the indices of the elements belonging to the curve
def realS(p,g,d,a,k,s):
    res = []
    for i in range(1,k+1):
        temp = modexp(g,s[i-1],p)
        prod = 1
        for j in range(d+1):            
            prod = (prod * modexp(a[j],pow(i,j),p)) % p
        if(prod == temp):
            res.append(i)
    return res;

# Compute the secret element using the polynomials of Lagrange
def lag(s, ind, q):
    l = 0
    for i in ind:
        prod = 1
        for j in ind:
            if (i!=j):
                prod *= j*inv((j-i)%q,q)
        l += s[i-1]*prod
    return l % q

# Collect the input values
def feld(vals):
    p = vals[0]
    q = (p-1)/2
    g = vals[1]
    d = vals[2]
    a = vals[3:5+d-1]
    k = vals[5+d-1]
    s = vals[5+d:]
    ind = realS(p,g,d,a,k,s)
    l = lag(s,ind, q)
    return l

# Main program
line = sys.stdin.readline()
while line:
    vals = [int(a) for a in line.split()]
    l = feld(vals)
    print l
    line = sys.stdin.readline()
