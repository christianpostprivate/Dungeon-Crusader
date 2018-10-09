import pygame as pg
from random import choice, randint, seed
from datetime import datetime
import traceback

import settings as st
import functions as fn
import sprites as spr

vec = pg.math.Vector2


class Room:
    def __init__(self, game, doors, type_='default'):
        self.game = game
        self.doors = doors
        self.type = type_
        self.w = st.WIDTH // st.TILESIZE
        self.h = (st.HEIGHT - st.GUI_HEIGHT) // st.TILESIZE
        
        self.visited = False
        self.pos = [0, 0]
        self.dist = -1
        
        # choose a random tmx file for this room
        if self.type == 'start':
            self.tm_file = 'room_0.tmx'
        else:
            # pop room layout from rooms pool
            self.tm_file = 'room_{}.tmx'.format(st.TM_POOL.pop())
        
        # a list of doors that are locked
        self.locked_doors = []
        # checks if room is shut (all doors are closed)
        # MEMO make this also a list so that particular doors can be shut
        self.shut = False
        # a list of sprites that represent the closed doors
        self.shut_doors = []
        # boolean for if the player has done all the tasks in a room
        self.cleared = False
        
        self.build()
        
        self.object_data = []
   
     
    def build(self):       
        for key in self.game.imageLoader.room_image_dict:
            if fn.compare(self.doors, key):
                self.image = self.game.imageLoader.room_image_dict[key]        
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
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 112, 'y': 16,  
                                'width': 16 + 16, 'height': 16})
        if 'S' not in self.doors:
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 112, 'y': 160,  
                                'width': 16 + 16, 'height': 16})
        if 'W' not in self.doors:
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 16, 'y': 80,  
                                'width': 16, 'height': 32})   
        if 'E' not in self.doors:
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 224, 'y': 80,  
                                'width': 16, 'height': 32})

    
    def shutDoors(self):
        '''
        Closes all doors of the room
        --> instanciate a solid Door object in each entrance
        MEMO: MAYBE PUT THIS IN THE DUNGEON CLASS IDK
        '''
        if not self.shut:
            for door in self.doors:
                pos = (st.DOOR_POSITIONS[door][0], st.DOOR_POSITIONS[door][1] 
                        + st.GUI_HEIGHT)
                d = spr.Door(self.game, pos, direction=door)
                self.shut_doors.append(d)
            
            self.shut = True
        
    
    def openDoors(self):
        '''
        delets all door sprites
        '''
        if self.shut:
            for d in self.shut_doors:
                d.kill()
            self.shut = False
                   


