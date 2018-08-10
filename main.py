import pygame as pg
import traceback
#from os import path
#from random import seed, random

import settings as st
import sprites as spr
import functions as fn
import rooms

vec = pg.math.Vector2

# testing stuff
#print(fn.objects_from_tmx('room_1.tmx'))
#print(fn.tileset_from_tmx('room_1.tmx'))
#print(spr.export_globals())


class Game():
    def __init__(self):
        # initialise game window etc.
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()

        pg.key.set_repeat(150, 150)
        pg.mouse.set_visible(False)

        self.screen = pg.display.set_mode((st.WIDTH, st.HEIGHT))

        self.clock = pg.time.Clock()
        self.running = True
        self.loaded = False

        # booleans for drawing the hit rects and other debug stuff
        self.debug = False
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
        
        self.enemy_image_dict = {
            'skeleton': fn.img_list_from_strip('skeleton.png', 16, 16, 0, 2)
            }


        #self.tileset_names = ['tileset.png', 'tileset_sand.png',
                              #'tileset_green.png','tileset_red.png']
        self.tileset_names = ['tileset_red_8x8.png']
        
        self.tileset_image = fn.loadImage(self.tileset_names[0], 1)

        # THIS IS NEW!
        self.tileset_dict = {key: fn.tileImageScale(key, 8, 8, scale=True) 
                                for key in self.tileset_names}


    def loadSavefile(self):
        self.player.loadSelf()
        self.dungeon.loadSelf()


    def writeSavefile(self):

        pg.display.set_caption('  SAVING...')
        # make a save object for the dungeon
        self.saveGame.data['tileset'] = self.dungeon.tileset

        self.player.saveSelf()
        self.dungeon.saveSelf()

        print('GAME SAVED')
        pg.display.set_caption(self.caption)


    def new(self):
        #print('width', st.WIDTH / st.GLOBAL_SCALE, 'height', 
              #st.HEIGHT / st.GLOBAL_SCALE)
        #print('tiles_w', st.TILES_W)


        # start a new game
        # initialise sprite groups
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.gui = pg.sprite.Group()
        self.enemies = pg.sprite.Group()

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

        # spawn the new objects (invisible)
        fn.transitRoomNEW(self, self.dungeon)

        # create a background image from the tileset for the current room
        self.background = fn.tileRoom(self,
                                      self.tileset_dict[self.dungeon.tileset],
                                      self.dungeon.room_index)

        # TESTING ENEMIES
        #images = fn.img_list_from_strip('skeleton.png', 16, 16, 0, 2)
        #enemy1 = spr.Enemy(self, (300, 500), images)
        #enemy2 = spr.Enemy(self, (300, 500), images)

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
        if self.debug:
            self.caption = str(self.player.state) + ' ' + str(self.player.attack_update)
        else:
            self.caption = st.TITLE
        pg.display.set_caption(self.caption)
        if self.slowmotion:
            pg.display.set_caption('slowmotion')

        # game loop update

        # check for key presses
        self.key_down = fn.keyDown(self.event_list)

        if self.state == 'GAME':
            for sprite in self.all_sprites:
                if sprite == self.player:
                    sprite.update(self.walls)
                else:
                    sprite.update()
                    
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
                if event.key == pg.K_r and self.debug:
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
                    self.debug = not self.debug

                if event.key == pg.K_F4:
                    self.slowmotion = not self.slowmotion


    def draw(self):
        self.screen.blit(self.background, (0, st.GUI_HEIGHT))

        for sprite in self.all_sprites:
            sprite.draw()

        if self.debug:
            for sprite in self.all_sprites:
                pg.draw.rect(self.screen, st.CYAN, sprite.hit_rect, 1)
            for sprite in self.walls:
                pg.draw.rect(self.screen, st.CYAN, sprite.hit_rect, 1)

        self.drawGUI()

        pg.display.flip()


    def drawGUI(self):
        # Interface (Items, HUD, map)
        
        if self.dungeon.done:
            self.inventory.map_img = self.dungeon.blitRooms()

        self.inventory.draw()



    def RoomTransition(self, new_pos, direction):
        '''
        this method creates the illusion of the player transitioning from one
        room to the next by sliding both room backgrounds in the respective 
        direction
        '''
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
                          'UP': vec(0, - (st.HEIGHT - st.GUI_HEIGHT * 2)),
                          'DOWN': vec(0, st.HEIGHT),
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

            self.screen.blit(old_background, pos2)
            self.screen.blit(self.background, pos)    
            self.drawGUI()

            pg.display.flip()

        # put wall objects in the room after transition
        fn.transitRoomNEW(self, self.dungeon)



g = Game()
try:
    while g.running:
        g.new()
except Exception:
    traceback.print_exc()
    pg.quit()

pg.quit()
