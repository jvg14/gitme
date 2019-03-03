#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 16:02:04 2019

@author: johanngudmundsson
"""

import pygame
from pygame import *

# initialize game engine
pygame.init()

window_width=1000
window_height=1800

animation_increment=10
clock_tick_rate=20

# Open a window
size = (window_width, window_height)
screen = pygame.display.set_mode(size)

# Set title to the window
pygame.display.set_caption("THOR GAMES")

dead=False

clock = pygame.time.Clock()
background_image = pygame.image.load("btb_valmynd.png").convert()
click_sound = pygame.mixer.Sound("sound.ogg")
click_sound.play()

while(dead==False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True

    screen.blit(background_image, [0, 0])
    

    pygame.display.flip()
    clock.tick(clock_tick_rate)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (50, 70, 90)


#Fonts
FONT = pygame.font.SysFont ("Times New Roman", 60)


text1 = FONT.render("START", True, WHITE)
text2 = FONT.render("OPTIONS", True, WHITE)
text3 = FONT.render("ABOUT", True, WHITE)

#Buttons
rect1 = pygame.Rect(300,300,205,80)
rect2 = pygame.Rect(300,400,205,80)
rect3 = pygame.Rect(300,500,205,80)

buttons = [
    [text1, rect1, BLACK],
    [text2, rect2, BLACK],
    [text3, rect3, BLACK],
    ]

running = False

def game_intro():
    while not running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    if button[1].collidepoint(event.pos):
                        button[2] = HOVER_COLOR
                    else:
                        button[2] = BLACK

                        screen.blit(bg, (0, 0))
        for text, rect, color in buttons:
            pygame.draw.rect(screen, color, rect)
            screen.blit(text, rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if rect1.collidepoint(event.pos):
                        screen.fill((0, 0, 0))
                    elif rect2.collidepoint(event.pos):
                        print ('options')
                    elif rect3.collidepoint(event.pos):
                        print ('about')

            if event.type == KEYDOWN:
                if (event.key == K_UP):
                    print ("UP was pressed")
                elif (event.key == K_DOWN):
                    print ("DOWN was pressed")
                elif (event.key == K_w):
                    print ("W was pressed")
                elif (event.key == K_s):
                    print ("S was pressed")
                else:
                    print ("error")




            pygame.display.flip()
            clock.tick(60)



game_intro()
pygame.quit()