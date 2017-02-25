import pygame as pg

from .. import prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.window import Window
from ..components.items import UnitItem, UNIT_ITEM_INFO
from ..components.message_window import MessageWindow
from ..components.purchase_unit_item_categories_window import PurchaseUnitItemCategoriesWindow
from ..components.wallpaper_window import WallpaperWindow

#WINDOW FUNCTIONS
#    Change Wallpaper
 #   Rent Control - adjust rent (takes effect on next lease)
  #      show current lease
  #      show months left
  #      show next lease rent w/controls to change rent
  #  Show Quality Score -
  #  Show Lease Time Remaing -
  #  Show Tenant Happiness -
  #  Show Problems / Repairs Needed ?



class UnitInfoWindow(Window):
    def __init__(self, building, player, unit):
        super(UnitInfoWindow, self).__init__(building, player)
        self.unit = unit
        self.make_buttons()
        self.tenant_rect = pg.Rect(0, 0, 68, 120)
        self.tenant_rect.midtop = (self.rect.centerx, self.rect.top + 128)
        self.timer = 0
        self.click_time = 125

    def raise_rent(self, *args):
        self.unit.next_rent += 1
        self.next_rent_label.set_text("${}".format(int(self.unit.next_rent)))

    def lower_rent(self, *args):
        if self.unit.next_rent > 0:
            self.unit.next_rent -= 1
            self.next_rent_label.set_text("${}".format(int(self.unit.next_rent)))

    def make_buttons(self):
        self.buttons = ButtonGroup()
        self.labels = pg.sprite.Group()

        Label("Unit {}".format(self.unit.unit_num),
                {"midtop": (self.rect.centerx, self.rect.top + 8)},
                self.labels, font_size=24)
        m = None
        if self.unit.tenant:
            m = self.unit.tenant.monster_type
        qual = self.unit.get_quality_score(m)
        Label("Quality  {}".format(qual), {"midtop": (self.rect.centerx, self.rect.top + 40)},
                self.labels, font_size=16)
        Label("Current Rent  ${}".format(int(self.unit.rent)), {"midtop": (self.rect.centerx, self.rect.top + 60)},
                self.labels, font_size=16)
        if self.unit.tenant:
            months = "{} Days".format(self.unit.lease)
        else:
            months = " N/A "
        Label("Lease Ends {}".format(months), {"midtop": (self.rect.centerx, self.rect.top + 80)},
                self.labels, font_size=16)
        top = self.rect.top + 112
        Label("Next Lease Rent", {"midtop": (self.rect.centerx, top)},
                 self.labels, font_size=16)
        top += 24
        self.next_rent_label = Label("${}".format(int(self.unit.next_rent)),
                                                 {"midtop": (self.rect.centerx, top)},
                                                  self.labels, font_size=16)
        idle, hover = self.make_button_images("+", "tiny", 12)
        w, h =  idle.get_size()
        left = self.next_rent_label.rect.left - (w + 16)
        left2 = self.next_rent_label.rect.right + 16
        self.raise_rent_button = Button((left2, top), self.buttons,
                                                        idle_image=idle, hover_image=hover,
                                                        button_size=(w, h)) #call=self.raise_rent,
        idle, hover = self.make_button_images("-", "tiny", 12)
        self.lower_rent_button = Button((left, top), self.buttons,
                                                        idle_image=idle, hover_image=hover,
                                                        button_size=(w, h))   #call=self.lower_rent,

        top = self.rect.top + 256
        idle, hover = self.make_button_images("Buy Wallpaper", "large", 16)
        w, h = idle.get_size()
        Button((self.rect.centerx-(w//2), top), self.buttons,
                   idle_image=idle, hover_image=hover,
                   call=self.to_wallpaper)
        top += 64
        idle, hover = self.make_button_images("Buy Items", "large", 16)
        Button((self.rect.centerx-(w//2), top), self.buttons,
                   idle_image=idle, hover_image=hover,
                   call=self.to_items)

        idle, hover = self.make_button_images("Cancel", "small")
        b_size = idle.get_size()
        left = self.rect.centerx - (b_size[0] // 2)
        Button((left, self.rect.bottom - 56), self.buttons, idle_image=idle,
                  hover_image=hover, call=self.cancel)

    def to_items(self, *args):
        for slot in self.unit.item_slots:
            if not slot.item:
                open_slot = slot
                break
        else:
            self.done = True
            self.next = "SHOW_WINDOW"
            self.persist["menu"] = MessageWindow(self.building, self.player,
                                                                      "There are no empty item slots in this unit")
        self.done = True
        self.next = "SHOW_WINDOW"
        self.persist["menu"] = PurchaseUnitItemCategoriesWindow(self.building, self.player, open_slot, self.unit)

    def to_wallpaper(self, *args):
        self.done = True
        self.next = "SHOW_WINDOW"
        self.persist["menu"] = WallpaperWindow(self.building, self.player, self.unit)

    def cancel(self, *args):
        self.done = True
        self.next = "GAMEPLAY"

    def get_event(self, event):
        self.buttons.get_event(event)

    def update(self, dt, mouse_pos):
        self.timer -= dt
        if self.timer < 0:
            self.timer = 0
        self.buttons.update(mouse_pos)
        if pg.mouse.get_pressed()[0] and not self.timer:
            if self.lower_rent_button.hover:
                self.lower_rent()
                self.timer += self.click_time
            elif self.raise_rent_button.hover:
                self.raise_rent()
                self.timer += self.click_time

    def draw(self, surface):
        self.building.draw(surface)
        self.draw_window(surface)
        self.buttons.draw(surface)
        self.labels.draw(surface)
        if self.unit.tenant:
            surface.blit(self.unit.tenant.image, self.tenant_rect)