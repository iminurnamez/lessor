import pygame as pg

from .. import prepare
from ..components.window import Window
from ..components.labels import Label, Button, ButtonGroup, MultiLineLabel
from ..components.items import LANDSCAPE_ITEMS, Fence, Trees, Gravestones
from ..components.message_window import MessageWindow


class PurchaseYardItemWindow(Window):
    def __init__(self, building, player, item_name):
        super(PurchaseYardItemWindow, self).__init__(building, player)
        self.item_name = item_name
        self.classes = {
            "Iron Fence": Fence,
            "Spooky Trees": Trees,
            "Gravestones": Gravestones}
        self.make_buttons()

    def make_buttons(self):
        self.buttons = ButtonGroup()
        self.labels = pg.sprite.Group()
        category, quality, bonuses, price, flavor_text = LANDSCAPE_ITEMS[self.item_name]
        img = prepare.GFX["icon_button"].copy()
        r = img.get_rect()
        item_icon = prepare.GFX["icon-{}".format("".join(self.item_name.lower().replace(" ", "")))]
        icon_rect = item_icon.get_rect(center=r.center)
        img.blit(item_icon, icon_rect)
        left = self.rect.centerx - (r.width // 2)
        top = self.rect.top + 16
        b = Button((left, top), self.buttons, button_size=r.size,
                         idle_image=img)
        label1 = Label(self.item_name, {"midtop": (b.rect.centerx, b.rect.bottom + 8)},
                              self.labels, font_size=24)
        label2 = Label("${}".format(price), {"midtop": (label1.rect.centerx, label1.rect.bottom + 8)},
                              self.labels, font_size=24)
        label3 = MultiLineLabel(prepare.FONTS["PortmanteauRegular"], 14,
                                          flavor_text, prepare.TEXT_COLOR,
                                          {"midtop": (label2.rect.centerx, label2.rect.bottom + 24)},
                                          char_limit=42, align="center", vert_space=8)
        self.labels.add(label3)
        qual_text = "+{} Building Quality".format(quality)
        label4 = Label(qual_text, {"midtop": (self.rect.centerx, label3.rect.bottom + 24)},
                 self.labels, font_size=16)
        names = ["Vampire", "Ghost", "Witch", "Demon", "Homocidal Maniac",
                       "Pumpkin Head", "Zombie", "Skeleton", "Frankenfolk"]
        bonus_dict = {n: b for n, b in zip(names, bonuses)}
        bonuses_ = [(name, bonus) for name, bonus in bonus_dict.items() if bonus != 0]
        bonuses_ = sorted(bonuses_, key=lambda x: x[1], reverse=True)
        top = label4.rect.bottom + 16
        for name, bonus in bonuses_:
            if bonus < 0:
                text = "{} {}".format(name, bonus)
            else:
                text = "{} +{}".format(name, bonus)
            Label(text, {"midtop": (self.rect.centerx, top)}, self.labels,
                     font_size=12, text_color=prepare.TEXT_COLOR)
            top += 24

        idle, hover = self.make_button_images("Buy", "large")
        w, h = idle.get_size()
        Button((self.rect.centerx - (w//2), self.rect.bottom - 120), self.buttons,
                   idle_image=idle, hover_image=hover, call=self.buy_item)
        idle, hover = self.make_button_images("Cancel", "small")
        w, h = idle.get_size()
        Button((self.rect.centerx-(w//2), self.rect.bottom - 56), self.buttons,
                   idle_image=idle, hover_image=hover, button_size=(w, h),
                   call=self.cancel)

    def buy_item(self, *args):
        category, quality, bonuses, price, flavor_text = LANDSCAPE_ITEMS[self.item_name]
        if self.item_name in (x.name for x in self.building.landscape_items):
            self.done = True
            self.next = "SHOW_WINDOW"
            self.persist["menu"] = MessageWindow(self.building, self.player, "You already have one of these")
        elif price > self.player.cash:
            self.done = True
            self.next = "SHOW_WINDOW"
            self.persist["menu"] = MessageWindow(self.building, self.player, "You can't afford this right now")
        else:
            self.player.cash -= price
            self.classes[self.item_name](self.building)
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
        self.labels.draw(surface)