import pygame as pg

from .. import prepare
from ..components.labels import Label, Button, ButtonGroup, MultiLineLabel
from ..components.window import Window
from ..components.message_window import MessageWindow
from ..components.items import UNIT_ITEM_INFO, UnitItem


class UnitItemInfoWindow(Window):
    def __init__(self, building, player, item_slot, unit, item_name):
        super(UnitItemInfoWindow, self).__init__(building, player)
        self.item_slot = item_slot
        self.unit = unit
        self.item_name = item_name
        self.make_buttons()
        
    def make_buttons(self):
        self.buttons = ButtonGroup()
        self.labels = pg.sprite.Group()
        category, quality, bonuses, price, flavor_text = UNIT_ITEM_INFO[self.item_name]
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
        label3 = MultiLineLabel(prepare.FONTS["PortmanteauRegular"], 12,
                                          flavor_text, prepare.TEXT_COLOR,
                                          {"midtop": (label2.rect.centerx, label2.rect.bottom + 24)},
                                          char_limit=42, align="center", vert_space=8)
        self.labels.add(label3)
        qual_text = "+{} Unit Quality".format(quality)
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
        item_name = self.item_name
        unit_items = [slot.item for slot in self.unit.item_slots if slot.item is not None]
        item_type, quality, bonuses, price, text = UNIT_ITEM_INFO[item_name]
        if item_type == "Bed":
            num_beds = len([x for x in unit_items if x.item_type == "Bed"])
            if num_beds > 0:
                self.done = True
                self.next = "SHOW_WINDOW"
                self.persist["menu"] = MessageWindow(self.building, self.player, "You can't put any more beds in this unit")
                return
        elif item_type == "Lighting":
            lights = [x for x in unit_items if x.item_type == "Lighting"]
            if lights:
                self.done = True
                self.next = "SHOW_WINDOW"
                self.persist["menu"] = MessageWindow(self.building, self.player, "You can't put any more lighting in this unit")
                return
        elif item_type == "Appliance":
            num_appliances = len([x for x in unit_items if x.item_type == "Appliance"])
            if num_appliances + 1 > self.unit.item_limits[self.unit.unit_size]["Appliance"]:
                self.done = True
                self.next = "SHOW_WINDOW"
                self.persist["menu"] = MessageWindow(self.building, self.player, "You can't put any more appliances in this unit")
                return
        elif item_type == "Fireplace":
            num_fireplaces = len([x for x in unit_items if x.item_type == "Fireplace"])
            if num_fireplaces > 0:
                self.done = True
                self.next = "SHOW_WINDOW"
                self.persist["menu"] = MessageWindow(self.building, self.player, "You can't put any more fireplaces in this unit")
                return        
        
        if price > self.player.cash:
            self.done = True
            self.next = "SHOW_WINDOW"
            self.persist["menu"] = MessageWindow(self.building, self.player, "You can't afford this right now")
            return
        if item_name in (x.name for x in unit_items):
            self.done = True
            self.next = "SHOW_WINDOW"
            self.persist["menu"] = MessageWindow(self.building, self.player, "This unit already has one of these")
            return
        self.player.cash -= price
        item = UnitItem(item_name)
        self.item_slot.add_item(item)
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