# Example file showing a basic pygame "game loop"
import pygame
from math import sin
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
frame = 0


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((45, 255, 227))



    pygame.draw.rect(screen,(255,0,0,),pygame.Rect(sin(frame/70)*100,0,100,100))
    pygame.draw.rect(screen,(255,0,0,),pygame.Rect(sin(frame/70)*100,0,100,100))




    # flip() the display to put your work on screen
    pygame.display.flip()

    frame += 1
    clock.tick(60)  # limits FPS to 60

pygame.quit()