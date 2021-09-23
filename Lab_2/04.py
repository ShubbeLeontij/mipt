#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:08:58 2021

@author: student
"""

import turtle as t

n = 1000
a = 1
t.shape('turtle')

for i in range(n):
    t.left(360/n)
    t.forward(a)

exit()