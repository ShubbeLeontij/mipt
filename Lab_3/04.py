import turtle as t

x = -500
y = 0
vx = 0.5
vy = 1
g = 0.01
n = 2000
dt = 1

t.shape('turtle')
t.forward(1000)
t.backward(1500)
for i in range(n):
    t.goto(x, y)
    x += vx * dt
    y += vy * dt - g * dt**2 / 2
    vy -= g * dt
    if y < 0:
        vy = -vy
