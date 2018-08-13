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


class Game:
    def __init__(self):
        # initialise game window etc.
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()

        pg.key.set_repeat(10, 150)
        pg.mouse.set_visible(True)

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
        self.in_transition = False

        self.saveGame = spr.saveObject()
        self.saveGame.load()

        self.loadData()


    def loadData(self):
        #loading assets (images, sounds)
        self.imageLoader = spr.ImageLoader(self)
        self.imageLoader.load()
        

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
        # start a new game
        # initialise sprite groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.LayeredUpdates()
        self.gui = pg.sprite.LayeredUpdates()
        self.enemies = pg.sprite.LayeredUpdates()

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
        fn.transitRoom(self, self.dungeon)

        # create a background image from the tileset for the current room
        self.background = fn.tileRoom(self,
                          self.imageLoader.tileset_dict[self.dungeon.tileset],
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
        if self.debug:
            self.caption = str(self.player.acc) + ' ' + str(self.player.state)
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
            self.direction, self.new_room, self.new_pos = fn.screenWrap(
                    self.player, self.dungeon)

            if self.new_room != self.dungeon.room_index:
                self.dungeon.room_index = self.new_room
                self.state = 'TRANSITION'
                
        elif self.state == 'MENU':
            self.inventory.update()
            
        elif self.state == 'TRANSITION':
            self.RoomTransition(self.new_pos, self.direction)


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
        if self.state != 'TRANSITION':
            # draw the background (tilemap)
            self.screen.blit(self.background, (0, st.GUI_HEIGHT))
            # draw the sprites
            self.all_sprites.draw(self.screen)
            
            # draw hitboxes in debug mode
            if self.debug:
                for sprite in self.all_sprites:
                    pg.draw.rect(self.screen, st.CYAN, sprite.hit_rect, 1)
    
            # draw the inventory
            self.drawGUI()

        pg.display.update()


    def drawGUI(self):
        # Interface (Items, HUD, map, textboxes etc)
        self.inventory.map_img = self.dungeon.blitRooms()
        self.inventory.draw()



    def RoomTransition(self, new_pos, direction):
        '''
        this method creates the illusion of the player transitioning from one
        room to the next by sliding both room backgrounds in the respective 
        direction
        '''
        if not self.in_transition:
            # store the old background image temporarily
            self.old_background = self.background
            # build the new room
            self.background = fn.tileRoom(self,
                          self.imageLoader.tileset_dict[self.dungeon.tileset],
                          self.dungeon.room_index)
    
            # move the player to the other side of the screen
            #print('old', self.player.pos)
            self.player.pos = vec(new_pos)
            self.player.hit_rect.center = vec(new_pos)
            self.player.spawn_pos = vec(new_pos)
            self.player.rect.bottom = self.player.hit_rect.bottom
            #print('new', self.player.pos)
            # scroll the new and old background
            # start positions for the new bg are based on the direction the
            # player is moving
            start_positions = {
                              'UP': vec(0, - (st.HEIGHT - st.GUI_HEIGHT * 2)),
                              'DOWN': vec(0, st.HEIGHT),
                              'LEFT': vec(- st.WIDTH, st.GUI_HEIGHT),
                              'RIGHT': vec(st.WIDTH, st.GUI_HEIGHT)
                              }
    
            self.bg_pos1 = start_positions[direction]
            # pos2 is the old bg's position that gets pushed out of the screen
            self.bg_pos2 = vec(0, st.GUI_HEIGHT)
            self.in_transition = True
            
        else:    
            if self.bg_pos1 != (0, st.GUI_HEIGHT):
                # moves the 2 room backrounds until the new background is at (0,0)
                # the pos has to be restrained to prevent moving past (0,0) and
                # stay forever in the loop
                scroll_speed = st.SCROLLSPEED
                if direction == 'UP':
                    self.bg_pos1.y += scroll_speed
                    self.bg_pos2.y += scroll_speed
                    self.bg_pos1.y = min(st.GUI_HEIGHT, self.bg_pos1.y)
                elif direction == 'DOWN':
                    self.bg_pos1.y -= scroll_speed
                    self.bg_pos2.y -= scroll_speed
                    self.bg_pos1.y = max(st.GUI_HEIGHT, self.bg_pos1.y)
                elif direction == 'LEFT':
                    self.bg_pos1.x += scroll_speed
                    self.bg_pos2.x += scroll_speed
                    self.bg_pos1.x = min(0, self.bg_pos1.x)
                elif direction == 'RIGHT':
                    self.bg_pos1.x -= scroll_speed
                    self.bg_pos2.x -= scroll_speed
                    self.bg_pos1.x = max(0, self.bg_pos1.x)
    
                self.screen.blit(self.old_background, self.bg_pos2)
                self.screen.blit(self.background, self.bg_pos1)    
                self.drawGUI()
            else:
                # put wall objects in the room after transition
                fn.transitRoom(self, self.dungeon)
                self.in_transition = False
                self.state = 'GAME'

g = Game()
try:
    while g.running:
        g.new()
except Exception:
    traceback.print_exc()
    pg.quit()

pg.quit()
