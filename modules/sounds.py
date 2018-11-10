import pygame as pg
from os import path

import settings as st

Sound = pg.mixer.Sound

class SoundLoader:
    def __init__(self, game):
        self.game = game
        
    
    def get_sound(self, filename, volume):
        sound = Sound(path.join(st.SOUND_FOLDER, filename))
        sound.set_volume(volume * st.SFX_VOL)
        return sound
    
    
    def get_music(self, filename, volume):
        music = Sound(path.join(st.SOUND_FOLDER, filename))
        music.set_volume(volume * st.MU_VOL)
        return music
        
        
    def load(self):      
        self.snd = {
                'slash': self.get_sound('slash.wav', 0.4),
                'rupee': self.get_sound('rupee.wav', 1),
                'heart': self.get_sound('heart.wav', 1),
                'bomb': self.get_sound('sfx_exp_various1.wav', 1),
                'shut': self.get_sound('sfx_exp_various4.wav', 1),
                'magic1': self.get_sound('sfx_sounds_impact9.wav', 0.8),
                'magic2': self.get_sound('sfx_exp_odd1.wav', 0.8),
                'fanfare1': self.get_sound('sfx_sounds_fanfare3.wav', 1)
                }
        
        self.music = {
                'dungeon1': self.get_music('Memoraphile - Spooky Dungeon.ogg', 1)
                }
        
        
        
        
