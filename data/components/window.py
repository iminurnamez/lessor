import pygame as pg

from .. import prepare
from ..components.labels import Label, Button, ButtonGroup, MultiLineLabel
from ..components.items import LANDSCAPE_ITEMS


class Window(object):
    def __init__(self, building, player):
        self.building = building
        self.player = player
        self.image = prepare.GFX["window_background"]
        self.rect = self.image.get_rect(center=prepare.SCREEN_RECT.center)
        self.done = False
        self.persist = {}

    def get_event(self, event):
        pass

    def draw_window(self, surface):
        surface.blit(self.image, self.rect)

    def make_button_images(self, text, size, font_size=24):
        idle = prepare.GFX["{}_button".format(size)].copy()
        hover = prepare.GFX["{}_button_hover".format(size)].copy()
        w, h = idle.get_size()
        label = Label(text, {"center": (w//2, h//2)},
                            font_size=font_size, text_color=prepare.TEXT_COLOR)
        label.draw(idle)
        label.draw(hover)
        return idle, hover



        
        


