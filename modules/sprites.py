import pygame as pg
import pickle
from os import path
import traceback
from random import choice, choices
import sys
import json

import functions as fn
import settings as st
import cutscenes as cs

vec = pg.math.Vector2

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

vecNull = vec(0, 0)
vecR = vec(RIGHT)
vecL = vec(LEFT)

PLACEHOLDER_IMG = pg.Surface((st.TILESIZE, st.TILESIZE))
PLACEHOLDER_IMG.fill(st.RED)

# load a dictionary of sprites.py namespace
module_dict = sys.modules[__name__].__dict__

# load enemy stats from json file
enemystats = json.loads(open(path.join(st.ENEMY_FOLDER, 
                                       'enemystats.json')).read())

  
def create(game, data, offset=vec(0, st.GUI_HEIGHT)):
    d = data
    g = game
    # takes a dictionary of sprite properties
    name = d['name'].capitalize()
    #instantiate the sprite 
    spr = module_dict[name](g, (d['x'] + offset.x, d['y'] + offset.y),
                                (d['width'], d['height']))
    for key, value in d.items():
        try:
            setattr(spr, key, value)
        except:
            print('cant set value of {0} for {1}'.format(key, spr))
    
    if hasattr(spr, 'on_create'):
        # do initialisation stuff after ___init__()
        spr.on_create()
    
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
        self.start_screen = fn.loadImage('new_game.png')
        self.player_img = {
            'walk': fn.img_list_from_strip('knight_strip.png', 16, 16,
                                                0, 10),
            'attack': fn.img_list_from_strip('knight_attack.png', 16, 16,
                                                0, 4)
            }
        
        self.tileset_dict = {key: fn.tileImage(key, 8, 8) 
                                for key in self.tileset_names}
        # set the image for testing
        self.tileset_image = fn.loadImage(self.tileset_names[0], 1)
        self.solid_img ={
            'block': fn.getSubimg(self.tileset_image, 16, 16, (16, 0)),
            'sign':  fn.loadImage('sign.png'),
            'chest': fn.img_list_from_strip('chest.png', 16, 16, 0, 2),
            'switch': fn.img_list_from_strip('switch.png', 16, 16, 0, 2),
            'conveyor': fn.img_list_from_strip('treadmill.png', 16, 16, 0, 4),
            'platform': fn.loadImage('platform.png')
            }

        self.doors_image = fn.loadImage('doors_strip.png', 1)
        
        self.door_image_dict = {
                'W': fn.getSubimg(self.doors_image, 24, 32, (0, 0), (24, 32)),
                'N': fn.getSubimg(self.doors_image, 32, 24, (32, 0), (32, 24)),
                'E': fn.getSubimg(self.doors_image, 24, 32, (72, 0), (24, 32)),
                'S': fn.getSubimg(self.doors_image, 32, 24, (96, 8), (32, 24))
                }
        
        self.door_key_image_dict = {
                'W': fn.getSubimg(self.doors_image, 24, 32, (128, 0), (24, 32)),
                'N': fn.getSubimg(self.doors_image, 32, 24, (160, 0), (32, 24)),
                'E': fn.getSubimg(self.doors_image, 24, 32, (200, 0), (24, 32)),
                'S': fn.getSubimg(self.doors_image, 32, 24, (224, 8), (32, 24))
                }
              
        self.room_img = fn.img_list_from_strip('minimap_strip_7x5.png',
                                                  7, 5, 0, 20)
        
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
                                               0, 7),
            'slime': fn.img_list_from_strip('slime_strip.png', 16, 16, 0, 10),
            'slime_small': fn.img_list_from_strip('slime_strip.png', 16, 16, 
                                                 0, 10, size=st.TILESIZE_SMALL),
            'bat': fn.img_list_from_strip('bat_strip.png', 16, 16, 0, 9),
            'sorcerer_boss': fn.img_list_from_strip('evil_sorcerer_strip.png', 
                                                    32, 48, 0, 5),
            'blade_trap': fn.loadImage('blade_trap.png')
            }
        
        self.npc_img = {
                'merchant': fn.loadImage('merchant.png')
                }
        
        self.inv_item_strip = fn.img_list_from_strip('inv_item_strip.png', 
                                                     16, 16, 0, 25) 
        
        self.bottles_strip = fn.img_list_from_strip('bottles_strip.png', 
                                                    16, 16, 0, 10)
        
        self.bottle_img = {
                'empty': self.bottles_strip[0],
                'red potion': self.bottles_strip[1],
                'green potion': self.bottles_strip[2],
                'blue potion': self.bottles_strip[3]
                }
        
        self.inv_item_img = {
                'sword': self.inv_item_strip[0],
                'staff': self.inv_item_strip[1],
                'bow': self.inv_item_strip[2],
                'hookshot': self.inv_item_strip[3],
                'bottle': self.bottles_strip[0],
                'lamp': self.inv_item_strip[5],
                }
        
        self.item_strip1 = fn.img_list_from_strip('item_strip2.png', 8, 8, 
                                                 0, 5, size=st.TILESIZE_SMALL)
        self.rupees = fn.img_list_from_strip('rupees.png', 8, 8, 
                                                 0, 5, size=st.TILESIZE_SMALL)
        self.hookshot_strip = fn.img_list_from_strip('hookshot2.png', 16, 16,
                                                     0, 2)
        
        self.item_img = {
            'sword': fn.loadImage('sword.png'),
            'staff': fn.loadImage('staff.png'),
            'bow': fn.loadImage('bow.png'),
            'hookshot': self.hookshot_strip[0],
            'heart': self.item_strip1[0],
            'rupee': self.item_strip1[1], 
            'key': self.item_strip1[2],
            'mana': self.item_strip1[3],
            'arrow':  fn.loadImage('arrow.png'),
            'bombs': fn.loadImage('bomb.png'),
            'bomb_drop': self.item_strip1[4]
            }
        
        self.shop_items = {
                'heart': self.item_img['heart'].copy(),
                'red potion': self.bottle_img['red potion'].copy(),
                'green potion': self.bottle_img['green potion'].copy(),
                'blue potion': self.bottle_img['blue potion'].copy(),
                'small key': self.item_img['key'].copy()
                }
        
        self.item_anims = {
                'sword': fn.img_list_from_strip('sword_anim.png', 16, 16,
                                                0, 16)
                }
        
        self.projectiles = fn.img_list_from_strip('projectiles.png', 8, 8, 
                                    0, 7, size=st.TILESIZE_SMALL)
        
        self.effects = {
                'blink1': fn.img_list_from_strip('blink1.png', 16, 16, 0, 4),
                'magic_explosion': fn.img_list_from_strip(
                                    'magic_explosion.png', 32, 32, 0, 8),
                'bomb_explosion': fn.img_list_from_strip(
                                    'explosion.png', 32, 32, 0, 7)
                }
        
        self.gui_img = {
            'background': fn.loadImage('inventory_bg.png'),
            'cursor': [fn.loadImage('cursor.png'), pg.Surface((16, 16), 
                    flags=pg.SRCALPHA)],
            'health': fn.loadImage('health_string.png'),
            'hearts': fn.img_list_from_strip('hearts_strip.png', 8, 8, 
                                               0, 6),
            'magic_items': fn.loadImage('magic_and_items.png'),
            'magicbar': fn.loadImage('magicbar.png'),
            'arrows': fn.img_list_from_strip('arrows.png', 8, 8, 0, 5, 
                                             size=st.TILESIZE_SMALL)
            }
        
        self.font = st.FONT
        
        # FOR TESTING
        self.map_sprites = {
                'skeleton': self.enemy_img['skeleton'][0],
                'slime': self.enemy_img['slime'][0],
                'bat': self.enemy_img['bat'][0],
                'chest': self.solid_img['chest'][0],
                'block': self.solid_img['block']
                }
        
        
        self.light_mask_img = fn.loadImage('light_yellow.png', scale=1)
        


