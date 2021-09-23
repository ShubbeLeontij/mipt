#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:51:11 2021

@author: student
"""

import turtle as t

n = 100
a = 1
circles = 10
t.shape('turtle')
t.left(90)


def paint_circle(a, n, direction):
    for i in range(n):
        if direction == 'right':
            t.right(360/n)
        else:
            t.left(360/n)
        t.forward(a)
        
for j in range(2, circles+2):
    if j%2:
        paint_circle(a*(j//2), n, 'right')
    else:
        paint_circle(a*(j//2), n, 'left')
    
exit()