class Dungeon:
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
        # 1D list of rooms
        self.room_list = []

        # starting room
        self.start = [h // 2, w // 2]
        r_start = Room(self.game, 'NSWE', 'start')
        self.rooms[self.start[0]][self.start[1]] = r_start
        self.room_list.append(r_start)
        self.room_index = self.start
        
        self.room_current = self.rooms[self.room_index[0]][self.room_index[1]]
        
        self.done = False
        
        self.saveGame = self.game.saveGame
        
        self.tileset = choice(self.game.imageLoader.tileset_names)
        
        
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
        
        st.randomizeRooms()
        
        self.build(rng_seed)

        self.closeDoors()
        # assign a distance from the start to every room
        self.floodFill()
        
        # set keys, lock doors etc
        self.keyLogic()
            
        dt = datetime.now() - start
        ms = dt.seconds * 1000 + dt.microseconds / 1000.0
        print('Dungeon built in {} ms'.format(round(ms, 1)))
        
        
    def findEnd(self):
        # finds the farest room from the start
        for room in self.room_list:
            if room.dist == self.dist_longest:
                print('Endboss 2 in', room.pos)
                return room.pos
        
        
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
                                r = Room(self.game, 'S')
                                self.rooms[i - 1][j] = r
                                self.room_list.append(r)
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
      
                                r = Room(self.game, rng)
                                self.rooms[i - 1][j] = r
                                self.room_list.append(r)
                                  
                            self.done = False
                        
                        if 'W' in room.doors and self.rooms[i][j - 1] == None:
                            if j == 1:
                                r = Room(self.game, 'E')
                                self.rooms[i][j - 1] = r
                                self.room_list.append(r)
                            else:
                                rng = choice(st.ROOMS['W'])
                                
                                if 'N' in rng and self.rooms[i - 1][j - 1]:
                                    rng = rng.replace('N', '')
                                if 'W' in rng and self.rooms[i][j - 2]: 
                                    rng = rng.replace('W', '')
                                if 'S' in rng and self.rooms[i + 1][j - 1]: 
                                    rng = rng.replace('S', '')
                                
                                r = Room(self.game, rng)
                                self.rooms[i][j - 1] = r
                                self.room_list.append(r)
                             
                            self.done = False
                        
                        if 'E' in room.doors and self.rooms[i][j + 1] == None:
                            if j == len(self.rooms) - 2:
                                r = Room(self.game, 'W')
                                self.rooms[i][j + 1] = r
                                self.room_list.append(r)
                            else:
                                rng = choice(st.ROOMS['E'])
                                
                                if 'N' in rng and self.rooms[i - 1][j + 1]:
                                    rng = rng.replace('N', '')
                                if 'E' in rng and self.rooms[i][j + 2]: 
                                    rng = rng.replace('E', '')
                                if 'S' in rng and self.rooms[i + 1][j + 1]: 
                                    rng = rng.replace('S', '')
                                
                                r = Room(self.game, rng)
                                self.rooms[i][j + 1] = r
                                self.room_list.append(r)
                            
                            self.done = False                              
                        
                        if 'S' in room.doors and self.rooms[i + 1][j] == None:
                            if i == len(self.rooms) - 2:
                                r = Room(self.game, 'N')
                                self.rooms[i + 1][j] = r
                                self.room_list.append(r)
                            else:
                                rng = choice(st.ROOMS['S'])
                                
                                if 'W' in rng and self.rooms[i + 1][j - 1]:
                                    rng = rng.replace('W', '')
                                if 'E' in rng and self.rooms[i + 1][j + 1]: 
                                    rng = rng.replace('E', '')
                                if 'S' in rng and self.rooms[i + 2][j]: 
                                    rng = rng.replace('S', '')
                                
                                r = Room(self.game, rng)
                                self.rooms[i + 1][j] = r
                                self.room_list.append(r)
                            
                            self.done = False

    
    def closeDoors(self):
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                room = self.rooms[i][j]
                if room:
                    # set the room's position value
                    room.pos = [i, j]
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
                    
    
    def lockDoors(self, room, mode):
        for door in room.locked_doors:
            pos = st.DOOR_POSITIONS[door]
            if mode == 'smallkey':
                room.layout.append({'id': 0, 'name': 'keydoor', 'x': pos[0], 
                                'y': pos[1], 'width': 48, 'height': 48, 
                                'direction': door})


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
            
        
    def keyLogic(self):
        # find longest distance
        self.dist_longest = 0
        for room in self.room_list:
            self.dist_longest = max(self.dist_longest, room.dist)
            
        # set the farest room to endboss
        for room in self.room_list:
            if room.dist == self.dist_longest:
                print('Endboss in', room.pos)
                room.type = 'endboss'
                pos = room.pos
                room.tm_file = 'room_0.tmx'
                room.build()
                 # put boss in room
                room.layout.append({'id': 0, 'name': 'sorcerer_boss', 
                    'x': 15 * st.TILESIZE_SMALL, 'y': 12 * st.TILESIZE_SMALL, 
                    'width': 48, 'height': 48})
                break
        
        # find the adjacent room and lock it
        room = self.rooms[pos[0]][pos[1]]
        if 'N' in room.doors:
            self.rooms[pos[0] - 1][pos[1]].locked_doors.append('S')
            self.lockDoors(self.rooms[pos[0] - 1][pos[1]], 'smallkey')
        elif 'S' in room.doors:
            self.rooms[pos[0] + 1][pos[1]].locked_doors.append('N')
            self.lockDoors(self.rooms[pos[0] + 1][pos[1]], 'smallkey')
        elif 'W' in room.doors:
            self.rooms[pos[0]][pos[1] - 1].locked_doors.append('E')
            self.lockDoors(self.rooms[pos[0]][pos[1] - 1], 'smallkey')
        elif 'E' in room.doors:
            self.rooms[pos[0]][pos[1] + 1].locked_doors.append('W')
            self.lockDoors(self.rooms[pos[0]][pos[1] + 1], 'smallkey')
            
        # find second longest distance
        dist_longest = 0
        for room in self.room_list:
            if room.type != 'endboss' and len(room.doors) == 1:
                dist_longest = max(dist_longest, room.dist)

        for room in self.room_list:
            if room.dist == dist_longest and room.type != 'endboss':
                room.type = 'miniboss'
                room.layout.append({'id': 0, 'name': 'chest', 
                                    'x': 15 * st.TILESIZE_SMALL, 
                                'y': 11 * st.TILESIZE_SMALL, 
                                'width': 16, 'height': 16, 
                                'loot': 'smallkey', 'loot_amount': 1})
                print('key in', room.pos)
                break
                 

    def blitRooms(self):
        # blit a mini-map image onto the screen
        
        # room image size
        size = (6, 4)
        
        # mini map size
        w = 59
        h = 39

        self.map_img = pg.Surface((w, h), flags=pg.SRCALPHA)
        self.map_img.fill(st.BLACK)
        
        imgs = self.game.imageLoader.room_img
             
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                room = self.rooms[i][j]
                #pos = (j * (w / self.size.x) - 1, i  * (h / self.size.y) - 1)
                pos = (j * size[0] - 1, i * size[1] - 1)
                if room:# and room.visited:
                    self.map_img.blit(room.image, pos)
                    if room.type == 'start':
                        # draw a square representing the starting room
                        self.map_img.blit(imgs[17], pos)
                else:
                    self.map_img.blit(imgs[0], pos)

        # animated red square representing the player
        now = pg.time.get_ticks()
        pos2 = (self.room_index[1] * size[0] - 1, 
                self.room_index[0] * size[1] - 1)
        player_imgs = [imgs[18], imgs[19]]
        
        if now - self.last_update > 500:
                self.last_update = now
                # change the image
                self.current_frame = (self.current_frame + 1) % len(player_imgs)
        self.map_img.blit(player_imgs[self.current_frame], pos2)
        
        scaled = (w, h)
        return pg.transform.scale(self.map_img, scaled)
        
    
    def SaveToPNG(self):               
        print('saving dungeon as PNG')
        # save a png image of this dungeon
        # image size
        size_w = int(self.size.x * st.TILES_W * st.TILESIZE)
        size_h = int(self.size.y * st.TILES_H * st.TILESIZE)
        
        dungeon_img = pg.Surface((size_w, size_h))
        dungeon_img.fill(st.BLACK)
        
        print(size_w, '*', size_h)
        
        h = dungeon_img.get_height()
        w = dungeon_img.get_width()
        for i in range(int(self.size.x)):
            pg.draw.line(dungeon_img, st.WHITE, 
                         (i * st.TILES_W * st.TILESIZE - 1, 0),
                         (i * st.TILES_W * st.TILESIZE - 1, h), 2)
        for i in range(int(self.size.y)):
            pg.draw.line(dungeon_img, st.WHITE, 
                         (0, i * st.TILES_H * st.TILESIZE - 1),
                         (w, i * st.TILES_H * st.TILESIZE - 1), 2)
        
        for room in self.room_list:
            pos_x = room.pos[1] * st.TILES_W * st.TILESIZE 
            pos_y = room.pos[0] * st.TILES_H * st.TILESIZE
            room_img = fn.tileRoom(self.game, 
                          self.game.imageLoader.tileset_dict[self.tileset],
                          room.pos)
    
            # get object images
            for obj in room.layout:
                try:
                    image = self.game.imageLoader.map_sprites[obj['name']]
                    room_img.blit(image, (obj['x'], obj['y']))
                except Exception:
                    #traceback.print_exc()
                    pass
                
            dungeon_img.blit(room_img, (pos_x, pos_y))
                    
        try:
            dungeon_img = pg.transform.scale(dungeon_img, (w, h))
            pg.image.save(dungeon_img, 'dungeon_image.png')
            pass
        except Exception:
            traceback.print_exc()
            
            
