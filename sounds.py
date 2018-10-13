import pygame as pg
from os import path

import settings as st

Sound = pg.mixer.Sound

class SoundLoader:
    def __init__(self, game):
        self.game = game
        
    
    def get_sound(self, filename, volume):
        sound = Sound(path.join(st.SOUND_FOLDER, filename))
        sound.set_volume(1 * st.SFX_VOL)
        return sound
        
        
    def load(self):
        self.snd_slash = self.get_sound('slash.wav', 1)
        self.snd_rupee = self.get_sound('rupee.wav', 1)
        self.snd_heart = self.get_sound('heart.wav', 1)
        self.snd_bomb = self.get_sound('sfx_exp_various1.wav', 1)
        self.snd_shut = self.get_sound('sfx_exp_various4.wav', 1)
        self.snd_magic1 = self.get_sound('sfx_sounds_impact9.wav', 0.8)
        self.snd_magic2 = self.get_sound('sfx_exp_odd1.wav', 0.8)
        
        
        
        
