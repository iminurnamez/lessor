import pygame as pg


from .. import prepare
from ..components.labels import Label, Button, ButtonGroup, MultiLineLabel
from ..components.message_window import MessageWindow
from ..components.window import Window
from ..components.items import Wallpaper, WALLPAPER_INFO
from ..components.buy_wallpaper_window import BuyWallpaperWindow


class WallpaperWindow(Window):
    def __init__(self, building, player, unit):
        super(WallpaperWindow, self).__init__(building, player)
        self.unit = unit
        self.make_buttons()

    def make_buttons(self):
        self.labels = pg.sprite.Group()
        self.buttons = ButtonGroup()
        Label("Wallpapers", {"midtop": (self.rect.centerx, self.rect.top + 8)},
                self.labels, font_size=24)
        top = self.rect.top + 48
        for name in WALLPAPER_INFO:
            if name == "Default":
                continue
            idle, hover = self.make_button_images(name, "large", 16)
            w, h = idle.get_size()
            Button((self.rect.centerx-(w//2), top), self.buttons,
                       idle_image=idle, hover_image=hover,
                       call=self.buy_wallpaper, args=name)
            top += 56
        idle, hover = self.make_button_images("Cancel", "small")
        w, h = idle.get_size()
        Button((self.rect.centerx - (w//2), self.rect.bottom - 56),
                   self.buttons, idle_image=idle, hover_image=hover,
                   button_size=(w, h), call=self.cancel)

    def buy_wallpaper(self, name):
        if self.unit.wallpaper.name == name:
            self.done = True
            self.next = "SHOW_WINDOW"
            self.persist["menu"] = MessageWindow(self.building, self.player,
                        "This unit already has this wallpaper")
        else:
            self.done = True
            self.next = "SHOW_WINDOW"
            self.persist["menu"] = BuyWallpaperWindow(self.building, self.player, self.unit, name)

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
        self.labels.draw(surface)
        self.buttons.draw(surface)

