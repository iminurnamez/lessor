import pygame as pg

from .. import prepare
from ..components.labels import Label, Button, ButtonGroup, MultiLineLabel
from ..components.window import Window


class MessageWindow(Window):
    def __init__(self, building, player, message):
        super(MessageWindow, self).__init__(building, player)
        self.msg = MultiLineLabel(prepare.FONTS["PortmanteauRegular"],
                                             24, message, prepare.TEXT_COLOR,
                                             {"center": self.rect.center}, bg=None,
                                             char_limit=21, align="center", vert_space=16)
        self.buttons = ButtonGroup()
        idle, hover = self.make_button_images("OK", "small")
        w, h = idle.get_size()
        Button((self.rect.centerx - (w//2), self.rect.bottom - 56), self.buttons,
                  button_size=(w, h), idle_image=idle, hover_image=hover,
                  call=self.cancel)
    
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
        self.msg.draw(surface)
        self.buttons.draw(surface)
        
