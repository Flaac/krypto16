# -*- coding: utf-8 -*-

import sys

# Extended Euclidean Algorithm
def extEuc(a, b):
        s1 = 1
        s2 = 0
        t1 = 0
        t2 = 1
        r = 0
        while(r != 1):
            q = a/b
            r = a%b
            st = s1 - q * s2
            s1 = s2
            s2 = st
            tt = t1 - q * t2
            t1 = t2
            t2 = tt
            a = b
            b = r            
        return [s2, t2]
    

#Computing the Chinese Remainder Theorem
def crt(q,a):
    N = 1
    for i in q:
        N *= i
    res = 0
    for i in range(len(q)):
        s = extEuc(N/q[i],q[i])[0]
        res += s*a[i]*N/q[i]
    return res % N
        
# Main part of the program
line = sys.stdin.readline()
while line:
    tab = [int(a) for a in line.split()]
    print crt(tab[1:tab[0]+1],tab[tab[0]+1:])
    line = sys.stdin.readline()
