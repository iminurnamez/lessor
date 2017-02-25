import pygame as pg

from .. import prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.window import Window


class DeleteUnitItemWindow(Window):
    def __init__(self, building, player, item_slot):
        super(DeleteUnitItemWindow, self).__init__(building, player)
        self.item_slot = item_slot
        self.make_buttons()
        
    def make_buttons(self):
        self.labels = pg.sprite.Group()
        self.buttons = ButtonGroup()
        item = self.item_slot.item

        img = prepare.GFX["icon_button"].copy()
        r = img.get_rect()
        item_icon = prepare.GFX["icon-{}".format("".join(item.name.lower().replace(" ", "")))]
        icon_rect = item_icon.get_rect(center=r.center)
        img.blit(item_icon, icon_rect)
        
        Button((self.rect.centerx - (r.w//2), self.rect.top + 32), self.buttons, idle_image=img,
                    button_size=r.size)
        
        left = self.rect.centerx - 128
        idle, hover = self.make_button_images("Delete", "large")
        w, h = idle.get_size()
        Button((left, self.rect.bottom - 120),
                   self.buttons, idle_image=idle, hover_image=hover,
                   call=self.delete_item)
        idle, hover = self.make_button_images("Cancel", "small")
        w, h = idle.get_size()
        Button((left, self.rect.bottom - 56), self.buttons,
                   idle_image=idle, hover_image=hover,
                   button_size=(w, h), call=self.cancel)
                   
    def delete_item(self, *args):
        self.item_slot.remove_item()
        self.done = True
        self.next = "GAMEPLAY"

    def cancel(self, *args):
        self.done = True
        self.next = "GAMEPLAY"
        
    def get_event(self, event):
        self.buttons.get_event(event)
        
    def update(self, dt, mouse_pos):
        self.buttons.update(mouse_pos)
        
    def draw(self, surface):
        self.building.draw(surface)
        self.draw_window(surface)
        self.buttons.draw(surface)
        self.lalbels.draw(surface)