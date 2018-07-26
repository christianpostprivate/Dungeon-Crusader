import pygame as pg

# window settings and constants
GLOBAL_SCALE = 4
TILESIZE = 16 * GLOBAL_SCALE
TILES_W = 13
TILES_H = 9
GUI_MARGIN = min(1, int(0.5 * GLOBAL_SCALE))
GUI_HEIGHT = TILESIZE + 2 * GUI_MARGIN
WIDTH = TILESIZE * TILES_W
HEIGHT = TILESIZE * TILES_H + GUI_HEIGHT


# ingame settings
DUNGEON_SIZE = (10, 10)
SCROLLSPEED = 0.7 * GLOBAL_SCALE # TOO FAST FOR SMALL SCALES!
SCROLLSPEED_MENU = 3 * GLOBAL_SCALE
FPS = 60
TITLE = 'Random generated dungeons (press R to reload)'

# player settings
PLAYER_SPEED = 1 * GLOBAL_SCALE
PLAYER_HIT_RECT = pg.Rect(0, 0, int(TILESIZE * 0.8), int(TILESIZE * 0.6))

# player hp 
PLAYER_HP_START = 3.0
PLAYER_HP_MAX = 14.0



# possible rooms for picking
ROOMS = {
        'N': ['NS', 'NS', 'NS', 'NS', 'S', 'S', 'S', 'WS', 'ES', 'SWE', 'NSW', 'NSE'],
        'W': ['WE', 'WE', 'WE', 'WE', 'E', 'E', 'E', 'ES', 'EN', 'SWE', 'NSE', 'NWE'],
        'E': ['WE', 'WE', 'WE', 'WE', 'W', 'W', 'W', 'WS', 'WN', 'SWE', 'NSW', 'NWE'],
        'S': ['NS', 'NS', 'NS', 'NS', 'N', 'N', 'N', 'WN', 'EN', 'NSE', 'NSW', 'NWE']
        }


# default colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PINK = (255, 0, 255)
