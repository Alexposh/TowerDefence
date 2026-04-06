import pygame as pg
from enemy_data import ENEMY_SPAWN_DATA
import random
import constants as c

class World():
    def __init__(self, data, map_image):
        self.level = 1
        self.health = c.HEALTH
        self.money = c.MONEY
        self.tile_map = []
        self.waypoints = []
        self.image = map_image
        self.level_data = data
        self.enemy_list = []
        self.spawned_enemies = 0

    def process_data(self):
        # loop through data to extract relevant info
        for layer in self.level_data['layers']:
            if layer['name'] == 'tilemap':
                self.tile_map = layer['data']
                # print(self.tile_map)
            elif layer['name'] == 'waypoints':
                # print(layer)
                for obj in layer['objects']:
                    waypoint_data = obj['polygon']
                    self.process_waypoints(waypoint_data)
    
    def process_waypoints(self, data):
        #iterate through waypoint to extract individual sets of x ay coordinates
        for point in data:
            temp_x = point.get("x")
            temp_y = point.get("y")
            self.waypoints.append((temp_x, temp_y))

    def process_enemies(self):
        enemies = ENEMY_SPAWN_DATA[self.level - 1]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)
        random.shuffle(self.enemy_list)

    def draw(self, surface):
        surface.blit(self.image, (0, 0))
