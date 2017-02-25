from itertools import cycle

import pygame as pg

from .. import prepare


class MusicManager(object):
    def __init__(self):
        self.songs = [
            "13marilynT",
            "crypt-Loop",
            "WrongRiteTheme",
            "WTF!Ghost!"]
        self.volumes = {
            "13marilynT": .8,
            "crypt-Loop": .8,
            "WrongRiteTheme": .5,
            "WTF!Ghost!": .5}
        self.playlist = cycle(self.songs)
        self.muted = False
        
    def get_event(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_m:
                self.muted = not self.muted
                if self.muted:
                    pg.mixer.music.stop()
                else:
                    pg.mixer.music.play(-1)              
            if event.key == pg.K_SPACE:
                self.next_song()

    def next_song(self):
        self.song = next(self.playlist)
        pg.mixer.music.set_volume(self.volumes[self.song])
        pg.mixer.music.load(prepare.MUSIC[self.song])
        pg.mixer.music.play(-1)
