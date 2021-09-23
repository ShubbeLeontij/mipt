#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:51:11 2021

@author: student
"""

import turtle as t

n = 100
a = 5
circles = 6
t.shape('turtle')


def paint_circle(a, n):
    for i in range(n):
        t.left(360/n)
        t.forward(a)
        
for j in range(circles):
    paint_circle(a, n)
    t.left(360/circles)
    
exit()