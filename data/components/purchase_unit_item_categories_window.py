import pygame as pg

from .. import prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.window import Window
from ..components.purchase_unit_item_window import PurchaseUnitItemWindow

def make_button_images(text, size):
    idle = prepare.GFX["{}_button".format(size)].copy()
    hover = prepare.GFX["{}_button_hover".format(size)].copy()
    w, h = idle.get_size()
    label = Label(text, {"center": (w//2, h//2)},
                        font_size=24, text_color=prepare.TEXT_COLOR)
    label.draw(idle)
    label.draw(hover)
    return idle, hover
    

class PurchaseUnitItemCategoriesWindow(Window):
    def __init__(self, building, player, item_slot, unit):
        super(PurchaseUnitItemCategoriesWindow, self).__init__(building, player)
        self.item_slot = item_slot
        self.unit = unit
        self.make_buttons()
        
    def make_buttons(self):
        self.labels = pg.sprite.Group()
        self.buttons = ButtonGroup()
        style = {"text_color": prepare.TEXT_COLOR, "font_size": 24}
        Label("Purchase Unit Items", {"midtop": (self.rect.centerx, self.rect.top + 16)}, 
                 self.labels, **style)
        w, h = 256, 48
        left = self.rect.centerx - (w // 2)
        top = self.rect.top + 64
        for category in ("Lighting", "Bed", "Fireplace", "Appliance", "Decoration"):
            idle, hover = make_button_images(category, "large")
            Button((left, top), self.buttons, idle_image=idle, hover_image=hover,
                       call=self.to_category, args=[category])
            top += 80           
        left = self.rect.centerx - (192 // 2)
        idle_, hover_ = make_button_images("Cancel", "small")
        Button((left, self.rect.bottom - 64), self.buttons, idle_image=idle_,
                   hover_image=hover_, call=self.cancel)

    def to_category(self, category):
        self.done = True
        self.next = "SHOW_WINDOW"
        self.persist["menu"] = PurchaseUnitItemWindow(
                    self.building, self.player, self.item_slot,
                    self.unit, category[0], self)
        
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
            
        
        