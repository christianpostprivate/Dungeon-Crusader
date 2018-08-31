import pygame as pg
import pickle
from os import path
import traceback
from random import choice, choices

import functions as fn
import settings as st
#import rooms as rm
import cutscenes as cs

vec = pg.math.Vector2

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

vecNull = vec(0, 0)


exported_globals = globals()

 
def create(game, data):
    d = data
    g = game
    # takes a dictionary of sprite properties
    name = d['name'].capitalize()
    #instantiate the sprite 
    # MAKE THIS ONE FUNCTION FOR EVERY SPRITE BY LOOPING THROUGH KWARGS
    if name == 'Keydoor':
        spr = exported_globals[name](g, (d['x'], d['y'] +  st.GUI_HEIGHT),
                 size=(d['width'], d['height']), direction=d['direction'])
    elif name == 'Sign':
        spr = exported_globals[name](g, (d['x'], d['y'] +  st.GUI_HEIGHT),
                 size=(d['width'], d['height']), text=d['text'])
    else:
        spr = exported_globals[name](g, (d['x'], d['y'] +  st.GUI_HEIGHT),
             (d['width'], d['height']))
    spr.data = d
        


class saveObject:
    def __init__(self):
        self.data = {}
        self.filename = 'savefile.dat'
        self.filename = path.join(st.SAVE_FOLDER, self.filename)


    def save(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self, file)


    def load(self):
        try:
            with open(self.filename, 'rb') as file:
                self.data = pickle.load(file).data
                #print(self.data)
        except Exception:
            traceback.print_exc()
            return
        
        
        
class ImageLoader:
    '''
    A class that loads all images at the start of the game
    '''
    def __init__(self, game):
        self.game = game
        
        self.tileset_names = ['tileset_red_8x8.png']

    
    def load(self):
        self.player_img = {
            'walk': fn.img_list_from_strip('knight_strip.png', 16, 16,
                                                0, 10),
            'attack': fn.img_list_from_strip('knight_attack.png', 16, 16,
                                                0, 4)
            }
        
        self.tileset_dict = {key: fn.tileImageScale(key, 8, 8, scale=True) 
                                for key in self.tileset_names}
        # set the image for testing
        self.tileset_image = fn.loadImage(self.tileset_names[0], 1)
        self.solid_img ={
            'block': fn.getSubimg(self.tileset_image, 16, 16, (16, 0)),
            'sign':  fn.loadImage('sign.png'),
            'chest': fn.img_list_from_strip('chest.png', 16, 16, 0, 2)
            }

        self.doors_image = fn.loadImage('doors_strip.png', 1)
        
        self.door_image_dict = {
                'W': fn.getSubimg(self.doors_image, 24, 32, (0, 0), 
                                  (24 * st.GLOBAL_SCALE, 32 * st.GLOBAL_SCALE)),
                'N': fn.getSubimg(self.doors_image, 32, 24, (32, 0), 
                                  (32 * st.GLOBAL_SCALE, 24 * st.GLOBAL_SCALE)),
                'E': fn.getSubimg(self.doors_image, 24, 32, (72, 0), 
                                  (24 * st.GLOBAL_SCALE, 32 * st.GLOBAL_SCALE)),
                'S': fn.getSubimg(self.doors_image, 32, 24, (96, 8), 
                                  (32 * st.GLOBAL_SCALE, 24 * st.GLOBAL_SCALE))
                }
        
        self.door_key_image_dict = {
                'W': fn.getSubimg(self.doors_image, 24, 32, (128, 0), 
                                  (24 * st.GLOBAL_SCALE, 32 * st.GLOBAL_SCALE)),
                'N': fn.getSubimg(self.doors_image, 32, 24, (160, 0), 
                                  (32 * st.GLOBAL_SCALE, 24 * st.GLOBAL_SCALE)),
                'E': fn.getSubimg(self.doors_image, 24, 32, (200, 0), 
                                  (24 * st.GLOBAL_SCALE, 32 * st.GLOBAL_SCALE)),
                'S': fn.getSubimg(self.doors_image, 32, 24, (224, 8), 
                                  (32 * st.GLOBAL_SCALE, 24 * st.GLOBAL_SCALE))
                }
              
        self.room_img = fn.img_list_from_strip('minimap_strip_7x5.png',
                                                  7, 5, 0, 20, False)
        
        self.room_image_dict = {
                                'empty': self.room_img[0],
                                'NSWE': self.room_img[1],
                                'N': self.room_img[3],
                                'E': self.room_img[4],
                                'S': self.room_img[5],
                                'W': self.room_img[6],
                                'NE': self.room_img[7],
                                'NS': self.room_img[8],
                                'NW': self.room_img[9],
                                'SE': self.room_img[10],
                                'WE': self.room_img[11],
                                'SW': self.room_img[12],
                                'NWE': self.room_img[13],
                                'NES': self.room_img[14],
                                'SWE': self.room_img[15],
                                'NWS': self.room_img[16]
                                }
        
        self.enemy_img = {
            'skeleton': fn.img_list_from_strip('skeleton_strip.png', 16, 16, 
                                               0, 2),
            'slime': fn.img_list_from_strip('slime_strip.png', 16, 16, 0, 4),
            'slime_small': fn.img_list_from_strip('slime_strip.png', 16, 16, 
                                                 0, 3, size=st.TILESIZE_SMALL),
            'bat': fn.img_list_from_strip('bat_strip.png', 16, 16, 0, 3)
            }
        
        self.item_strip1 = fn.img_list_from_strip('item_strip2.png', 8, 8, 
                                                 0, 4, size=st.TILESIZE_SMALL)        
        self.item_img = {
            'sword': fn.loadImage('sword.png'),
            'staff': fn.loadImage('staff.png'),
            'heart': self.item_strip1[0],
            'rupee': self.item_strip1[1], 
            'key': self.item_strip1[2],
            'mana': self.item_strip1[3]
            }
        
        self.inv_item_strip = fn.img_list_from_strip('inv_item_strip.png', 16, 16, 
                                                 0, 25, size=st.TILESIZE)        
        self.inv_item_img = {
                'sword': self.inv_item_strip[0],
                'staff': self.inv_item_strip[1],
                'bow': self.inv_item_strip[2]
                }
        
        
        self.magicball = fn.img_list_from_strip('projectiles.png', 8, 8, 
                                    3, 3, size=st.TILESIZE_SMALL)
        
        self.gui_img = {
            'background': fn.loadImage('inventory_bg.png'),
            'cursor': [fn.loadImage('cursor.png'),
                          pg.Surface((16, 16)).fill(st.TRANS)],
            'health': fn.loadImage('health_string.png'),
            'hearts': fn.img_list_from_strip('hearts_strip.png', 8, 8, 
                                               0, 6, scale=False),
            'magic_items': fn.loadImage('magic_and_items.png'),
            'magicbar': fn.loadImage('magicbar.png'),
            'arrows': fn.img_list_from_strip('arrows.png', 8, 8, 0, 4, 
                                        scale=True, size=st.TILESIZE_SMALL)
            }
        
        self.font = st.FONT
        


