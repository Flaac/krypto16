# -*- coding: utf-8 -*-

import sys

# Compute the Jacobi value of (a/b)
def jacobi(a,b):
    if(a<2):
        return a;
    s = 1
    while(a & 1 == 0):
        s = s * pow(-1,(b*b-1)/8)
        a = a >> 1
    if(a < b and a > 1):
        temp = a
        a = b
        b = temp
        s = s * pow(-1,(a-1)*(b-1)/4)
    return s*jacobi(a%b,b)

# Compute the discriminant (t) and the total of point (n)
def EC(p,a,b):
    t = (4*a*a*a + 27*b*b) % p
    r = 1 if t == 0 else 0
    n = p
    i = 0
    while(i < p):
        f = (i*i*i + a*i + b)
        n = n + jacobi(f,p)
        i = i + 1
    return r,n


# Main part of the program
line = sys.stdin.readline()
while line:
    vals = [int(a) for a in line.split()]
    p,q = EC(vals[0], vals[1], vals[2])
    print(str(p)+ " " + str(q))
    line = sys.stdin.readline()
