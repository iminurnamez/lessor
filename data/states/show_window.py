import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.building import Building


class ShowWindow(tools._State):
    def __init__(self):
        super(ShowWindow, self).__init__()
        
    def make_buttons(self):    
        self.buttons = ButtonGroup()
        crane = prepare.GFX["button-build"]
        crane_idle = prepare.GFX["button-build-idle"]
        b_size = crane.get_size()
        Button((16, 16), self.buttons, button_size=b_size,
                   idle_image=crane_idle, hover_image=crane,
                   call=self.build)
        dozer = prepare.GFX["button-bulldoze"]
        dozer_idle = prepare.GFX["button-bulldoze-idle"]
        Button((16, 112), self.buttons, button_size=b_size,
                   idle_image=dozer_idle, hover_image=dozer)
        
    def startup(self, persistent):
        self.persist = persistent
        self.menu = self.persist["menu"]
        self.cursor = self.persist["cursor"]
        
    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        self.cursor.get_event(event)
        self.menu.get_event(event)
        
    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.cursor.update(dt, mouse_pos)
        self.menu.update(dt, mouse_pos)
        if self.menu.done:
            self.menu.done = False
            self.done = True
            self.next = self.menu.next
            if "menu" in self.menu.persist:
                self.persist["menu"] = self.menu.persist["menu"]
            

    def draw(self, surface):
        self.menu.draw(surface)
        self.cursor.draw(surface)

        