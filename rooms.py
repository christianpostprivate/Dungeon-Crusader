import pygame as pg
from random import choice, randint, seed
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
        
        # choose a random tmx file for this room
        if self.type == 'start':
            self.tm_file = 'room_0.tmx'
        else:
            self.tm_file = 'room_{}.tmx'.format(choice(st.TILEMAP_FILES))
        
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

        # read tileset and object data from file
        self.tiles = fn.tileset_from_tmx(self.tm_file)
        self.layout = fn.objects_from_tmx(self.tm_file)
       
        # north
        if 'N' in self.doors:            
            # create the door tiles
            self.tiles[1][door_w * 2 - 2] = 17
            self.tiles[1][door_w * 2 - 1] = 18
            self.tiles[1][door_w * 2 - 0] = 19
            self.tiles[1][door_w * 2 + 1] = 70
            
            self.tiles[2][door_w * 2 - 2] = 37
            self.tiles[2][door_w * 2 - 1] = 38
            self.tiles[2][door_w * 2 - 0] = 39
            self.tiles[2][door_w * 2 + 1] = 90
            
            self.tiles[3][door_w * 2 - 2] = 57
            self.tiles[3][door_w * 2 - 1] = 58
            self.tiles[3][door_w * 2 - 0] = 59
            self.tiles[3][door_w * 2 + 1] = 110

        # south
        if 'S' in self.doors:
            self.tiles[self.h * 2 - 4][door_w * 2 - 2] = 132
            self.tiles[self.h * 2 - 4][door_w * 2 - 1] = 133
            self.tiles[self.h * 2 - 4][door_w * 2 + 0] = 134
            self.tiles[self.h * 2 - 4][door_w * 2 + 1] = 135
            
            self.tiles[self.h * 2 - 3][door_w * 2 - 2] = 152
            self.tiles[self.h * 2 - 3][door_w * 2 - 1] = 153
            self.tiles[self.h * 2 - 3][door_w * 2 + 0] = 154
            self.tiles[self.h * 2 - 3][door_w * 2 + 1] = 155
            
            self.tiles[self.h * 2 - 2][door_w * 2 - 2] = 172
            self.tiles[self.h * 2 - 2][door_w * 2 - 1] = 173
            self.tiles[self.h * 2 - 2][door_w * 2 + 0] = 174
            self.tiles[self.h * 2 - 2][door_w * 2 + 1] = 175
            
        # west
        if 'W' in self.doors:            
            self.tiles[door_h * 2 - 2][1] = 41
            self.tiles[door_h * 2 - 2][2] = 42
            self.tiles[door_h * 2 - 2][3] = 43
            
            self.tiles[door_h * 2 - 1][1] = 61
            self.tiles[door_h * 2 - 1][2] = 62
            self.tiles[door_h * 2 - 1][3] = 63
            
            self.tiles[door_h * 2 - 0][1] = 81
            self.tiles[door_h * 2 - 0][2] = 82
            self.tiles[door_h * 2 - 0][3] = 83
            
            self.tiles[door_h * 2 + 1][1] = 101
            self.tiles[door_h * 2 + 1][2] = 102
            self.tiles[door_h * 2 + 1][3] = 103
            
        # east
        if 'E' in self.doors:            
            self.tiles[door_h * 2 - 2][self.w * 2 - 4] = 195
            self.tiles[door_h * 2 - 2][self.w * 2 - 3] = 196
            self.tiles[door_h * 2 - 2][self.w * 2 - 2] = 197
            
            self.tiles[door_h * 2 - 1][self.w * 2 - 4] = 215
            self.tiles[door_h * 2 - 1][self.w * 2 - 3] = 216
            self.tiles[door_h * 2 - 1][self.w * 2 - 2] = 217
            
            self.tiles[door_h * 2 - 0][self.w * 2 - 4] = 235
            self.tiles[door_h * 2 - 0][self.w * 2 - 3] = 236
            self.tiles[door_h * 2 - 0][self.w * 2 - 2] = 237
            
            self.tiles[door_h * 2 + 1][self.w * 2 - 4] = 198
            self.tiles[door_h * 2 + 1][self.w * 2 - 3] = 199
            self.tiles[door_h * 2 + 1][self.w * 2 - 2] = 78
            
        # close doors with wall objects:
        if 'N' not in self.doors:
            self.layout.append({'id': 0, 'name': 'wall', 'x': 360, 'y': 48,  
                                'width': 48, 'height': 48})
        if 'S' not in self.doors:
            self.layout.append({'id': 0, 'name': 'wall', 'x': 360, 'y': 480,  
                                'width': 48, 'height': 48})
        if 'W' not in self.doors:
            self.layout.append({'id': 0, 'name': 'wall', 'x': 48, 'y': 264,  
                                'width': 48, 'height': 48})   
        if 'E' not in self.doors:
            self.layout.append({'id': 0, 'name': 'wall', 'x': 672, 'y': 264,  
                                'width': 48, 'height': 48})

                   

class Dungeon():
    def __init__(self, game, size):
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
        
        self.saveGame = self.game.saveGame
        
        self.tileset = choice(self.game.tileset_names)
        
        
    def saveSelf(self):   
        self.saveGame.data = {**self.saveGame.data,
                              'size': (self.size.x, self.size.y),
                              'room_index': self.room_index,
                              'seed': self.seed
                              }     
        self.saveGame.save()
       
        
    def loadSelf(self):
        try:
            self.saveGame.load()
            
            self.size.x, self.size.y = self.saveGame.data['size']
            self.room_index = self.saveGame.data['room_index']
            self.seed = self.saveGame.data['seed']
            
            self.create(self.seed)

        except:
            pass
       
        
    def create(self, rng_seed): 
        start = datetime.now()
        
        if rng_seed != None:
            self.seed = rng_seed
        else:
            self.seed = randint(1000000, 9999999)
        
        print('Dungeon seed: ', self.seed)
        
        self.build(rng_seed)

        self.closeDoors()
        self.floodFill()
        
        dt = datetime.now() - start
        ms = dt.seconds * 1000 + dt.microseconds / 1000.0
        print('Dungeon built in {} ms'.format(round(ms, 1)))
        
        
    def build(self, rng_seed):   
        # set seed for randomisation
        seed(a=rng_seed)
        
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
        size = (6, 4)
        
        # mini map size
        w = 59
        h = 39

        self.map_img = pg.Surface((w, h), flags=pg.SRCALPHA)
        self.map_img.fill(st.BLACK)
             
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                room = self.rooms[i][j]
                #pos = (j * (w / self.size.x) - 1, i  * (h / self.size.y) - 1)
                pos = (j * size[0] - 1, i * size[1] - 1)
                if room and room.visited:
                    self.map_img.blit(room.image, pos)
                    if room.type == 'start':
                        # draw a square representing the starting room
                        self.map_img.blit(self.game.room_images[17], pos)
                else:
                    self.map_img.blit(self.game.room_images[0], pos)

        # animated red square representing the player
        now = pg.time.get_ticks()
        pos2 = (self.room_index[1] * size[0] - 1, 
                self.room_index[0] * size[1] - 1)
        player_imgs = [self.game.room_images[18], self.game.room_images[19]]
        
        if now - self.last_update > 500:
                self.last_update = now
                # change the image
                self.current_frame = (self.current_frame + 1) % len(player_imgs)
        self.map_img.blit(player_imgs[self.current_frame], pos2)
        
        scaled = (w * st.GLOBAL_SCALE, h * st.GLOBAL_SCALE)
        return pg.transform.scale(self.map_img, scaled)
        
        
