#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 17:49:28 2021

@author: student
"""

import turtle as t

a = 0.01
n = 100
circles = 10

t.shape('turtle')

for i in range(1, circles*n):
    t.forward(a*i)
    t.left(360/n)

exit()