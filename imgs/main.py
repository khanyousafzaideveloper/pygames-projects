import pygame
import math
import time

GRASS = pygame.image.load("imgs/grass.jpg")
TRACK = pygame.image.load("imgs/track.png")
TRACK_BORDER = pygame.image.load("imgs/track-border.png")
FINISH = pygame.image.load("imgs/finish.png")
RED_CAR = pygame.image.load("imgs/red-car.png")
GREEN_CAR = pygame.image.load("imgs/green-car.png")

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Racing Game!")
FPS = 60

run = True
clock = pygame.time.Clock()

while run:
    clock.tick(FPS)

    WIN.blit(GRASS, (0, 0))
    WIN.blit(TRACK, (0,0))
    WIN.blit(FINISH, (0,0))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break


pygame.quit()        

