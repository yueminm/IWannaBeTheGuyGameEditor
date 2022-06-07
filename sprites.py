import pygame as pg
from settings import *
import sys

vec = pg.math.Vector2

#basic structure learned from: http://blog.lukasperaza.com/getting-started-with-pygame/
#additional functions learned from: https://www.youtube.com/watch?v=uWvb3QzA48c&list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq&index=1

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        image = pg.transform.scale(image,(width // 5 * 2, height // 5 * 2))
        return image



class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.x = x
        self.y = y
        self.load_images()
        self.image = self.standing_frames_r[0]
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.pos = vec(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.left = False
        self.right = False
        self.jumptime = 0

    def load_images(self):
        self.standing_frames_l = [self.game.spritesheet.get_image(7, 4, 92, 84),
                                  self.game.spritesheet.get_image(116, 4, 92, 84),
                                  self.game.spritesheet.get_image(229, 5, 96, 84),
                                  self.game.spritesheet.get_image(337, 9, 94, 80)]
        for frame in self.standing_frames_l:
            frame.set_colorkey(white)
        self.standing_frames_r = []
        for frame in self.standing_frames_l:
            self.standing_frames_r.append(pg.transform.flip(frame, True, False))
        self.walking_frames_l = [self.game.spritesheet.get_image(2, 97, 100, 84),
                                 self.game.spritesheet.get_image(108, 98, 100, 84),
                                 self.game.spritesheet.get_image(216, 98, 92, 84),
                                 self.game.spritesheet.get_image(313, 100, 96, 84),
                                 self.game.spritesheet.get_image(411, 102, 100, 84)]
        for frame in self.walking_frames_l:
            frame.set_colorkey(white)
        self.walking_frames_r = []
        for frame in self.walking_frames_l:
            self.walking_frames_r.append(pg.transform.flip(frame, True, False))
        
        self.jumping_frame = self.game.spritesheet.get_image(7, 213, 100, 80)

    def update(self):
        self.animate()
        self.acc = vec(0, player_grav)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.pos.x -= 5
            self.walking = True
            self.left = True
            self.right = False
        if keys[pg.K_RIGHT]:
            self.pos.x += 5
            self.walking = True
            self.left = False
            self.right = True
        if keys[pg.QUIT]:
            pg.quit()
        else:
            self.walking = False
        
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > width - self.rect.width // 2:
            self.pos.x = width - self.rect.width // 2
        if self.pos.x < self.rect.width // 2:
            self.pos.x = self.rect.width // 2
        
        self.rect.midbottom = self.pos
    
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.jumptime = 1
            self.vel.y = -13
        elif (not hits) and self.jumptime == 1:
            self.vel.y = -13
            self.jumptime += 1

    def animate(self):
        now = pg.time.get_ticks()

        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                bottom = self.rect.bottom
                if self.right:
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames_l)
                bottom = self.rect.bottom
                if self.right:
                    self.image = self.standing_frames_r[self.current_frame]
                if self.left:
                    self.image = self.standing_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, facing):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.x = pos[0]
        self.y = pos[1]
        self.facing = facing
        self.image = pg.Surface((10, 10), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        pg.draw.circle(self.image, yellow, (5, 5), 5)
    
    def update(self):
        if self.facing == 'left':
            self.rect.x -= 10
        elif self.facing == 'right':
            self.rect.x += 10



class Enemy(pg.sprite.Sprite):
    def __init__(self, game, level, leftEdge):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.leftEdge = leftEdge
        self.rightEdge = leftEdge + 100
        self.level = level
        self.load_images()
        self.image = pg.Surface((25, 55), pg.SRCALPHA)
        image = self.walking_frames_r[0]
        self.image.blit(image, (0, 15))
        self.rect = self.image.get_rect()
        self.rect.x = self.leftEdge
        self.rect.y = self.level
        self.right = True
        self.left = False
        self.last_update = 0
        self.current_frame = 0
        self.visible = True
        self.health = 10
    
    def load_images(self):
        self.walking_frames_r = [self.game.spritesheet1.get_image(0, 0, 57, 100),
                                 self.game.spritesheet1.get_image(60, 0, 57, 100),
                                 self.game.spritesheet1.get_image(120, 0, 57, 100),
                                 self.game.spritesheet1.get_image(180, 0, 57, 100)]
        for frame in self.walking_frames_r:
            frame.set_colorkey(black)
        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            self.walking_frames_l.append(pg.transform.flip(frame, True, False))
    
    def update(self):
        self.animate()
        if self.visible:
            if self.right:
                self.rect.x += 3
                if self.rect.x > self.rightEdge - self.rect.width // 2:
                    self.rect.x = self.rightEdge - self.rect.width // 2
                    self.left = True
                    self.right = False
            elif self.left:
                self.rect.x -= 3
                if self.rect.x < self.leftEdge + self.rect.width // 2:
                    self.rect.x = self.leftEdge + self.rect.width // 2
                    self.left = False
                    self.right = True
            pg.draw.rect(self.image, red, (0, 0, 25, 4))
            pg.draw.rect(self.image, green, (0, 0, self.health * 2.5, 4))

        else:
            self.rect.x = -100
            self.rect.y = -100
    
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.walking_frames_r)
            if self.right:
                self.image = self.walking_frames_r[self.current_frame]
            elif self.left:
                self.image = self.walking_frames_l[self.current_frame]
    
    def hit(self):
        if self.health > 0:
            self.health -= 1
            if self.health == 0:
                self.visible = False
                self.rect.x = -100
                self.rect.y = -100

    

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(brown)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



class Moon(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((52, 52))
        image = pg.image.load('Moon.png')
        self.image.blit(image, (0, 0))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



class Thorn(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40, 40))
        image = pg.image.load('Thorn.png')
        self.image.set_colorkey(black)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



class Apple(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((24, 24))
        image = pg.image.load('Apple.png')
        self.game = game
        self.image.set_colorkey(black)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.falling = False
    
    def update(self):
        if self.rect.x - 50 <= self.game.player.rect.x <= self.rect.x + 24:
            self.falling = True
        if self.falling:
            self.rect.y += 30
    


class Checkpoint(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((28, 32))
        image = pg.image.load('Checkpoint.png')
        self.image.set_colorkey(black)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y