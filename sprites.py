import pygame as pg
import pickle
from os import path
import traceback
from random import choice

import functions as fn
import settings as st
#import rooms as rm

vec = pg.math.Vector2

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def export_globals():
    return globals()


class saveObject():
    def __init__(self):
        self.data = {}
        self.filename = 'savefile.dat'
        directory = path.dirname(__file__)
        self.filename = path.join(directory, self.filename)


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



class Player(pg.sprite.Sprite):
    def __init__(self, game,  pos):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # images for animation
        self.image_strip = fn.img_list_from_strip('knight_strip.png', 16, 16,
                                                    0, 10)
        self.walk_frames_l = [self.image_strip[6], self.image_strip[7]]
        self.walk_frames_r = [self.image_strip[2], self.image_strip[3]]
        self.walk_frames_u = [self.image_strip[4], self.image_strip[5]]
        self.walk_frames_d = [self.image_strip[0], self.image_strip[1]]
        self.idle_frames_l = [self.image_strip[6]]
        self.idle_frames_r = [self.image_strip[2]]
        self.idle_frames_u = [self.image_strip[9]]
        self.idle_frames_d = [self.image_strip[8]]

        self.attack_strip = fn.img_list_from_strip('knight_attack.png', 16, 16,
                                                    0, 4)

        self.attack_frames_l = [self.attack_strip[3]]
        self.attack_frames_r = [self.attack_strip[2]]
        self.attack_frames_u = [self.attack_strip[1]]
        self.attack_frames_d = [self.attack_strip[0]]

        self.image = self.walk_frames_d[0]

        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.hit_rect = st.PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.dir = vec(DOWN)
        self.lastdir = vec(DOWN)

        self.state = 'IDLE'
        self.max_hp = st.PLAYER_HP_START
        self.hp = 3.25

        self.itemA = None
        self.itemB = None

        self.sword = None

        self.anim_update = 0
        self.attack_update = 0
        self.current_frame = 0
        

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
        if not self.state == 'ATTACK':
            # acceleration
            self.acc = vec(1, 1) * st.PLAYER_ACC

            self.friction = 0.1


            keys = pg.key.get_pressed()
            # add acceleration to velocity
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.vel.x -= self.acc.x
                
                self.dir = vec(LEFT)
                self.lastdir = vec(LEFT)

            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.vel.x += self.acc.x
                
                self.dir = vec(RIGHT)
                self.lastdir = vec(RIGHT)

            if keys[pg.K_UP] or keys[pg.K_w]:
                self.vel.y -= self.acc.y

                self.dir = vec(UP)
                self.lastdir = vec(UP)

            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.vel.y += self.acc.y

                self.dir = vec(DOWN)
                self.lastdir = vec(DOWN)

            # apply friction
            self.vel *= (1 - self.friction)

            # cap speed at maximum
            if self.vel.length() > st.PLAYER_MAXSPEED:
                self.vel.scale_to_length(st.PLAYER_MAXSPEED)

            # stop the player from sliding infinitely
            if self.vel.length() < 0.1:
                self.vel = vec(0, 0)

            if self.vel.length() > 0.2:
                self.state = 'WALKING'
            else:
                self.state = 'IDLE'

            if self.game.key_down == pg.K_SPACE:
                self.state = 'ATTACK'
                self.vel = vec(0, 0)

        elif self.state == 'ATTACK':
            self.attack()
            self.attack_update += 1
            if self.attack_update > 20:
                self.attack_update = 0
                self.state = 'IDLE'

        # FOR TESTING
        if self.game.debug:
            if self.game.key_down == pg.K_PAGEUP:
                self.hp += 0.25
            elif self.game.key_down == pg.K_PAGEDOWN:
                self.hp -= 0.25



    def update(self, others):
        self.get_keys()

        self.animate()

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel
        self.hit_rect.centerx = self.pos.x
        fn.collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        fn.collide_with_walls(self, self.game.walls, 'y')

        # position the hitrect at the bottom of the image
        self.rect.midbottom = self.hit_rect.midbottom
        
        # restrain hp between 0 and max
        self.hp = max(0, min(self.hp, self.max_hp))


    def draw(self):
        self.game.screen.blit(self.image, self.rect.topleft)


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

        elif self.state == 'ATTACK':
            if self.lastdir == RIGHT:
                self.image = self.attack_frames_r[0]
            elif self.lastdir == LEFT:
                self.image = self.attack_frames_l[0]
            if self.lastdir == DOWN:
                self.image = self.attack_frames_d[0]
            elif self.lastdir == UP:
                self.image = self.attack_frames_u[0]


    def attack(self):
        if not self.game.all_sprites.has(self.sword):
            self.sword = Sword(self.game, self)
        


class Solid(pg.sprite.Sprite):
    def __init__(self, game, pos, size):
        self.groups = game.walls, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.bb_width, self.bb_height = size
        self.rect = pg.Rect(pos, (self.bb_width, self.bb_height))
        self.hit_rect = self.rect

    def update(self):
        # not used right now
        pass

    def draw(self):
        if self.image:
            self.game.screen.blit(self.image, self.rect.topleft)
            

class Wall(Solid):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)
        self.image = None
        
        
