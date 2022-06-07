import pygame as pg

pg.mixer.init()



#Game Setting
title = 'TP_Helen_M'
width = 1000
height = 690
height1 = 750
fps = 30


white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
brown = (205, 133, 63)



moon = pg.image.load('Moon.png')
apple = pg.image.load('Apple.png')
checkpoint = pg.image.load('Checkpoint.png')
thornImage = pg.image.load('Thorn.png')
enemy = pg.image.load('Enemy_R.png')
start2 = pg.image.load('Start2.jpg')
gameover = pg.image.load('Gameover.png')
win = pg.image.load('Win.jpg')



shootSound = pg.mixer.Sound('Shoot.wav')
checkSound = pg.mixer.Sound('Check.wav')

music = pg.mixer.music.load('music.mp3')




player_grav = 1