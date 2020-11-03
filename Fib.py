#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 19:19:16 2020

@author: afsalmoideen
"""

__author__ = "Afsal Moideen"
__date__ = "2020-11-01"
__version__ = "1.0.1" 
__maintainer__ = "Afsal Moideen" 
__email__ = "ac20adi@herts.ac.uk"



x = int(input("Enter till how many numbers you want fibonacci series = "))


def fibo(n):
    a = 0
    b = 1
    
    if n < 0:
        print("Invalid value enter a valid one!")
    elif n == 1:
        print(a)
        
    else:
        print(a)
        print(b)
        
        for i in range(2, n):  # 2 elements are printed so 0 and 1 are already occupied now from index 2 start
            c = a+b
            a = b
            b = c
            print(c)
            
fibo(x)