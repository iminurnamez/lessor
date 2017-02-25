import pygame as pg

from .. import prepare
from ..components.labels import Label, Button, ButtonGroup, MultiLineLabel
from ..components.window import Window


class VisitorInfoWindow(Window):
    def __init__(self, building, player, tenant):
        super(VisitorInfoWindow, self).__init__(building, player)
        self.tenant = tenant
        self.tenant_rect = self.tenant.image.get_rect(midtop=(self.rect.centerx, self.rect.top + 64))
        self.make_buttons()
        
    def make_buttons(self):
        self.buttons = ButtonGroup()
        self.labels = pg.sprite.Group()
        
        label = Label(self.tenant.monster_type,
                           {"midtop": (self.rect.centerx, self.rect.top + 16)},
                            self.labels, font_size=24)
        top = self.tenant_rect.bottom + 16
        for s in self.tenant.sentiments:
            msg = MultiLineLabel(prepare.FONTS["PortmanteauRegular"],
                                             14, s, prepare.TEXT_COLOR,
                                             {"midtop": (self.rect.centerx, top)}, bg=None,
                                             char_limit=32, align="center", vert_space=8)
            self.labels.add(msg)
            top = msg.rect.bottom + 16

        idle, hover = self.make_button_images("Cancel", "small")
        w, h = idle.get_size()
        Button((self.rect.centerx - (w//2), self.rect.bottom - 56),
                   self.buttons, idle_image=idle, hover_image=hover,
                   button_size=(w, h), call=self.cancel)
    
    def cancel(self, *args):
        self.done  = True
        self.next = "GAMEPLAY"
        
    def get_event(self, event):
        self.buttons.get_event(event)
        
    def update(self, dt, mouse_pos):
        self.buttons.update(mouse_pos)
        
    def draw(self, surface):
        self.building.draw(surface)
        self.draw_window(surface)
        self.labels.draw(surface)
        self.buttons.draw(surface)
        surface.blit(self.tenant.image, self.tenant_rect)
