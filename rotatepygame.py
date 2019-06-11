import pygame
import sys
import time

def rotate45(gameObject, rotations={}):
    r = rotations.get(gameObject,0) + 45
    rotations[gameObject] = r
    return pygame.transform.rotate(gameObject, r)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    Tardis = pygame.image.load("/home/caratred/112295153.jpg")
    Tardis.set_colorkey((255, 0, 0))

    tardis_angle = 0
    while True:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # update game state
        tardis_angle = (tardis_angle + 45) % 360

        # draw
        screen.fill( (0,0,0) )
        screen.blit(pygame.transform.rotate(Tardis, tardis_angle), (800,600))
        pygame.image.save(Tardis,'/home/caratred/rotatedimage.jpeg')

main()
