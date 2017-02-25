import pygame as pg

from .. import prepare
from ..components.labels import Label, Button, ButtonGroup, MultiLineLabel
from ..components.window import Window
from ..components.message_window import MessageWindow
from ..components.purchase_yard_items_window import PurchaseYardItemsWindow

       
class BuildWindow(Window):
    def __init__(self, building, player):
        super(BuildWindow, self).__init__(building, player)
        self.make_buttons()

    def make_buttons(self):
        self.buttons = ButtonGroup()
        self.labels = pg.sprite.Group()
        Label("Build", {"midtop": (self.rect.centerx, self.rect.top + 16)},
                self.labels, font_size=24, text_color=prepare.TEXT_COLOR)
        price = self.building.get_floor_build_cost()
        idle, hover = self.make_button_images("Build Floor ${}".format(price), "large", 16)
        w, h = idle.get_size()
        left = self.rect.centerx - (w // 2)
        top = self.rect.top + 80
        Button((left, top), self.buttons, idle_image=idle, hover_image=hover, 
                   call=self.build_floor)
        top += 96
        idle, hover = self.make_button_images("Landscaping", "large", 16)
        Button((left, top), self.buttons, idle_image=idle, hover_image=hover,
                   call=self.to_yard_items)
        idle, hover = self.make_button_images("Cancel", "small")
        w, h = idle.get_size()
        Button((self.rect.centerx - (w//2), self.rect.bottom - 56),
                   self.buttons, idle_image=idle, hover_image=hover,
                   button_size=(w, h), call=self.cancel)
        
    def build_floor(self, *args):
        cost = self.building.get_floor_build_cost()
        if self.player.cash >= cost:
            self.player.cash -= cost
            self.building.add_floor()
            self.done = True
            self.next = "GAMEPLAY"
        else:
            self.done = True
            self.next = "SHOW_WINDOW"
            menu = MessageWindow(self.building, self.player, "You can't afford that right now")
            self.persist["menu"] = menu

    def to_yard_items(self, *args):
        self.done = True
        self.next = "SHOW_WINDOW"
        menu = PurchaseYardItemsWindow(self.building, self.player)
        self.persist["menu"] = menu
        
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
        self.labels.draw(surface)