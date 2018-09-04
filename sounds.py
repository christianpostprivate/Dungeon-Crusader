import pygame as pg
from os import path

import settings as st

class SoundLoader:
    def __init__(self, game):
        self.game = game
        
    def load(self):
        self.snd_slash = pg.mixer.Sound(path.join(st.SOUND_FOLDER, 'slash.wav'))
        self.snd_slash.set_volume(1 * st.SFX_VOL)
        self.snd_rupee = pg.mixer.Sound(path.join(st.SOUND_FOLDER, 'rupee.wav'))
        self.snd_rupee.set_volume(1 * st.SFX_VOL)
        self.snd_heart = pg.mixer.Sound(path.join(st.SOUND_FOLDER, 'heart.wav'))
        self.snd_heart.set_volume(1 * st.SFX_VOL)
