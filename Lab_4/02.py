import pygame
from pygame.draw import *
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
BLUE = (64, 128, 255)
LIGHT_BLUE = (0, 200, 200)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)


def draw_bird(screen, color, x, y, size):
    arc(screen, color, (x, y, size, size * 0.5), math.pi * 0.5, math.pi)
    arc(screen, color, (x - size, y, size, size * 0.5), 0, math.pi * 0.5)


def draw_fish(screen, color, x, y, size):
    polygon(screen, PINK,
            ((x + size * 0.25, y + size * 0.3), (x + size * 0.1, y + size * 0.5), (x + size * 0.3, y + size * 0.5)))
    polygon(screen, PINK,
            ((x + size * 0.7, y + size * 0.3), (x + size * 0.7, y + size * 0.6), (x + size * 0.9, y + size * 0.5)))
    polygon(screen, PINK,
            ((x + size * 0.6, y + size * 0.1), (x + size * 0.7, y - size * 0.1), (x + size * 0.2, y - size * 0.2)))
    ellipse(screen, color, (x, y, size, size * 0.4))
    circle(screen, BLUE, (x + size * 0.8, y + size * 0.2), size * 0.05)
    polygon(screen, color, ((x, y + size * 0.2), (x - size * 0.2, y), (x - size * 0.2, y + size * 0.4)))


def draw_gull(screen, color, x, y, size):
    ellipse(screen, color, (x, y, size, size / 2))
    ellipse(screen, color, (x + size * 0.8, y + size * 0.1, size / 2, size / 4))
    ellipse(screen, color, (x + size, y, size / 2, size / 4))
    ellipse(screen, BLACK, (x + size * 1.3, y + size * 0.04, size / 10, size / 20))
    line(screen, YELLOW, (x + size * 1.5, y + size * 0.12), (x + size * 1.8, y + size * 0.12), int(size * 0.06))
    line(screen, BLACK, (x + size * 1.5, y + size * 0.12), (x + size * 1.8, y + size * 0.12), int(size * 0.01))
    polygon(screen, color,
            ((x + size * 0.25, y + size * 0.25), (x - size * 0.25, y + size * 0.25), (x - size * 0.25, y)))
    polygon(screen, color,
            ((x + size * 0.5, y + size * 0.5), (x + size * 0.25, y - size * 0.25), (x - size * 0.6, y - size * 0.5)))

    circle(screen, color, (x + size * 0.5, y + size * 0.5), size / 8)
    circle(screen, color, (x + size * 0.5, y + size * 0.6), size / 8)
    ellipse(screen, color, (x + size * 0.5, y + size * 0.5, size / 2, size / 8))
    ellipse(screen, color, (x + size * 0.5, y + size * 0.6, size / 2, size / 8))
    line(screen, YELLOW, (x + size, y + size * 0.55), (x + size * 1.2, y + size * 0.55), int(size * 0.03))
    line(screen, YELLOW, (x + size, y + size * 0.67), (x + size * 1.2, y + size * 0.67), int(size * 0.03))
    line(screen, YELLOW, (x + size, y + size * 0.55), (x + size * 1.2, y + size * 0.63), int(size * 0.03))
    line(screen, YELLOW, (x + size, y + size * 0.67), (x + size * 1.2, y + size * 0.73), int(size * 0.03))
    line(screen, YELLOW, (x + size, y + size * 0.55), (x + size * 1.2, y + size * 0.7), int(size * 0.03))
    line(screen, YELLOW, (x + size, y + size * 0.67), (x + size * 1.2, y + size * 0.8), int(size * 0.03))
    line(screen, YELLOW, (x + size, y + size * 0.55), (x + size, y + size * 0.65), int(size * 0.03))
    line(screen, YELLOW, (x + size, y + size * 0.67), (x + size, y + size * 0.77), int(size * 0.03))


pygame.init()

FPS = 30
width = 794
height = 1123
screen = pygame.display.set_mode((width, height))

# sky and water
rect(screen, (21, 21, 78), (0, 0, width, 116))
rect(screen, (141, 95, 211), (0, 116, width, 178 - 116))
rect(screen, (205, 87, 222), (0, 178, width, 282 - 178))
rect(screen, (222, 87, 170), (0, 282, width, 430 - 282))
rect(screen, (255, 99, 55), (0, 430, width, 552 - 430))
rect(screen, (00, 66, 80), (0, 552, width, height - 552))

# drawing objects
draw_gull(screen, WHITE, 400, 800, 160)

draw_fish(screen, LIGHT_BLUE, 600, 950, 80)

draw_bird(screen, WHITE, 100, 100, 150)
draw_bird(screen, WHITE, 150, 400, 150)
draw_bird(screen, WHITE, 500, 200, 150)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
