import pygame as pg
from random import choice, randint
from datetime import datetime

import settings as st
import functions as fn

vec = pg.math.Vector2


class Room():
    def __init__(self, game, doors, type_='default'):
        self.game = game
        self.doors = doors
        self.type = type_
        self.w = st.WIDTH // st.TILESIZE
        self.h = (st.HEIGHT - st.GUI_HEIGHT) // st.TILESIZE
        
        self.visited = True
        self.dist = -1
        
        self.build()
   
     
    def build(self):       
        for key in self.game.room_image_dict:
            if fn.compare(self.doors, key):
                self.image = self.game.room_image_dict[key]
        
        self.tileRoom()
        
        
    def tileRoom(self):
        
        # positions of the doors
        door_w = self.w // 2
        door_h = self.h // 2
        
        # layout is for objects, tiles for the tileset index
        self.layout = []
        self.tiles = []
        for i in range(self.h):
            self.layout.append([])
            self.tiles.append([])
            if i == 0 :
                for j in range(self.w):
                    self.layout[i].append(1)
                    
                    if j == 0:
                        self.tiles[i].append(12)
                    elif j == self.w - 1:
                        self.tiles[i].append(13)
                    else:
                        self.tiles[i].append(28)
            elif i == self.h - 1:
                for j in range(self.w):
                    self.layout[i].append(1)
                    
                    if j == 0:
                        self.tiles[i].append(21)
                    elif j == self.w - 1:
                        self.tiles[i].append(22)
                    else:
                        self.tiles[i].append(10)
            else:
                for j in range(self.w):
                    if j == 0:
                        self.layout[i].append(1)
                        
                        self.tiles[i].append(20)
                        
                    elif j == self.w - 1:    
                        self.layout[i].append(1)
                        
                        self.tiles[i].append(18)
                    else:
                        self.layout[i].append(0)
                        self.tiles[i].append(0)
       
        # north
        if 'N' in self.doors:
            self.layout[0][door_w] = 0
            # 35, 34, 33
            self.tiles[0][door_w + 1] = 35
            self.tiles[0][door_w] = 34
            self.tiles[0][door_w - 1] = 33
            
        # south
        if 'S' in self.doors:
            self.layout[self.h - 1][door_w] = 0
            
            self.tiles[self.h - 1][door_w + 1] = 32
            self.tiles[self.h - 1][door_w] = 31
            self.tiles[self.h - 1][door_w - 1] = 30
        
        # west
        if 'W' in self.doors:
            self.layout[door_h][0] = 0
            
            self.tiles[door_h + 1][0] = 24
            self.tiles[door_h][0] = 15
            self.tiles[door_h - 1][0] = 6
        
        # east
        if 'E' in self.doors:
            self.layout[door_h][self.w - 1] = 0
            
            self.tiles[door_h + 1][self.w - 1] = 23
            self.tiles[door_h][self.w - 1] = 14
            self.tiles[door_h - 1][self.w - 1] = 5
        
        
    def buildInterior(self):
        # in the room
        w = self.w - 1
        h = self.h - 1
        
        door_w = self.w // 2
        door_h = self.h // 2
        # floor tile index
        floor = 4
        for i in range(1, h):
            for j in range(1, w):
                if randint(0, 100) <= 10 and (
                        i != door_h and j != door_w): 
                    self.layout[i][j] = 1    
                    self.tiles[i][j] = 1
                else:
                    self.layout[i][j] = 0  
                    self.tiles[i][j] = floor
                    
                    

