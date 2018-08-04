import pygame as pg
from os import path
import traceback
import csv

import settings as st
import sprites as spr

vec = pg.math.Vector2


def clamp(var, lower, upper):
    # restrains a variable's value between two values
    return max(lower, min(var, upper))
    

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def collide_with_walls(sprite, group, dir_):
    if dir_ == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # hit from left
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.w / 2
            # hit from right
            elif hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.w / 2
                            
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
            
    elif dir_ == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # hit from top
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.h / 2
            # hit from bottom
            elif hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.h / 2
                
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


def screenWrap(player, dungeon):
    #checks if the player goes outside the screen
    #if they do, set their new position based on where they went
    index = list(dungeon.room_index)
    direction = ''
    new_pos = vec(player.hit_rect.center)
    if player.rect.left < st.TILESIZE:
        direction = 'LEFT'
        player.vel = vec(0, 0)
        new_pos.x  = st.WIDTH - player.rect.width - st.TILESIZE
        index[1] -= 1
    if player.rect.right > st.WIDTH - st.TILESIZE:
        direction = 'RIGHT'
        player.vel = vec(0, 0)
        new_pos.x = player.hit_rect.width + st.TILESIZE
        index[1] += 1
    if player.rect.top < st.GUI_HEIGHT + st.TILESIZE:
        player.vel = vec(0, 0)
        direction = 'UP'
        new_pos.y = st.HEIGHT - player.hit_rect.height - st.TILESIZE
        index[0] -= 1
    if player.rect.bottom > st.HEIGHT - st.TILESIZE:
        player.vel = vec(0, 0)
        direction = 'DOWN'
        new_pos.y = player.rect.height + st.GUI_HEIGHT + st.TILESIZE
        index[0] += 1
    try:
        return direction, index, new_pos
    except Exception:
        traceback.print_exc()


def transitRoom(game, group, dungeon):
    #deletes all instances in the group and adds new ones
    #based on the room data matching the given room number
    index = dungeon.room_index
    data = dungeon.rooms[index[0]][index[1]].layout
    data_small = dungeon.rooms[index[0]][index[1]].layout_small
    try:
        group.empty()
        for sprite in game.all_sprites:
            if sprite == spr.Wall:
                game.all_sprites.remove(sprite)
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] == 1:
                    spr.Wall(game, (j * st.TILESIZE, i * st.TILESIZE
                                              + st.GUI_HEIGHT), 
                                        (st.TILESIZE, st.TILESIZE))
                elif data[i][j] == 2:
                    spr.Wall(game, (j * st.TILESIZE, i * st.TILESIZE
                                              + st.GUI_HEIGHT), 
                                        (st.TILESIZE, st.TILESIZE), 'block')
        for i in range(len(data_small)):
            for j in range(len(data_small[i])):
                if data_small[i][j] == 1:
                    spr.Wall(game, (j * st.TILESIZE_SMALL, i * st.TILESIZE_SMALL
                                    + st.GUI_HEIGHT), (st.TILESIZE_SMALL, 
                                                   st.TILESIZE_SMALL * 4))
                elif data_small[i][j] == 2:
                    spr.Wall(game, (j * st.TILESIZE_SMALL, i * st.TILESIZE_SMALL
                                    + st.GUI_HEIGHT), (st.TILESIZE_SMALL * 4, 
                                                   st.TILESIZE_SMALL))
                    
        dungeon.rooms[index[0]][index[1]].visited = True
        
        return group
    except Exception:
        #if something goes wrong, return an empty group
        traceback.print_exc()
        return group
    

def loadImage(filename, scale=st.GLOBAL_SCALE):
    directory = path.dirname(__file__)
    img_folder = path.join(directory, 'images')
    file = path.join(img_folder, filename)
    try:
        img = pg.image.load(file).convert_alpha()
        width, height = img.get_width(), img.get_height()
        size = (int(width * scale), int(height * scale))
        return pg.transform.scale(img, size)
    except Exception:
        traceback.print_exc()
        return


def img_list_from_strip(filename, width, height, startpos, number, scale=True):
    directory = path.dirname(__file__)
    img_folder = path.join(directory, 'images')
    file = path.join(img_folder, filename)
    try:
        img = pg.image.load(file).convert_alpha()
    except Exception:
        traceback.print_exc()
        return
    img_set = []
    for i in range(startpos, (startpos + number)):
        rect = ((i * width, 0), (width, height))
        if scale:
            subimg = pg.transform.scale(img.subsurface(rect), 
                                        (st.TILESIZE, st.TILESIZE))
        else:
            subimg = img.subsurface(rect)
        img_set.append(subimg)
    return img_set


def getSubimg(image, width, height, topleft, scale=True):

    rect = (topleft, (width, height))
    if scale:
        subimg = pg.transform.scale(image.subsurface(rect), 
                                    (st.TILESIZE, st.TILESIZE))
    else:
        subimg = image.subsurface(rect)
    return subimg
    

def tileImageScale(filename, size_w, size_h, scale=1, 
                   alpha=False):
    directory = path.dirname(__file__)
    img_folder = path.join(directory, 'images')
    file = path.join(img_folder, filename)
    try:
        img = pg.image.load(file).convert()
        if alpha:
            color = img.get_at((0,0))
            img.set_colorkey(color)
    except Exception:
        traceback.print_exc()
        return
    
    # size of the tileset
    width, height = img.get_width(), img.get_height()
    tiles_hor = width // size_w
    tiles_vert = height // size_h
    wh_ratio = size_w / size_h
    tileset = []
    for i in range(tiles_vert):
        for j in range(tiles_hor):
            rect = (size_w * j, size_h * i, size_w, size_h)
            subimg = img.subsurface(rect)
            tileset.append(pg.transform.scale(
                    subimg, (int(st.TILESIZE_SMALL * scale * wh_ratio), 
                             int(st.TILESIZE_SMALL * scale))))
    #print(filename, len(tileset))
    return tileset


def tileRoom(game, tileset, index):
    image = pg.Surface((st.WIDTH, st.HEIGHT - st.GUI_HEIGHT))
    data = game.dungeon.rooms[index[0]][index[1]].tiles
    for i in range(len(data)):
        for j in range(len(data[i])):
            x = j * st.TILESIZE_SMALL
            y = i * st.TILESIZE_SMALL
            try:
                image.blit(tileset[data[i][j]], (x, y))
            except Exception:
                traceback.print_exc()
                return
    return image


def compare(str1, str2):
    # checks if two strings contain the same letters, but in any order
    if len(str1) != len(str2):
        return False
    
    str_temp1 = str1
    str_temp2 = str2
    for s in str1:
        if s not in str_temp2:
            return False
        else:
           str_temp2 = str_temp2.replace(s, '', 1)

    for s in str2:
        if s not in str_temp1:
            return False
        else:
           str_temp1 = str_temp1.replace(s, '', 1)
           
    return True


def keyDown(events):
    for event in events:
        if event.type == pg.KEYDOWN:
            return event.key


def tileset_from_csv(filename, size=(32, 24)):
    directory = path.dirname(__file__)
    img_folder = path.join(directory, 'rooms')
    file = path.join(img_folder, filename)
    data = []
    try:
        with open(file, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if len(row) > 1:
                    if len(row) > size[0]:
                        row.pop()
                    data.append([int(i) for i in row])
        if len(data) == size[1]:
            return data
        else:
            print('data size does not fit')
            return

    except Exception:
        traceback.print_exc()
        return

