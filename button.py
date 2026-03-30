import pygame as pg

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self rect.topleft = (x,y)
    
    def draw(self, surface):
        # get mouse position
    
        # check mouseover and clicked conditions

        # draw button on screen