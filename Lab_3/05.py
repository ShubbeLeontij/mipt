from random import randint
import turtle


turtles = 10
n = 1000
dt = 1
size = 300
max_v = 10


class Molecule(turtle.Turtle):
    def __init__(self, shape, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        super().__init__(shape=shape)
        self.penup()
        self.turtlesize(0.5)
        self.speed(0)

    def update(self):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.goto(self.x, self.y)

        if self.x < -size or self.x > size:
            self.vx = -self.vx
        if self.y < -size or self.y > size:
            self.vy = -self.vy


coords = [(size, size), (size, -size), (-size, -size), (-size, size)]
border_turtle = turtle.Turtle()
border_turtle.speed(0)
border_turtle.penup()
border_turtle.goto(coords[-1])
border_turtle.pendown()
for coord in coords:
    border_turtle.goto(coord)
border_turtle.hideturtle()
del border_turtle

pool = [Molecule('circle', randint(-size, size), randint(-size, size),
                 randint(-max_v, max_v), randint(-max_v, max_v)) for i in range(turtles)]
for i in range(n):
    for mol in pool:
        mol.update()
