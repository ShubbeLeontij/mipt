#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 17:40:46 2021

@author: student
"""

import turtle as t

def paint_star(a, n):
    for i in range(n):
        t.forward(a)
        t.left(180 - (180)/n)
    
    
t.shape('turtle')

paint_star(300, 5)

t.penup()
t.goto(-400, 0)
t.pendown()

paint_star(300, 11)

exit()