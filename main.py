# Example file showing a basic pygame "game loop"
import pygame
from math import sin, cos
import random as rnd
import time
# pygame setup
pygame.init()
pygame.font.init()

deffont = pygame.font.SysFont('Arial', 30)


WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
frame = 0




class Tube():
    def __init__(self, y, gap_height=200): 
        self.color = (50,200,0)

        wid = 50

        self.rec_top = pygame.Rect(WIDTH-wid, 0           , wid, 230+y)
        self.rec_dwn = pygame.Rect(WIDTH-wid, HEIGHT-230+y, wid, 230-y)

        self.x = WIDTH-wid
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rec_top)
        pygame.draw.rect(screen, self.color, self.rec_dwn)

    def set_x(self, x):
        self.x = x
        self.rec_top.x = x
        self.rec_dwn.x = x
    
    def decrease_x(self, x=1):
        self.x -= x
        self.rec_top.x -= x
        self.rec_dwn.x -= x


tubez = Tube(0)
curr_y = 0
currynormalized = (HEIGHT/2) + curr_y



player = 100
jumping = 0

jumpFactor = 0.14
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_pressed(num_buttons=3)[0]:
        jumping = -jumpFactor*30
        player += jumping
        jumping += jumpFactor

    if player < HEIGHT-50:
        player += jumping
        jumping += jumpFactor

    screen.fill((45, 255, 227))

    tubez.draw()
    tubez.decrease_x(5)

    pygame.draw.rect(screen,(255,0,0),pygame.Rect(100,player,50,50))

    text_surface = deffont.render(f'Score: {score}', False, (0, 0, 0))
    screen.blit(text_surface, (0,0))


    pygame.display.flip()

    if tubez.x <=150 and tubez.x >=100:
        if player>currynormalized+100 or player<currynormalized-100:
            print("GAME OVER")

            screen.fill((0, 0, 0))
            game_over1 = deffont.render(f'GAME OVER!', False, (255, 255, 255))
            game_over2 = deffont.render(f'Score: {score}', False, (255, 255, 255))
            game_over3 = deffont.render(f'Game will close in 10s', False, (255, 255, 255))

            screen.blit(game_over1, (WIDTH/2, HEIGHT/2-15))
            screen.blit(game_over2, (WIDTH/2, HEIGHT/2+15))
            screen.blit(game_over3, (WIDTH/2, HEIGHT/2+45))



            pygame.display.flip()

            time.sleep(10)
            running = False


    if (tubez.x <= 0):
        del tubez
        score += 1
        curr_y = rnd.randint(-150, 150)
        tubez = Tube(curr_y)
        currynormalized = (HEIGHT/2) + curr_y


    frame += 1
    clock.tick(60)  # limits FPS to 60



pygame.quit()