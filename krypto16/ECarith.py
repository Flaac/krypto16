# -*- coding: utf-8 -*-
"""
Created on Thu May 12 10:19:31 2016

@author: flac
@title: Elliptic Curve Arithmetic - Kattis
"""

import sys;

# Compute the binary decomposition
def toBin(a):
    tab = []
    while a != 0:
        tab.append(a & 1)
        a = a >> 1
    return list(reversed(tab))

# Doubling operation of the point P(px, py)
# Handle the infinity point (0,0)
def double(px,py):
    if py == 0 and px == 0:
        return px % p ,py % p
    else:    
        l = (3*px*px + a)*inv(2*py) % p
        zx = (l*l - 2*px)
        zy = -l*zx + l*px - py
        return zx % p, zy % p	

# Addition two points P(px,py) and Q(qx, qy)
def add(px,py,qx,qy):
    if px == 0 and py == 0:
	return qx,qy
    else:
	l = ((qy-py)*inv((qx-px))) % p
	zx = (l*l - px - qx)
	zy = -l*zx + l*px - py
	return zx % p, zy % p
    
# Compute the inverse of a modulus p
# (Extended Euclidean Algorithm)
def inv(a):
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
    
# Double-and-add algorithm
def da(e):
    l = toBin(e % q)
    kx = 0
    ky = 0
    for i in l:
	kx,ky =double(kx,ky)
        if(i==1):
            kx,ky = add(kx,ky,gx,gy)
    return kx,ky
    
# Constant of the curve 'prime192v3'
p = 0xfffffffffffffffffffffffffffffffeffffffffffffffff;
a = 0xfffffffffffffffffffffffffffffffefffffffffffffffc;
b = 0x22123dc2395a05caa7423daeccc94760a7d462256bd56916;
gx = 0x7d29778100c65a1da1783716588dce2b8b4aee8e228f1896;
gy = 0x38a90f22637337334b49dcb66a6dc8f9978aca7648a943b0;
q = 0xffffffffffffffffffffffff7a62d031c83f4294f640ec13;
tabp = toBin(p-2)

# Main
line = sys.stdin.readline()
while line:
    e = int(line,16)
    ex, ey = da(e)
    print(str(hex(ex).rstrip("L"))+ " " + str(hex(ey).rstrip("L")))
    line = sys.stdin.readline()

