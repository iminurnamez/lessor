import pygame as pg

from .. import prepare
from ..components.labels import Label, Button, ButtonGroup, MultiLineLabel
from ..components.window import Window


class DeleteUnitsWindow(Window):
    def __init__(self, building, player, floor):
        super(DeleteUnitsWindow, self).__init__(building, player)
        self.floor = floor
        self.make_buttons()
        
    def make_buttons(self):
        self.labels = pg.sprite.Group()
        self.buttons = ButtonGroup()
        text = "Delete all units on this floor?"
        label = MultiLineLabel(
                    prepare.FONTS["PortmanteauRegular"],
                    24, text, prepare.TEXT_COLOR, 
                    {"midtop": (self.rect.centerx, self.rect.top + 64)},
                    bg=None, char_limit=21, align="center", vert_space=16)
        self.labels.add(label)
        idle, hover = self.make_button_images("Delete Units", "large")
        w, h = idle.get_size()
        left = self.rect.centerx - (w//2)
        Button((left, self.rect.bottom - 120),
                   self.buttons, idle_image=idle, hover_image=hover,
                   call=self.delete_units)
        idle, hover = self.make_button_images("Cancel", "small")
        w, h = idle.get_size()
        left = self.rect.centerx - (w//2)
        Button((left, self.rect.bottom - 56), self.buttons,
                   idle_image=idle, hover_image=hover,
                   button_size=(w, h), call=self.cancel)
        
    def cancel(self, *args):
        self.done = True
        self.next = "GAMEPLAY"
       
    def delete_units(self, *args):
        self.floor.remove_units()
        self.cancel()
        
    def get_event(self, event):
        self.buttons.get_event(event)
        
    def update(self, dt, mouse_pos):
        self.buttons.update(mouse_pos)
        
    def draw(self, surface):
        self.building.draw(surface)
        self.draw_window(surface)
        self.buttons.draw(surface)
        self.labels.draw(surface)