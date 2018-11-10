import pygame as pg
import traceback

from modules.main import Game

if __name__ == '__main__':
    g = Game()
    try:
        g.show_start_screen()
        while g.running:
            g.new()
    except Exception:
        traceback.print_exc()
    
    pg.quit()