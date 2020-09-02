import pygame as pg
from pygame import gfxdraw
import numpy as np
import math
import random
import sys
import os
pg.init()


size = width, height = (1366,768)
hw, hh = width // 2, height // 2
win = pg.display.set_mode(size)
pg.display.set_caption("SIMULATION")
DIR = os.path.dirname(os.path.realpath(__file__))
IMGS_DIR = os.path.join(DIR, "imgs")
yellow = [(255,255,0), (255,232, 13)]
red = [(255,0,0), (149,28,28)]

class Sun:
    def __init__(self):
        self.img = pg.image.load(os.path.join(IMGS_DIR, "sun.png")).convert_alpha()
        self.surface = pg.transform.scale(self.img, (300,300))
        self.rect = self.surface.get_rect()
        self.rect.center = (hw, hh)
        self.angle = 0
        self.rotate_surface = self.surface
        self.locations = self.locationx, self.locationy = [x for x in range(self.rect.centerx + 1) if x >= 683 - 300],  [y for y in range(self.rect.centery+1) if y >= 384 - 300]
    def draw(self,win):
        win.blit(self.rotate_surface, self.rect)
    def update(self):
        self.rotate_surface = self.rot_center(self.surface, self.angle)    
    
    
    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pg.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image 






class Earth:
    def __init__(self):
        self.img = pg.image.load(os.path.join(IMGS_DIR, "earth.png")).convert_alpha()
        self.surface = pg.transform.scale(self.img, (150,150))
        self.rect = self.surface.get_rect()
        self.rect.center = (hw+ 100, hh + 500)
        self.rect.x, self.rect.y = (hw+ 100, hh + 500)
        self.angle = 0
        self.rotate_surface = self.surface
        self.ticks = 0
    def draw(self, win):
        win.blit(self.rotate_surface,self.rect)
        #Atmosphere
        pg.draw.circle(win, (5,207,252), (self.rect.x + 72, self.rect.y+ 72), 68, 1)
        
    def update(self):
        self.speed = 15
        self.ticks += 10
        self.rotate_surface = self.rot_center(self.surface, self.angle)
        if self.ticks >= 5000 and self.ticks <= 5010:
            self.rect.center = (hw + 100, hh + 500)
            self.rect.x, self.rect.y = (hw+ 100, hh + 500)
            self.ticks = 0
            self.angle = 0
        else:
            self.rect[0] += np.cos(np.radians(360 - self.angle)) * self.speed
            
            self.rect[1] += np.sin(np.radians(360- self.angle)) * self.speed
        


    
    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pg.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
        



class Gamma_Rays:
    def __init__(self, sun):
        self.pos = np.array([sun.rect.centerx, sun.rect.centery])
        self.distance = 0
        self.angle = 0
        self.img =pg.image.load(os.path.join(IMGS_DIR,"gamma ray.png")).convert_alpha()
        self.surface = pg.transform.scale(self.img, (30,30))
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = self.pos[0] , self.pos[1]
        self.rotate_surface = self.surface
        self.ticks = 0
        self.speed = 15
    def draw(self, win):
        win.blit(self.rotate_surface, self.pos)
        
    def effect(self, sun):
        self.ticks += 1
        self.distance += 15
        self.rotate_surface = self.rot_center(self.surface,self.angle)
    def disappear(self):
        return self.distance
          
        
    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pg.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
    def collision(self, atmosphere):
        gamma_mask = pg.mask.from_surface(self.img)
        atmosphere_mask = pg.mask.from_surface(atmosphere.img)
        
        gamma_offset = (self.pos[0] - atmosphere.rect.x, self.pos[1] - atmosphere.rect.y)
        
        c_point = atmosphere_mask.overlap(gamma_mask, gamma_offset)
        if c_point:
            return True
        return False

clock = pg.time.Clock()      
e = Earth()
s = Sun()
gamma_rays = []
rem_gamma = []
generator1 =  np.array([x for x in range(400) if x % 2== 0] )
generator2 =  np.array([x for x in range(400) if x % 3  == 0] )
generator4 =  np.array([x for x in range(400) if x % 5 == 0] )

def main():
    while True:
        add_gamma = False
        topright_place = False
        topleft_place = False
        bottomright_place = False
        bottomleft_place = False

        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit(0)
        win.fill((0,0,0))
        mouse_pressed = pg.mouse.get_pressed()
        if mouse_pressed == (1,0,0):
            add_gamma = True
            
            
        
        e.update()
        s.update()
        s.angle += 0.2
        e.angle += 2
        
        

        for x,g in enumerate(gamma_rays):
            g.effect(s)
            if x in generator1 and not g.collision(e) :
                topright_place = True
                g.pos[0] += 30
                g.pos[1] -= 30
                g.angle = -30
            elif x in generator2 and not g.collision(e) :
                bottomright_place = True
                g.pos[0] += 30
                g.pos[1] += 30
                g.angle = 225
            elif x in generator4 and not g.collision(e) :
                topleft_place = True
                g.pos[0] -= 30
                g.pos[1] -= 30
                g.angle = 30
            else:
                bottomleft_place = True
                g.pos[0] -= 30
                g.pos[1] += 30
                g.angle = -225
            
            if g.disappear() < 5000:            
                g.draw(win)
            
        for g in gamma_rays:
            if g.collision(e) and g.pos[1] >= e.rect.x:
                if topright_place:
                    g.pos[0] -= 30
                    g.pos[1] += 30
                    g.angle = -225
                elif topleft_place:
                    g.pos[0] += 30
                    g.pos[1] += 30
                    g.angle = 225
                elif bottomright_place:
                    g.pos[0] -= 30
                    g.pos[1] -= 30
                    g.angle = 30
                elif bottomleft_place:
                    g.pos[0] += 30
                    g.pos[1] -= 30
                    g.angle = -30
            if g.pos[0] > width or g.pos[0] < 0 or g.pos[1] > height or g.pos[1] < 0:
                rem_gamma.append(g)
                
        for r in rem_gamma:
            try:
                gamma_rays.remove(r)
            except ValueError:
                pass
            
        if add_gamma:
            gamma_rays.append(Gamma_Rays(s))
            for g in gamma_rays:
                g.pos[1] = random.randint(s.locationy[0] + 200, s.locationy[-1])
                g.pos[0] = random.randint(s.locationx[0] + 200, s.locationx[-1])
        e.draw(win)
        s.draw(win)
        pg.gfxdraw.circle(win, random.randint(15,width), random.randint(15,height), 1, random.choice(yellow))
        pg.gfxdraw.filled_circle(win, random.randint(15,width), random.randint(15,height), random.randint(1,2), random.choice(red))
        
        pg.display.flip()

        clock.tick(30)
if __name__ == "__main__":
    main()