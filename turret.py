import pygame as pg
import constants as c
import math

class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheet, pos):
        pg.sprite.Sprite.__init__(self)
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.range = 280
        self.cooldown = 1500
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None

        # position variables


        # animation variables
        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        # update image    
        self.angle = 90  
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        

        # create transparent circle showeing image
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
    


    def load_images(self):
        # extract images from spritesheet
        size = self.sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self, enemy_group):
        # if target is in range (is picked by self.picked) then fire animation
        if self.target:
            self.play_animation()
        else:
            # search for new target once turret cools down
            if pg.time.get_ticks() - self.last_shot > self.cooldown:
                self.pick_target(enemy_group)
            
    def pick_target(self, enemy_group):
        # find an enemyto target
        x_dist = 0
        y_dist = 0
        # check distance to enemy to see if it is in range
        for enemy in enemy_group:
            x_dist =  enemy.pos[0] - self.pos[0]
            y_dist = enemy.pos[1] - self.pos[1]
            dist = math.sqrt(x_dist**2 + y_dist **2)
            if dist < self.range:
                self.target = enemy
                self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                # print("shooting")

    def play_animation(self):
        # update image
        self.original_image = self.animation_list[self.frame_index]
        self.frame_index += 1
        # check if enought ime has passed saince the last update
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            # self.frame_index += 1
            # check if the animation has finished and reset to idle
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                # record completed time and clear target so cooldown can begin

                # self.last_shot = pg.time.get_ticks()
                self.target = None


    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
           
