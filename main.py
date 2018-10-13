import pygame as pg
import traceback

import settings as st
import sprites as spr
import functions as fn
import rooms
import cutscenes as cs
import sounds as snd

vec = pg.math.Vector2

#directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Game:
    def __init__(self):
        # initialise game window, settings etc.
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()

        pg.joystick.init()

        pg.key.set_repeat(10, st.KEY_DELAY)
        pg.mouse.set_visible(False)

        # detect gamepad
        pg.joystick.init()
        self.gamepads = [pg.joystick.Joystick(x) for x in range(
                     pg.joystick.get_count())]
        if self.gamepads:
            self.gamepads[0].init()
            #buttons = self.gamepads[0].get_numbuttons()
            # fn.testGamepad(self.gamepad[0])

        #self.font_name = pg.font.match_font(st.FONT_NAME)

        self.actual_screen = pg.display.set_mode((st.S_WIDTH, st.S_HEIGHT))
        #self.screen = pg.Surface((st.WIDTH, st.HEIGHT), flags=pg.SRCALPHA)
        self.screen = pg.Surface((st.WIDTH, st.HEIGHT))

        self.clock = pg.time.Clock()
        self.running = True
        self.loaded = False

        # booleans for drawing the hit rects and other debug stuff
        self.debug = False
        self.slowmotion = False
        self.draw_vectors = False
        self.show_player_stats = False
        self.caption = ''
        #self.debug_font = pg.font.Font(st.FONT, 24)

        self.key_down = None
        self.state = 'GAME'
        self.in_transition = False

        self.saveGame = spr.saveObject()
        self.saveGame.load()

        self.loadAssets()

        self.timer = 0


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


    def show_start_screen(self):
        # game splash/start screen
        self.screen = pg.Surface((st.WIDTH, st.HEIGHT))
        self.screen.blit(self.imageLoader.start_screen, (0, 0))
        self.screen = pg.transform.scale(self.screen,(st.S_WIDTH, st.S_HEIGHT))
        self.actual_screen.blit(self.screen, (0, 0))
        pg.display.update()
        self.wait_for_key()


    def wait_for_key(self):
        pg.time.wait(500)
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(st.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False


    def new(self):
        # start a new game
        # initialise sprite groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.LayeredUpdates()
        self.gui = pg.sprite.LayeredUpdates()
        self.enemies = pg.sprite.LayeredUpdates()
        self.npcs = pg.sprite.LayeredUpdates()
        self.traps = pg.sprite.LayeredUpdates()
        self.item_drops = pg.sprite.LayeredUpdates()
        self.dialogs = pg.sprite.LayeredUpdates()

        # instantiate dungeon
        self.dungeon = rooms.Dungeon(self, st.DUNGEON_SIZE)
        if self.loaded:
            self.dungeon.tileset = self.saveGame.data['tileset']
        else:
            self.dungeon.create(rng_seed=None)

        self.inventory = spr.Inventory(self)

        # spawn the player in the middle of the room
        self.player = spr.Player(self, (st.WIDTH // 2, st.TILESIZE * 12))

        # ADD SOME ITEMS FOR TESTING -------------------------
        s = spr.Sword(self, self.player)
        self.inventory.addItem(s)
        self.player.itemA = s
        self.inventory.addItem(spr.Hookshot(self, self.player))
        self.inventory.addItem(spr.Staff(self, self.player))
        bow = spr.Bow(self, self.player)
        self.inventory.addItem(bow)
        bombs = spr.Bombs(self, self.player)
        self.inventory.addItem(bombs)
        
        self.player.itemB = bow

        b = spr.Bottle(self, self.player)
        b.fill('red potion')
        self.inventory.addItemSlot(b, (0, 4))
        b = spr.Bottle(self, self.player)
        b.fill('green potion')
        self.inventory.addItemSlot(b, (1, 4))
        b = spr.Bottle(self, self.player)
        b.fill('blue potion')
        self.inventory.addItemSlot(b, (2, 4))
        self.inventory.addItem(spr.Lamp(self, self.player))


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

        # testing a dark transparent overlay
        #self.dim_screen = pg.Surface((st.WIDTH, st.HEIGHT - st.GUI_HEIGHT)).convert_alpha()
        #self.dim_screen.fill((0, 0, 0, 180))

        # Night effect
        self.fog = pg.Surface((st.WIDTH, st.HEIGHT - st.GUI_HEIGHT))
        self.fog.fill(st.NIGHT_COLOR)
        self.light_mask = self.imageLoader.light_mask_img
        size = (self.light_mask.get_width() * 5, self.light_mask.get_height() * 5)
        self.light_mask_big = pg.transform.scale(self.imageLoader.light_mask_img,
                             size)
        '''
        spr.Merchant(self, (st.TILESIZE * 8, st.TILESIZE * 7))
        items = list(self.imageLoader.shop_items.keys())
        shuffle(items)
        spr.ItemShop(self, (st.TILESIZE_SMALL * 10, st.TILESIZE * 8), items.pop())
        spr.ItemShop(self, (st.TILESIZE_SMALL * 15, st.TILESIZE * 8), items.pop())
        spr.ItemShop(self, (st.TILESIZE_SMALL * 20, st.TILESIZE * 8), items.pop())

        spr.Chest(self, (st.TILESIZE * 6, st.TILESIZE * 10), (16, 16),
                      loot='small key', loot_amount=10)
        spr.Sign(self, (st.TILESIZE * 10, st.TILESIZE * 8), (16, 16),
                 text='instructions')
        '''
        #spr.Animation(self, (st.TILESIZE * 6, st.TILESIZE * 8), 
         #             self.imageLoader.effects['magic_explosion'], 60)

        self.run()


    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            #reset game screen
            self.screen = pg.Surface((st.WIDTH, st.HEIGHT))

            if self.slowmotion:
                self.clock.tick(2)
            else:
                #self.clock.tick(st.FPS)
                self.dt = self.clock.tick(st.FPS) / 1000
            self.events()
            fn.get_inputs(self)
            self.update()
            self.draw()


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

                if event.key == pg.K_k and self.debug:
                    # kill all enemies
                    for e in self.enemies:
                        e.hp = 0

                if event.key == pg.K_F4:
                    self.slowmotion = not self.slowmotion

                if event.key == pg.K_F1:
                    self.show_player_stats = not self.show_player_stats

                if event.key == pg.K_p:
                    self.soundLoader.snd_heart.play()
                    print('test')


    def update(self):
        if self.debug:
            #self.caption = self.player.lampState
            self.caption = (str(round(self.clock.get_fps(), 2)))

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

        elif self.state == 'MENU' or self.state == 'MENU_TRANSITION':
            self.inventory.update()

        elif self.state == 'TRANSITION':
            #self.RoomTransition(self.new_pos, self.direction)
            # ^this went into draw()
            pass

        elif self.state == 'CUTSCENE':
            self.dialogs.update()
            self.walls.update()

        # DEBUG STUFF
        if self.key_down == pg.K_F12:
            self.caption = 'SAVING DUNGEON IMAGE'
            pg.display.set_caption(self.caption)
            self.dungeon.SaveToPNG()


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

            for sprite in self.all_sprites:
                if hasattr(sprite, 'draw_after'):
                    sprite.draw_after()

        else:
            self.RoomTransition(self.new_pos, self.direction)


        # ----- DEBUG STUFF ----- #
        # draw hitboxes in debug mode
        if self.debug:
            for sprite in self.all_sprites:
                if hasattr(sprite, 'hit_rect'):
                    pg.draw.rect(self.screen, st.CYAN, sprite.hit_rect, 1)
                if hasattr(sprite, 'interact_rect'):
                    pg.draw.rect(self.screen, st.GREEN,
                                 sprite.interact_rect, 1)
                if self.draw_vectors:
                    if hasattr(sprite, 'aggro_dist'):
                        pg.draw.circle(self.screen, st.RED,
                                    (int(sprite.pos.x), int(sprite.pos.y)),
                                    sprite.aggro_dist, 1)

        # draw Fog
        #if self.state != 'MENU':
         #   self.drawFog()

        # draw the inventory
        self.drawGUI()

        self.screen = pg.transform.scale(self.screen,(st.S_WIDTH, st.S_HEIGHT))
        self.actual_screen.blit(self.screen, (0, 0))
        pg.display.update()


    def drawFog(self):
        self.fog.fill(st.NIGHT_COLOR)
        if self.player.lampState == 'ON':
            self.light_rect_big = self.light_mask_big.get_rect()
            self.light_rect_big.centerx = self.player.rect.centerx
            self.light_rect_big.centery = self.player.rect.centery - st.GUI_HEIGHT
            self.fog.blit(self.light_mask_big, self.light_rect_big)

        elif self.player.lampState == 'OFF':
            self.light_rect = self.light_mask.get_rect()
            self.light_rect.centerx = self.player.rect.centerx
            self.light_rect.centery = self.player.rect.centery - st.GUI_HEIGHT
            self.fog.blit(self.light_mask, self.light_rect)

        elif self.player.lampState == 'ON_TRANSITION':
            self.light_mask_copy = self.imageLoader.light_mask_img.copy()
            size = int((self.player.attack_update / st.LAMP_SWITCH_TIME)
                    * self.light_mask_big.get_rect().width)
            size = max(self.light_mask.get_rect().width, size)
            self.light_mask_copy = pg.transform.scale(self.light_mask_copy,
                                                      (size, size))
            self.light_rect = self.light_mask_copy.get_rect()
            self.light_rect.centerx = self.player.rect.centerx
            self.light_rect.centery = self.player.rect.centery - st.GUI_HEIGHT
            self.fog.blit(self.light_mask_copy, self.light_rect)

        elif self.player.lampState == 'OFF_TRANSITION':
            self.light_mask_copy = self.imageLoader.light_mask_img.copy()
            size = int((1 - self.player.attack_update / st.LAMP_SWITCH_TIME)
                    * self.light_mask_big.get_rect().width)
            size = max(self.light_mask.get_rect().width, size)
            self.light_mask_copy = pg.transform.scale(self.light_mask_copy,
                                                      (size, size))
            self.light_rect = self.light_mask_copy.get_rect()
            self.light_rect.centerx = self.player.rect.centerx
            self.light_rect.centery = self.player.rect.centery - st.GUI_HEIGHT
            self.fog.blit(self.light_mask_copy, self.light_rect)

        self.screen.blit(self.fog, (0, st.GUI_HEIGHT), special_flags=pg.BLEND_MULT)

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

            # blit the background and sprites to prevent flickering
            self.screen.blit(self.old_background, (0, st.GUI_HEIGHT))
            self.all_sprites.draw(self.screen)

            # build the new room
            self.background = fn.tileRoom(self,
                          self.imageLoader.tileset_dict[self.dungeon.tileset],
                          self.dungeon.room_index)
            # scroll the new and old background
            # start positions for the new bg are based on the direction the
            # player is moving

            start_positions = {
                              UP: vec(0, - (st.HEIGHT - st.GUI_HEIGHT * 2)),
                              DOWN: vec(0, st.HEIGHT),
                              LEFT: vec(- st.WIDTH, st.GUI_HEIGHT),
                              RIGHT: vec(st.WIDTH, st.GUI_HEIGHT)
                              }

            self.bg_pos1 = start_positions[direction]
            # pos2 is the old bg's position that gets pushed out of the screen
            self.bg_pos2 = vec(0, st.GUI_HEIGHT)
            self.in_transition = True

            fn.transitRoom(self, self.dungeon, self.bg_pos1)

        else:
            if self.bg_pos1 != (0, st.GUI_HEIGHT):
                # moves the 2 room backrounds until the new background is at (0,0)
                # PROBLEM: Only works with certain scroll speeds!

                # calculate the move vector based on the direction
                move = (vec(0, 0) - direction) * st.SCROLLSPEED

                # move the background surfaces
                self.bg_pos1 += move
                self.bg_pos2 += move

                if direction == UP:
                    self.bg_pos1.y = min(st.GUI_HEIGHT, self.bg_pos1.y)
                elif direction == DOWN:
                    self.bg_pos1.y = max(st.GUI_HEIGHT, self.bg_pos1.y)
                elif direction == LEFT:
                    self.bg_pos1.x = min(0, self.bg_pos1.x)
                elif direction == RIGHT:
                    self.bg_pos1.x = max(0, self.bg_pos1.x)

                # move the sprites during transition
                # MEMO: get the target position of the sprite somehow
                for sprite in self.all_sprites:
                    sprite.rect.topleft += move
                    sprite.hit_rect.topleft += move
                    sprite.pos += move

                self.screen.blit(self.old_background, self.bg_pos2)
                self.screen.blit(self.background, self.bg_pos1)
                self.all_sprites.draw(self.screen)
                #self.drawGUI()
            else:
                # update the player's position
                self.player.pos = vec(new_pos)
                self.player.hit_rect.center = vec(new_pos)
                self.player.spawn_pos = vec(new_pos)
                self.player.rect.bottom = self.player.hit_rect.bottom
                # end transtition
                self.in_transition = False
                self.state = 'GAME'

                # blit the background and sprites to prevent flickering
                self.screen.blit(self.background, (0, st.GUI_HEIGHT))
                self.all_sprites.draw(self.screen)


if __name__ == '__main__':
    g = Game()
    try:
        g.show_start_screen()
        while g.running:
            g.new()
    except Exception:
        traceback.print_exc()

    pg.quit()
