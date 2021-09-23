#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:08:58 2021

@author: student
"""

import turtle as t

n = 10
a = 10
t.shape('turtle')

def paint_square(i, a):
    t.forward(a*i)
    t.left(90)
    t.forward(a*i)
    t.left(90)
    t.forward(a*i)
    t.left(90)
    t.forward(a*i)
    
    
for i in range(1, n+1):
    paint_square(i, a)
    
    t.penup()
    t.forward(a/2)
    t.left(90)
    t.backward(a/2)
    t.pendown()
    
    
exit()