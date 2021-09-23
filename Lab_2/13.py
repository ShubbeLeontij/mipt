#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:51:11 2021

@author: student
"""

import turtle as t

n = 100

def paint_arc(a, n):
    for i in range(n):
        t.right(180/n)
        t.forward(a)

def paint_circle(a, n):
    for i in range(n):
        t.right(360/n)
        t.forward(a)
        

t.shape('turtle')

#big circle
t.penup()
t.forward(159)
t.right(90)
t.pendown()
t.color('yellow')
t.begin_fill()
paint_circle(10, n) #r = 159
t.end_fill()

#left eye
t.color('blue')
t.penup()
t.goto(-50, 50)
t.pendown()
t.begin_fill()
paint_circle(1, n) #r = 15.9
t.end_fill()

#right eye
t.color('blue')
t.penup()
t.goto(81.8, 50) #81.8 = 50 + 2 * 15.9
t.pendown()
t.begin_fill()
paint_circle(1, n) #r = 15.9
t.end_fill()

#mouth
t.color('red')
t.width(5)
t.penup()
t.goto(50, -50)
t.pendown()
paint_arc(1.57, n) #r = 50 so a = r * pi / n = 1.57

#nose
t.color('black')
t.width(10)
t.penup()
t.goto(0, 25)
t.pendown()
t.goto(0, -25)

exit()