#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:08:58 2021

@author: student
"""

import turtle as t

n = 12
a = 100
t.shape('turtle')

def paint_part(a):
    t.forward(a)
    t.stamp()
    t.backward(a)
    
    
for i in range(1, n+1):
    paint_part(a)
    
    t.left(360/n)
    
exit()