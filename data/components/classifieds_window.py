import pygame as pg

from .. import prepare
from ..components.labels import Label, Button, ButtonGroup, MultiLineLabel
from ..components.window import Window
from ..components.world import PAPER_INFO, Ad
from ..components.message_window import MessageWindow


class ClassifiedsWindow(Window):
    def __init__(self, building, player):
        super(ClassifiedsWindow, self).__init__(building, player)
        self.make_buttons()
        
    def make_buttons(self):
        self.buttons = ButtonGroup()
        self.labels = pg.sprite.Group()
        papers = sorted(self.building.world.newspapers,
                                key=lambda x: x.circulation,
                                reverse=True)
        label = Label("Classifieds",
                           {"midtop": (self.rect.centerx, self.rect.top + 8)},
                           self.labels, font_size=16)
        top = label.rect.bottom + 16
        for i, p in enumerate(papers):
            idle, hover = self.make_button_images(p.name, "small", 12)
            w, h = idle.get_size()
            dist = -(w + 16)
            if i % 2:
                dist = 16
            Button((self.rect.centerx + dist, top), self.buttons,
                       idle_image=idle, hover_image=hover,
                       call=self.to_classified, button_size=(w, h), args=p)
            if i % 2:
                top += 64
        idle, hover = self.make_button_images("Cancel", "small")
        w, h = idle.get_size()
        Button((self.rect.centerx - (w//2), self.rect.bottom - 56),
                   self.buttons, idle_image=idle, hover_image=hover,
                   button_size=(w, h), call=self.cancel)    
        
    def cancel(self, *args):
        self.done = True
        self.next = "GAMEPLAY"
        
    def to_classified(self, paper):
        if paper.ads:
            self.persist["menu"] = MessageWindow(self.building, self.player,
                        "You already have an ad in this newspaper")
        else:
            self.persist["menu"] = ClassifiedWindow(self.building, self.player, paper)
        self.done = True
        self.next = "SHOW_WINDOW"
        
    def get_event(self, event):
        self.buttons.get_event(event)
        
    def update(self, dt, mouse_pos):
        self.buttons.update(mouse_pos)
        
    def draw(self, surface):
        self.building.draw(surface)
        self.draw_window(surface)
        self.labels.draw(surface)
        self.buttons.draw(surface)
        
        
        
class ClassifiedWindow(Window):
    def __init__(self, building, player, paper):
        super(ClassifiedWindow, self).__init__(building, player)
        self.paper = paper
        self.make_buttons()
        
    def make_buttons(self):
        self.buttons = ButtonGroup()
        self.labels = pg.sprite.Group()

        title = Label(self.paper.name, {"midtop": (self.rect.centerx, self.rect.top + 16)},
                          self.labels, font_size=24)
        label = MultiLineLabel(prepare.FONTS["PortmanteauRegular"],
                                         12, '"{}"'.format(self.paper.tagline), prepare.TEXT_COLOR,
                                         {"midtop": (self.rect.centerx, title.rect.bottom)},
                                         bg=None, char_limit=32, align="center", vert_space=0)
        self.labels.add(label)
        circ = Label("{:,} Readers".format(self.paper.circulation),
                          {"midtop": (self.rect.centerx, label.rect.bottom + 16)},
                          self.labels, font_size=16)
        
        readers = sorted(self.paper.audience.items(), key=lambda x: x[1], reverse=True)
        top = circ.rect.bottom
        left1 = self.rect.centerx - 112
        left2 = self.rect.centerx + 112
        for m, num in readers:
            if not num:
                continue
            Label(m, {"topleft": (left1, top)},self.labels, font_size=12)
            Label("{}%".format(num), {"topright": (left2, top)}, self.labels,
                    font_size=12)
            top += 16    
        top = self.rect.top + 256
        i = 0
        for num_weeks, price_mod in self.paper.ad_price_mods:
            price =  self.paper.price * price_mod
            txt = "{} Weeks ${:,}".format(num_weeks, price)
            idle, hover = self.make_button_images(txt, "small", 16)
            w, h = idle.get_size()
            left = self.rect.centerx - (w + 16)
            if i % 2:
                left = self.rect.centerx + 16
            Button((left, top), self.buttons, idle_image=idle, 
                       hover_image=hover, button_size=(w, h),
                       call=self.buy_ad, args=[num_weeks, price])
            i += 1
            if not i % 2:
                top += 64
        idle, hover = self.make_button_images("Back", "small")
        w, h = idle.get_size()
        Button((self.rect.centerx - (w//2), self.rect.bottom - 56),
                   self.buttons, idle_image=idle, hover_image=hover,
                   button_size=(w, h), call=self.cancel)
                   
    def buy_ad(self, args):
        num_weeks, price = args
        if self.player.cash < price:
            self.persist["menu"] = MessageWindow(
                        self.building, self.player, 
                        "You can't afford this right now")
            self.next = "SHOW_WINDOW"
        else:
            self.player.cash -= price
            days = num_weeks * 7
            Ad(days, self.paper.ads)
            self.next = "GAMEPLAY"
        self.done = True
        
    def cancel(self, *args):
        self.done = True
        self.next = "SHOW_WINDOW"
        self.persist["menu"] = ClassifiedsWindow(self.building, self.player)
        
    def get_event(self, event):
        self.buttons.get_event(event)

    def update(self, dt, mouse_pos):
        self.buttons.update(mouse_pos)

    def draw(self, surface):
        self.building.draw(surface)
        self.draw_window(surface)
        self.labels.draw(surface)
        self.buttons.draw(surface)  