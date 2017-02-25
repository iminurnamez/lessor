import pygame as pg

from ..components.labels import Label, Button, ButtonGroup
from ..components.window import Window
from ..components.message_window import MessageWindow


class AddUnitsWindow(Window):
    def __init__(self, building, player, floor):
        super(AddUnitsWindow, self).__init__(building, player)
        self.floor = floor
        self.make_buttons()

    def make_buttons(self):
        self.buttons = ButtonGroup()
        b_size = 256, 48
        top = self.rect.top + 64
        left = self.rect.centerx - (b_size[0] // 2)
        for size, num in zip(("Small", "Medium", "Large", "Penthouse"), (4, 3, 2, "")):
            if num == "":
                u = "Unit"
            else:
                u = "Units"
            price = self.building.unit_costs[size.lower()]
            text = "{} {} {} ${:,}".format(num, size, u, price)
            args = [size.lower()]
            idle, hover = self.make_button_images(text, "large", 14)
            w, h = idle.get_size()
            Button((left, top), self.buttons, idle_image=idle, hover_image=hover, call=self.add_units, args=size)
            top += 96
        idle, hover = self.make_button_images("Cancel", "small")
        w, h = idle.get_size()
        Button((self.rect.centerx - (w//2), self.rect.bottom - 56),
                   self.buttons, idle_image=idle, hover_image=hover,
                   button_size=(w, h), call=self.cancel)
                   
    def cancel(self, *args):
        self.done = True
        self.next = "GAMEPLAY"

    def add_units(self, unit_size):
        cost = self.building.unit_costs[unit_size.lower()]
        if self.player.cash >= cost:
            self.player.cash -= cost
            self.floor.add_units(unit_size)
            self.next = "GAMEPLAY"
        else:
            self.next = "SHOW_WINDOW"
            self.persist["menu"] = MessageWindow(self.building, self.player, "You can't afford that right now")
        self.done = True

    def get_event(self, event):
        self.buttons.get_event(event)

    def update(self, dt, mouse_pos):
        self.buttons.update(mouse_pos)

    def draw(self, surface):
        self.building.draw(surface)
        self.draw_window(surface)
        self.buttons.draw(surface)