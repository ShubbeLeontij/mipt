import pygame
from pygame.draw import *
import math

def draw_bird(screen, color, x, y, size, tilt=0):
    arc(screen, color, (x, y, size, size / 2), math.pi / 2, math.pi)
    arc(screen, color, (x - size, y, size, size / 2), 0, math.pi / 2)

def draw_fish(screen, color, x, y, size):
    pass

def draw_gull(screen, color, x, y, size):
    ellipse(screen, color, (x, y, size, size / 2))
    ellipse(screen, color, (x + size * 0.8, y + size * 0.1, size / 2, size / 4))
    ellipse(screen, color, (x + size, y, size / 2, size / 4))
    ellipse(screen, (0, 0, 0), (x + size * 1.3, y + size * 0.04, size / 10, size / 20))

pygame.init()

FPS = 30
width = 794
height = 1123
screen = pygame.display.set_mode((width, height))

rect(screen, (21, 21, 78), (0, 0, width, 116))
rect(screen, (141, 95, 211), (0, 116, width, 178 - 116))
rect(screen, (205, 87, 222), (0, 178, width, 282 - 178))
rect(screen, (222, 87, 170), (0, 282, width, 430 - 282))
rect(screen, (255, 99, 55), (0, 430, width, 552 - 430))
rect(screen, (00, 66, 80), (0, 552, width, height - 552))

draw_gull(screen, (255, 255, 255), 300, 300, 100)
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
