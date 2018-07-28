import pygame as pg
import traceback
#from os import path
#from random import seed, random

import settings as st
import sprites as spr
import functions as fn
import rooms

vec = pg.math.Vector2

class Game():
    def __init__(self):
        # initialise game window etc.
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()
        
        pg.key.set_repeat(200, 150)

        self.screen = pg.display.set_mode((st.WIDTH, st.HEIGHT))
        
        self.clock = pg.time.Clock()
        self.running = True
        self.loaded = False
        
        # booleans for drawing the hit rects and other debug stuff
        self.draw_debug = False
        self.slowmotion = False
        self.caption = ''
        
        self.key_down = None
        self.state = 'GAME'
        
        self.saveGame = spr.saveObject()
        self.saveGame.load()
        
        self.loadData()
    

    def loadData(self):      
        self.room_images = fn.img_list_from_strip('minimap_strip_7x5.png', 
                                                  7, 5, 0, 20, False)
        
        self.room_image_dict = {
                                'empty': self.room_images[0],
                                'NSWE': self.room_images[1],
                                'N': self.room_images[3],
                                'E': self.room_images[4],
                                'S': self.room_images[5],
                                'W': self.room_images[6],
                                'NE': self.room_images[7],
                                'NS': self.room_images[8],
                                'NW': self.room_images[9],
                                'SE': self.room_images[10],
                                'WE': self.room_images[11],
                                'SW': self.room_images[12],
                                'NWE': self.room_images[13],
                                'NES': self.room_images[14],
                                'SWE': self.room_images[15],
                                'NWS': self.room_images[16]
                                }
        
        
        self.tileset_names = ['tileset.png', 'tileset_sand.png', 
                              'tileset_green.png','tileset_red.png']
        
        #self.tileset_list = [fn.tileImageScale(tileset, 16, 16,
                                #scale=1) for tileset in self.tileset_names]
        
        # THIS IS NEW!
        self.tileset_dict = {key: fn.tileImageScale(key, 16, 16,
                                scale=1) for key in self.tileset_names}
        
        
    def loadSavefile(self):       
        self.player.loadSelf()
        self.dungeon.loadSelf()
               
       
    def writeSavefile(self):

        pg.display.set_caption('  SAVING...')
        # TO DO: EACH DUNGEON SHOULD HAVE ITS OWN TILESET
        # self.tileset should be only the string
        # make a save object for the dungeon
        self.saveGame.data['tileset'] = self.dungeon.tileset
        
        self.player.saveSelf()
        self.dungeon.saveSelf()
        
        print('GAME SAVED')
        pg.display.set_caption(self.caption)
        
        
    def new(self):       
        # start a new game
        # initialise sprite groups
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.gui = pg.sprite.Group()
        
        # instantiate dungeon
        self.dungeon = rooms.Dungeon(self, st.DUNGEON_SIZE)
        if self.loaded:
            self.dungeon.tileset = self.saveGame.data['tileset']
        else:  
            self.dungeon.create(rng_seed=None)
        
        # spawn the player in the middle of the screen/room
        self.player = spr.Player(self, (st.WIDTH // 2, st.HEIGHT // 2))
        
        self.inventory = spr.Inventory(self)
        
        # load settings
        if self.loaded:
            self.loadSavefile()
            
        # spawn the wall objects (invisible)
        self.walls = fn.transitRoom(self, self.walls, self.dungeon)
        
        # create a background image from the tileset for the current room
        self.background = fn.tileRoom(self, 
                                      self.tileset_dict[self.dungeon.tileset], 
                                      self.dungeon.room_index)
        
        self.run()
        

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            if self.slowmotion:
                self.clock.tick(5)
            else:
                self.clock.tick(st.FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        
        self.caption = st.TITLE
        pg.display.set_caption(self.caption)
        if self.slowmotion:
            pg.display.set_caption('slowmotion')
        
        # game loop update
        
        # check for key presses
        self.key_down = fn.keyDown(self.event_list)
        
        if self.state == 'GAME':
            self.player.update(self.walls)
            self.inventory.update()
            # check for room transitions on screen exit (every frame)
            direction, new_room, new_pos = fn.screenWrap(self.player, self.dungeon)
    
            if new_room != self.dungeon.room_index:
                self.dungeon.room_index = new_room
                self.RoomTransition(new_pos, direction)
        elif self.state == 'MENU':
            self.inventory.update()


    def events(self):
        # game loop events
        self.event_list = pg.event.get()
        for event in self.event_list:
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    #self.screen.fill((0, 0, 0))
                    self.loaded = False
                    self.new()
                    
                if event.key == pg.K_F9:
                    # load save game
                    self.loaded = True
                    self.playing = False
                    
                if event.key == pg.K_F6:
                    # save game
                    self.writeSavefile()
                    
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                    
                if event.key == pg.K_s:
                    self.slowmotion = not self.slowmotion


    def draw(self):
        self.screen.fill(st.BLACK)
        self.screen.blit(self.background, (0, st.GUI_HEIGHT))

        self.player.draw()

        if self.draw_debug:
            pg.draw.rect(self.screen, st.RED, self.player.hit_rect, 1)
            for wall in self.walls:
                pg.draw.rect(self.screen, st.RED, wall.rect, 1)  
                
        self.drawGUI()
                          
        pg.display.flip()
        
        
    def drawGUI(self):
        # Interface (Items, HUD, map)
        self.inventory.draw()
        if self.dungeon.done:
            self.dungeon.blitRooms()
            
    
    def RoomTransition(self, new_pos, direction):
        # store the old background image temporarily
        old_background = self.background
        # build the new room
        self.background = fn.tileRoom(self, 
                                      self.tileset_dict[self.dungeon.tileset], 
                                      self.dungeon.room_index)
        
        # move the player to the other side of the screen
        self.player.pos = new_pos
        self.player.rect.center = self.player.pos
        self.player.hit_rect.bottom = self.player.rect.bottom
        
        # scroll the new and old background
        # start positions for the new bg are based on the direction the
        # player is moving
        start_positions = {
                          'UP': vec(0, - st.HEIGHT + st.GUI_HEIGHT),  
                          'DOWN': vec(0, st.HEIGHT + st.GUI_HEIGHT),
                          'LEFT': vec(- st.WIDTH, st.GUI_HEIGHT),
                          'RIGHT': vec(st.WIDTH, st.GUI_HEIGHT)
                          }
        
        pos = start_positions[direction]
        # pos2 is the old bg's position that gets pushed out of the screen
        pos2 = vec(0, st.GUI_HEIGHT)
        
        while pos != (0, st.GUI_HEIGHT):
            # moves the 2 room backrounds until the new background is at (0,0)
            # the pos has to be restrained to prevent moving past (0,0) and 
            # stay forever in the loop
            scroll_speed = st.SCROLLSPEED
            if direction == 'UP':
                pos.y += scroll_speed
                pos2.y += scroll_speed
                pos.y = min(st.GUI_HEIGHT, pos.y)
            elif direction == 'DOWN':
                pos.y -= scroll_speed
                pos2.y -= scroll_speed
                pos.y = max(st.GUI_HEIGHT, pos.y)
            elif direction == 'LEFT':
                pos.x += scroll_speed
                pos2.x += scroll_speed
                pos.x = min(0, pos.x)
            elif direction == 'RIGHT':
                pos.x -= scroll_speed
                pos2.x -= scroll_speed
                pos.x = max(0, pos.x)
            
            self.screen.blit(self.background, pos)
            self.screen.blit(old_background, pos2)
            self.drawGUI()
            #self.player.draw()

            pg.display.flip()
        
        # put wall objects in the room after transition
        self.walls = fn.transitRoom(self, self.walls, self.dungeon)



g = Game()
try:
    while g.running:
        g.new()
except Exception:
    traceback.print_exc()
    pg.quit()

pg.quit()
