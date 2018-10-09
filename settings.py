import pygame as pg
from os import path
from random import choice

vec = pg.math.Vector2

# window settings and constants
SCREEN_SCALE = 3
TILESIZE = 16
TILESIZE_SMALL = 8
TILES_W = 16
TILES_H = 12
GUI_MARGIN = 1
GUI_HEIGHT = TILESIZE * 3
WIDTH = 2 * TILESIZE_SMALL * TILES_W
HEIGHT = 2 * TILESIZE_SMALL * TILES_H + GUI_HEIGHT
S_WIDTH = WIDTH * SCREEN_SCALE
S_HEIGHT = HEIGHT * SCREEN_SCALE

# file paths
directory = path.dirname(__file__)

FONT_FOLDER = path.join(directory, 'fonts')
IMAGE_FOLDER = path.join(directory, 'images')
ROOM_FOLDER = path.join(directory, 'rooms')
SAVE_FOLDER = path.join(directory, 'saves')
TEXT_FOLDER = path.join(directory, 'text')
SOUND_FOLDER = path.join(directory, 'sounds')
 
# ingame settings
DUNGEON_SIZE = (10, 10)
SCROLLSPEED = 4 # TOO FAST FOR SMALL SCALES!
SCROLLSPEED_MENU = 6
FPS = 60
FONT = path.join(FONT_FOLDER, 'slkscr.TTF')
TITLE = ('DUNGEON CRUSADER | move: ARROW or WASD | attack: SPACE | ' +
        'inventory: ESC | save: F6 | load: F9 | debug mode: H')

SFX_VOL = 0.3
MU_VOL = 0.3

KEY_DELAY = 150

# player settings
PLAYER_MAXSPEED = 1
PLAYER_ACC = 0.4
PLAYER_FRICTION = 0.1
PLAYER_HIT_RECT = pg.Rect(0, 0, int(TILESIZE * 0.8), int(TILESIZE * 0.6))

# player hp 
PLAYER_HP_START = 7.0
PLAYER_HP_MAX = 14.0
PLAYER_HP_ROW = 7

# item stats
# mana the lamp uses per frame
LAMP_MANA = 0.001
# time it takes to switch the lamp on/off (put this in the lamp object somehow)
LAMP_SWITCH_TIME = 30

# possible rooms for picking
ROOMS = {
    'N': ['NS', 'NS', 'NS', 'NS', 'S', 'S', 'S', 'WS', 'ES', 'SWE', 'NSW', 'NSE'],
    'W': ['WE', 'WE', 'WE', 'WE', 'E', 'E', 'E', 'ES', 'EN', 'SWE', 'NSE', 'NWE'],
    'E': ['WE', 'WE', 'WE', 'WE', 'W', 'W', 'W', 'WS', 'WN', 'SWE', 'NSW', 'NWE'],
    'S': ['NS', 'NS', 'NS', 'NS', 'N', 'N', 'N', 'WN', 'EN', 'NSE', 'NSW', 'NWE']
    }

DOOR_POSITIONS = {
        'N': (WIDTH // 2 - TILESIZE, TILESIZE_SMALL),
        'S': (WIDTH // 2 - TILESIZE, HEIGHT - 2 * TILESIZE - GUI_HEIGHT),
        'W': (TILESIZE_SMALL, HEIGHT // 2 - GUI_HEIGHT + TILESIZE_SMALL),
        'E': (WIDTH - 2 * TILESIZE, HEIGHT // 2 - GUI_HEIGHT + TILESIZE_SMALL)
        }


# list of tmx file numbers to pick from
TILEMAP_FILES = [1, 2, 5, 8, 9, 10, 11, 12, 13, 14, 15]
#TILEMAP_FILES = [15]

TM_POOL = []
def randomizeRooms():
    for i in range(DUNGEON_SIZE[0] * DUNGEON_SIZE[1]):
        TM_POOL.append(choice(TILEMAP_FILES))

# effects
DAMAGE_ALPHA = [i for i in range(0, 255, 15)]

# default colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PINK = (255, 0, 255)
TRANS = (0, 0, 0, 0)

NIGHT_COLOR = (10, 10, 10)

# key bindings
KEY_A = pg.K_z
KEY_B = pg.K_x
KEY_MENU = pg.K_ESCAPE
KEY_UP = pg.K_UP
KEY_DOWN = pg.K_DOWN
KEY_LEFT = pg.K_LEFT
KEY_RIGHT = pg.K_RIGHT
KEY_ENTER = pg.K_RETURN

DEADZONE = 0.2


