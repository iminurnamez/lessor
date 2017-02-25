import pygame as pg

from .. import prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.window import Window
from ..components.message_window import MessageWindow
from ..components.items import UnitItem, UNIT_ITEM_INFO
from ..components.unit_item_info_window import UnitItemInfoWindow


def make_button_images(text, size):
    idle = prepare.GFX["{}_button".format(size)].copy()
    hover = prepare.GFX["{}_button_hover".format(size)].copy()
    w, h = idle.get_size()
    label = Label(text, {"center": (w//2, h//2)},
                        font_size=24, text_color=prepare.TEXT_COLOR)
    label.draw(idle)
    label.draw(hover)
    return idle, hover


class PurchaseUnitItemWindow(Window):
    def __init__(self, building, player, item_slot, unit, category, previous_menu):
        super(PurchaseUnitItemWindow, self).__init__(building, player)
        self.item_slot = item_slot
        self.unit = unit
        self.previous = previous_menu
        self.make_buttons(category)

    def make_buttons(self, category):
        self.labels = pg.sprite.Group()
        self.buttons = ButtonGroup()
        label = Label(category, {"midtop": (self.rect.centerx, self.rect.top + 16)}, self.labels,
                           font_size=24, text_color=prepare.TEXT_COLOR)
        top = label.rect.bottom + 5
        names = [x for x in UNIT_ITEM_INFO if UNIT_ITEM_INFO[x][0] == category]
        names = sorted(names, key=lambda x: UNIT_ITEM_INFO[x][1])
        left = self.rect.left + 48
        for name in names:
            img = prepare.GFX["icon_button"].copy()
            img2 = prepare.GFX["icon_button_hover"].copy()
            r = img.get_rect()
            item_icon = prepare.GFX["icon-{}".format("".join(name.lower().replace(" ", "")))]
            icon_rect = item_icon.get_rect(center=r.center)
            img.blit(item_icon, icon_rect)
            img2.blit(item_icon, icon_rect)
            b = Button((left, top), self.buttons, button_size=r.size,
                             idle_image=img, hover_image=img2,
                             call=self.to_item_window, args=[name])
            Label(name, {"midtop": (b.rect.centerx, b.rect.bottom + 3)},
                    self.labels, font_size=8, text_color=prepare.TEXT_COLOR)
            left += 112
            if left > self.rect.right - 72:
                top += 112
                left = self.rect.left + 48
        top += 112

        idle, hover = make_button_images("Cancel", "small")
        b_size = idle.get_size()
        left = self.rect.centerx - (b_size[0] // 2)
        Button((left, self.rect.bottom - 56), self.buttons, idle_image=idle,
                  hover_image=hover, call=self.cancel)

    def cancel(self, *args):
        self.done = True
        self.next = "SHOW_WINDOW"
        self.persist["menu"] = self.previous

    def to_item_window(self, name):
        self.done = True
        self.next = "SHOW_WINDOW"
        self.persist["menu"] = UnitItemInfoWindow(self.building, self.player, self.item_slot, self.unit, name[0])

    def get_event(self, event):
        self.buttons.get_event(event)

    def update(self, dt, mouse_pos):
        self.buttons.update(mouse_pos)

    def draw(self, surface):
        self.building.draw(surface)
        self.draw_window(surface)
        self.buttons.draw(surface)
        self.labels.draw(surface)



