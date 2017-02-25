import pygame as pg

from .. import prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.window import Window
from ..components.items import LANDSCAPE_ITEMS
from ..components.purchase_yard_item_window import PurchaseYardItemWindow


class PurchaseYardItemsWindow(Window):
    def __init__(self, building, player):
        super(PurchaseYardItemsWindow, self).__init__(building, player)
        self.make_buttons()
        
    def make_buttons(self):
        self.labels = pg.sprite.Group()
        self.buttons = ButtonGroup()
        label = Label("Landscaping",
                          {"midtop": (self.rect.centerx, self.rect.top + 16)},
                           self.labels, font_size=24)
        names = [x for x in LANDSCAPE_ITEMS]
        names = sorted(names,
                                key=lambda x: LANDSCAPE_ITEMS[x][1])
        left = self.rect.left + 48
        top = label.rect.bottom + 16
        for name in names:
            img = prepare.GFX["icon_button"].copy()
            img2 = prepare.GFX["icon_button_hover"].copy()
            r = img.get_rect()
            item_icon = prepare.GFX["icon-{}".format(
                        "".join(name.lower().replace(" ", "")))]
            icon_rect = item_icon.get_rect(center=r.center)
            img.blit(item_icon, icon_rect)
            img2.blit(item_icon, icon_rect)
            b = Button((left, top), self.buttons, button_size=r.size,
                             idle_image=img, hover_image=img2,
                             call=self.to_buy_window, args=name)
            Label(name, {"midtop": (b.rect.centerx, b.rect.bottom + 3)},
                    self.labels, font_size=8, text_color=prepare.TEXT_COLOR)
            left += 112
            if left > self.rect.right - 72:
                top += 112
                left = self.rect.left + 48
        top += 112

        idle, hover = self.make_button_images("Cancel", "small")
        b_size = idle.get_size()
        left = self.rect.centerx - (b_size[0] // 2)
        Button((left, self.rect.bottom - 56), self.buttons, idle_image=idle,
                  hover_image=hover, call=self.cancel)

    def to_buy_window(self, name):
        self.done = True
        self.next = "SHOW_WINDOW"
        self.persist["menu"] = PurchaseYardItemWindow(
                    self.building, self.player, name)        
        
    def cancel(self, *args):
        self.done = True
        self.next = "GAMEPLAY"
        
    def get_event(self, event):
        self.buttons.get_event(event)
        
    def update(self, dt, mouse_pos):
        self.buttons.update(mouse_pos)
        
    def draw(self, surface):
        self.draw_window(surface)
        self.buttons.draw(surface)
        self.labels.draw(surface)
        
        
        
