import pygame as pg
import sys
from settings import *
from sprites import *

#basic structure learned from: http://blog.lukasperaza.com/getting-started-with-pygame/
#additional functions learned from: https://www.youtube.com/watch?v=uWvb3QzA48c&list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq&index=1
#additional functions learned from: https://www.youtube.com/watch?v=2BikxsbkuIU

#images downloaded from: https://www.spriters-resource.com/pc_computer/iwannabetheguy/sheet/31495/
#images downloaded from: https://www.spriters-resource.com/pc_computer/iwannabetheguy/sheet/31043/
#images downloaded from: http://projectcrusade.forumotion.com/t3884-the-kid-i-wanna-be-the-guy-discussion-whazawhat
#images downloaded from: https://kayin.itch.io/iwbtg

#soundeffects downloaded from: https://www.sounds-resource.com/pc_computer/iwannabethebestguy4/sound/16380/
#background music downloaded from: https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/sound-effects-music/



class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((width, height1))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()
        self.font = pg.font.SysFont('comicsans', 50)
        self.font2 = pg.font.SysFont('comicsans', 30)
        self.font3 = pg.font.SysFont('comicsans', 20)
        self.death = 0
        self.win = False
        self.lose = False
        self.time = 0
        self.platform_list = {(0, height - 30, width, 30)}
        self.thorn_list = set()
        self.enemy_list = set()
        self.moon_list = set()
        self.checkpoint_list = set()
        self.apple_list = set()
        self.mousePos = []
        self.x = 10
        self.y = height - 90



    def load_data(self):
        self.spritesheet = Spritesheet('IWBTG.png')
        self.spritesheet1 = Spritesheet('Enemy.png')



    def new(self):
        self.win = False
        self.lose = False

        self.all_sprites = pg.sprite.Group()

        self.checkpoints = pg.sprite.Group()
        for checkpoint in self.checkpoint_list:
            c = Checkpoint(*checkpoint)
            self.all_sprites.add(c)
            self.checkpoints.add(c)

        self.player = Player(self, self.x, self.y)
        self. all_sprites.add(self.player)

        self.bullets = pg.sprite.Group()
        
        self.platforms = pg.sprite.Group()
        for plat in self.platform_list:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        self.moons = pg.sprite.Group()
        for moon in self.moon_list:
            m = Moon(*moon)
            self.all_sprites.add(m)
            self.moons.add(m)

        self.thorns = pg.sprite.Group()
        for thorn in self.thorn_list:
            t = Thorn(*thorn)
            self.all_sprites.add(t)
            self.thorns.add(t)

        self.enemies = pg.sprite.Group()
        for enemy in self.enemy_list:
            e = Enemy(*enemy)
            self.all_sprites.add(e)
            self.enemies.add(e)

        self.apples = pg.sprite.Group()
        for apple in self.apple_list:
            a = Apple(*apple)
            self.all_sprites.add(a)
            self.apples.add(a)
  
        self.run1()
    


    def edit(self):
        self.all_sprites = pg.sprite.Group()

        self.checkpoints = pg.sprite.Group()
        for checkpoint in self.checkpoint_list:
            c = Checkpoint(*checkpoint)
            self.all_sprites.add(c)
            self.checkpoints.add(c)

        self.player = Player(self, self.x, self.y)
        self. all_sprites.add(self.player)

        self.bullets = pg.sprite.Group()
        
        self.platforms = pg.sprite.Group()
        for plat in self.platform_list:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        self.moons = pg.sprite.Group()
        for moon in self.moon_list:
            m = Moon(*moon)
            self.all_sprites.add(m)
            self.moons.add(m)

        self.thorns = pg.sprite.Group()
        for thorn in self.thorn_list:
            t = Thorn(*thorn)
            self.all_sprites.add(t)
            self.thorns.add(t)

        self.enemies = pg.sprite.Group()
        for enemy in self.enemy_list:
            e = Enemy(*enemy)
            self.all_sprites.add(e)
            self.enemies.add(e)

        self.apples = pg.sprite.Group()
  
        self.run2()



    def run1(self):
        self.playing = True
        while self.playing:
            self.clock.tick(fps)
            self.time += 0.03
            self.time2 = '%.3f' % self.time
            self.events()
            self.update1()
            if self.win == True:
                self.show_win_screen()
            if self.lose == True:
                self.show_go_screen()
    


    def run2(self):
        self.editing = True
        while self.editing:
            self.events()
            self.update2()
            keys = pg.key.get_pressed()
            if keys[pg.K_p]:
                g.new()



    def update1(self):
        self.all_sprites.update()

        hit_player_plat = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hit_player_plat:
            if self.player.vel.y >= 0:
                self.player.pos.y = hit_player_plat[0].rect.top
                self.player.vel.y = 0
            else:
                self.player.rect.y = hit_player_plat[0].rect.bottom
                self.player.vel.y = 0
                self.player.jumptime = 0
            

        if not len(self.bullets) == 0:
            for bullet in self.bullets:
                hit_bullet_enemy = pg.sprite.spritecollide(bullet, self.enemies, False)
                if hit_bullet_enemy:
                    hit_bullet_enemy[0].hit()
                    self.bullets.remove(bullet)
                    self.all_sprites.remove(bullet)

        if not len(self.bullets) == 0:
            for bullet in self.bullets:
                hit_bullet_checkpoint = pg.sprite.spritecollide(bullet, self.checkpoints, True)
                if hit_bullet_checkpoint:
                    checkSound.play()
                    self.x = hit_bullet_checkpoint[0].rect.x
                    self.y = hit_bullet_checkpoint[0].rect.y
    
        hit_player_enemy = pg.sprite.spritecollide(self.player, self.enemies, False)
        if hit_player_enemy:
            self.death += 1
            self.playing = False
            self.lose = True
        
        hit_player_moon = pg.sprite.spritecollide(self.player, self.moons, False)
        if hit_player_moon:
            self.playing = False
            self.win = True
        
        hit_player_thorn = pg.sprite.spritecollide(self.player, self.thorns, False)
        if hit_player_thorn:
            self.death += 1
            self.playing = False
            self.lose = True
        
        hit_player_apple = pg.sprite.spritecollide(self.player, self.apples, False)
        if hit_player_apple:
            self.death += 1
            self.playing = False
            self.lose = True
        
        keys = pg.key.get_pressed()
        if keys[pg.K_e]:
            self.time = 0
            self.death = 0
            self.x = 10
            self.y = height - 90
            self.edit()
        
        self.draw1()
    


    def update2(self):
        self.all_sprites.update()

        if len(self.mousePos) > 1:
            if 210 <= self.mousePos[-2][0] <= 246 and \
                height1 - 50 <= self.mousePos[-2][1] <= height1 - 14:
                self.platform_list.add((self.mousePos[-1][0]-20, self.mousePos[-1][1]-15, 40, 30))
                for plat in self.platform_list:
                    p = Platform(*plat)
                    self.all_sprites.add(p)
                    self.platforms.add(p)
            
            if 280 <= self.mousePos[-2][0] <= 320 and \
                height1 - 50 <= self.mousePos[-2][1] <= height1 - 10:
                self.thorn_list.add((self.mousePos[-1][0]-20, self.mousePos[-1][1]-20))
                for thorn in self.thorn_list:
                    t = Thorn(*thorn)
                    self.all_sprites.add(t)
                    self.thorns.add(t)
            
            if 350 <= self.mousePos[-2][0] <= 380 and \
                height1 - 50 <= self.mousePos[-2][1] <= height1:
                self.enemy_list.add((self, self.mousePos[-1][1]-25, self.mousePos[-1][0]-15))
                for enemy1 in self.enemy_list:
                    e = Enemy(*enemy1)
                    self.enemies.add(e)
                    self.screen.blit(enemy, (self.mousePos[-1][1]-15, self.mousePos[-1][1]-25))

            if 60 <= self.mousePos[-2][0] <= 112 and \
                height1 - 55 <= self.mousePos[-2][1] <= height1 - 3:
                self.moon_list.add((self.mousePos[-1][0]-26, self.mousePos[-1][1]-26))
                for moon in self.moon_list:
                    m = Moon(*moon)
                    self.all_sprites.add(m)
                    self.moons.add(m)
            
            if 140 <= self.mousePos[-2][0] <= 168 and \
                height1 - 50 <= self.mousePos[-2][1] <= height1 - 18:
                self.checkpoint_list.add((self.mousePos[-1][0]-12, self.mousePos[-1][1]-16))
                for checkpoint in self.checkpoint_list:
                    c = Checkpoint(*checkpoint)
                    self.all_sprites.add(c)
                    self.checkpoints.add(c)
            
            if 420 <= self.mousePos[-2][0] <= 444 and \
                height1 - 45 <= self.mousePos[-2][1] <= height1 - 21:
                self.apple_list.add((self, self.mousePos[-1][0]-12, self.mousePos[-1][1]-12))
                for applePos in self.apple_list:
                    a = Apple(*applePos)
                    self.all_sprites.add(a)
                    self.apples.add(a)
                    self.screen.blit(apple, (self.mousePos[-1][0]-12, self.mousePos[-1][1]-12))
        
        hit_player_plat = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hit_player_plat:
            if self.player.rect.y >= hit_player_plat[0].rect.bottom \
                and self.player.rect.x + self.player.rect.width <= hit_player_plat[0].rect.x + \
                    hit_player_plat[0].rect.width:
                self.player.vel.y = 0
                self.player.jumptime = 0
            elif self.player.vel.y > 0:
                self.player.pos.y = hit_player_plat[0].rect.top
                self.player.vel.y = 0
            elif self.player.vel.y <= 0:
                self.player.vel.y = 0
                self.player.jumptime = 0
        
        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            self.platform_list = {(0, height - 30, width, 30)}
            self.thorn_list = set()
            self.enemy_list = set()
            self.moon_list = set()
            self.checkpoint_list = set()
            self.apple_list = set()
            self.mousePos = []
            self.time = 0
            self.edit()

        self.draw2() 
        
    

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    shootSound.play()
                    pos = self.player.rect.center
                    if self.player.right:
                        d = Bullet(self, pos, 'right')
                        self.all_sprites.add(d)
                        self.bullets.add(d)
                    if self.player.left:
                        d = Bullet(self, pos, 'left')
                        self.all_sprites.add(d)
                        self.bullets.add(d)

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pos()
                self.mousePos.append(mouse)
                
                

    def draw1(self):
        self.screen.fill(black)
        self.all_sprites.draw(self.screen)
        deathCounter = self.font.render('Death: ' + str(self.death), 1, white)
        self.screen.blit(deathCounter, (600, 10))
        timer = self.font.render('Time: ' + str(self.time2) + 's', 1, white)
        self.screen.blit(timer, (600, 55))
        notice = self.font2.render('Press E to go back to the editor', 1, white)
        self.screen.blit(notice, (10, 10))
        guide1 = self.font2.render('Press ARROW KEYS to move', 1, white)
        self.screen.blit(guide1, (10, 50))
        guide2 = self.font2.render('Press SPACE to shoot', 1, white)
        self.screen.blit(guide2, (10, 90))



        pg.display.flip()
    


    def draw2(self):
        self.screen.fill(black)
        self.all_sprites.draw(self.screen)
        pg.draw.rect(self.screen, white, (0, height1 - 60, width, 60))
        self.screen.blit(moon, (60, height1 - 55))
        self.screen.blit(checkpoint, (140, height1 - 50))
        pg.draw.rect(self.screen, brown, (210, height1 - 50, 40, 30))
        self.screen.blit(thornImage, (280, height1 - 50))
        self.screen.blit(enemy, (350, height1 - 50))
        self.screen.blit(apple, (420, height1 - 45))
        notice1 = self.font2.render('Click on the elements below to place them on the screen', 1, white)
        self.screen.blit(notice1, (10, 10))
        notice2 = self.font2.render('Press D to clear the screen', 1, white)
        self.screen.blit(notice2, (10, 50))
        notice3 = self.font2.render('Press P to start playing', 1, white)
        self.screen.blit(notice3, (10, 90))        

        if len(self.mousePos) >= 1:
            if 280 <= self.mousePos[-1][0] <= 320 and \
                height1 - 50 <= self.mousePos[-1][1] <= height1 - 10:
                mouse = pg.mouse.get_pos()
                self.screen.blit(thornImage, (mouse[0] - 20, mouse[1] - 20))

            if 210 <= self.mousePos[-1][0] <= 246 and \
                height1 - 50 <= self.mousePos[-1][1] <= height1 - 14:
                mouse = pg.mouse.get_pos()
                pg.draw.rect(self.screen, brown, (mouse[0] - 20, mouse[1] - 15, 40, 30))
            
            if 350 <= self.mousePos[-1][0] <= 380 and \
                height1 - 50 <= self.mousePos[-1][1] <= height1:
                mouse = pg.mouse.get_pos()
                self.screen.blit(enemy, (mouse[0] - 15, mouse[1] - 25))
            
            if 60 <= self.mousePos[-1][0] <= 112 and \
                height1 - 55 <= self.mousePos[-1][1] <= height1 - 3:
                mouse = pg.mouse.get_pos()
                self.screen.blit(moon, (mouse[0] - 26, mouse[1] - 26))
                
            if 140 <= self.mousePos[-1][0] <= 168 and \
                height1 - 50 <= self.mousePos[-1][1] <= height1 - 18:
                mouse = pg.mouse.get_pos()
                self.screen.blit(checkpoint, (mouse[0] - 12, mouse[1] - 16))
            
            if 420 <= self.mousePos[-1][0] <= 444 and \
                height1 - 45 <= self.mousePos[-1][1] <= height1 - 21:
                mouse = pg.mouse.get_pos()
                self.screen.blit(apple, (mouse[0] - 12, mouse[1] - 12))
        '''
        if len(self.mousePos) >= 2: 
            if 350 <= self.mousePos[-2][0] <= 380 and \
                height1 - 50 <= self.mousePos[-1][1] <= height1:
                self.screen.blit(enemy, (self.mousePos[-1][1]-15, self.mousePos[-1][1]-25))
        '''
        pg.display.flip()



    def show_start_screen(self):
        self.screen.fill(black)
        self.screen.blit(start2, (0, 100))
        welcome2 = self.font2.render('Press any key to start editing your own level!', 1, white)
        self.screen.blit(welcome2, (50, 330))
        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    waiting = False
                    self.editing = True



    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(black)
        self.screen.blit(gameover, (120, 100))
        #notice = self.font.render('GAME OVER', 1, white)
        restart = self.font.render('Press any key to restart', 1, white)
        #self.screen.blit(notice, (200, 200))
        self.screen.blit(restart, (300, 300))
        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    self.new()
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
    


    def show_win_screen(self):
        self.screen.fill(black)
        self.screen.blit(win, (191, 0))
        deathCounter = self.font.render('Death: ' + str(self.death), 1, white)
        self.screen.blit(deathCounter, (400, 500))
        timer = self.font.render('Time: ' + str(self.time2) + 's', 1, white)
        self.screen.blit(timer, (400, 550))
        notice = self.font.render('Press any key to start a new round', 1, white)
        self.screen.blit(notice, (230, 600))
        pg.display.flip()
        self.time = 0
        self.death = 0
        self.x = 10
        self.y = height - 90
        self.wait_for_key()



    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    waiting = False
                    self.editing = True
                    self.playing = False
                    self.edit()
            


g = Game()
g.show_start_screen()
while g.running:
    pg.mixer.music.play(-1)
    g.edit()

        

pg.quit()