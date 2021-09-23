#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 17:49:28 2021

@author: student
"""

import turtle as t

a = 10
n = 10

t.shape('turtle')

for i in range(1, (n * 4 + 1)):
    t.forward(a * i)
    t.left(90)

exit()