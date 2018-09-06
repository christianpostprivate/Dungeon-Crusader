import pygame as pg
import traceback
#from os import path
#from random import seed, random

import settings as st
import sprites as spr
import functions as fn
import rooms
import cutscenes as cs
import sounds as snd

vec = pg.math.Vector2


class Game:
    def __init__(self):
        # initialise game window, settings etc.
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()

        pg.key.set_repeat(10, 150)
        pg.mouse.set_visible(False)
        
        #self.font_name = pg.font.match_font(st.FONT_NAME)

        self.screen = pg.display.set_mode((st.WIDTH, st.HEIGHT))

        self.clock = pg.time.Clock()
        self.running = True
        self.loaded = False

        # booleans for drawing the hit rects and other debug stuff
        self.debug = False
        self.slowmotion = False
        self.draw_vectors = False
        self.show_player_stats = False
        self.caption = ''
        self.debug_font = pg.font.Font(st.FONT, 24)

        self.key_down = None
        self.state = 'GAME'
        self.in_transition = False

        self.saveGame = spr.saveObject()
        self.saveGame.load()

        self.loadAssets()


    def loadAssets(self):
        #loading assets (images, sounds)
        self.imageLoader = spr.ImageLoader(self)
        self.soundLoader = snd.SoundLoader(self)
        try:
            self.imageLoader.load()
            self.soundLoader.load()
        except Exception:
            traceback.print_exc()
            self.running = False
        

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
        self.item_drops = pg.sprite.LayeredUpdates()
        self.dialogs = pg.sprite.LayeredUpdates()

        # instantiate dungeon
        self.dungeon = rooms.Dungeon(self, st.DUNGEON_SIZE)
        if self.loaded:
            self.dungeon.tileset = self.saveGame.data['tileset']
        else:
            self.dungeon.create(rng_seed=None)
     
        self.inventory = spr.Inventory(self)
        
        # ADD SOME ITEMS FOR TESTING -------------------------
        self.inventory.inv_items[0][0] = 'sword'
        self.inventory.inv_items[0][1] = 'staff'
        self.inventory.inv_items[0][2] = 'bow'
        self.inventory.inv_items[0][3] = 'hookshot'

        # spawn the player in the middle of the room
        self.player = spr.Player(self, (st.WIDTH // 2, st.HEIGHT // 2))

        # load settings
        if self.loaded:
            self.loadSavefile()

        # spawn the new objects (invisible)
        self.prev_room = self.dungeon.room_index
        fn.transitRoom(self, self.dungeon)

        # create a background image from the tileset for the current room
        self.background = fn.tileRoom(self,
                          self.imageLoader.tileset_dict[self.dungeon.tileset],
                          self.dungeon.room_index)
        
        # testing
        spr.Chest(self, (5 * st.TILESIZE, 10 * st.TILESIZE), (st.TILESIZE,
                  st.TILESIZE), loot='smallkey', loot_amount=1)
        
        spr.Chest(self, (5 * st.TILESIZE, 5 * st.TILESIZE), (st.TILESIZE,
                  st.TILESIZE), loot='smallkey', loot_amount=1)
        

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
            #self.caption = (str(self.player.friction) + ' ' + 
                            #str(self.player.vel))
            self.caption = 'DEBUG MODE'
            
        else:
            self.caption = st.TITLE
        pg.display.set_caption(self.caption)
        if self.slowmotion:
            pg.display.set_caption('slowmotion')

        # game loop update

        # check for key presses
        self.key_down = fn.keyDown(self.event_list)

        if self.state == 'GAME':
            self.all_sprites.update()
                    
            self.dialogs.update()
            self.inventory.update()
            # check for room transitions on screen exit (every frame)
            self.direction, self.new_room, self.new_pos = fn.screenWrap(
                    self.player, self.dungeon)

            if self.new_room != self.dungeon.room_index:
                self.prev_room = self.dungeon.room_index
                self.dungeon.room_index = self.new_room
                self.state = 'TRANSITION'
                
            # When in a fight, shut the doors:
            if not self.dungeon.room_current.cleared:
                cs.checkFight(self)
                
        elif self.state == 'MENU':
            self.inventory.update()
            
        elif self.state == 'TRANSITION':
            self.RoomTransition(self.new_pos, self.direction)
            
        elif self.state == 'CUTSCENE':
            self.dialogs.update()
            self.walls.update()
        
        
        # DEBUG STUFF
        if self.key_down == pg.K_F12:
            self.caption = 'SAVING DUNGEON IMAGE'
            pg.display.set_caption(self.caption)
            self.dungeon.SaveToPNG()
            


    def events(self):
        # game loop events
        self.event_list = pg.event.get()
        for event in self.event_list:
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                # Key events
                if event.key == pg.K_r and self.debug:
                    self.loaded = False
                    self.new()

                if event.key == pg.K_v and self.debug:
                    self.draw_vectors = not self.draw_vectors

                if event.key == pg.K_F9:
                    # load save game
                    self.loaded = True
                    self.playing = False

                if event.key == pg.K_F6:
                    # save game
                    self.writeSavefile()

                if event.key == pg.K_h:
                    self.debug = not self.debug
                
                # REMOVE THIS!
                if event.key == pg.K_k:
                    # kill all enemies
                    for s in self.enemies:
                        s.kill()

                if event.key == pg.K_F4:
                    self.slowmotion = not self.slowmotion
                
                if event.key == pg.K_F1:
                    self.show_player_stats = not self.show_player_stats
                    
                if event.key == pg.K_p:
                    self.soundLoader.snd_heart.play()
                    print('test')


    def draw(self):
        if self.state != 'TRANSITION':
            # draw the background (tilemap)
            self.screen.blit(self.background, (0, st.GUI_HEIGHT))
            # call additional draw methods (before drawing)
            for sprite in self.all_sprites:
                if hasattr(sprite, 'draw_before'):
                    sprite.draw_before()
            # draw the sprites
            self.all_sprites.draw(self.screen)
            # draw the inventory
            self.drawGUI()
            
            # ----- DEBUG STUFF ----- #
            # draw hitboxes in debug mode
            if self.debug:
                for sprite in self.all_sprites:
                    pg.draw.rect(self.screen, st.CYAN, sprite.hit_rect, 1)
                    if isinstance(sprite, spr.Keydoor):
                        pg.draw.rect(self.screen, st.GREEN, 
                                     sprite.interact_rect, 1)
                    if self.draw_vectors:    
                        if hasattr(sprite, 'aggro_dist'):
                            pg.draw.circle(self.screen, st.RED, 
                                        (int(sprite.pos.x), int(sprite.pos.y)), 
                                        sprite.aggro_dist, 1)
                    
            if self.show_player_stats:
                strings = [str(self.player.state), 
                           ('(' + str(int(self.player.pos.x)) + ', '
                              + str(int(self.player.pos.y)) + ')'),
                           'Room: ' + str(self.dungeon.room_current.pos),
                           'type: ' + str(self.dungeon.room_current.type)]
                for i in range(len(strings)):
                    # show debug infos
                    pos = vec(16, st.GUI_HEIGHT + 16 + (i * 24 + 8))
                    text_surface = self.debug_font.render(strings[i], 
                                            False, st.WHITE)
                    text_rect = text_surface.get_rect()
                    text_rect.topleft = pos
                    self.screen.blit(text_surface, text_rect)


        pg.display.update()


    def drawGUI(self):
        # Interface (Items, HUD, map, textboxes etc)
        for dialog in self.dialogs:
            dialog.draw()
        
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
                    self.player.rect.y += scroll_speed
                elif direction == 'DOWN':
                    self.bg_pos1.y -= scroll_speed
                    self.bg_pos2.y -= scroll_speed
                    self.bg_pos1.y = max(st.GUI_HEIGHT, self.bg_pos1.y)
                    self.player.rect.y -= scroll_speed
                elif direction == 'LEFT':
                    self.bg_pos1.x += scroll_speed
                    self.bg_pos2.x += scroll_speed
                    self.bg_pos1.x = min(0, self.bg_pos1.x)                   
                    self.player.rect.x += scroll_speed
                elif direction == 'RIGHT':
                    self.bg_pos1.x -= scroll_speed
                    self.bg_pos2.x -= scroll_speed
                    self.bg_pos1.x = max(0, self.bg_pos1.x)                   
                    self.player.rect.x -= scroll_speed
                    
                #print(self.player.rect.center)
    
                self.screen.blit(self.old_background, self.bg_pos2)
                self.screen.blit(self.background, self.bg_pos1)    
                self.drawGUI()
                
                # for testing, remove later!
                #self.all_sprites.draw(self.screen)
            else:
                # put objects in the room after transition
                fn.transitRoom(self, self.dungeon)
                # update the player's position
                self.player.pos = vec(new_pos)
                self.player.hit_rect.center = vec(new_pos)
                self.player.spawn_pos = vec(new_pos)
                self.player.rect.bottom = self.player.hit_rect.bottom
                # end transtition
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