class Player(pg.sprite.Sprite):
    def __init__(self, game,  pos):
        self.group = game.all_sprites
        pg.sprite.Sprite.__init__(self)
        self.layer = 10
        self.group.add(self, layer=self.layer)
        self.game = game

        # images for animation
        self.image_strip = self.game.imageLoader.player_img['walk']
        
        self.walk_frames_l = [self.image_strip[6], self.image_strip[7]]
        self.walk_frames_r = [self.image_strip[2], self.image_strip[3]]
        self.walk_frames_u = [self.image_strip[4], self.image_strip[5]]
        self.walk_frames_d = [self.image_strip[0], self.image_strip[1]]
        self.idle_frames_l = [self.image_strip[6]]
        self.idle_frames_r = [self.image_strip[2]]
        self.idle_frames_u = [self.image_strip[9]]
        self.idle_frames_d = [self.image_strip[8]]

        self.attack_strip = self.game.imageLoader.player_img['attack']

        self.attack_frames_l = [self.attack_strip[3]]
        self.attack_frames_r = [self.attack_strip[2]]
        self.attack_frames_u = [self.attack_strip[1]]
        self.attack_frames_d = [self.attack_strip[0]]
        
        # -----------------------------------------------------
        self.fall_frames = [self.image_strip[6], self.image_strip[4], 
                            self.image_strip[2], self.image_strip[0]]
        self.fall_time = 0
        self.falling_time = 0
        self.ticks_to_fall = 800  # 1.5 seconds roughly
        self.eff_by_hole = False

        # -----------------------------------------------------

        self.image = self.walk_frames_d[0]

        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        # spawning position in the room
        self.spawn_pos = vec(pos)
        self.rect.center = pos
        self.hit_rect = st.PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.dir = vec(DOWN)
        self.lastdir = vec(DOWN)
        self.friction = st.PLAYER_FRICTION


        self.state = 'IDLE'
        self.max_hp = st.PLAYER_HP_START
        self.hp = 3.0
        self.mana = 10
        self.max_mana = 10
        
        self.items = {
                'sword': lambda: Sword(self.game, self),
                'staff': lambda: Staff(self.game, self)
                }
        
        self.itemA = 'sword'
        self.itemB = None
 
        self.item_using = None

        self.anim_update = 0
        self.attack_update = 0
        self.current_frame = 0     
        
        self.item_counts = {
                'rupee': 0,
                'smallkey': 0
                }

        # testing a save function
        self.saveGame = self.game.saveGame


    def saveSelf(self):
        self.saveGame.data = {**self.saveGame.data,
                              'pos': (self.pos.x, self.pos.y),
                              'state': self.state,
                              'hp': self.hp,
                              'itemA': self.itemA,
                              'itemB': self.itemB
                              }

        self.saveGame.save()


    def loadSelf(self):
        try:
            self.saveGame.load()

            self.pos.x, self.pos.y = self.saveGame.data['pos']
            self.state = self.saveGame.data['state']
            self.hp = self.saveGame.data['hp']
            self.itemA = self.saveGame.data['itemA']
            self.itemB = self.saveGame.data['itemB']
        except:
            pass


    def get_keys(self):
        if self.state == 'IDLE' or self.state == 'WALKING':
            keys = pg.key.get_pressed()
            
            # set the acceleration vector based on key presses
            move_x = ((keys[st.KEY_RIGHT] or keys[pg.K_d]) -
                     (keys[st.KEY_LEFT] or keys[pg.K_a]))
            move_y = ((keys[st.KEY_DOWN] or keys[pg.K_s]) - 
                      (keys[st.KEY_UP] or keys[pg.K_w]))

            self.acc = vec(move_x, move_y)
            if self.acc.length_squared() > 1:
                self.acc.normalize()
            self.acc *= st.PLAYER_ACC
            
            # set image's direction based on key pressed
            if move_x == -1:        
                self.dir = vec(LEFT)
                self.lastdir = vec(LEFT)

            if move_x == 1:              
                self.dir = vec(RIGHT)
                self.lastdir = vec(RIGHT)

            if move_y == -1:
                self.dir = vec(UP)
                self.lastdir = vec(UP)

            if move_y == 1:
                self.dir = vec(DOWN)
                self.lastdir = vec(DOWN)

            if self.acc.length() < 0.1:
                # if velocity is less than the threshold, set state to idle
                self.state = 'IDLE'
            else:
                 # set the state to walking
                 self.state = 'WALKING'
                
            if self.game.key_down == st.KEY_A:
                if self.itemA:
                    self.state = 'USE_A'
                    self.vel = vec(0, 0)
                
            if self.game.key_down == st.KEY_B:
                if self.itemB:
                    self.state = 'USE_B'
                    self.vel = vec(0, 0)
                
        elif self.state == 'USE_A':
            self.useA()
            self.attack_update += 1
            if self.attack_update > 20:
                self.attack_update = 0
                self.state = 'IDLE'
        
        elif self.state == 'USE_B':
            self.useB()
            self.attack_update += 1
            if self.attack_update > 20:
                self.attack_update = 0
                self.state = 'IDLE'
                
        elif self.state == 'HITSTUN':
            # can't receive input when stunned
            pass
        
        elif self.state == 'FALL':
            if self.fall_time == 0:
                self.fall_time = pg.time.get_ticks()
                self.fall_time += self.ticks_to_fall  # add N seconds for the fall time
            if self.falling_time > self.fall_time:  # fall until time passes N amount
                self.falling_time = 0
                self.fall_time = 0
                self.state = 'IDLE'
                self.pos = vec(self.spawn_pos)
                self.stun(3)
            else:
                self.falling_time = pg.time.get_ticks()  # set fall time to current time


        # FOR DEBUG TESTING
        if self.game.debug:
            if self.game.key_down == pg.K_PAGEUP:
                self.hp += 0.25
                self.mana += 0.5
                self.item_counts['rupee'] += 1
                self.item_counts['smallkey'] += 1
            elif self.game.key_down == pg.K_PAGEDOWN:
                self.hp -= 0.25
                self.mana -= 0.5
                self.item_counts['rupee'] -= 1
                self.item_counts['smallkey'] -= 1


    def update(self):
        # get player input
        self.get_keys()
        
        # add acceleration to velocity
        self.vel += self.acc
        # apply friction
        self.vel *= (1 - self.friction)

        # limit velocity
        if self.vel.length_squared() > st.PLAYER_MAXSPEED ** 2:
            self.vel.scale_to_length(st.PLAYER_MAXSPEED)        
        elif self.vel.length_squared() < 0.01:
            self.vel *= 0
              
        # add velocity to position
        self.pos += self.vel
        if self.state != 'HITSTUN':
            self.acc *= 0
        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        # collision detection
        self.hit_rect.centerx = self.pos.x
        fn.collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        fn.collide_with_walls(self, self.game.walls, 'y')

        # position the hitrect at the bottom of the image
        self.rect.midbottom = self.hit_rect.midbottom
        
        # restrain items between 0 and max
        self.hp = max(0, min(self.hp, self.max_hp))
        self.mana = max(0, min(self.mana, self.max_mana))
        self.item_counts['rupee'] = max(0, min(self.item_counts['rupee'], 999))
        self.item_counts['smallkey'] = max(0, 
                        min(self.item_counts['smallkey'], 99))
        
        # player animations
        self.animate()
        
        self.eff_by_hole = False


    def animate(self):
        now = pg.time.get_ticks()

        if self.state == 'WALKING':
            if now - self.anim_update > 200:
                self.anim_update = now
                self.current_frame = (self.current_frame + 1) % len(
                                      self.walk_frames_l)
                if self.dir == RIGHT:
                    self.image = self.walk_frames_r[self.current_frame]
                elif self.dir == LEFT:
                    self.image = self.walk_frames_l[self.current_frame]
                if self.dir == DOWN:
                    self.image = self.walk_frames_d[self.current_frame]
                elif self.dir == UP:
                    self.image = self.walk_frames_u[self.current_frame]
        
        elif self.state == 'IDLE':
            if self.lastdir == RIGHT:
                self.image = self.idle_frames_r[0]
            elif self.lastdir == LEFT:
                self.image = self.idle_frames_l[0]
            if self.lastdir == DOWN:
                self.image = self.idle_frames_d[0]
            elif self.lastdir == UP:
                self.image = self.idle_frames_u[0]

        elif self.state == 'USE_A' or self.state == 'USE_B':
            if self.lastdir == RIGHT:
                self.image = self.attack_frames_r[0]
            elif self.lastdir == LEFT:
                self.image = self.attack_frames_l[0]
            if self.lastdir == DOWN:
                self.image = self.attack_frames_d[0]
            elif self.lastdir == UP:
                self.image = self.attack_frames_u[0]
        
        elif self.state == 'HITSTUN':
            if self.lastdir == RIGHT:
                self.image = self.idle_frames_r[0]
            elif self.lastdir == LEFT:
                self.image = self.idle_frames_l[0]
            if self.lastdir == DOWN:
                self.image = self.idle_frames_d[0]
            elif self.lastdir == UP:
                self.image = self.idle_frames_u[0]
            # flicker to indicate damage
            try:
                alpha = next(self.damage_alpha)
                self.image = self.image.copy()
                self.image.fill((255, 255, 255, alpha), 
                                special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.state = 'IDLE'
        
        elif self.state == 'FALL':
            if now - self.anim_update > 100:
                self.anim_update = now
                self.current_frame = (self.current_frame + 1) % len(
                                      self.fall_frames)
                self.image = self.fall_frames[self.current_frame].copy()
                
                fall_pct = max(0, ((self.fall_time - self.falling_time) / 
                            self.ticks_to_fall))
                
                self.image = pg.transform.scale(self.image, 
                                        (int(self.image.get_width() * fall_pct),
                                         int(self.image.get_height() * fall_pct)))
            
            
    def useA(self):
        if not self.game.all_sprites.has(self.item_using):
            self.item_using = self.items[self.itemA]()
    
    
    def useB(self):
        if not self.game.all_sprites.has(self.item_using):
            self.item_using = self.items[self.itemB]()
            
    
    def stun(self, time):
        self.vel *= 0
        self.acc *= 0
        self.state = 'HITSTUN'
        self.lastimage = self.image.copy()
        self.damage_alpha = iter(st.DAMAGE_ALPHA * time)

    
    def knockback(self, other, time, intensity):
        if self.state != 'HITSTUN':
            self.vel = vec(0, 0)
            # calculate vector from other to self
            knockdir = self.pos - other.pos
            if knockdir.length_squared() > 0:
                knockdir = knockdir.normalize()
                self.acc = knockdir * st.GLOBAL_SCALE * intensity
                self.state = 'HITSTUN'
                self.lastimage = self.image.copy()
                self.damage_alpha = iter(st.DAMAGE_ALPHA * time)
        


class Solid(pg.sprite.Sprite):
    '''
    Container Class for all solid objects
    '''
    def __init__(self):
        self.groups = self.game.walls, self.game.all_sprites
        self.layer = 1
        pg.sprite.Sprite.__init__(self)
        for g in self.groups:
            g.add(self, layer=self.layer)
        self.rect = pg.Rect(self.pos, self.size)
        self.hit_rect = self.rect.copy()


    def update(self):
        # not used right now
        pass
        
            

class Wall(Solid):
    '''
    An invisible wall object with variable size
    '''
    def __init__(self, game, pos, size, **kwargs):
        self.game = game
        self.pos = vec(pos)
        self.size = size
        self.image = pg.Surface(size, pg.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        super().__init__()
        
        
        
class Block(Solid):
    '''
    A solid block with an image, always same size
    ''' 
    def __init__(self, game, pos, size, **kwargs):
        self.game = game
        self.pos = vec(pos)
        self.size = size
        self.image = self.game.imageLoader.solid_img['block']
        super().__init__()
        
        
class Sign(Solid):
    '''
    A sign that the player can interact with
    ''' 
    def __init__(self, game, pos, size, text, **kwargs):
        self.game = game
        self.pos = vec(pos)
        self.size = size
        self.text = cs.text_dict[text]
        self.image = self.game.imageLoader.solid_img['sign']
        self.reading = False
        super().__init__()      
        
     
    def update(self):
        if (pg.sprite.collide_rect(self.game.player, self) and 
            self.game.player.dir == vec(UP)):
            if self.game.key_down == pg.K_RETURN and len(self.game.dialogs) == 0:
                self.game.state = 'CUTSCENE'
                cs.Textbox(self.game, (st.WIDTH / 2, st.HEIGHT / 3 * 2), self.text)
            else:
                if self.game.state == 'CUTSCENE' and len(self.game.dialogs) == 0:
                    self.game.state = 'GAME'
                    

class Chest(Solid):
    '''
    A sign that the player can interact with
    ''' 
    def __init__(self, game, pos, size, **kwargs):
        self.game = game
        self.pos = vec(pos)
        self.loot = kwargs['loot']
        self.loot_amount = kwargs['loot_amount']
        # HIER KOMMT NOCH TEXT PASSEND ZUM ITEM
        self.text = cs.text_dict['chest_opened'].format(self.loot)
        self.image = self.game.imageLoader.solid_img['chest'][0]
        self.size = self.image.get_size()
        self.image_open = self.game.imageLoader.solid_img['chest'][1]
        self.open = False
        super().__init__()      
        
     
    def update(self):
        if (pg.sprite.collide_rect(self.game.player, self) and 
            self.game.player.dir == vec(UP)):
            if self.game.key_down == pg.K_RETURN and not self.open:
                # open chest
                self.open = True
                self.image = self.image_open
                self.game.state = 'CUTSCENE'
                cs.Textbox(self.game, (st.WIDTH / 2, st.HEIGHT / 3 * 2), 
                           self.text)
                self.game.player.item_counts[self.loot] += self.loot_amount
            else:
                self.game.state = 'GAME'
                    

class Door(Solid):
    '''
     A closed door that disappears if the player achieves a goal
    '''
    def __init__(self, game, pos,**kwargs):
        self.game = game
        self.pos = vec(pos)
        self.image = self.game.imageLoader.door_image_dict[kwargs['direction']]
        self.size = self.image.get_size()
        super().__init__()
        
        

class Keydoor(Solid):
    '''
     A closed door that opens if the player has a key
    '''
    def __init__(self, game, pos, size, **kwargs):
        self.game = game
        self.pos = vec(pos)
        self.dir_dict = {
                'S': DOWN,
                'N': UP,
                'E': RIGHT,
                'W': LEFT
        }
        self.dir = kwargs['direction']
        self.image = self.game.imageLoader.door_key_image_dict[kwargs['direction']]
        self.size = self.image.get_size()
        super().__init__()
        offset = vec(10, 10)
        self.interact_rect = self.rect.inflate(offset)
        self.interact_rect.center = self.hit_rect.center
        
    
    def update(self):
        player = self.game.player
        if (self.interact_rect.colliderect(player.rect) and 
            player.dir == self.dir_dict[self.dir]):
                    
            if player.item_counts['smallkey'] == 0:
                # if player doesn't have a key
                if (self.game.key_down == pg.K_RETURN and 
                    len(self.game.dialogs) == 0):
                    self.game.state = 'CUTSCENE'
                    cs.Textbox(self.game, (st.WIDTH / 2, st.HEIGHT / 3 * 2), 
                               cs.text_dict['key_needed'])
                else:
                    if (self.game.state == 'CUTSCENE' and 
                        len(self.game.dialogs) == 0):
                        self.game.state = 'GAME'
            else:
                # if player has at least one key
                if self.game.key_down == pg.K_RETURN:
                    player.item_counts['smallkey'] -= 1
                    
                    # remove self from room data
                    index = self.game.dungeon.room_index
                    room = self.game.dungeon.rooms[index[0]][index[1]]
                    room.locked_doors.remove(self.dir)
                    # delete self from sprite groups
                    self.kill()
        
        

class Hole(pg.sprite.Sprite):
    '''
    A hole that the player can fall into (and spawn at the entrance)
    '''
    def __init__(self, game, pos, size, **kwargs):
        self.game = game
        self.group = self.game.all_sprites
        self.layer = 1
        pg.sprite.Sprite.__init__(self)

        self.group.add(self, layer=self.layer)
            
        self.pos = vec(pos)
        self.size = size
        self.image = pg.Surface(size, pg.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.hit_rect = pg.Rect((0, 0), (int(st.TILESIZE * 0.6), 
                                int(st.TILESIZE * 0.6)))
        self.hit_rect.center = self.rect.center
        
    
    def update(self):
        # detect collision
        player = self.game.player
        if player.state != 'FALL' and not player.eff_by_hole:
            if fn.collide_hit_rect(player, self):
                # Attract the player to the center of the hole
                desired = self.rect.center - player.pos
                mag = desired.length()
                force = desired.normalize() * st.GLOBAL_SCALE * 10 / mag
                player.pos += force
                if desired.length_squared() < 50:
                    # set the player back to the entrance point
                    #player.pos = vec(player.spawn_pos)
                    #player.stun(3)
                    player.state = 'FALL'
                else:
                    player.eff_by_hole = True
                    
    
    def updateData(self):
        pass
            
            
# --------------- Inventory & Items -------------------------------------------

class Inventory(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.gui
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # if in menu then True, otherwise False
        self.menu = False

        self.size = (st.WIDTH, st.HEIGHT)
        self.start_pos = vec(0, (0 - st.HEIGHT + st.GUI_HEIGHT))
        self.pos = vec(self.start_pos)
        self.image = pg.Surface(self.size)
        self.image.fill(st.BLACK)

        self.map_img = None

        # inventory background
        self.gui_img = self.game.imageLoader.gui_img['background']      
        self.cursor_images = self.game.imageLoader.gui_img['cursor']        
        self.cursor_pos = vec(24 * st.GLOBAL_SCALE, 40 * st.GLOBAL_SCALE)
        
        # "health" string
        self.health_string = self.game.imageLoader.gui_img['health']
        # images for the player health
        self.heart_images = self.game.imageLoader.gui_img['hearts']
        self.magic_image = self.game.imageLoader.gui_img['magic_items']
        self.magic_bar = self.game.imageLoader.gui_img['magicbar']
        for i in range(len(self.heart_images)):
            self.heart_images[i] = pg.transform.scale(self.heart_images[i], 
                                  (8 * st.GLOBAL_SCALE, 8 * st.GLOBAL_SCALE))
            
        self.inv_index = [0, 0]
        
        # empty item matrix
        self.inv_size = [5, 5]
        self.inv_items = [[None for j in range(self.inv_size[1])] 
                           for i in range(self.inv_size[0])] 


    def update(self):
        if self.game.key_down == st.KEY_MENU:
            self.menu = not self.menu

        if self.menu:
            self.game.state = 'MENU'

            # sliding down animation
            if self.pos != (0, 0):
                self.pos.y += st.SCROLLSPEED_MENU
                self.pos.y = min(0, self.pos.y)
    
            # let the player move the cursor and select items                
            self.move_cursor()               

        else:
            # sliding up animation
            if self.pos != self.start_pos:
                self.pos.y -= st.SCROLLSPEED_MENU
                self.pos.y = min(0, self.pos.y)
            else:
                if self.game.state == 'MENU':
                    self.game.state = 'GAME'


    def draw(self):
        self.image.fill(st.BLACK)
        # draw player health
        player = self.game.player
        for i in range(int(player.max_hp)):
            # calculate position
            if i < st.PLAYER_HP_MAX // 2:
                pos = (6 * st.GLOBAL_SCALE + 10 * i * st.GLOBAL_SCALE, 
                      (st.HEIGHT - 34 * st.GLOBAL_SCALE))
            else:
                pos = (6 * st.GLOBAL_SCALE + 10 * (i - 7) * st.GLOBAL_SCALE, 
                      (st.HEIGHT - 24 * st.GLOBAL_SCALE))

            # draw hearts:
            if i < int(player.hp):
                img = self.heart_images[1]
            elif i == int(player.hp):
                if player.hp % 1 == 0.25:
                    img = self.heart_images[4]
                elif player.hp % 1 == 0.5:
                    img = self.heart_images[3]
                elif player.hp % 1 == 0.75:
                    img = self.heart_images[2]
                else:
                    img = self.heart_images[5]
            else:
                img = self.heart_images[5]

            self.image.blit(img, pos)
        
        self.image.blit(self.health_string, (25 * st.GLOBAL_SCALE, 
                                             st.HEIGHT - 42 * st.GLOBAL_SCALE))
        
        # draw magic bar and item slots
        # MEMO: might want to make multiple images 
        
        #draw mana bar
        bar_stretched = self.magic_bar.copy()
        mana_pct = self.game.player.mana / self.game.player.max_mana
        factor = mana_pct * 28 * st.GLOBAL_SCALE
        one_minus_factor = (1 - mana_pct) * 26 * st.GLOBAL_SCALE
        bar_stretched = pg.transform.scale(bar_stretched, 
                           (bar_stretched.get_width(),
                           int(factor)))
        self.image.blit(bar_stretched, (82 * st.GLOBAL_SCALE, 
                        st.HEIGHT - 31 * st.GLOBAL_SCALE + one_minus_factor))
        
        
        self.image.blit(self.magic_image, (77 * st.GLOBAL_SCALE, 
                                             st.HEIGHT - 48 * st.GLOBAL_SCALE))
        
        # draw item amounts
        # rupees
        font = self.game.imageLoader.font
        font_size = 8 * st.GLOBAL_SCALE
        x_off = 166
        text_pos = vec(x_off * st.GLOBAL_SCALE, 201 * st.GLOBAL_SCALE)
        number = 'x%03d' % self.game.player.item_counts['rupee']
        fn.draw_text(self.image, number,
                     font, font_size, st.WHITE, text_pos, align='w')
        
        # keys
        text_pos = vec(x_off * st.GLOBAL_SCALE, 217 * st.GLOBAL_SCALE)
        number = 'x %02d' % self.game.player.item_counts['smallkey']
        fn.draw_text(self.image, number,
                     font, font_size, st.WHITE, text_pos, align='w')

        # draw the mini map
        map_pos = (192 * st.GLOBAL_SCALE, st.HEIGHT - 44 * st.GLOBAL_SCALE)
        self.image.blit(self.map_img, map_pos)

        # draw the inventory background
        self.image.blit(self.gui_img, (0, 0))
        
        # draw the items
        self.draw_items()
        
        # draw the cursor
        self.draw_cursor()
        
        self.game.screen.blit(self.image, self.pos)
        
       
    def move_cursor(self):
        key = self.game.key_down
        # set the movement vector based on key presses
        move_x = (key == st.KEY_RIGHT or key == pg.K_d) - (key == st.KEY_LEFT or 
                 key == pg.K_a)
        move_y = (key == st.KEY_DOWN or key == pg.K_s) - (key == st.KEY_UP or 
                 key == pg.K_w)
        
        # change the inventory index
        self.inv_index[0] += move_x
        self.inv_index[1] += move_y        
        self.inv_index[0] = fn.clamp(self.inv_index[0], 0, self.inv_size[0] - 1)
        self.inv_index[1] = fn.clamp(self.inv_index[1], 0, self.inv_size[1] - 1)
        
        # move the cursor
        self.cursor_pos += vec(move_x, move_y) * 24 * st.GLOBAL_SCALE
        
        self.cursor_pos.x = fn.clamp(self.cursor_pos.x, 24 * st.GLOBAL_SCALE, 
                                     120 * st.GLOBAL_SCALE)
        self.cursor_pos.y = fn.clamp(self.cursor_pos.y, 40 * st.GLOBAL_SCALE, 
                                     136 * st.GLOBAL_SCALE)
        
        # select items    
        player = self.game.player 
        x = self.inv_index[1]
        y = self.inv_index[0]                     
        if key == st.KEY_A:
            if self.inv_items[x][y]:
                # put the item into slot A
                # if there is already an item, put it in slot B
                # if the item is already in slot B, clear slot B
                lastA = player.itemA
                player.itemA = self.inv_items[x][y]
                if player.itemA and player.itemB == None:
                    player.itemB = player.itemA
                if player.itemB == self.inv_items[x][y]:
                    player.itemB = lastA
                if player.itemB == player.itemA:
                    player.itemB = None
            else:
                # play negative sound
                pass
            
            print(player.itemA, player.itemB)
        
        if key == st.KEY_B:
            if self.inv_items[x][y]:
                # put the item into slot B
                lastB = player.itemB
                player.itemB = self.inv_items[x][y]
                if player.itemB and player.itemB == None:
                    player.itemA = player.itemB
                if player.itemA == self.inv_items[x][y]:
                    player.itemA = lastB
                if player.itemA == player.itemB:
                    player.itemA = None
            else:
                # play negative sound
                pass
            
            print(player.itemA, player.itemB)
    
    
    def draw_cursor(self):
        self.image.blit(self.cursor_images[0], self.cursor_pos)
        
    
    def draw_items(self):
        player = self.game.player
        
        for i in range(self.inv_size[0]):
            for j in range(self.inv_size[1]):
                pos = vecNull
                pos.x = (24 + 24 * i) * st.GLOBAL_SCALE
                pos.y = (40 + 24 * j) * st.GLOBAL_SCALE
                
                if self.inv_items[j][i]:
                    self.image.blit(self.game.imageLoader.inv_item_img[
                            self.inv_items[j][i]], pos)
        
        # draw item in slots A and B
        if player.itemA:
            imageA = self.game.imageLoader.inv_item_img[player.itemA]
            posA = (110 * st.GLOBAL_SCALE, 216 * st.GLOBAL_SCALE)
            self.image.blit(imageA, posA)
        if player.itemB:
            imageB = self.game.imageLoader.inv_item_img[player.itemB]        
            posB = (134 * st.GLOBAL_SCALE, 216 * st.GLOBAL_SCALE)   
            self.image.blit(imageB, posB)
                
                
                



class Sword(pg.sprite.Sprite):
    def __init__(self, game, player):
        self.group = game.all_sprites
        self.layer = player.layer
        pg.sprite.Sprite.__init__(self)
        self.group.add(self, layer=self.layer)
        self.player = player
        self.game = game
        self.image = self.game.imageLoader.item_img['sword']

        self.pos = vec(0, 0)
        self.rot = 0

        self.damage = 1

        self.dir = self.player.lastdir
        # rotate image based on player direction and set position
        if self.dir == UP:
            self.rot = 0
            self.pos = vec(self.player.pos.x - 4 * st.GLOBAL_SCALE, 
                           self.player.pos.y - 24 * st.GLOBAL_SCALE)
            
        elif self.dir == DOWN:
            self.rot = 180
            self.pos = vec(self.player.pos.x, self.player.pos.y + 4 
                           * st.GLOBAL_SCALE)
            
        elif self.dir == RIGHT:
            self.rot = 270
            self.pos = vec(self.player.pos.x + 7 * st.GLOBAL_SCALE,
                           self.player.pos.y - 4 * st.GLOBAL_SCALE)
            
        elif self.dir == LEFT:
            self.rot = 90
            self.pos = vec(self.player.pos.x - 20 * st.GLOBAL_SCALE,
                           self.player.pos.y - 4 * st.GLOBAL_SCALE)

        self.image = pg.transform.rotate(self.image, self.rot)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center


    def update(self):
        if not self.player.state == 'USE_A' and not self.player.state == 'USE_B':
            self.game.all_sprites.remove(self)

        for enemy in pg.sprite.spritecollide(self, self.game.enemies, False):
            if enemy.state != 'HITSTUN':
                enemy.hp -= self.damage
                enemy.knockback(self.player, 1, 0.1)


    def draw(self):
        self.game.screen.blit(self.image, self.pos)
        


class Staff(pg.sprite.Sprite):
    def __init__(self, game, player):
        self.group = game.all_sprites
        self.layer = player.layer
        pg.sprite.Sprite.__init__(self)
        self.group.add(self, layer=self.layer)
        self.player = player
        self.game = game
        self.image = self.game.imageLoader.item_img['staff']

        self.pos = vec(0, 0)
        self.rot = 0

        self.fired = False
        
        self.dir = self.player.lastdir
        # rotate image based on player direction and set position
        if self.dir == UP:
            self.rot = 0
            self.pos = vec(self.player.pos.x - 4 * st.GLOBAL_SCALE, 
                           self.player.pos.y - 24 * st.GLOBAL_SCALE)
            
        elif self.dir == DOWN:
            self.rot = 180
            self.pos = vec(self.player.pos.x, self.player.pos.y + 4 
                           * st.GLOBAL_SCALE)
            
        elif self.dir == RIGHT:
            self.rot = 270
            self.pos = vec(self.player.pos.x + 7 * st.GLOBAL_SCALE,
                           self.player.pos.y - 4 * st.GLOBAL_SCALE)
            
        elif self.dir == LEFT:
            self.rot = 90
            self.pos = vec(self.player.pos.x - 20 * st.GLOBAL_SCALE,
                           self.player.pos.y - 4 * st.GLOBAL_SCALE)

        self.image = pg.transform.rotate(self.image, self.rot)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center


    def update(self):
        if not self.fired:
            if self.player.mana >= 1:
                self.lastdir = self.player.lastdir
                Magicball(self.game, self, self.rect.center)
                self.player.mana -= 1
                self.fired = True
        
        if not self.player.state == 'USE_A' and not self.player.state == 'USE_B':
            self.game.all_sprites.remove(self)


    def draw(self):
        self.game.screen.blit(self.image, self.pos)
        


class Projectile(pg.sprite.Sprite):
    def __init__(self):
        self.vel = vec(0, 0)       
        self.anim_update = 0
        self.current_frame = 0

        self.dir = self.player.lastdir
        
        if self.rotating:
            self.rot = 0
            # rotate image based on player direction and set position
            if self.dir == UP:
                self.rot = 0
                self.pos = vec(self.player.pos.x - 4 * st.GLOBAL_SCALE, 
                               self.player.pos.y - 24 * st.GLOBAL_SCALE)
                
            elif self.dir == DOWN:
                self.rot = 180
                self.pos = vec(self.player.pos.x, self.player.pos.y + 4 
                               * st.GLOBAL_SCALE)
                
            elif self.dir == RIGHT:
                self.rot = 270
                self.pos = vec(self.player.pos.x + 7 * st.GLOBAL_SCALE,
                               self.player.pos.y - 4 * st.GLOBAL_SCALE)
                
            elif self.dir == LEFT:
                self.rot = 90
                self.pos = vec(self.player.pos.x - 20 * st.GLOBAL_SCALE,
                               self.player.pos.y - 4 * st.GLOBAL_SCALE)
                
            self.image = pg.transform.rotate(self.image, self.rot)
        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center
        
        
    def update(self):
        self.acc = vec(self.dir) * self.speed
        self.vel += self.acc
        
        # limit velocity
        if self.vel.length_squared() > self.max_speed ** 2:
            self.vel.scale_to_length(self.max_speed)
        
        self.pos += self.vel
        
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center
        
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.kill()
            
        hits = pg.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            for hit in hits:
                hit.hp -= self.damage
                self.kill()
                
        self.animate()
                
    
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.anim_update > self.anim_speed:
            self.anim_update = now
            self.current_frame = (self.current_frame + 1) % len(
                                  self.image_frames)
            self.image = self.image_frames[self.current_frame]

      

class Magicball(Projectile):
    def __init__(self, game, player, pos, rotating=False):
        self.group = game.all_sprites
        self.layer = player.layer
        pg.sprite.Sprite.__init__(self)
        self.group.add(self, layer=self.layer)
        self.player = player
        self.game = game
        self.rotating = rotating
        self.pos = vec(pos)
        
        self.image_frames = self.game.imageLoader.magicball
        self.image = self.image_frames[0]
        
        self.speed = 2 * st.GLOBAL_SCALE
        self.max_speed = 3 * st.GLOBAL_SCALE
        self.damage = 1
        self.anim_speed = 100
        
        super().__init__()
    
    

class Item:       
    def drop(name, game, pos):
        if name in Item.__dict__:
            Item.__dict__[name](game, pos)
            
            
    class ItemDrop(pg.sprite.Sprite):
        def __init__(self):
            self.groups = self.game.all_sprites, self.game.item_drops
            self.layer = self.game.player.layer - 1
            pg.sprite.Sprite.__init__(self)
            
            for g in self.groups:
                g.add(self, layer=self.layer)
        
        
        def update(self):
            if fn.collide_hit_rect(self.player, self):
                self.collect()
        
        def collect(self):
            self.kill()
        
        
    class heart(ItemDrop):
        def __init__(self, game, pos):
            self.game = game                    
            self.player = self.game.player
            self.pos = vec(pos)
            super().__init__()
            
            self.image = self.game.imageLoader.item_img['heart']
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hit_rect = self.rect
           
            
        def collect(self):
            self.player.hp += 1
            super().collect()
            
            
    class mana(ItemDrop):
        def __init__(self, game, pos):
            self.game = game                    
            self.player = self.game.player
            self.pos = vec(pos)
            super().__init__()
            
            self.image = self.game.imageLoader.item_img['mana']
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hit_rect = self.rect
           
            
        def collect(self):
            self.player.mana += 5
            super().collect()
            
     
    class rupee(ItemDrop):
        def __init__(self, game, pos):
            self.game = game                    
            self.player = self.game.player
            self.pos = vec(pos)
            super().__init__()
            
            self.image = self.game.imageLoader.item_img['rupee']
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hit_rect = self.rect
            
            
        def collect(self):
            self.player.item_counts['rupee'] += 1
            super().collect()
            
        
    class key(ItemDrop):
        def __init__(self, game, pos):
            self.game = game                    
            self.player = self.game.player
            self.pos = vec(pos)
            super().__init__()
            
            self.image = self.game.imageLoader.item_img['key']
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hit_rect = self.rect
            
        
        def collect(self):
            self.player.item_counts['key'] += 1
            super().collect()
        
# ----------------------- ENEMIES ---------------------------------------------
        
class Enemy(pg.sprite.Sprite):
    '''
    Container class for all enemies
    '''
    def __init__(self):
        self.groups = self.game.all_sprites, self.game.enemies
        self.layer = self.game.player.layer + 1
        pg.sprite.Sprite.__init__(self)
        
        for g in self.groups:
            g.add(self, layer=self.layer)

        self.image = self.walk_frames[0]
        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.vel = vec(0, 0)
        self.dir = vec(DOWN)
        self.moveTo = None
        self.acc = vec(0, 0)
        self.friction = 0.1
        self.state = 'IDLE'
        

        # default values (change in individual init after super().__init__())
        self.maxSpeed = 0.5 * st.GLOBAL_SCALE
        self.anim_update = 0
        self.walk_update = 0
        self.current_frame = 0
        self.anim_speed = 300
        
        # testing a save function
        #self.saveGame = self.game.saveGame
        
        
    def move(self):
        if self.state == 'WALKING':
   
            # set acceleration based on 4-way movement
            if self.moveTo == LEFT:
                self.acc.x = -1       
                self.dir = vec(LEFT)
    
            if self.moveTo == RIGHT:
                self.acc.x = 1          
                self.dir = vec(RIGHT)
    
            if self.moveTo == UP:
                self.acc.y = -1
                self.dir = vec(UP)
    
            if self.moveTo == DOWN:
                self.acc.y = 1
                self.dir = vec(DOWN)
                
            self.acc *= st.GLOBAL_SCALE                
        
        elif self.state == 'SEEK':
            target = self.game.player.pos - self.pos
            if target.length_squared() > 0:
                target = target.normalize()
                self.acc = target * self.maxSpeed
            
            else:
                self.acc = vecNull
                
        elif self.state == 'HITSTUN':
            # can't change acceleration when stunned
            pass
        
        
    def update(self):
        # change the drawing layer in relation to the player
        if self.hit_rect.top > self.game.player.hit_rect.top:
            for g in self.groups:
                g.change_layer(self, self.game.player.layer + 1)
        else:
            for g in self.groups:
                g.change_layer(self, self.game.player.layer - 1)
       
        # change the moving direction after a certain time
        now = pg.time.get_ticks()
        if now - self.walk_update > 2000:
            self.walk_update = now
            self.moveTo = choice([LEFT, RIGHT, DOWN, UP])
        
        # calculate acceleration
        self.move()
        
        # add acceleration to velocity
        self.vel += self.acc
               
        if self.state != 'HITSTUN':
            # reset acceleration
            self.acc *= 0
             # apply friction
            self.vel *= (1 - self.friction)
    
            # cap speed at maximum
            if self.vel.length_squared() > self.maxSpeed ** 2:
                self.vel.scale_to_length(self.maxSpeed)
        
        # add velocity to position
        self.pos += self.vel
        
        # update the position
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        # collision with walls
        self.hit_rect.centerx = self.pos.x
        fn.collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        fn.collide_with_walls(self, self.game.walls, 'y')
        
        # restrain position to stay in the room
        self.pos.x = fn.clamp(self.pos.x, st.TILESIZE * 2, 
                              st.WIDTH - st.TILESIZE * 2)
        self.pos.y = fn.clamp(self.pos.y, st.GUI_HEIGHT + st.TILESIZE * 2, 
                              st.HEIGHT - st.TILESIZE * 2)

        # position the hitbox at the bottom of the image
        self.rect.midbottom = self.hit_rect.midbottom

        self.collide_with_player()
        if self.hp <= 0:
            self.destroy()
                       
        self.animate()
        
           
    def animate(self):
        now = pg.time.get_ticks()

        if self.state == 'WALKING' or self.state == 'SEEK':
            if now - self.anim_update > self.anim_speed:
                self.anim_update = now
                self.current_frame = (self.current_frame + 1) % len(
                                      self.walk_frames)
                self.image = self.walk_frames[self.current_frame]

        elif self.state == 'HITSTUN':
            # flicker to indicate damage
            try:
                alpha = next(self.damage_alpha)
                self.image = self.lastimage.copy()
                self.image.fill((255, 255, 255, alpha), 
                                special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.state = 'WALKING'
                
        
        elif self.state == 'IDLE':
            if hasattr(self, 'idle_frames'):
                if now - self.anim_update > self.anim_speed:
                    self.anim_update = now
                    self.current_frame = (self.current_frame + 1) % len(
                                          self.idle_frames)
                    self.image = self.idle_frames[self.current_frame]


    def collide_with_player(self):
        # detect collision
        player = self.game.player
        if fn.collide_hit_rect(player, self) and player.state != 'HITSTUN':
            player.knockback(self, self.kb_time, self.kb_intensity)
            player.hp -= self.damage
            
    
    def knockback(self, other, time, intensity):
        if self.state != 'HITSTUN':
            self.vel = vec(0, 0)
            # calculate vector from other to self
            knockdir = self.pos - other.pos
            if knockdir.length_squared() > 0:
                knockdir = knockdir.normalize()
                self.acc = knockdir * st.GLOBAL_SCALE * intensity
            else:
                self.acc = vecNull
            self.state = 'HITSTUN'
            self.lastimage = self.image.copy()
            self.damage_alpha = iter(st.DAMAGE_ALPHA * time)
        
    
    def destroy(self):
        self.dropItem()
        self.kill()
            
        
    def updateData(self):
        self.data['x'] = self.pos.x
        self.data['y'] = self.pos.y
        
    
    def dropItem(self):
        # drop an item based on the weighted probability
        if hasattr(self, 'drop_rates'):
            items = list(self.drop_rates.keys())
            weights = list(self.drop_rates.values())
    
            c = choices(items, weights)[0]
            try:
                Item.drop(c, self.game, self.pos)
            except:
                pass



class Skeleton(Enemy):
    def __init__(self, game, pos, *args, **kwargs):
        self.game = game
        self.pos = vec(pos)
        self.walk_frames = self.game.imageLoader.enemy_img['skeleton']
        super().__init__()
        
        self.state = 'WALKING'
        
        self.hit_rect = pg.Rect(0, 0, int(st.TILESIZE * 0.8), 
                                int(st.TILESIZE * 0.6))
        
        self.damage = 0.5
        self.hp = 3
        # knockback stats
        self.kb_time = 1
        self.kb_intensity = 1
        
        self.drop_rates = {
                'none': 0.6,
                'heart': 0.05,
                'rupee': 0.2
                }
        
        

class Slime(Enemy):
    def __init__(self, game, pos, *args, **kwargs):
        self.game = game
        self.pos = vec(pos)
        self.walk_frames = self.game.imageLoader.enemy_img['slime']
        super().__init__()
        
        self.state = 'WALKING'
        
        self.hit_rect = pg.Rect(0, 0, int(st.TILESIZE * 0.8), 
                                int(st.TILESIZE * 0.6))
        
        self.damage = 0.5
        self.hp = 3
        # knockback stats
        self.kb_time = 1
        self.kb_intensity = 1
        
    
    def destroy(self):
        # create two little slimes
        for i in range(-45, 90, 90):
            # calculate vector between slime and player, and rotate it
            # either -45 or 45 degrees
            rot = (self.pos - self.game.player.pos).rotate(i)
            rot = rot.normalize() * st.GLOBAL_SCALE
            s = Slime_small(self.game, self.pos + rot)
            s.knockback(self, 2, 0.05)
        
        super().destroy()
        


class Slime_small(Enemy):
    def __init__(self, game, pos, *args, **kwargs):
        self.game = game
        self.pos = vec(pos)
        self.walk_frames = self.game.imageLoader.enemy_img['slime_small']
        super().__init__()
        
        self.hit_rect = pg.Rect(0, 0, int(st.TILESIZE * 0.4), 
                                int(st.TILESIZE * 0.3))
        
        self.maxspeed = 10 * st.GLOBAL_SCALE
        self.friction = 0
        
        self.damage = 0.25
        self.hp = 2
        # knockback stats
        self.kb_time = 1
        self.kb_intensity = 1
        
        self.data = {
                'name': 'slime_small',
                'x': self.pos.x,
                'y': self.pos.y,
                'width': self.rect.width,
                'height': self.rect.height
                }
        
        self.drop_rates = {
                'none': 0.08,
                'heart': 0.1,
                'rupee': 0.1,
                'mana': 0.8
                }


      
class Bat(Enemy):
    def __init__(self, game, pos, *args, **kwargs):
        self.game = game
        self.pos = vec(pos)
        self.walk_frames = [self.game.imageLoader.enemy_img['bat'][0],
                            self.game.imageLoader.enemy_img['bat'][1]]
        self.idle_frames = [self.game.imageLoader.enemy_img['bat'][2]]
        super().__init__()
        
        self.hit_rect = pg.Rect(0, 0, int(st.TILESIZE * 0.8), 
                                int(st.TILESIZE * 0.6))
        
        self.anim_speed = 150
        self.damage = 0.5
        self.hp = 3
        self.aggro_dist = 50 * st.GLOBAL_SCALE
        self.maxSpeed = 0.5 * st.GLOBAL_SCALE
        # knockback stats
        self.kb_time = 1
        self.kb_intensity = 1
        self.timer = 0
        
        self.drop_rates = {
                'none': 0.8,
                'heart': 0.15,
                'rupee': 0.3
                }
            
    
    def update(self):
        super().update()
        
        self.hit_rect.center = self.rect.center
        
        # state machine
        if self.state != 'HITSTUN':
            dist = self.pos - self.game.player.pos
            if self.state == 'IDLE':
                if dist.length_squared() < self.aggro_dist ** 2 / 2:
                    self.state = 'SEEK'
                
            if self.state == 'SEEK':
                if dist.length_squared() > self.aggro_dist ** 2:
                    self.state = 'WALKING'
                    
            elif self.state == 'WALKING':
                if dist.length_squared() < self.aggro_dist ** 2:
                    self.state = 'SEEK'
                
                self.timer += 1
                if self.timer > st.FPS * 10:
                    self.state = 'IDLE'
                    self.timer = 0
        

        