class Player(pg.sprite.Sprite):
    def __init__(self, game,  pos):
        self.group = game.all_sprites
        pg.sprite.Sprite.__init__(self)
        self.layer = 10
        self.group.add(self, layer=self.layer)
        self.game = game

        # images for animation
        self.image_strip = self.game.imageLoader.player_img['walk']

        self.walk_frames = {
                LEFT: [self.image_strip[6], self.image_strip[7]],
                RIGHT: [self.image_strip[2], self.image_strip[3]],
                UP: [self.image_strip[4], self.image_strip[5]],
                DOWN: [self.image_strip[0], self.image_strip[1]]
                }
        
        self.idle_frames = {
                LEFT: [self.image_strip[6]],
                RIGHT: [self.image_strip[2]],
                UP: [self.image_strip[9]],
                DOWN: [self.image_strip[8]]
                }

        self.attack_strip = self.game.imageLoader.player_img['attack']
        
        self.attack_frames = {
                LEFT: [self.attack_strip[3]],
                RIGHT: [self.attack_strip[2]],
                UP: [self.attack_strip[1]],
                DOWN: [self.attack_strip[0]]
                }
        
        self.fall_frames = [self.image_strip[6], self.image_strip[4], 
                            self.image_strip[2], self.image_strip[0]]
        self.fall_time = 0
        self.falling_time = 0
        self.ticks_to_fall = 800  # 1.5 seconds roughly
        self.eff_by_hole = False
        self.eff_by_conveyor = False
        self.eff_by_platform = False

        self.image = self.walk_frames[DOWN][0]
        
        self.sound = self.game.soundLoader

        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        # spawning position when player falls into a hole
        self.spawn_pos = vec(pos)
        self.rect.center = pos
        self.hit_rect = st.PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.dir = vec(DOWN)
        self.lastdir = vec(DOWN)
        self.friction = vec(0, 0)
        self.state = 'IDLE'
        
        self.lampState = 'OFF'
        self.hp = 3.0
        self.max_hp = st.PLAYER_HP_START
        self.mana = 10
        self.max_mana = 10
        
        # animation frames for heart refill
        self.heart_refill_frames = 0
        self.target_health = 0
        self.mana_refill_frames = 0
        self.target_mana = 0
                
        self.itemA = None
        self.itemB = None
        self.item_using = None

        self.anim_update = 0
        self.attack_update = 0
        self.current_frame = 0     
        
        self.item_counts = {
                'rupee': 0,
                'small key': 0,
                'arrows': 20,
                'bombs': 10
                }
        
        self.item_max = {
                'rupee': 999,
                'small key': 99,
                'arrows': 99,
                'bombs': 99
                }

        # testing a save function
        self.saveGame = self.game.saveGame
        
        # SHADOW
        self.shadow_surf = pg.Surface((12, 6)).convert_alpha()
        self.shadow_surf.fill(st.TRANS)
        self.shadow_rect = self.shadow_surf.get_rect()
        pg.draw.ellipse(self.shadow_surf, (0, 0, 0, 180), self.shadow_rect)
        


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
            keys = self.game.keys
            move = keys['DPAD']
            #move = keys['STICK_L']

            self.acc = vec(move)
            if self.acc.length_squared() > 1:
                self.acc.normalize()
            self.acc *= st.PLAYER_ACC
            
            # set image's direction based on key pressed
            if move.x == -1:        
                self.dir = vec(LEFT)
                self.lastdir = vec(LEFT)
            elif move.x == 1:              
                self.dir = vec(RIGHT)
                self.lastdir = vec(RIGHT)

            if move.y == -1:
                self.dir = vec(UP)
                self.lastdir = vec(UP)
            elif move.y == 1:
                self.dir = vec(DOWN)
                self.lastdir = vec(DOWN)

            if self.acc.length() < 0.1:
                # if velocity is less than the threshold, set state to idle
                self.state = 'IDLE'
            else:
                 # set the state to walking
                 self.state = 'WALKING'
                
            if keys['A']:
                if self.itemA:
                    self.state = 'USE_A'
                    self.vel = vec(0, 0)
                
            if keys['B']:
                if self.itemB:
                    self.state = 'USE_B'
                    self.vel = vec(0, 0)
                
        elif self.state == 'USE_A':
            self.itemA.use()
            self.attack_update += 1
            if self.attack_update > self.itemA.cooldown:
                self.attack_update = 0
                self.state = 'IDLE'
                self.itemA.reset()
        
        elif self.state == 'USE_B':
            self.itemB.use()
            self.attack_update += 1
            if self.attack_update > self.itemB.cooldown:
                self.attack_update = 0
                self.state = 'IDLE'
                self.itemB.reset()
                
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
                self.pos = vec(self.spawn_pos)
                self.image = self.idle_frames[(self.lastdir.x, self.lastdir.y)][0]
                # adjust the rect after image is normal size again
                self.rect = self.image.get_rect()
                #self.state = 'IDLE'
                self.stun(3)
            else:
                self.falling_time = pg.time.get_ticks()  # set fall time to current time

        elif self.state == 'PUSHING':
            keys = self.game.keys
            
            # set the acceleration vector based on key presses
            if self.lastdir == LEFT or self.lastdir == RIGHT:
                move_x = keys['DPAD'].x
            else:
                move_x = 0
            if self.lastdir == UP or self.lastdir == DOWN:
                move_y = keys['DPAD'].y
            else:
                move_y = 0

            self.acc = vec(move_x, move_y)
            if self.acc.length_squared() > 1:
                self.acc.normalize()
            self.acc *= st.PLAYER_ACC
            
            # set image's direction based on key pressed
            if move_x == -1:        
                self.dir = vec(LEFT)
                #self.lastdir = vec(LEFT)

            if move_x == 1:              
                self.dir = vec(RIGHT)
                #self.lastdir = vec(RIGHT)

            if move_y == -1:
                self.dir = vec(UP)
                #self.lastdir = vec(UP)

            if move_y == 1:
                self.dir = vec(DOWN)
                #self.lastdir = vec(DOWN)

            if self.acc.length() < 0.1:
                # if velocity is less than the threshold, set state to idle
                self.state = 'IDLE'

        # FOR DEBUG TESTING
        if self.game.debug:
            if self.game.key_down == pg.K_PAGEUP:
                self.hp += 0.25
                self.mana += 0.5
                #self.item_counts['rupee'] += 1
                #self.item_counts['small key'] += 1
                for key, value in self.item_counts.items():
                    self.item_counts[key] += 1
            elif self.game.key_down == pg.K_PAGEDOWN:
                self.hp -= 0.25
                self.mana -= 0.5
                #self.item_counts['rupee'] -= 1
                #self.item_counts['small key'] -= 1
                for key, value in self.item_counts.items():
                    self.item_counts[key] -= 1


    def update(self):
        # get player input
        self.get_keys()
        
        # add acceleration to velocity
        self.vel += self.acc

        # calculate friction
        self.friction *= 0
        if self.vel.length_squared() > 0:
            self.friction = vec(self.vel) * -1
            self.friction = self.friction.normalize()
            self.friction *= st.PLAYER_FRICTION
            # apply friction
            self.vel += self.friction

        # limit velocity
        if self.vel.length_squared() > st.PLAYER_MAXSPEED ** 2:
            self.vel.scale_to_length(st.PLAYER_MAXSPEED)        
        elif self.vel.length_squared() < 0.01:
            self.vel *= 0
              
        # add velocity to position
        self.pos += self.vel
        if self.state != 'HITSTUN':
            self.acc *= 0
        
        self.rect.center = self.pos
        # collision detection
        if self.state != 'HOOKSHOT':
            self.hit_rect.centerx = self.pos.x
            fn.collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            fn.collide_with_walls(self, self.game.walls, 'y')

        # position the rect at the bottom of the hitbox
        # leave 1 pixel space so that the game can detect collision
        # with solid objects
        self.rect.midbottom = self.hit_rect.midbottom
        self.rect.bottom = self.hit_rect.bottom + 1        
        
        # refill hearts if target health changed
        self.fillHearts()
        self.fillMana()
        
        # restrain items between 0 and max
        self.hp = max(0, min(self.hp, self.max_hp))
        self.mana = max(0, min(self.mana, self.max_mana))
        for key, value in self.item_counts.items():
            self.item_counts[key] = max(0, min(self.item_counts[key], 
                                               self.item_max[key]))
        
        # player animations
        self.animate()
        
        self.eff_by_hole = False
        self.eff_by_conveyor = False
        self.eff_by_platform = False
        
        # lamp consumes mana
        if self.lampState != 'OFF' and self.mana > st.LAMP_MANA:
            self.mana -= st.LAMP_MANA      
        else:
            self.lampState = 'OFF'
        

    def animate(self):
        now = pg.time.get_ticks()

        if self.state == 'WALKING':
            if now - self.anim_update > 200:
                self.anim_update = now
                self.current_frame = (self.current_frame + 1) % len(
                                      self.walk_frames[LEFT])
                
                self.image = self.walk_frames[(self.lastdir.x, 
                                self.lastdir.y)][self.current_frame]
        
        elif self.state == 'PUSHING':
            # ADD OWN ANIMATION FOR PUSHING!!!
            if now - self.anim_update > 200:
                self.anim_update = now
                self.current_frame = (self.current_frame + 1) % len(
                                      self.walk_frames[LEFT])
                
                self.image = self.walk_frames[(self.lastdir.x, 
                                self.lastdir.y)][self.current_frame]
        
        elif self.state == 'IDLE':
            self.image = self.idle_frames[(self.lastdir.x, self.lastdir.y)][0]

        elif self.state == 'USE_A' or self.state == 'USE_B':
            self.image = self.attack_frames[(self.lastdir.x, self.lastdir.y)][0]
        
        elif self.state == 'HITSTUN':
            self.image = self.idle_frames[(self.lastdir.x, self.lastdir.y)][0]
            # flicker to indicate damage
            try:
                alpha = next(self.damage_alpha)
                self.image = self.lastimage.copy()
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
                # adjust rect to the new image size
                self.rect = self.image.get_rect()
            
    
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
                self.acc = knockdir * intensity
                self.state = 'HITSTUN'
                self.lastimage = self.image.copy()
                self.damage_alpha = iter(st.DAMAGE_ALPHA * time)
                
           
    def fillHearts(self):
        if self.hp < self.target_health:
            self.heart_refill_frames += 1
            if self.heart_refill_frames > st.FPS // 20:
                self.hp += 0.25
                self.heart_refill_frames = 0      
        else:
            self.target_health = 0
    
    
    def fillMana(self):
        if self.mana < self.target_mana:
            self.mana_refill_frames += 1
            if self.mana_refill_frames > st.FPS // 60:
                self.mana += 0.2
                self.mana_refill_frames = 0
        else:
            self.target_mana = 0
            

    def draw_before(self):

        # draw a shadow
        self.shadow_rect.centerx = self.rect.centerx
        self.shadow_rect.bottom = self.rect.bottom + 2
        
        self.game.screen.blit(self.shadow_surf, self.shadow_rect)
        


