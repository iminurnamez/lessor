import pygame as pg

from .. import tools, prepare
from ..components.labels import Label
from ..components.tutorial import Tutorial
from ..components.music_manager import MusicManager
from ..components.animation import Animation


def make_button_images(self, text, size, font_size=24):
        idle = prepare.GFX["{}_button".format(size)].copy()
        hover = prepare.GFX["{}_button_hover".format(size)].copy()
        w, h = idle.get_size()
        label = Label(text, {"center": (w//2, h//2)},
                            font_size=font_size, text_color=prepare.TEXT_COLOR)
        label.draw(idle)
        label.draw(hover)
        return idle, hover





class TitleScreen(tools._State):
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.animations = pg.sprite.Group()
        self.label1 = Label("Sometimes your landlord is a monster...",
                                   {"center": prepare.SCREEN_RECT.center},
                                   font_size=32, fill_color=(0,0,0))
        self.label2 = Label("...sometimes your tenant is",
                                   {"center": prepare.SCREEN_RECT.center},
                                   font_size=32, fill_color=(0,0,0))
        self.title = Label("The Lessor of 2 Evil St.", {"center": prepare.SCREEN_RECT.center},
                                 font_size=64, fill_color=(0,0,0))
        self.label = self.label1
        self.label.alpha = 0
        ani = Animation(alpha=255, duration=4000)
        ani.callback = self.f1
        ani.start(self.label)

        self.animations.add(ani)
        self.music_manager = MusicManager()

    def f1(self):
        ani = Animation(alpha=0, duration=2000)
        ani.start(self.label)
        ani.callback = self.f2
        self.animations.add(ani)

    def f2(self):
        self.label = self.label2
        self.label.alpha = 0
        ani = Animation(alpha=255, duration=4000)
        ani.start(self.label)
        ani.callback = self.f3
        self.animations.add(ani)

    def f3(self):
        ani = Animation(alpha=0, duration=2000)
        ani.start(self.label)
        ani.callback = self.f4
        self.animations.add(ani)

    def f4(self):
        self.label = self.title
        self.label.alpha = 0
        ani = Animation(alpha=255, duration=4000)
        ani.start(self.label)
        self.animations.add(ani)

    def startup(self, persistent):
        self.persist = persistent
        self.cursor = self.persist["cursor"]
        self.music_manager.next_song()

    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.done = True
            self.next = "GAMEPLAY"
            self.persist["cursor"] = self.cursor
            t = pg.sprite.Group()
            tutorial = Tutorial(t)
            self.persist["tutorials"] = t
            self.persist["music manager"] = self.music_manager
        self.cursor.get_event(event)

    def update(self, dt):
        self.animations.update(dt)
        self.cursor.update(dt, pg.mouse.get_pos())
        self.label.image.set_alpha(self.label.alpha)

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        self.label.draw(surface)
        self.cursor.draw(surface)
