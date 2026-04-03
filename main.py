import pygame as pg
import json
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import constants as c

#initialise pygame
pg.init()

# create clock
clock = pg.time.Clock()

#create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")


# game variables 

placing_turrets = False
selected_turret = None
#load images

#map
map_image = pg.image.load('assests/levels/level.png').convert_alpha() 

# turret spritesheet
turret_spritesheets = []

for x in range(1, c.TURRET_LEVELS + 1):
    turret_sheet = pg.image.load(f'assests/turrets/blue_lvl{x}.png').convert_alpha()
    turret_spritesheets.append(turret_sheet)
# turret_sheet = pg.image.load('assests/turrets/turret_set2_fire.png').convert_alpha()

#individual turret image for mouse cursor
cursor_turret = pg.image.load('assests/turrets/a1.png').convert_alpha()

#enemies
enemy_image = pg.image.load('assests/images/enemies/enemy_1.png').convert_alpha()

# buttons
buy_turret_image = pg.image.load('assests/images/buttons/buy.png').convert_alpha()
cancel_image = pg.image.load('assests/images/buttons/cancel.png').convert_alpha()
upgrade_turret_image = pg.image.load('assests/images/buttons/upgrade.png').convert_alpha()


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
        # CHECK if there is already a turret there
        space_is_free = True
        for turret in turret_group:
            if (mouse_pos) == (turret.pos): 
                space_is_free = False
                # print('turret already there')
        # if this a free space, create a turret 
        if space_is_free:
            new_turret = Turret(turret_spritesheets, mouse_pos)
            turret_group.add(new_turret)
            # print('new turret')

def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    mouse_pos = (mouse_tile_x * c.TILE_SIZE + 32, mouse_tile_y * c.TILE_SIZE + 32)
    for turret in turret_group:
            if (mouse_pos) == (turret.pos): 
                return turret

def clear_selection():
    for turret in turret_group:
        turret.selected = False

#create world
world = World(world_data, map_image)
world.process_data()

# create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)

# create Button
turret_button = Button(c.SCREEN_WIDTH + 50, 100, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 50, 260, upgrade_turret_image, True)

run = True
while run:

    clock.tick(c.FPS)

    ###################################
    # UPDATING SECTION 
    ###################################

    # update groups
    enemy_group.update() 
    turret_group.update(enemy_group)

    # highlight selected turret 
    if selected_turret:
        selected_turret.selected = True

    ###################################
    # DRAWING SECTION 
    ###################################
    
    screen.fill("grey100") 

    # draw level
    world.draw(screen)

    #draw enemy path
    # pg.draw.lines(screen,"grey0", False, world.waypoints)

    #draw groups
    enemy_group.draw(screen)
    # turret_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    # draw buttons 
    # button for placing turrets
    if turret_button.draw(screen):
        # print("new turret")
        placing_turrets = True
    # if placing turrets, show the cancel button as well
    if placing_turrets:
        # show cursor as turret 
        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= c.SCREEN_WIDTH:
            screen.blit(cursor_turret, cursor_rect)

        if cancel_button.draw(screen):
           placing_turrets = False

    # if a turret is selwcted, then show the button to upgrade it
    if selected_turret:
        # IF A TURRET CAN BE UPGRADED, ONLY THEN SHO THE UPGRADE BUTTON
        if selected_turret.upgrade_level < c.TURRET_LEVELS:
            if upgrade_button.draw(screen):
                selected_turret.upgrade()


    # Event handler
    for event in  pg.event.get():
        #quit program
        if event.type == pg.QUIT:
            run = False
        #mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                # clear selected turrets
                selected_turret = None
                clear_selection()
                if placing_turrets:
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)              

    # update_display
    pg.display.flip()

pg.quit()