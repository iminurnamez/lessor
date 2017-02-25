import pygame as pg

from .. import tools, prepare
from ..components.labels import MultiLineLabel

class WinScreen(tools._State):
    def __init__(self):
        super(WinScreen, self).__init__()
        text = "Congratulations, you are the Evil Landlord of the Year"
        self.label = MultiLineLabel(
                prepare.FONTS["PortmanteauRegular"],
                24, text, prepare.TEXT_COLOR,
                {"center": prepare.SCREEN_RECT.center}, bg=None,
                char_limit=16, align="center", vert_space=16)
                                             
    def startup(self, persistent):
        self.persist = persistent
        self.cursor = self.persist["cursor"]
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        self.cursor.get_event(event)
        
    def update(self, dt):
        self.cursor.update(dt, pg.mouse.get_pos())
        
    def draw(self, surface):
        surface.fill((28, 10, 38))
        self.label.draw(surface)
        self.cursor.draw(surface)

