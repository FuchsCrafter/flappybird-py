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

mdflap_img = pygame.transform.scale(pygame.image.load("assets/yellowbird-midflap.png"), (50, 50))
mdflap_rect = mdflap_img.get_rect()
mdflap_rect.x = 100

dnflap_img = pygame.transform.scale(pygame.image.load("assets/yellowbird-downflap.png"), (50, 50))
dnflap_rect = dnflap_img.get_rect()
dnflap_rect.x = 100

upflap_img = pygame.transform.scale(pygame.image.load("assets/yellowbird-upflap.png"), (50, 50))
upflap_rect = upflap_img.get_rect()
upflap_rect.x = 100

background_img = pygame.transform.scale(pygame.image.load("assets/background.png"), (HEIGHT/512 * 288, HEIGHT))
background_rect = background_img.get_rect()

current_img =  upflap_img
current_rect = upflap_rect


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
frame = 0




class Tube():
    def __init__(self, y, gap_height=250): # init tubes
        self.color = (20,200,10)

        self.texture = pygame.image.load("assets/tube.png")


        self.wid = 50
        self.fac = gap_height

        self.y = y

        # define top texture
        self.img_top = pygame.transform.rotate(pygame.transform.scale(self.texture, (self.wid, self.fac+self.y)), 180)
        self.rec_top = self.img_top.get_rect()

        # define bottom texture
        self.img_dwn = pygame.transform.flip(pygame.transform.scale(self.texture, (self.wid, self.fac-self.y)), True, False)
        self.rec_dwn = self.img_top.get_rect() 
        
        self.x = WIDTH-self.wid

        # distance from top
        self.rec_top.top = 0
        self.rec_dwn.top = HEIGHT-self.fac+self.y

        # distance from left
        self.rec_top.left = WIDTH-self.wid
        self.rec_dwn.left = WIDTH-self.wid
    
    def draw(self): # handles drawing
        screen.blit(self.img_top, self.rec_top)
        screen.blit(self.img_dwn, self.rec_dwn)

    def set_x(self, x): # handles setting x
        self.x = x
        self.rec_top.x = x
        self.rec_dwn.x = x
    
    def reload_recs(self):
        self.rec_top = pygame.Rect(WIDTH-self.wid, 0                     , self.wid, self.fac+self.y)
        self.rec_dwn = pygame.Rect(WIDTH-self.wid, HEIGHT-self.fac+self.y, self.wid, self.fac-self.y)
    
    def decrease_x(self, x=1): # handles decreasing x for moving tubes
        self.x -= x
        self.rec_top.x -= x
        self.rec_dwn.x -= x


tubez = Tube(0)
curr_y = 0
currynormalized = (HEIGHT/2) + curr_y

player = 100
jumping = 0
jumpFactor = 0.2
score = 0

while running:

    # handle quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            jumping = -jumpFactor*30
            player += jumping
            jumping += jumpFactor


    # handle player on the ground
    if player < HEIGHT-50:
        player += jumping
        jumping += jumpFactor
    
    if player > HEIGHT-50:
        player = HEIGHT - 50

    if player <= 0:
        jumping = 0
        player = 1

    if jumping > 1:
        current_img = upflap_img
        current_rect = upflap_rect
    elif jumping > 0:
        current_img = mdflap_img
        current_rect = mdflap_rect
    else:
        current_img = dnflap_img
        current_rect = dnflap_rect

    # clear display
    screen.fill((45, 255, 227))

    # set background
    _ = -(frame % background_rect.width)
    background_rect.x = _
    while _ < WIDTH*2:
        screen.blit(background_img, background_rect)
        _ += background_rect.width
        background_rect.x = _


    # handle tubes
    tubez.draw()
    tubez.decrease_x(5 + min(score/5, 12))

    # draw player
    current_rect.y = player
    screen.blit(current_img, current_rect)

    # handle score display
    text_surface = deffont.render(f'Score: {score}', False, (0, 0, 0))
    screen.blit(text_surface, (0,0))

    # flip display
    pygame.display.flip()

    # handle Game over
    if tubez.x <=150 and tubez.x >=100:
        if player>currynormalized+tubez.fac/2 or player<currynormalized-tubez.fac/2:
            print("GAME OVER")

            screen.fill((0, 0, 0))
            game_over1 = deffont.render(f'GAME OVER!', False, (255, 255, 255))
            game_over2 = deffont.render(f'Score: {score}', False, (255, 255, 255))
            game_over3 = deffont.render(f'Game will close in 3s', False, (255, 255, 255))

            screen.blit(game_over1, (WIDTH/2, HEIGHT/2-15))
            screen.blit(game_over2, (WIDTH/2, HEIGHT/2+15))
            screen.blit(game_over3, (WIDTH/2, HEIGHT/2+45))

            pygame.display.flip()

            time.sleep(3)
            running = False

    # handle tubes reaching left screen border
    if (tubez.x < 0-tubez.wid):
        del tubez
        score += 1
        curr_y = rnd.randint(-150, 150)
        tubez = Tube(curr_y)
        currynormalized = (HEIGHT/2) + curr_y


    frame += 1
    clock.tick(60)  # limits FPS to 60



pygame.quit()