class Dungeon():
    def __init__(self, game, size):
        start = datetime.now()
        self.size = vec(size)
        self.game = game
        # variables for animation
        self.last_update = 0
        self.current_frame = 0
                  
        w = int(self.size.x)
        h = int(self.size.y)
        # empty dungeon
        self.rooms = [[None for i in range(w)] for j in range(h)]

        # starting room
        self.start = [h // 2, w // 2]
        self.rooms[self.start[0]][self.start[1]] = Room(self.game, 'NSWE', 
                                                        'start')
        self.room_index = self.start
        
        self.done = False
        
        self.build()
        dt = datetime.now() - start
        ms = dt.seconds * 1000 + dt.microseconds / 1000.0
        print('Dungeon built in {} ms'.format(round(ms, 1)))
        
        
    def build(self):  
        while self.done == False:
            self.done = True
            for i in range(1, len(self.rooms) - 1):
                for j in range(1, len(self.rooms[i]) - 1):
                    room = self.rooms[i][j]
                    if room:
                        if 'N' in room.doors and self.rooms[i - 1][j] == None:
                            if i == 1:
                                self.rooms[i - 1][j] = Room(self.game, 'S')
                            else:
                                # pick random door constellation
                                rng = choice(st.ROOMS['N'])
                                
                                # prevent one-sided doors
                                if 'N' in rng and self.rooms[i - 2][j]:
                                    rng = rng.replace('N', '')
                                if 'W' in rng and self.rooms[i - 1][j - 1]:
                                    rng = rng.replace('W', '')
                                if 'E' in rng and self.rooms[i - 1][j + 1]: 
                                    rng = rng.replace('E', '')
      
                                self.rooms[i - 1][j] = Room(self.game, rng)
                                
                            self.done = False
                        
                        if 'W' in room.doors and self.rooms[i][j - 1] == None:
                            if j == 1:
                                self.rooms[i][j - 1] = Room(self.game, 'E')
                            else:
                                rng = choice(st.ROOMS['W'])
                                
                                if 'N' in rng and self.rooms[i - 1][j - 1]:
                                    rng = rng.replace('N', '')
                                if 'W' in rng and self.rooms[i][j - 2]: 
                                    rng = rng.replace('W', '')
                                if 'S' in rng and self.rooms[i + 1][j - 1]: 
                                    rng = rng.replace('S', '')
                                
                                self.rooms[i][j - 1] = Room(self.game, rng)
                                
                            self.done = False
                        
                        if 'E' in room.doors and self.rooms[i][j + 1] == None:
                            if j == len(self.rooms) - 2:
                                 self.rooms[i][j + 1] = Room(self.game, 'W')
                            else:
                                rng = choice(st.ROOMS['E'])
                                
                                if 'N' in rng and self.rooms[i - 1][j + 1]:
                                    rng = rng.replace('N', '')
                                if 'E' in rng and self.rooms[i][j + 2]: 
                                    rng = rng.replace('E', '')
                                if 'S' in rng and self.rooms[i + 1][j + 1]: 
                                    rng = rng.replace('S', '')
                                
                                self.rooms[i][j + 1] = Room(self.game, rng)
                                
                            self.done = False                              
                        
                        if 'S' in room.doors and self.rooms[i + 1][j] == None:
                            if i == len(self.rooms) - 2:
                                pass
                                self.rooms[i + 1][j] = Room(self.game, 'N')
                            else:
                                rng = choice(st.ROOMS['S'])
                                
                                if 'W' in rng and self.rooms[i + 1][j - 1]:
                                    rng = rng.replace('W', '')
                                if 'E' in rng and self.rooms[i + 1][j + 1]: 
                                    rng = rng.replace('E', '')
                                if 'S' in rng and self.rooms[i + 2][j]: 
                                    rng = rng.replace('S', '')
                                
                                self.rooms[i + 1][j] = Room(self.game, rng)
                                
                            self.done = False

        self.closeDoors()
        self.floodFill()

    
    
    def closeDoors(self):
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                room = self.rooms[i][j]
                if room:
                    if 'N' in room.doors and self.rooms[i - 1][j]:
                        if 'S' not in self.rooms[i - 1][j].doors:
                            room.doors = room.doors.replace('N', '')
  
                    if 'S' in room.doors and self.rooms[i + 1][j]:
                        if 'N' not in self.rooms[i + 1][j].doors:
                            room.doors = room.doors.replace('S', '')
                    
                    if 'W' in room.doors and self.rooms[i][j - 1]:
                        if 'E' not in self.rooms[i][j - 1].doors:
                            room.doors = room.doors.replace('W', '')
                            
                    if 'E' in room.doors and self.rooms[i][j + 1]:
                        if 'W' not in self.rooms[i][j + 1].doors:
                            room.doors = room.doors.replace('E', '')
                    
                    # re-build the rooms after changes
                    room.build()
                    # set the inner layout of the room
                    room.buildInterior()


    def floodFill(self):
        cycle = 0
        starting_room = self.rooms[self.start[0]][self.start[1]]
        starting_room.dist = 0
        done = False
        while not done:
            done = True
            for i in range(1, len(self.rooms) - 1):
                for j in range(1, len(self.rooms[i]) - 1):
                    room = self.rooms[i][j]
                    
                    if room and room.dist == cycle:
                        if 'N' in room.doors and self.rooms[i - 1][j]:
                            if self.rooms[i - 1][j].dist == -1:
                                self.rooms[i - 1][j].dist = cycle + 1
                                done = False
                            
                        if 'S' in room.doors and self.rooms[i + 1][j]:
                            if self.rooms[i + 1][j].dist == -1:
                                self.rooms[i + 1][j].dist = cycle + 1
                                done = False
                        
                        if 'W' in room.doors and self.rooms[i][j - 1]:
                            if self.rooms[i][j - 1].dist == -1:
                                self.rooms[i][j - 1].dist = cycle + 1
                                done = False
                        
                        if 'E' in room.doors and self.rooms[i][j + 1]:
                            if self.rooms[i][j + 1].dist == -1:
                                self.rooms[i][j + 1].dist = cycle + 1
                                done = False
                        
            cycle += 1
    

    def blitRooms(self):
        # blit a mini-map image onto the screen
        
        # room image size
        size = (int(3.5 * st.GLOBAL_SCALE), int(3.5 * st.GLOBAL_SCALE / 2))
        
        # mini map size
        w = self.size.x * size[0]
        h = st.GUI_HEIGHT - 2 * st.GUI_MARGIN
        margin = st.GUI_MARGIN

        self.map_img = pg.Surface((w, h), flags=pg.SRCALPHA)
        self.map_img.fill(st.BLACK)
             
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                room = self.rooms[i][j]
                pos = (j * (w / self.size.x), i * (h / self.size.y))
                if room and room.visited:
                    self.map_img.blit(pg.transform.scale(room.image,
                                      size), pos)
                    if room.type == 'start':
                        # draw a square representing the starting room
                        self.map_img.blit(pg.transform.scale(
                                self.game.room_images[12], size), pos)
                else:
                    self.map_img.blit(pg.transform.scale(
                            self.game.room_images[17], size), pos)
         
        # animated red square representing the player
        now = pg.time.get_ticks()
        pos2 = (self.room_index[1] * (w / self.size.x), 
                self.room_index[0] * (h / self.size.y))
        player_imgs = [pg.transform.scale(self.game.room_images[11], size),
                       pg.transform.scale(self.game.room_images[17], size)]
        
        if now - self.last_update > 500:
                self.last_update = now
                # change the image
                self.current_frame = (self.current_frame + 1) % len(player_imgs)
        self.map_img.blit(player_imgs[self.current_frame], pos2)
                
        self.game.inventory.image.blit(self.map_img, 
                                       (st.WIDTH - w - margin, 
                                        st.HEIGHT - st.GUI_HEIGHT + margin))
        
        
