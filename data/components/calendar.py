import pygame as pg

from .. import prepare
from ..components.labels import Label


class Calendar(object):
    def __init__(self):
        self.day_length = 2000
        self.day = 1
        self.total_days = 1
        self.month = 1
        self.year = 1
        self.timer = 0
        self.label = Label(
                    self.get_date_string(),
                    {"topright": (prepare.SCREEN_RECT.right - 48, 8)}, font_path=prepare.FONTS["PortmanteauRegular"],
                    font_size=24, text_color="antiquewhite")
        
    def update(self, dt):
        self.timer += dt
        self.days_passed, self.timer = divmod(self.timer, self.day_length)
        self.day += self.days_passed
        self.total_days += self.days_passed
        if self.day > 30:
            self.day = 1
            self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        if self.days_passed:
            self.label.set_text(self.get_date_string())
            
    def get_date_string(self):
        yr = "{}".format(self.year)
        if self.year < 10:
            yr = "0" + yr
        return "{}/{}/{}".format(self.month, self.day, yr)

    def draw(self, surface):
        self.label.draw(surface)