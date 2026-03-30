import pygame as pg
import json
from enemy import Enemy
from world import World
from turret import Turret
import constants as c

#initialise pygame
pg.init()

# create clock
clock = pg.time.Clock()

#create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")

#load images

#map
map_image = pg.image.load('assests/levels/level.png').convert_alpha() 

#individual turret image for mouse cursor
cursor_turret = pg.image.load('assests/turrets/turret1.png').convert_alpha()

#enemies
enemy_image = pg.image.load('assests/images/enemies/enemy_1.png').convert_alpha()

# buttons
buy_turret_image = pg.image.load('assests/turrets/turret1.png').convert_alpha()
cancel_image = pg.image.load('assests/turrets/turret1.png').convert_alpha()

#load jon data for level
with open('assests/levels/mapdata1.tmj') as file:
    world_data = json.load(file)

def create_turret(pos):
    mouse_tile_x = pos[0] // c.TILE_SIZE
    mouse_tile_y = pos[1] // c.TILE_SIZE
    mouse_pos = (mouse_tile_x * c.TILE_SIZE + 32, mouse_tile_y * c.TILE_SIZE + 32)
    # print(mouse_pos[0])
    # calculate the sequential number of tiles 
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x

    # check if that tile is grass
    if world.tile_map[mouse_tile_num] == 25:
        # CHECK if there is alreadya turret there
        space_is_free = True
        for turret in turret_group:
            if (mouse_pos) == (turret.pos): 
                space_is_free = False
                print('turret already there')
        # if this a free space, create a turret 
        if space_is_free:
            new_turret = Turret(cursor_turret, mouse_pos)
            turret_group.add(new_turret)
            print('new turret')

#create world
world = World(world_data, map_image)
world.process_data()

# create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)

run = True
while run:

    clock.tick(c.FPS)

    screen.fill("grey100")

    # draw level
    world.draw(screen)

    #draw enemy path
    pg.draw.lines(screen,"grey0", False, world.waypoints)

    # update groups
    enemy_group.update() 

    #draw groups
    enemy_group.draw(screen)
    turret_group.draw(screen)

    # Event handler
    for event in  pg.event.get():
        #quit program
        if event.type == pg.QUIT:
            run = False
        #mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                create_turret(mouse_pos)                

    # update_display
    pg.display.flip()

pg.quit()