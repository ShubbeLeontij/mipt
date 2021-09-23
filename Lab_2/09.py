import turtle as t

a = 30
t.shape('turtle')
t.penup()
t.goto(a/2, -250)


def paint(a, n):
    for i in range(n):
        t.left(360/n)
        t.forward(a)


for j in range(3, 10):
    t.pendown()
    paint(a * j, j)
    t.penup()
    t.right(90)
    t.forward(a/2)
    t.left(90)
    t.forward(a/2)