class Solid(pg.sprite.Sprite):
    '''
    Container Class for all solid objects
    '''
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = vec(pos)
        self.size = size
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
        super().__init__(game, pos, size)
        
        self.image = pg.Surface(size, pg.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        
        
        
class Block(Solid):
    '''
    A solid block with an image, always same size
    ''' 
    def __init__(self, game, pos, size, **kwargs):
        super().__init__(game, pos, size)
        
        self.image = self.game.imageLoader.solid_img['block']
        
    
    
class Block_push(Solid):
    def __init__(self, game, pos, size, **kwargs):
        super().__init__(game, pos, size)
        
        self.image = self.game.imageLoader.solid_img['block']
        self.size = self.image.get_size()
        self.rect = pg.Rect(self.pos, self.size)
        self.hit_rect = self.rect.copy()

        offset = vec(4, 4)
        self.interact_rect = self.rect.inflate(offset)
        self.interact_rect.center = self.hit_rect.center
        
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
        self.push_timer = 0
    
    
    def update(self):
        player = self.game.player
        if self.interact_rect.colliderect(player.hit_rect):
            # if player pushes, move in that direction
            self.push_timer += 1
            if self.push_timer > 0.8 * st.FPS:
                self.acc = vec(player.dir)
                player.state = 'PUSHING'
        else:
            self.vel *= 0
            self.push_timer = 0
        
        self.vel += self.acc  
        self.acc *= 0
        self.pos += self.vel
        self.rect.topleft = self.pos
        
        # collision with walls
        self.hit_rect.left = self.pos.x
        fn.collide_with_walls_topleft(self, self.game.walls, 'x')
        self.hit_rect.top = self.pos.y
        fn.collide_with_walls_topleft(self, self.game.walls, 'y')
        
        self.interact_rect.center = self.hit_rect.center
    
    
        
class Sign(Solid):
    '''
    A sign that the player can interact with
    ''' 
    def __init__(self, game, pos, size, **kwargs):
        super().__init__(game, pos, size)
        self.image = self.game.imageLoader.solid_img['sign']
        self.reading = False
        
        try:
            self.text = cs.text_dict[kwargs['text']]
        except:
            pass
    
    
    def on_create(self):
        self.text = cs.text_dict[self.text]
        
        
    def update(self):
        if (pg.sprite.collide_rect(self.game.player, self) and 
            self.game.player.dir == vec(UP)):
            if self.game.keys['X'] and len(self.game.dialogs) == 0:
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
        super().__init__(game, pos, size)    
        
        try:
            self.loot = kwargs['loot']
            self.loot_amount = kwargs['loot_amount']
            if self.loot_amount <= 1:
                self.text = cs.text_dict['chest_opened'].format(
                        self.loot_amount, self.loot)
            else:
                self.text = cs.text_dict['chest_opened'].format(
                        self.loot_amount, self.loot + "s")
        except:
            pass
        # TO DO: Image showing the item
        
        self.image = self.game.imageLoader.solid_img['chest'][0]
        self.size = self.image.get_size()
        self.image_open = self.game.imageLoader.solid_img['chest'][1]
        self.open = False
        
    
    def on_create(self):
        if self.loot_amount <= 1:
            self.text = cs.text_dict['chest_opened'].format(
                    self.loot_amount, self.loot)
        else:
            self.text = cs.text_dict['chest_opened'].format(
                    self.loot_amount, self.loot + "s")
        
    
     
    def update(self):
        if (pg.sprite.collide_rect(self.game.player, self) and 
            self.game.player.dir == vec(UP)):
            if self.game.keys['X'] and not self.open:
                # open chest
                self.open = True
                self.image = self.image_open
                self.game.state = 'CUTSCENE'
                cs.Textbox(self.game, (st.WIDTH / 2, st.HEIGHT / 3 * 2), 
                           self.text)
                self.game.player.item_counts[self.loot] += self.loot_amount
            else:
                if (self.game.state == 'CUTSCENE' and 
                    len(self.game.dialogs) == 0):
                    self.game.state = 'GAME'
                  
                    

class Door(Solid):
    '''
     A closed door that disappears if the player achieves a goal
    '''
    def __init__(self, game, pos,**kwargs):
        super().__init__(game, pos, size=(0, 0))
        
        self.image = self.game.imageLoader.door_image_dict[kwargs['direction']]
        self.size = self.image.get_size()
        
        self.rect = pg.Rect(self.pos, self.size)
        self.hit_rect = self.rect.copy()
        
        

class Keydoor(Solid):
    '''
     A closed door that opens if the player has a key
    '''
    def __init__(self, game, pos, size, **kwargs):
        super().__init__(game, pos, size)
        
        self.dir_dict = {
                'S': DOWN,
                'N': UP,
                'E': RIGHT,
                'W': LEFT
        }
    
    def on_create(self):
        self.image = self.game.imageLoader.door_key_image_dict[self.direction]
        self.size = self.image.get_size()
        self.rect = pg.Rect(self.pos, self.size)
        self.hit_rect = self.rect.copy()

        offset = vec(10, 10)
        self.interact_rect = self.rect.inflate(offset)
        self.interact_rect.center = self.hit_rect.center
        
    
    def update(self):
        self.interact_rect.center = self.hit_rect.center
        player = self.game.player
        if (self.interact_rect.colliderect(player.rect) and 
            player.dir == self.dir_dict[self.direction]):
                    
            if player.item_counts['small key'] == 0:
                # if player doesn't have a key
                if (self.game.keys['X'] and 
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
                if self.game.keys['X']:
                    player.item_counts['small key'] -= 1
                    
                    # remove self from room data
                    index = self.game.dungeon.room_index
                    room = self.game.dungeon.rooms[index[0]][index[1]]
                    room.locked_doors.remove(self.direction)
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
        if player.state == 'HOOKSHOT':
            return
        if (player.state != 'FALL' and not player.eff_by_hole 
            and not player.eff_by_platform):
            if fn.collide_hit_rect(player, self):
                # Attract the player to the center of the hole
                desired = self.rect.center - player.pos
                mag = desired.length()
                force = desired.normalize() * 10 / mag
                player.pos += force
                if desired.length_squared() < 50:
                    # set the player back to the entrance point
                    #player.pos = vec(player.spawn_pos)
                    #player.stun(3)
                    # ^moved to player.get_keys()
                    player.state = 'FALL'
                else:
                    player.eff_by_hole = True
        
        # enemies  
        '''       DOES NOT WORK    
        for enemy in self.game.enemies:
            if enemy.state != 'FALL' and not enemy.eff_by_hole:
                if fn.collide_hit_rect(enemy, self):
                    print(enemy.state)
                    # Attract the player to the center of the hole
                    desired = self.rect.center - enemy.pos
                    mag = desired.length()
                    force = desired.normalize() * 10 / mag
                    enemy.pos += force
                    if desired.length_squared() < 500:
                        enemy.state = 'FALL'
                    else:
                        enemy.eff_by_hole = True
        '''
                    
    
    def updateData(self):
        pass
    
    
    
class Switch(pg.sprite.Sprite):
    def __init__(self, game, pos, size, **kwargs):
        self.game = game
        self.group = self.game.all_sprites
        self.layer = 0
        pg.sprite.Sprite.__init__(self)

        self.group.add(self, layer=self.layer)
            
        self.pos = vec(pos)
        self.size = size
        
        self.image = self.game.imageLoader.solid_img['switch'][0]
        self.size = self.image.get_size()
        self.rect = pg.Rect(self.pos, self.size)
        #self.hit_rect = self.rect.copy()
        offset = vec(-8, -8)
        self.hit_rect = self.rect.inflate(offset)

        self.pushed = False
    
    
    def update(self):
        player = self.game.player
        # checks for collision with the player or a solid object
        if (self.hit_rect.colliderect(player.hit_rect) or 
            pg.sprite.spritecollide(self, self.game.walls, False, 
                                    fn.collide_hit_rect)):
            self.pushed = True
            self.image = self.game.imageLoader.solid_img['switch'][1]
            
            # testing
            self.game.dungeon.room_current.openDoors()
        else:
            self.pushed = False
            self.image = self.game.imageLoader.solid_img['switch'][0]
            
            self.game.dungeon.room_current.shutDoors()
        


class Conveyor(pg.sprite.Sprite):
    def __init__(self, game, pos, size, direction, speed, **kwargs):
        self.game = game
        self.group = self.game.all_sprites
        self.layer = 0
        pg.sprite.Sprite.__init__(self)

        self.group.add(self, layer=self.layer)
            
        self.pos = vec(pos)
        self.size = size             
        self.direction = vec(direction)
        
        images = self.game.imageLoader.solid_img['conveyor']
        # rotate images based on direction
        # right is 0°
        angle = self.direction.angle_to(vec(RIGHT))
        self.images = [pg.transform.rotate(images[i], angle) 
                       for i in range(len(images))]
        self.image = self.images[0]
        
        self.size = self.image.get_size()
        self.rect = pg.Rect(self.pos, self.size)
        offset = vec(-4, -4)
        self.hit_rect = self.rect.inflate(offset)
        
        self.speed = speed
        
        self.anim_speed = 10 / speed
        self.timer = 0
        self.current_frame = 0

        
    
    
    def update(self):
        self.animate()        
        player = self.game.player         
        if not player.eff_by_conveyor:
            if self.hit_rect.colliderect(player.hit_rect):
               player.pos += self.direction * self.speed
               player.eff_by_conveyor = True
            
    
    def animate(self):
        self.rect.topleft = self.pos
        now = pg.time.get_ticks()
        if now - self.timer > self.anim_speed:
            self.timer = now
            self.current_frame = (self.current_frame + 1) % len(
                                      self.images)
            self.image = self.images[self.current_frame]
        
        
        
class Moving_platform(pg.sprite.Sprite):
    def __init__(self, game, pos, size, **kwargs):
        self.game = game
        self.group = self.game.all_sprites
        self.layer = 0
        pg.sprite.Sprite.__init__(self)

        self.group.add(self, layer=self.layer)
            
        self.pos = vec(pos)
        self.size = size
        
        self.image = self.game.imageLoader.solid_img['platform']
        
        self.size = self.image.get_size()
        self.rect = pg.Rect(self.pos, self.size)
        offset = vec(-4, -4)
        self.hit_rect = self.rect.inflate(offset)
        
    
    def update(self):
        self.direction = vec(self.direction_x, self.direction_y)
        self.pos += self.direction * self.movement_speed
        self.rect.topleft = self.pos
        self.hit_rect.center = self.rect.center

        player = self.game.player            
        if not player.eff_by_platform:
            if self.hit_rect.colliderect(player.hit_rect):
                player.pos += self.direction * self.movement_speed
                player.eff_by_platform = True
               
        hits = pg.sprite.spritecollide(self, self.game.all_sprites, False)
        for hit in hits:
            if isinstance(hit, Moving_platform) or isinstance(hit, Wall):
                if hit != self:
                    self.movement_speed *= -1
                    
            
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
        self.cursor_images[1].fill(st.TRANS)
        self.cursor_pos = vec(24, 40)
        
        # "health" string
        self.health_string = self.game.imageLoader.gui_img['health']
        # images for the player health
        self.heart_images = self.game.imageLoader.gui_img['hearts']
        self.magic_image = self.game.imageLoader.gui_img['magic_items']
        self.magic_bar = self.game.imageLoader.gui_img['magicbar']
        for i in range(len(self.heart_images)):
            self.heart_images[i] = pg.transform.scale(self.heart_images[i], 
                                  (8, 8))
            
        self.inv_index = [0, 0]
        
        self.bar_stretch = 100
        
        # empty item matrix
        self.inv_size = [5, 5]
        self.inv_items = [[None for j in range(self.inv_size[1])] 
                           for i in range(self.inv_size[0])] 
        
        self.anim_update = 0
        self.anim_delay = 300
        self.current_frame = 0
        
        self.heart_frames = 0


    def update(self):
        if self.game.keys['START'] and self.game.state != 'MENU_TRANSITION':
            self.menu = not self.menu

        if self.menu:
            self.game.state = 'MENU_TRANSITION'

            # sliding down animation
            if self.pos != (0, 0):
                self.pos.y += st.SCROLLSPEED_MENU
                self.pos.y = min(0, self.pos.y)
            
            else:
                self.game.state = 'MENU'
    
            # let the player move the cursor and select items                
            self.move_cursor()               

        else:
            # sliding up animation
            if self.pos != self.start_pos:
                self.game.state = 'MENU_TRANSITION'
                self.pos.y -= st.SCROLLSPEED_MENU
                self.pos.y = min(0, self.pos.y)
            else:
                if self.game.state != 'GAME':
                    self.game.state = 'GAME'


    def draw(self):
        self.image.fill(st.BLACK)
        # draw player health
        player = self.game.player
        for i in range(int(player.max_hp)):
            # calculate position
            if i < st.PLAYER_HP_ROW:
                pos = (6 + 10 * i, st.HEIGHT - 34)
            else:
                pos = (6 + 10 * (i - st.PLAYER_HP_ROW), st.HEIGHT - 24)

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
        
        self.image.blit(self.health_string, (25, st.HEIGHT - 42))
        
        # draw magic bar and item slots
        # MEMO: might want to make multiple images !!!!
        
        #draw mana bar
        bar_stretched = self.magic_bar.copy()
        mana_pct = self.game.player.mana / self.game.player.max_mana
        factor = mana_pct * 28
        one_minus_factor = int((1 - mana_pct) * 27)
        bar_stretched = pg.transform.scale(bar_stretched, 
                       (bar_stretched.get_width(), int(factor)))
        self.image.blit(bar_stretched, (82, st.HEIGHT - 31 + one_minus_factor))
        
        self.image.blit(self.magic_image, (77, st.HEIGHT - 48))
       
        # draw other item amounts
        # rupees
        font = self.game.imageLoader.font
        font_size = 8
        x_off = 166
        text_pos = vec(x_off, 201)
        number = 'x%03d' % self.game.player.item_counts['rupee']
        fn.draw_text(self.image, number,
                     font, font_size, st.WHITE, text_pos, align='midleft')
        
        # keys
        text_pos = vec(x_off, 217)
        number = 'x %02d' % self.game.player.item_counts['small key']
        fn.draw_text(self.image, number,
                     font, font_size, st.WHITE, text_pos, align='midleft')

        # draw the mini map
        map_pos = (192, st.HEIGHT - 44)
        self.image.blit(self.map_img, map_pos)

        # draw the inventory background
        self.image.blit(self.gui_img, (0, 0))
        
        # draw the items
        self.draw_items()
        
        # draw the cursor
        self.draw_cursor()
        
        self.game.screen.blit(self.image, self.pos)
        
       
    def move_cursor(self):
        keys = self.game.keys
        # set the movement vector based on key presses
        move = keys['DPAD_MENU']
        
        # change the inventory index
        self.inv_index[0] += int(move.x)
        self.inv_index[1] += int(move.y)        
        self.inv_index[0] = fn.clamp(self.inv_index[0], 0, self.inv_size[0] - 1)
        self.inv_index[1] = fn.clamp(self.inv_index[1], 0, self.inv_size[1] - 1)
        
        # move the cursor
        self.cursor_pos += move * 24
        
        self.cursor_pos.x = fn.clamp(self.cursor_pos.x, 24, 120)
        self.cursor_pos.y = fn.clamp(self.cursor_pos.y, 40, 136)
        
        if move != (0, 0):
            self.anim_update = self.anim_delay + pg.time.get_ticks()
            self.current_frame = 0
        
        # select items    
        player = self.game.player 
        x = self.inv_index[1]
        y = self.inv_index[0]                     
        if keys['A']:
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
                # if no item is at x, y
                pass
        
        if keys['B']:
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
                # if no item is at x, y
                pass
    
    
    def draw_cursor(self):
        # MEMO: ANIMATE CURSOR!
        now = pg.time.get_ticks()
        if now - self.anim_update > self.anim_delay:
            self.anim_update = now
            self.current_frame = (self.current_frame + 1) % len(
                                  self.cursor_images)
        
        self.image.blit(self.cursor_images[self.current_frame], self.cursor_pos)
        
    
    def draw_items(self):
        player = self.game.player
        
        for i in range(self.inv_size[0]):
            for j in range(self.inv_size[1]):
                pos = vecNull
                pos.x = (24 + 24 * i)
                pos.y = (40 + 24 * j)
                
                item = self.inv_items[j][i]
                
                if item:
                    self.image.blit(item.inv_image, pos)
                                  
        # draw Item name
        font = self.game.imageLoader.font
        font_size = 8
        text_pos = vec(80, 168)
        item = self.inv_items[self.inv_index[1]][self.inv_index[0]]
        if item:
            text = item.type
            fn.draw_text(self.image, text, font, font_size, st.WHITE, 
                         text_pos, align='center')
        
        # draw item in slots A and B
        if player.itemA:
            posA = vec(111, 216)
            self.draw_item(player, player.itemA, posA, font, font_size)

        if player.itemB:    
            posB = vec(135, 216)   
            self.draw_item(player, player.itemB, posB, font, font_size)

    
    def draw_item(self, player, slot, pos, font, font_size):
        '''
        helper function that draws items and item amounts in Slots A and B
        '''
        image = slot.inv_image   
        self.image.blit(image, pos)
        
        # draw item amounts
        if slot.type == 'bow':
            text = str(player.item_counts['arrows'])
            text_pos = pos + vec(12, 14)
            fn.draw_text(self.image, text, font, font_size, st.WHITE, 
                     text_pos, align='center')
        elif slot.type == 'bombs':
            text = str(player.item_counts['bombs'])
            text_pos = pos + vec(12, 14)
            fn.draw_text(self.image, text, font, font_size, st.WHITE, 
                     text_pos, align='center')
            
    
    def addItem(self, item):
        # find first emtpy slot (from top left to bottom right)
        # then put the item there
        for i in range(self.inv_size[0]):
            for j in range(self.inv_size[1]):
                if self.inv_items[i][j] == None:
                    self.inv_items[i][j] = item
                    return
                
    def addItemSlot(self, item, slot):
        # find first emtpy slot (from top left to bottom right)
        # then put the item there
        try:
            self.inv_items[slot[1]][slot[0]] = item
        except Exception:
            traceback.print_exc()
            


class Bottle:
    def __init__(self, game, player):
        self.player = player
        self.game = game
        self.type = 'bottle'
        self.content = None
        self.inv_image = self.game.imageLoader.bottle_img['empty']
        self.cooldown = 10
    
    
    def fill(self, substance):
        if self.content == None:
            self.content = substance
            self.inv_image = self.game.imageLoader.bottle_img[substance]
            self.type += ' (' + substance +')'
    
    
    def use(self):
        if self.content == 'red potion':
            self.player.target_health = self.player.max_hp
        elif self.content == 'green potion':
            self.player.target_mana = self.player.max_mana
        elif self.content == 'blue potion':
            self.player.target_mana = self.player.max_mana
            self.player.target_health = self.player.max_hp
        
        self.inv_image = self.game.imageLoader.bottle_img['empty']
        self.content = None
        
        if self.player.target_health != 0 or self.player.target_mana != 0:
            self.cooldown += 1


    def reset(self):
        pass
    


class Bombs:
    '''
    inventory item for Bombs
    '''
    def __init__(self, game, player):
        self.player = player
        self.game = game
        self.type = 'bombs'
        self.inv_image = self.game.imageLoader.item_img['bombs']
        self.cooldown = 40
        self.fired = False
    
    def use(self):
        # drop a bomb
        if self.player.item_counts[self.type] > 0 and not self.fired:
            self.player.item_counts[self.type] -= 1
            Bomb(self.game, self.player.pos + self.player.dir * 12)
            self.fired = True


    def reset(self):
        self.fired = False
    


class Bomb(pg.sprite.Sprite):
    '''
    The Bomb that the player drops
    '''
    def __init__(self, game,  pos):
        self.group = game.all_sprites
        pg.sprite.Sprite.__init__(self)
        self.layer = game.player.layer
        self.group.add(self, layer=self.layer)
        self.game = game

        self.image = self.game.imageLoader.item_img['bombs']
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.game = game
        self.pos = vec(pos)
        self.rect.center = self.pos
        self.hit_rect.center = self.pos
        
        
        self.timer = 0
        self.fuse_time = 4 * st.FPS
        
    
    def update(self):
        self.timer += 1
        if self.timer < self.fuse_time:
            # flash animation
            pass
        else:
            # create Explosion sprite
            images = self.game.imageLoader.effects['bomb_explosion']
            Explosion(self.game, vec(self.pos), images, 80, damage=3, 
                                    sound=self.game.soundLoader.snd['bomb'],
                        hit_rect=pg.Rect(images[0].get_rect().inflate(-6, -6)))
            self.kill()
    


class Lamp:
    def __init__(self, game, player):
        self.player = player
        self.game = game
        self.type = 'lamp'
        self.inv_image = self.game.imageLoader.inv_item_img[self.type]
        self.used = False
        self.cooldown = st.LAMP_SWITCH_TIME
        
    
    def use(self):
        if not self.used:
            # lamp state machine
            if self.player.lampState == 'OFF':
                self.player.lampState = 'ON_TRANSITION'
            elif self.player.lampState == 'ON':
                self.player.lampState = 'OFF_TRANSITION'
            self.used = True
    
    
    def reset(self):
        self.used = False
        if self.player.lampState == 'OFF_TRANSITION':
            self.player.lampState = 'OFF'
        elif self.player.lampState == 'ON_TRANSITION':
            self.player.lampState = 'ON'
                
   
             
class AttackItem(pg.sprite.Sprite):
    def __init__(self, game, player):
        self.group = game.all_sprites
        self.layer = player.layer
        pg.sprite.Sprite.__init__(self)
        self.player = player
        self.game = game
        
        self.image = self.game.imageLoader.item_img[self.type].copy()
        self.inv_image = self.game.imageLoader.inv_item_img[self.type]
        
        self.cooldown = 20


    def update(self):
        # delete sprite if animation is over
        if not self.player.state == 'USE_A' and not self.player.state == 'USE_B':
            self.game.all_sprites.remove(self)
            
    
    def use(self):
        self.image = self.game.imageLoader.item_img[self.type].copy()
        self.group.add(self, layer=self.layer)
        
        self.pos = vec(0, 0)
        self.rot = 0

        self.dir = self.player.lastdir
        # rotate image based on player direction and set position
        if self.dir == UP:
            self.rot = 0
            self.pos = self.player.pos + vec(-4, -24)
            
        elif self.dir == DOWN:
            self.rot = 180
            self.pos = self.player.pos + vec(0, 4)
            
        elif self.dir == RIGHT:
            self.rot = 270
            self.pos = self.player.pos + vec(7, -4)
            
        elif self.dir == LEFT:
            self.rot = 90
            self.pos = self.player.pos + vec(-20, -4)

        self.image = pg.transform.rotate(self.image, self.rot)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center
    
    


class Sword(AttackItem):
    def __init__(self, game, player):
        self.type = 'sword'
        super().__init__(game, player)
        self.cooldown = 15
        img = self.game.imageLoader.item_anims[self.type]
        self.animations = {
                UP: img[:4],
                DOWN: img[4:8],
                RIGHT: img[8:12],
                LEFT: img[12:]
                }
        
        self.anim_update = 0
        self.current_frame = 0
        self.anim_speed = 80
        
        self.fired = False
        self.damage = 1


    def update(self):
        super().update()

        for enemy in pg.sprite.spritecollide(self, self.game.enemies, False):
            if enemy.state != 'HITSTUN':
                enemy.hp -= self.damage
                enemy.knockback(self.player, 1, 0.1)
                
    
    def use(self):
        # overwrites super().use() for the animation
        # maybe refactor this later and put back into parent
        self.group.add(self, layer=self.layer)
        
        self.pos = vec(0, 0)
        self.dir = self.player.lastdir
        if self.dir == UP:
            self.pos = self.player.pos + vec(-6, -22)
        elif self.dir == DOWN:
            self.pos = self.player.pos + vec(-9, 1)
        elif self.dir == RIGHT:
            self.pos = self.player.pos + vec(4, -14)
        elif self.dir == LEFT:
            self.pos = self.player.pos + vec(-20, -14)
  
        anim = self.animations[(self.dir.x, self.dir.y)]
        self.image = anim[self.current_frame]
        
        now = pg.time.get_ticks()
        if now - self.anim_update > self.anim_speed:
            self.anim_update = now
            self.current_frame = (self.current_frame + 1) % len(anim)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center
        
        if not self.fired:
            # play slash sound      
            self.game.soundLoader.snd['slash'].play()
            self.fired = True
            
    
    def reset(self):
        self.fired = False
        self.current_frame = 0
        
        

class Staff(AttackItem):
    def __init__(self, game, player):
        self.type = 'staff'
        super().__init__(game, player)
        self.fired = False
        self.cooldown = 15
        
    
    def use(self):
        super().use()
        if not self.fired and self.player.mana >= 1:
                self.lastdir = self.player.lastdir
                Magicball(self.game, self, self.rect.center)
                self.game.soundLoader.snd['magic1'].play()
                self.player.mana -= 1
                self.fired = True
        
    
    def reset(self):
        self.fired = False
        


class Bow(AttackItem):
    def __init__(self, game, player):
        self.type = 'bow'
        super().__init__(game, player)
        self.fired = False
        self.cooldown = 50
        
    
    def use(self):
        # overwrites super().use() for the animation
        # maybe refactor this later and put back into parent
        self.image = self.game.imageLoader.item_img[self.type].copy()
        self.group.add(self, layer=self.layer)
        
        self.pos = vec(0, 0)
        self.rot = 0

        self.dir = self.player.lastdir
        # rotate image based on player direction and set position
        if self.dir == UP:
            self.rot = 0
            self.pos = self.player.pos + vec(-8, -22)
            
        elif self.dir == DOWN:
            self.rot = 180
            self.pos = self.player.pos + vec(-6, 0)
            
        elif self.dir == RIGHT:
            self.rot = 270
            self.pos = self.player.pos + vec(3, -8)
            
        elif self.dir == LEFT:
            self.rot = 90
            self.pos = self.player.pos + vec(-18, -8)

        self.image = pg.transform.rotate(self.image, self.rot)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center
        
        if not self.fired and self.player.item_counts['arrows'] > 0:
            self.lastdir = self.player.lastdir
            Arrow(self.game, self, self.rect.center)
            self.player.item_counts['arrows'] -= 1
            self.fired = True
    
    
    def reset(self):
        self.fired = False
        
        

class Hookshot(AttackItem):
    def __init__(self, game, player):
        self.type = 'hookshot'
        super().__init__(game, player)
        self.spr_chain = self.game.imageLoader.hookshot_strip[1]
        self.fired = False
        

    def update(self):
        # KNOWN BUGS:
        # WHEN PLAYER GETS HIT DURING SHOOTING,
        # HOOKSHOT MAY NOT BE ABLE TO RETURN TO PLAYER       
        if not self.hit:
            self.player.state = 'HOOKSHOT'
            self.pos += self.vel
            self.rect.center = self.pos
            self.hit_rect.center = self.rect.center
            # collide with walls, enemies, items etc
            # REFACTOR THIS MAYBE WITH ALL_SPRITES AS GROUP COLLISION
            # NEEDS ONLY 1 LIST
            wall_hits = pg.sprite.spritecollide(self, self.game.walls, False)
            enemy_hits = pg.sprite.spritecollide(self, self.game.enemies, False)
            item_hits = pg.sprite.spritecollide(self, self.game.item_drops, False)
            if wall_hits:
                for wall in wall_hits:
                    if self.hit_rect.colliderect(wall.hit_rect):
                        self.hit = True
                        if isinstance(wall, Block) or isinstance(wall, Chest):
                            # if hitting a block or chest, pull the player to it
                            self.pulling = wall
                        else:
                            # create blinking effect
                            Effect(self.game, vec(self.pos), 
                                     self.game.imageLoader.effects['blink1'],
                                     50)
            if enemy_hits:
                if self.hit_rect.colliderect(enemy_hits[0].hit_rect):
                    # stun the enemy
                    enemy_hits[0].freeze(2.5 * st.FPS)
                    self.hit = True
            if item_hits:
                if self.hit_rect.colliderect(item_hits[0].hit_rect):
                    self.grabbed = item_hits[0]
                    self.hit = True
            if ((self.pos - self.player.pos).length_squared() 
                        > self.maxlen ** 2):
                # if max length is reached, pull in
                self.hit = True
            
        else:
            if not self.pulling:
                self.pos -= self.vel
                self.rect.center = self.pos
                self.hit_rect.center = self.rect.center
                if self.hit_rect.colliderect(self.player.rect):
                    self.kill()
                    self.player.state = 'IDLE'
                
                # pull grabbed item towards player
                if self.grabbed:
                    self.grabbed.rect.center = self.pos
            
            # pull the player towards a block
            elif self.pulling:
                self.player.state = 'HOOKSHOT'
                self.player.pos += self.vel
                
                self.player.hit_rect.centerx = self.player.pos.x
                hits = pg.sprite.spritecollide(self.player, self.game.walls, 
                                               False, fn.collide_hit_rect)
                if hits:
                    # hit from left
                    if hits[0].hit_rect.centerx > self.player.hit_rect.centerx:
                        self.player.pos.x = hits[0].hit_rect.left - self.player.hit_rect.w / 2
                    # hit from right
                    elif hits[0].hit_rect.centerx < self.player.hit_rect.centerx:
                        self.player.pos.x = hits[0].hit_rect.right + self.player.hit_rect.w / 2
                                    
                    self.player.vel.x = 0
                    self.player.hit_rect.centerx = self.player.pos.x
                    
                    self.kill()
                    self.player.state = 'IDLE'

                self.player.hit_rect.centery = self.player.pos.y
                hits = pg.sprite.spritecollide(self.player, self.game.walls, 
                                               False, fn.collide_hit_rect)
                if hits:
                    # hit from top
                    if hits[0].hit_rect.centery > self.player.hit_rect.centery:
                        self.player.pos.y = hits[0].hit_rect.top - self.player.hit_rect.h / 2
                    # hit from bottom
                    elif hits[0].hit_rect.centery < self.player.hit_rect.centery:
                        self.player.pos.y = hits[0].hit_rect.bottom + self.player.hit_rect.h / 2
                        
                    self.player.vel.y = 0
                    self.player.hit_rect.centery = self.player.pos.y
    
                    self.kill()
                    self.player.state = 'IDLE'
    
    
    def use(self):
        super().use()
        
        self.group.change_layer(self, self.player.layer - 2)
            
        self.hit = False
        self.grabbed = None
        self.pulling = None
        self.pos = vec(self.player.pos)
        self.maxlen = 6 * st.TILESIZE
        
        self.speed = 3
        self.vel = vec(0, -1).rotate(-self.rot)
        self.vel *= self.speed
        
        self.rect.center = self.pos
        
        self.hit_rect = pg.Rect((0, 0), (st.TILESIZE_SMALL, st.TILESIZE_SMALL))
        self.hit_rect.center = self.pos
        
        if not self.fired:
            self.fired = True
        
        
    def draw_before(self):
        #draw n chain links between the hookshot head and the player
        n = 10
        for i in range(n):
            # calculate a vector v from self to player
            v = self.pos - self.player.pos
            # stretch the vector based on i
            v *= (i / n)
            pos = self.player.pos + v - vec(st.TILESIZE_SMALL, st.TILESIZE_SMALL)
            self.game.screen.blit(self.spr_chain, pos)
            #pg.draw.line(self.game.screen, st.RED, (int(self.player.pos.x), 
            #            int(self.player.pos.y)), (int(self.pos.x), 
            #               int(self.pos.y)), 4)
            
    
    def reset(self):
        self.fired = False


class Projectile(pg.sprite.Sprite):
    '''
    Container class for projectiles fired by items, enemies etc.
    Sprite can have a fixed rotation based on the player's direction
    TO DO: change player to any emitter to enable enemy shooting
    '''
    def __init__(self, game, player, pos, rotating):
        self.group = game.all_sprites
        self.layer = player.layer
        pg.sprite.Sprite.__init__(self)
        self.group.add(self, layer=self.layer)
        self.player = player
        self.game = game
        self.rotating = rotating
        self.pos = vec(pos)
        
        self.vel = vec(0, 0)       
        self.anim_update = 0
        self.current_frame = 0
        
        self.state = 'SHOT'
        
        # set own direction based on the direction the player sprite is facing
        self.dir = self.player.lastdir
        
        if self.rotating:
            self.rot = 0
            if self.dir == UP:
                self.rot = 0
                # TO DO: change the position so that it fits every possible
                # sprite
                self.pos = self.player.pos + vec(8, 4)
            
            elif self.dir == DOWN:
                self.rot = 180
                self.pos = self.player.pos + vec(8, 8)
                
            elif self.dir == RIGHT:
                self.rot = 270
                self.pos = self.player.pos + vec(8, 8)
                
            elif self.dir == LEFT:
                self.rot = 90
                self.pos = self.player.pos + vec(0, 8)
                
            self.image = pg.transform.rotate(self.image, self.rot)
        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center
        
        
    def update(self):
        if self.state == 'SHOT':
            hits_walls = pg.sprite.spritecollide(self, self.game.walls, 
                                                 False, fn.collide_hit_rect)
            if hits_walls:
                self.state = 'HIT_WALL'
                
            hits_enemies = pg.sprite.spritecollide(self, self.game.enemies, 
                                                   False, fn.collide_hit_rect)
            if hits_enemies:
                for enemy in hits_enemies:
                    enemy.hp -= self.damage
                    self.state = 'HIT_ENEMY'
                    self.enemy = enemy
    
            self.acc = vec(self.dir) * self.speed
            self.vel += self.acc
            
            # limit velocity
            if self.vel.length_squared() > self.max_speed ** 2:
                self.vel.scale_to_length(self.max_speed)
                
            self.pos += self.vel
        
        else:
            self.destroy()
        
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center
        
        try:        
            self.animate()
        except:
            # has no animation frames
            pass
        
        
                
    
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.anim_update > self.anim_speed:
            self.anim_update = now
            self.current_frame = (self.current_frame + 1) % len(
                                  self.image_frames)
            self.image = self.image_frames[self.current_frame]
            
    
    def destroy(self):
        self.vel *= 0
        self.kill()

      

class Magicball(Projectile):
    def __init__(self, game, player, pos, rotating=False):  
        self.image_frames = [img.copy() for img 
                             in game.imageLoader.projectiles[2:5]]
        self.image = self.image_frames[0]
        super().__init__(game, player, pos, rotating)      
        
        self.speed = 2
        self.max_speed = 3
        self.damage = 4
        self.anim_speed = 100
        
        self.effect = None
        
    
    def destroy(self):
        #super().destroy()
        
        if self.effect == None:
            for img in self.image_frames:
                img.fill(st.TRANS)
            #self.effect = Effect(self.game, vec(self.pos), 
               #self.game.imageLoader.effects['magic_explosion'], 50)
            images = self.game.imageLoader.effects['magic_explosion']
            self.effect = Explosion(self.game, vec(self.pos), images, 50, 
                                    damage=3, 
                                    sound=self.game.soundLoader.snd['magic2'],
                        hit_rect=pg.Rect(images[0].get_rect().inflate(-6, -6)))

        
        else:
            if self.effect.end:
                self.kill()

class Arrow(Projectile):
    def __init__(self, game, player, pos, rotating=True):
        self.image = game.imageLoader.item_img['arrow']           
        super().__init__(game, player, pos, rotating)
        
        self.speed = 1
        self.max_speed = 3
        self.damage = 1
        self.anim_speed = 100
        
        self.destroy_timer = 0
        
    
    def destroy(self):
        if self.state == 'HIT_WALL':
            # push the arrow a bit into a wall
            if self.vel.length_squared() > 0:
                self.pos += self.vel.normalize() * 3
            self.vel *= 0
        elif self.state == 'HIT_ENEMY':
            self.pos = self.enemy.pos
        self.destroy_timer += 1
        if self.destroy_timer > 50:           
            self.kill()
          
    

class Item:       
    def drop(name, game, pos):
        if name in Item.__dict__:
            # instanciate the given sprite by its name
            Item.__dict__[name](game, pos)
        elif name == 'none':
            pass
        else:
            print('Can\'t drop {}.'.format(name))
            
            
    class ItemDrop(pg.sprite.Sprite):
        def __init__(self, game, pos):
            self.game = game                    
            self.player = self.game.player
            self.pos = vec(pos)
            self.groups = self.game.all_sprites, self.game.item_drops
            self.layer = self.game.player.layer - 1
            pg.sprite.Sprite.__init__(self)
            
            for g in self.groups:
                g.add(self, layer=self.layer)
            
            self.timer = 0
            self.duration = 6 * st.FPS
            
            self.alpha = iter([i for i in range(255, 0, -10)] * 3)
        
        
        def update(self):
            if fn.collide_hit_rect(self.player, self):
                self.collect()
            
            self.timer += 1
            if self.timer >= self.duration:
                try:
                    alpha = next(self.alpha)
                    self.image = self.lastimage.copy()
                    self.image.fill((255, 255, 255, alpha), 
                                    special_flags=pg.BLEND_RGBA_MULT)
                except:
                    self.kill()
            else:
                self.lastimage = self.image.copy()
        
        
        def collect(self):
            self.kill()
        
        
    class heart(ItemDrop):
        def __init__(self, game, pos):
            super().__init__(game, pos)
            self.image = self.game.imageLoader.item_img['heart']
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hit_rect = self.rect
           
            
        def collect(self):
            self.player.hp += 1
            self.game.soundLoader.snd['heart'].play()
            super().collect()
            
            
    class mana(ItemDrop):
        def __init__(self, game, pos):
            super().__init__(game, pos)          
            self.image = self.game.imageLoader.item_img['mana']
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hit_rect = self.rect
           
            
        def collect(self):
            self.player.mana += 5
            super().collect()
            
     
    class rupee(ItemDrop):
        def __init__(self, game, pos):
            super().__init__(game, pos)           
            self.image = self.game.imageLoader.item_img['rupee']
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hit_rect = self.rect
            
            self.value = 1
            
            
        def collect(self):
            self.player.item_counts['rupee'] += self.value
            self.game.soundLoader.snd['rupee'].play()
            super().collect()
            
    
    class rupee5(rupee):
        def __init__(self, game, pos):
            super().__init__(game, pos)           
            self.image = self.game.imageLoader.rupees[1]
            self.value = 5
    
    
    class rupee20(rupee):
        def __init__(self, game, pos):
            super().__init__(game, pos)           
            self.image = self.game.imageLoader.rupees[2]
            self.value = 20
            
    
    class rupee50(rupee):
        def __init__(self, game, pos):
            super().__init__(game, pos)           
            self.image = self.game.imageLoader.rupees[3]
            self.value = 50
    
    
    class rupee100(rupee):
        def __init__(self, game, pos):
            super().__init__(game, pos)           
            self.image = self.game.imageLoader.rupees[4]
            self.value = 100
            
        
    class key(ItemDrop):
        def __init__(self, game, pos):
            super().__init__(game, pos)         
            self.image = self.game.imageLoader.item_img['key']
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hit_rect = self.rect
            
        
        def collect(self):
            self.player.item_counts['key'] += 1
            super().collect()
            
            

class ItemShop(pg.sprite.Sprite):
    def __init__(self, game, pos, name):
        self.game = game                    
        self.player = self.game.player
        self.pos = vec(pos)
        self.group = self.game.all_sprites
        self.layer = self.game.player.layer - 1
        self.name = name
        pg.sprite.Sprite.__init__(self)

        self.group.add(self, layer=self.layer)
        
        self.price = item_prices[self.name]
        self.image = self.game.imageLoader.shop_items[self.name]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.hit_rect = self.rect

        # draw item cost on image
        price_image = pg.Surface((st.TILESIZE, st.TILESIZE))
        price_image.fill(st.WHITE)
        file = self.game.imageLoader.font
        font_size = 10
        font = pg.font.Font(file, font_size)
        font.set_bold(False)
        text_surface = font.render(str(self.price), False, st.BLACK)
        GenericSprite(self.game, (self.pos.x, self.pos.y + st.TILESIZE), 
                      text_surface, self.layer)
        
# ----------------------- ENEMIES ---------------------------------------------
        
class Enemy(pg.sprite.Sprite):
    '''
    Container class for all basic enemies
    '''
    def __init__(self, game, pos):
        self.game = game
        self.pos = vec(pos)
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
        self.freeze_frames = 0
        
        self.fall_time = 0
        self.falling_time = 0
        self.ticks_to_fall = 800
        self.eff_by_hole = False

        #self.maxSpeed = 0.5
        #self.seekForce = 0.5
        self.anim_update = 0
        self.walk_update = 0
        self.current_frame = 0
        #self.anim_speed = 300
        
        # load instance variables from file
        self.loadAttr()
        
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
        
        elif self.state == 'SEEK':
            desired = (self.game.player.pos - self.pos)
            if desired.length_squared() > 0:
                desired = desired.normalize() * self.maxSpeed
            steer = desired - self.vel
            if steer.length_squared() > self.seekForce ** 2:
                steer.scale_to_length(self.seekForce)
            self.acc = steer
                
        elif self.state == 'HITSTUN' or self.state == 'DYING':
            # can't change acceleration when stunned
            pass
    
        elif self.state == 'FALL':
            if self.fall_time == 0:
                self.fall_time = pg.time.get_ticks()
                self.fall_time += self.ticks_to_fall  # add N seconds for the fall time
            if self.falling_time > self.fall_time:  # fall until time passes N amount
                self.kill()
            else:
                self.falling_time = pg.time.get_ticks()
        
        
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
        if self.hp <= 0 and self.state != 'DYING':
            #self.destroy()
            self.vel *= 0
            self.anim_speed = 100
            self.state = 'DYING'
            
        if self.state == 'FROZEN':
            self.freeze_frames -= 1
            if self.freeze_frames <= 0:
                self.state = 'WALKING'
                       
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
        
        elif self.state == 'FROZEN':
            # tint the image blue
            self.image = self.lastimage.copy()
            self.image.fill((0, 0, 150), special_flags=pg.BLEND_RGB_ADD)
                      
        elif self.state == 'IDLE':
            if hasattr(self, 'idle_frames'):
                if now - self.anim_update > self.anim_speed:
                    self.anim_update = now
                    self.current_frame = (self.current_frame + 1) % len(
                                          self.idle_frames)
                    self.image = self.idle_frames[self.current_frame]
        
        elif self.state == 'DYING':
            if hasattr(self, 'die_frames'):
                if now - self.anim_update > self.anim_speed:
                    self.anim_update = now
                    if self.current_frame == len(self.die_frames):
                        self.destroy()
                    else:
                        self.image = self.die_frames[self.current_frame]
                        self.current_frame += 1


    def collide_with_player(self):
        if self.state == 'DYING':
            return
        
        # detect collision with player
        player = self.game.player
        if fn.collide_hit_rect(player, self):
            if (player.state != 'HITSTUN' and player.state != 'HOOKSHOT' and
                player.state != 'FALL'):
                player.knockback(self, self.kb_time, self.kb_intensity)
                player.hp -= self.damage
            
    
    def knockback(self, other, time, intensity):
        if self.state != 'HITSTUN':
            self.vel *= 0
            # calculate vector from other to self
            knockdir = self.pos - other.pos
            if knockdir.length_squared() > 0:
                knockdir = knockdir.normalize()
                self.acc = knockdir * intensity
            else:
                self.acc *= 0
            self.state = 'HITSTUN'
            self.lastimage = self.image.copy()
            self.damage_alpha = iter(st.DAMAGE_ALPHA * time)
            
    
    def freeze(self, frames):
        if self.state != 'FROZEN':
            self.lastimage = self.image.copy()
            self.vel *= 0
            self.state = 'FROZEN'
            self.freeze_frames = frames
        
    
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
                print('error. cannot drop item', c)


    def loadAttr(self):
        # loads instance variables from a dictionary
        if self.name in enemystats:
            for key, value in enemystats[self.name].items():
                try:
                    setattr(self, key, enemystats[self.name][key])
                except:
                    pass
        else:
            for key, value in enemystats['default'].items():
                try:
                    setattr(self, key, enemystats['default'][key])
                except:
                    pass



class Skeleton(Enemy):
    def __init__(self, game, pos, *args, **kwargs):
        self.name = 'skeleton'
        self.walk_frames = game.imageLoader.enemy_img[self.name][:2]
        self.die_frames = game.imageLoader.enemy_img[self.name][2:]
        super().__init__(game, pos)
        
        self.state = 'WALKING'
        
        self.hit_rect = pg.Rect(0, 0, int(st.TILESIZE * 0.8), 
                                int(st.TILESIZE * 0.6))
        
        

class Slime(Enemy):
    def __init__(self, game, pos, *args, **kwargs):
        self.name = 'slime'
        self.walk_frames = game.imageLoader.enemy_img[self.name][:4]
        self.die_frames = game.imageLoader.enemy_img[self.name][5:]
        super().__init__(game, pos)
        
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
            rot = rot.normalize()
            s = Slime_small(self.game, self.pos + rot, name='slime_small')
            s.knockback(self, 2, 0.05)
        
        super().destroy()
        


class Slime_small(Enemy):
    def __init__(self, game, pos, *args, **kwargs):
        self.name = 'slime_small'
        self.walk_frames = game.imageLoader.enemy_img[self.name][:4]
        self.die_frames = game.imageLoader.enemy_img[self.name][5:]
        super().__init__(game, pos)
        
        self.hit_rect = pg.Rect(0, 0, int(st.TILESIZE * 0.4), 
                                int(st.TILESIZE * 0.3))
        
        self.maxspeed = 10
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
        '''
        self.drop_rates = {'none': 0.01,
                'rupee': 0.5,
                'rupee5': 0.4,
                'rupee20': 0.3,
                'rupee50': 0.2,
                'rupee100': 0.1
                
                }'''


      
class Bat(Enemy):
    def __init__(self, game, pos, *args, **kwargs):
        self.name = 'bat'
        self.walk_frames = [game.imageLoader.enemy_img[self.name][0],
                            game.imageLoader.enemy_img[self.name][1]]
        self.idle_frames = [game.imageLoader.enemy_img[self.name][2]]
        self.die_frames = game.imageLoader.enemy_img[self.name][3:]
        super().__init__(game, pos)
        self.image = self.idle_frames[0]
        
        self.hit_rect = pg.Rect(0, 0, int(st.TILESIZE * 0.8), 
                                int(st.TILESIZE * 0.6))
        
        self.anim_speed = 150
        self.damage = 0.5
        self.hp = 3
        self.aggro_dist = 50
        self.maxSpeed = 0.6
        # knockback stats
        self.kb_time = 1
        self.kb_intensity = 1
        self.timer = 0
        
        self.drop_rates = {
                'none': 0.1,
                'heart': 0.0,
                'rupee5': 0.8
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
             
                    
                    
class Blade_trap(pg.sprite.Sprite):
    def __init__(self, game, pos, *args, **kwargs):
        self.game = game
        self.pos = vec(pos)
        self.groups = self.game.all_sprites, self.game.traps
        self.layer = self.game.player.layer + 1
        pg.sprite.Sprite.__init__(self)
        
        for g in self.groups:
            g.add(self, layer=self.layer)

        self.image = game.imageLoader.enemy_img['blade_trap']
        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect = self.rect.copy()
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.friction = 0.1
        self.state = 'IDLE'
        self.maxSpeed = 2
        
        self.damage = 1
        # knockback stats
        self.kb_time = 2
        self.kb_intensity = 2
        
    
    def move(self):
        player = self.game.player
        # set acceleration vector
        # based on where the player is
        # when in IDLE state
        if self.state == 'IDLE':
            if (self.pos.x - st.TILESIZE_SMALL < player.pos.x < 
                self.pos.x + st.TILESIZE_SMALL):
                self.acc.y = fn.sign(player.pos.y - self.pos.y)
                self.state = 'MOVING'
            if (self.pos.y - st.TILESIZE_SMALL < player.pos.y < 
                self.pos.y + st.TILESIZE_SMALL):
                self.acc.x = fn.sign(player.pos.x - self.pos.x)
                self.state = 'MOVING'
    
    
    def update(self):
        self.move()
        
        # save previous position
        pos = (self.pos.x, self.pos.y)
        
        self.vel += self.acc
        
        if self.state == 'RETREAT':
            self.vel *= 0.5
                   
        # reset acceleration
        if self.state == 'IDLE':
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
        hit_x = fn.collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        hit_y = fn.collide_with_walls(self, self.game.walls, 'y')
        
        # position the hitbox
        self.rect.center = self.hit_rect.center
        
        if hit_x or hit_y:
            self.state = 'IDLE'
            
        hits = pg.sprite.spritecollide(self, self.game.traps, False)
        for hit in hits:
            if hit != self:
                # if another trap was hit, reverse acceleration
                self.acc *= -1
                self.pos = vec(pos)
                self.rect.center = self.pos
                self.hit_rect.center = self.rect.center
                self.state = 'RETREAT'
        
        self.collide_with_player()
        
        
    def collide_with_player(self):
        # detect collision
        player = self.game.player
        if fn.collide_hit_rect(player, self):
            if player.state != 'HITSTUN' and player.state != 'HOOKSHOT':
                player.knockback(self, self.kb_time, self.kb_intensity)
                player.hp -= self.damage
        
        
        

class Sorcerer_boss(Enemy):
    def __init__(self, game, pos, *args, **kwargs):
        self.name = 'sorcerer_boss'
        self.walk_frames = game.imageLoader.enemy_img[self.name][:4]
        self.hit_image = game.imageLoader.enemy_img[self.name][4]
        super().__init__(game, pos)
        
        self.state = 'IDLE'        
        self.hit_rect = pg.Rect((0, 0), (self.image.get_width() * 0.6, 
                                 self.image.get_height() * 0.7))
        self.hit_rect.center = self.rect.center
        
        self.damage = 0.5
        self.hp = 20
        # knockback stats
        self.kb_time = 1
        self.kb_intensity = 2
        
        self.timer = 0
        self.shoot_time = 5 * st.FPS
        self.stun_timer = 0
        
        self.bats = pg.sprite.Group()
        
    
    def update(self):
        if self.state == 'HITSTUN':
            self.stun_timer += 1
            if self.stun_timer >= 20:
                self.state = 'IDLE'
                self.stun_timer = 0
        # change the drawing layer in relation to the player
        if self.hit_rect.top > self.game.player.hit_rect.top:
            for g in self.groups:
                g.change_layer(self, self.game.player.layer + 1)
        else:
            for g in self.groups:
                g.change_layer(self, self.game.player.layer - 1)
        
        # update the position
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect.center = self.pos

        self.collide_with_player()
        if self.hp <= 0:
            self.destroy()
            
        if self.state == 'FROZEN':
            self.freeze_frames -= 1
            if self.freeze_frames <= 0:
                self.state = 'IDLE'

        # calculate a vector from self to player
        dist = self.game.player.rect.center - self.pos
        angle = dist.angle_to(vecR)
        # set the image based on the vector's angle to a normal vector 
        # pointing to the right (vecR)
        if (-45 < angle < 45):
            # right
            self.image = self.walk_frames[3]
        elif (45 < angle < 135):
            # up
            self.image = self.walk_frames[2]
        elif (135 < angle < 180) or (-180 < angle < -135):
            # left
            self.image = self.walk_frames[1]
        else:
            # down
            self.image = self.walk_frames[0]
            
        if self.state == 'HITSTUN':
            # flicker to indicate damage
            try:
                alpha = next(self.damage_alpha)
                #self.image = self.lastimage.copy()
                self.image = self.hit_image.copy()
                self.image.fill((255, 255, 255, alpha), 
                                special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.state = 'IDLE'
        
        
        self.timer += 1
        if self.timer >= self.shoot_time:
            self.timer = 0
            if len(self.bats) <= 3:
                pos = self.pos + (dist.normalize() * st.TILESIZE)
                b = Bat(self.game, pos)
                self.bats.add(b)
                b.state = 'SEEK'
                
        

class NPC(Solid):
    def __init__(self, game, pos):
        self.game = game
        self.pos = vec(pos)
        self.groups = self.game.all_sprites, self.game.npcs
        self.layer = self.game.player.layer + 1
        pg.sprite.Sprite.__init__(self)
        
        for g in self.groups:
            g.add(self, layer=self.layer)

        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect = self.rect
        

    def update(self):
        # change the drawing layer in relation to the player
        if self.hit_rect.top > self.game.player.hit_rect.top:
            for g in self.groups:
                g.change_layer(self, self.game.player.layer + 1)
        else:
            for g in self.groups:
                g.change_layer(self, self.game.player.layer - 1)
        
        # update the position
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        # collision with walls
        self.hit_rect.centerx = self.pos.x
        fn.collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        fn.collide_with_walls(self, self.game.walls, 'y')

        # position the hitbox at the bottom of the image
        self.rect.midbottom = self.hit_rect.midbottom
        


class Merchant(NPC):
    def __init__(self, game, pos):
        self.name = 'merchant'
        self.idle_frames = [game.imageLoader.npc_img[self.name]]
        super().__init__(game, pos)
        
        self.hit_rect = pg.Rect(0, 0, int(st.TILESIZE * 0.8), 
                                int(st.TILESIZE * 0.6))
    
        

# ------------ Particles ------------------------------------------------------
                    
class Effect(pg.sprite.Sprite):
    '''
    Sprite that plays an animation from a given image list
    and then destroys itself
    '''
    def __init__(self, game,  pos, images, delay):
        self.group = game.all_sprites
        pg.sprite.Sprite.__init__(self)
        self.layer = 0
        self.group.add(self, layer=self.layer)
        self.game = game

        self.timer = 0
        self.frame = 0
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.game = game
        self.pos = pos
        self.delay = delay
        self.end = False
        
        
    def update(self):
        self.rect.center = self.pos
        now = pg.time.get_ticks()      
        if self.frame == len(self.images):
            self.kill()
            self.end = True
        if now - self.timer > self.delay:
            self.timer = now
            self.image = self.images[self.frame]
            self.frame = self.frame + 1
            
            
    
class Explosion(Effect):
    '''
    Effect that also damages enemies or the player
    '''
    def __init__(self, game,  pos, images, delay, **kwargs):
        super().__init__(game,  pos, images, delay)
        self.damage = kwargs['damage']
        if 'hit_rect' in kwargs:
            # define custom hit rect
            self.hit_rect = kwargs['hit_rect']
        else:    
            self.hit_rect = self.image.get_rect()
        
        self.hit_rect.center = self.rect.center
        if 'sound' in kwargs:
            kwargs['sound'].play()
            
            
    def update(self):
        self.rect.center = self.pos
        now = pg.time.get_ticks()      
        if self.frame == len(self.images):
            self.kill()
            self.end = True
        if now - self.timer > self.delay:
            self.timer = now
            self.image = self.images[self.frame]
            self.frame = self.frame + 1
            
        # collision with enemies
        hits = pg.sprite.spritecollide(self, self.game.enemies, False, 
                                       fn.collide_hit_rect)
        if hits:
            for enemy in hits:
                if enemy.state != 'HITSTUN':
                    enemy.hp -= self.damage
                    enemy.knockback(self, 1, 0.1)
        
            


class Animation(pg.sprite.Sprite):
    # sprite that displays a list of images as an animation
    def __init__(self, game,  pos, images, speed):
        self.group = game.all_sprites
        pg.sprite.Sprite.__init__(self)
        self.layer = 0
        self.group.add(self, layer=self.layer)
        self.game = game

        self.timer = 0
        self.current_frame = 0
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.pos = pos
        self.anim_speed = speed
        
        
    def update(self):
        self.rect.topleft = self.pos
        now = pg.time.get_ticks()     
        if now - self.timer > self.anim_speed:
            self.timer = now
            self.current_frame = (self.current_frame + 1) % len(
                                      self.images)
            self.image = self.images[self.current_frame]
            
            

class Particle(pg.sprite.Sprite):
    def __init__(self, game, pos, diameter):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self)
        self.layer = -1
        self.groups.add(self, layer=self.layer)
        self.game = game
        self.pos = vec(pos)
        
        self.image = pg.Surface((diameter, diameter))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
               
        pg.draw.ellipse(self.image, (255, 100, 0), self.rect)
        self.alpha = 255
        
        self.rect.center = self.pos
        
        self.decay = 10
        

    def update(self):
        # ADD VECTOR MOVEMENT
        self.rect.center = self.pos     
        self.image.set_alpha(self.alpha)      
        self.alpha -= self.decay
        if self.alpha <= 0:
            self.kill()
            
            
class GenericSprite(pg.sprite.Sprite):
    '''
    A generic sprite without an animation
    '''
    def __init__(self, game,  pos, image, layer):
        self.group = game.all_sprites
        pg.sprite.Sprite.__init__(self)
        self.layer = layer
        self.group.add(self, layer=self.layer)
        self.game = game

        self.timer = 0
        self.frame = 0
        self.image = image
        self.rect = self.image.get_rect()
        self.game = game
        self.pos = vec(pos)
        self.rect.topleft = self.pos
        
            


# -------------- Item prices --------------------------------------------------
item_prices = {
        'heart': 5,
        'red potion': 100,
        'green potion': 50,
        'blue potion': 250,
        'small key': 1000
        }