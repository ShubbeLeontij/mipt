#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:51:11 2021

@author: student
"""

import turtle as t

n = 100
a = 0.3
b = 1
arcs = 10

def paint_arc(a, n):
    for i in range(n):
        t.right(180/n)
        t.forward(a)


t.shape('turtle')
t.penup()
t.backward(300)
t.pendown()
t.left(90)
       
for j in range(arcs):
    if j%2:
        paint_arc(a, n)
    else:
        paint_arc(b, n)
    
exit()