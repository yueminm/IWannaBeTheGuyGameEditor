import pygame as pg
from settings import *

vec = pg.math.Vector2



class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    def get_image(self, x, y, width, height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        image = pg.transform.scale(image,(width // 5 * 2, width // 5 * 2))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.pos = vec(width / 2, height / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(7, 4, 92, 84),
                                self.game.spritesheet.get_image(116, 4, 92, 84),
                                self.game.spritesheet.get_image(229, 5, 96, 84),
                                self.game.spritesheet.get_image(337, 9, 94, 80)]
        self.walking_frames_l = [self.game.spritesheet.get_image(2, 97, 100, 84),
                                 self.game.spritesheet.get_image(108, 98, 100, 84),
                                 self.game.spritesheet.get_image(216, 98, 92, 84),
                                 self.game.spritesheet.get_image(313, 100, 96, 84),
                                 self.game.spritesheet.get_image(411, 102, 100, 84)]
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
        if keys[pg.K_RIGHT]:
            self.pos.x += 5
        
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > width:
            self.pos.x = width
        if self.pos.x < 0:
            self.pos.x = 0
        
        self.rect.midbottom = self.pos
    
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -15

    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]
             
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