class Block(Solid):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)
        self.image = fn.getSubimg(self.game.tileset_image, 16, 16, (16, 0))
            


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
        self.gui_img = fn.loadImage('inventory_bg.png')
        self.cursor_images = [
                              fn.loadImage('cursor.png'),
                              pg.Surface((16, 16)).fill(st.TRANS)
                              ]
        self.cursor_pos = vec(24 * st.GLOBAL_SCALE, 40 * st.GLOBAL_SCALE)
        
        # "health" string
        self.health_string = fn.loadImage('health_string.png')
        # images for the player health
        self.heart_images = fn.img_list_from_strip('hearts_strip.png',8, 8, 
                                                   0, 6, scale=False)
        for i in range(len(self.heart_images)):
            self.heart_images[i] = pg.transform.scale(self.heart_images[i], 
                                  (8 * st.GLOBAL_SCALE, 8 * st.GLOBAL_SCALE))
            
        self.inv_index = [0, 0]


    def update(self):
        if self.game.key_down == pg.K_ESCAPE:
            self.menu = not self.menu

        if self.menu:
            self.game.state = 'MENU'

            # sliding down animation
            if self.pos != (0, 0):
                self.pos.y += st.SCROLLSPEED_MENU
                self.pos.y = min(0, self.pos.y)
                
            self.move_cursor()

        else:
            # sliding up animation
            if self.pos != self.start_pos:
                self.pos.y -= st.SCROLLSPEED_MENU
                self.pos.y = min(0, self.pos.y)
            else:
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

        # draw the mini map
        map_pos = (192 * st.GLOBAL_SCALE, st.HEIGHT - 44 * st.GLOBAL_SCALE)
        self.image.blit(self.map_img, map_pos)

        # draw the inventory background
        self.image.blit(self.gui_img, (0, 0))
        self.draw_cursor()
        
        self.game.screen.blit(self.image, self.pos)
        
       
    def move_cursor(self):
        key = self.game.key_down
        # arrow keys
        move_x = (key == pg.K_RIGHT) - (key == pg.K_LEFT)
        move_y = (key == pg.K_DOWN) - (key == pg.K_UP)
        # WASD 
        move_x = (key == pg.K_d) - (key == pg.K_a)
        move_y = (key == pg.K_s) - (key == pg.K_w)
        
        self.cursor_pos.x += move_x * 24 * st.GLOBAL_SCALE
        self.cursor_pos.y += move_y * 24 * st.GLOBAL_SCALE
        
        self.cursor_pos.x = fn.clamp(self.cursor_pos.x, 24 * st.GLOBAL_SCALE, 
                                     120 * st.GLOBAL_SCALE)
        self.cursor_pos.y = fn.clamp(self.cursor_pos.y, 40 * st.GLOBAL_SCALE, 
                                     136 * st.GLOBAL_SCALE)
    
    
    def draw_cursor(self):
        self.image.blit(self.cursor_images[0], self.cursor_pos)



class Sword(pg.sprite.Sprite):
    def __init__(self, game, player):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.game = game
        self.image = fn.loadImage('sword.png')

        self.pos = vec(0, 0)
        self.rot = 0

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
        if not self.player.state == 'ATTACK':
            self.game.all_sprites.remove(self)


    def draw(self):
        self.game.screen.blit(self.image, self.pos)
        
# ----------------------- ENEMIES --------------------------
        
class Enemy(pg.sprite.Sprite):
    def __init__(self, game, pos, size):
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        #self.walk_frames = images
        self.image = self.walk_frames[0]
        
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.dir = vec(DOWN)
        self.lastdir = vec(DOWN)
        self.moveTo = None
        self.acc = vec(0, 0)
        self.maxSpeed = 0.5 * st.GLOBAL_SCALE

        self.state = 'IDLE'

        self.anim_update = 0
        self.walk_update = 0
        self.current_frame = 0
        
        # testing a save function
        self.saveGame = self.game.saveGame
        
        
    def move(self):
        # acceleration
        self.acc = vec(1, 1) * 0.3

        self.friction = 0.1

        # add acceleration to velocity
        if self.moveTo == LEFT:
            self.vel.x -= self.acc.x           
            self.dir = vec(LEFT)
            self.lastdir = vec(LEFT)

        if self.moveTo == RIGHT:
            self.vel.x += self.acc.x            
            self.dir = vec(RIGHT)
            self.lastdir = vec(RIGHT)

        if self.moveTo == UP:
            self.vel.y -= self.acc.y
            self.dir = vec(UP)
            self.lastdir = vec(UP)

        if self.moveTo == DOWN:
            self.vel.y += self.acc.y
            self.dir = vec(DOWN)
            self.lastdir = vec(DOWN)

        # apply friction
        self.vel *= (1 - self.friction)

        # cap speed at maximum
        if self.vel.length() > self.maxSpeed:
            self.vel.scale_to_length(self.maxSpeed)

        # stop from sliding infinitely
        if self.vel.length() < 0.1:
            self.vel = vec(0, 0)

        if self.vel.length() > 0.2:
            self.state = 'WALKING'
        else:
            self.state = 'IDLE'
        
        
    def update(self):
        self.move()
        
        self.animate()
        
        now = pg.time.get_ticks()
        if now - self.walk_update > 2000:
            self.walk_update = now
            self.moveTo = choice([LEFT, RIGHT, DOWN, UP])
            
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel
        self.hit_rect.centerx = self.pos.x
        fn.collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        fn.collide_with_walls(self, self.game.walls, 'y')

        # position the hitrect at the bottom of the image
        self.rect.midbottom = self.hit_rect.midbottom    
        
    
    def animate(self):
        now = pg.time.get_ticks()

        if self.state == 'WALKING':
            if now - self.anim_update > 300:
                self.anim_update = now
                self.current_frame = (self.current_frame + 1) % len(
                                      self.walk_frames)
                self.image = self.walk_frames[self.current_frame]
            
            
    def draw(self):
        self.game.screen.blit(self.image, self.rect.topleft)
        


class Skeleton(Enemy):
    def __init__(self, game, pos, size):
        self.walk_frames = game.enemy_image_dict['skeleton']
        super().__init__(game, pos, size)
        

