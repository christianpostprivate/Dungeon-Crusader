import pygame as pg
from os import path
import json
#import traceback

#import functions as fn
import settings as st

vec = pg.math.Vector2


# load text strings from file        
with open(path.join(st.TEXT_FOLDER, 'texts.json'), 'r') as f:
    text_dict = json.load(f) 



class Textbox(pg.sprite.Sprite):
    def __init__(self, game, pos, text):
        self.groups = game.dialogs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        self.size = (180, 64)
        self.pos = vec(pos)
        # set position based on players position
        if self.game.player.pos.y > (st.HEIGHT - st.GUI_HEIGHT) / 2 + st.GUI_HEIGHT:
            self.pos.y *= 0.5
        else:
            self.pos.y *= 1.25
        self.image_ori = pg.Surface(self.size)
        self.image_ori.fill(st.BLACK)
        self.rect = self.image_ori.get_rect()
        self.rect.center = self.pos        
        
        self.text = text
        self.font = pg.font.Font(st.FONT, 28)
        self.words_left = []
        self.words_prev = []
        
        self.done = False
        self.scroll = False
        self.text_end = False
        self.timer = 0
        self.popup_time = 30
        
        self.margin = vec(4, 4)
        self.spacing = 0.8 * st.TILESIZE
        
        self.arrow = Arrow(self.game, self.rect.midbottom, 'S')
        
    
    def popUp(self):
        if self.timer < self.popup_time and not self.done:
            # enlarge the textbox image gradually
            w = int((self.timer / self.popup_time) * self.size[0])
            h = int((self.timer / self.popup_time) * self.size[1])
            self.image = self.image_ori.copy()
            self.image = pg.transform.scale(self.image, (w, h))
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.timer += 1
        else:
            self.done = True
            self.timer = 0
            
    
    def vanish(self):
        self.done = False
        if self.timer < self.popup_time:
            # enlarge the textbox image gradually
            w = int(self.size[0] - (self.timer / self.popup_time) * self.size[0])
            h = int(self.size[1] - (self.timer / self.popup_time) * self.size[1])
            self.image = self.image_ori.copy()
            self.image = pg.transform.scale(self.image, (w, h))
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.timer += 1
        else:
            self.kill()
            
            
    def renderText(self):
        line = 0
        color = st.WHITE
        txt = ''
        txt_temp = ''
        # create a list of words from the string
        if len(self.words_left) == 0:
            # if words_left is emtpy, use self.text
            words = self.text.split(' ')
        else:
            # if there is text left, use it
            words = self.words_left
            
        for i in range(len(words)):
            if words[i] == words[-1]:
                self.text_end = True
            # add the next word to the temporary text
            txt_temp += words[i] + ' '
            text_surface = self.font.render(txt_temp, False, color)
            
            h = (text_surface.get_height() * line + self.spacing * 
                 max(0, line - 3))
            
            if (h < self.rect.height - self.margin.y * 2):
                if (text_surface.get_width() <             
                    self.rect.width - self.margin.x * 2):
                    # if text rect fits, render it
                    txt = txt_temp
                    text_surface = self.font.render(txt, False, color)
                    text_rect = text_surface.get_rect()
                    text_rect.topleft = (self.margin.x, self.margin.y + 
                                         self.spacing * line)
                    self.image.blit(text_surface, text_rect)
                    
                else:
                    # if the text rect is wider than the Textbox, 
                    # move to next line and set the current word as the first
                    # word in txt_temp
                    line += 1
                    txt_temp = words[i] + ' '

            else:
                if self.scroll:
                    self.words_left = words[i - 1:]
                    self.scroll = False
                break
            
        if self.game.keys['X']:
            self.scroll = True
                

    def update(self):  
        if not self.done and not self.text_end:    
            # player pop up animation until done
            self.popUp()
            
        if self.text_end and self.scroll:
            # if text is finished and user scrolls, play vanish animation
            self.vanish()
        
    
    def draw(self):
        if self.done:
            self.image.fill(st.BLACK)
            self.renderText()
        self.game.screen.blit(self.image, self.rect.topleft)
        
        if self.done:
            self.arrow.draw(self.game.screen)



class Arrow(pg.sprite.Sprite):
    def __init__(self, game, pos, direction):
        self.game = game
        self.pos = pos
        self.direction = direction
        
        self.images = {
                'S': self.game.imageLoader.gui_img['arrows'][0],
                'N': self.game.imageLoader.gui_img['arrows'][1],
                'W': self.game.imageLoader.gui_img['arrows'][2],
                'E': self.game.imageLoader.gui_img['arrows'][3]
                }
        
        self.image = self.images[direction]
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos
        
    def draw(self, surface):
        # ANIMATE!
        surface.blit(self.image, self.rect)
        
        

def checkFight(game):
    '''
    closes the doors and opens them when player defeats all enemies
    '''
    room = game.dungeon.room_current
    # if no enemies are in that room, mark this room as cleared and return
    if len(game.enemies) == 0:
        room.openDoors()
        room.cleared = True
        return
    # check if the room's doors are closed
    if room.shut == False:
        # check player's position
        margin_x = 5 * st.TILESIZE_SMALL
        margin_y = 5.5 * st.TILESIZE_SMALL + st.GUI_HEIGHT
        rect = pg.Rect((margin_x, margin_y), (st.WIDTH - 2 *  margin_x, 
                       st.HEIGHT - st.GUI_HEIGHT - margin_y))
        if rect.colliderect(game.player.hit_rect):
            # player is far enough in the room to shut the doors
            room.shutDoors()
    else:
        # if room is shut, check for the number of enemies
        if len(game.enemies) == 0:
            # if all enemies are defeated, open the doors
            room.openDoors()
            room.cleared = True
        

        
 