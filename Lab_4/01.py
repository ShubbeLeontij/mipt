import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

circle(screen, (255, 255, 0), (200, 200), 150)  # big yellow circle

circle(screen, (255, 0, 0), (275, 150), 20)  # right eye
circle(screen, (255, 0, 0), (125, 150), 40)  # left eye
circle(screen, (0, 0, 0), (275, 150), 10)  # right apple of the eye
circle(screen, (0, 0, 0), (125, 150), 20)  # left apple of the eye

line(screen, (0, 0, 0), (300, 100), (225, 150), 20)  # right eyebrow
line(screen, (0, 0, 0), (100, 90), (175, 130), 10)  # left eyebrow
rect(screen, (0, 0, 0), (100, 275, 200, 20))  # black mouth


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()