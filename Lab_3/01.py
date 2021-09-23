import random
import turtle as t

n = 100
t.shape('turtle')

for i in range(n):
    alpha = random.randint(0, 360)
    length = random.randint(0, 30)

    t.left(alpha)
    t.forward(length)
