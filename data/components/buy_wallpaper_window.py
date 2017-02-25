import pygame as pg


from .. import prepare
from ..components.labels import Label, Button, ButtonGroup, MultiLineLabel
from ..components.message_window import MessageWindow
from ..components.window import Window
from ..components.items import Wallpaper, WALLPAPER_INFO

class BuyWallpaperWindow(Window):
    def __init__(self, building, player, unit, name):
        super(BuyWallpaperWindow, self).__init__(building, player)
        self.unit = unit
        self.name = name
        self.make_buttons()

    def make_buttons(self):
        self.buttons = ButtonGroup()
        self.labels = pg.sprite.Group()

        Label("{} Wallpaper".format(self.name),
                {"midtop": (self.rect.centerx, self.rect.top + 16)},
                self.labels, font_size=24)
        self.paper = Wallpaper(self.name)
        self.paper_rect = self.paper.image.get_rect(midtop=(self.rect.centerx, self.rect.top + 48))
        top = self.paper_rect.bottom + 16
        Label("${}".format(self.paper.price), {"midtop": (self.rect.centerx, top)},
                                    self.labels, font_size=24)
        top += 32
        Label("Quality  {}".format(self.paper.quality), {"midtop": (self.rect.centerx, top)},
                self.labels, font_size=16)
        top += 24               
        for monster, bonus in self.paper.bonuses.items():
            if bonus == 0:
                continue
            elif bonus < 0:
                text = "{} {}".format(monster, bonus)
            else:
                text = "{} +{}".format(monster, bonus)
            Label(text, {"midtop": (self.rect.centerx, top)}, self.labels,
                     font_size=12)
            top += 24


        idle, hover = self.make_button_images("Buy", "large")
        w, h = idle.get_size()
        Button((self.rect.centerx-(w//2), self.rect.bottom - 112), self.buttons,
                   idle_image=idle, hover_image=hover, call=self.buy_wallpaper)
        idle, hover = self.make_button_images("Cancel", "small")
        w, h = idle.get_size()
        Button((self.rect.centerx - (w//2), self.rect.bottom - 56),
                   self.buttons, idle_image=idle, hover_image=hover,
                   button_size=(w, h), call=self.cancel)

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
        surface.blit(self.paper.image, self.paper_rect)
        self.labels.draw(surface)
        self.buttons.draw(surface)

    def buy_wallpaper(self, *args):
        if WALLPAPER_INFO[self.name][3] > self.player.cash:
            self.done = True
            self.next = "SHOW_WINDOW"
            self.persist["menu"] = MessageWindow(self.building, self.player,
                        "You can't afford this right now")
        else:
            self.player.cash -= WALLPAPER_INFO[self.name][3]
            self.unit.wallpaper = self.paper
            self.building.redraw = True
            self.done = True
            self.next = "GAMEPLAY"