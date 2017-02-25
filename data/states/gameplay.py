import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.building import Building
from ..components.build_window import BuildWindow
from ..components.delete_units_window import DeleteUnitsWindow
from ..components.classifieds_window import ClassifiedsWindow
from ..components.player import Player

        
class Gameplay(tools._State):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.player = Player()
        self.building = Building()
        self.make_buttons()
        self.player_cash_label = Label(
                    "${:,}".format(int(self.player.cash)),
                    {"topleft": (8, 8)},
                    text_color="antiquewhite",
                    font_size=28)
        self.bulldozing = False
        self.speed_index = 1
        self.speeds = [.5, 1, 2, 4]
        self.speed = self.speeds[self.speed_index]
        self.tutorials = pg.sprite.Group()
        
        
    def make_buttons(self):    
        self.buttons = ButtonGroup()
        crane = prepare.GFX["button-build"]
        crane_idle = prepare.GFX["button-build-idle"]
        b_size = crane.get_size()
        Button((16, 64), self.buttons, button_size=b_size,
                   idle_image=crane_idle, hover_image=crane,
                   call=self.build)
        dozer = prepare.GFX["button-bulldoze"]
        dozer_idle = prepare.GFX["button-bulldoze-idle"]
        Button((16, 160), self.buttons, button_size=b_size,
                   idle_image=dozer_idle, hover_image=dozer,
                   call=self.bulldoze)
        hover = prepare.GFX["button-classifieds"]
        idle = prepare.GFX["button-classifieds-idle"]
        Button((16, 256), self.buttons, button_size=b_size,
                   idle_image=idle, hover_image=hover,
                   call=self.to_ad_window)
        
    def bulldoze(self, *args):
        if not self.bulldozing:
            self.bulldozing = True
            self.cursor.image = self.cursor.bulldoze_image
        else:
            self.bulldozing = False
            self.cursor.image = self.cursor.default_image
            
    def build(self, *args):
        menu = BuildWindow(self.building, self.player)
        self.done = True
        self.next = "SHOW_WINDOW"
        self.persist["menu"] = menu
      
    def to_ad_window(self, *args):
        menu = ClassifiedsWindow(self.building, self.player)
        self.done = True
        self.next = "SHOW_WINDOW"
        self.persist["menu"] = menu
       

    def startup(self, persistent):
        self.persist = persistent
        self.cursor = self.persist["cursor"]
        if self.persist["tutorials"]:
            self.tutorials = self.persist["tutorials"]
        self.music_manager = self.persist["music manager"]    

    def get_event(self,event):
        self.music_manager.get_event(event)
        self.cursor.get_event(event)
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            if event.key == pg.K_UP:
                self.speed_index += 1
                if self.speed_index > len(self.speeds) - 1:
                    self.speed_index = len(self.speeds) - 1
                self.speed = self.speeds[self.speed_index]
            elif event.key == pg.K_DOWN:
                self.speed_index -= 1
                if self.speed_index < 0:
                    self.speed_index = 0
                self.speed = self.speeds[self.speed_index]
                
        if not self.bulldozing:
            self.building.get_event(event, self)
            self.buttons.get_event(event)
        else:
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 3:
                    self.bulldoze()
                if event.button == 1:
                    x = self.building.view_rect.left + event.pos[0]
                    y = self.building.view_rect.top + event.pos[1]
                    for floor in self.building.floors:
                        if floor.rect.collidepoint((x, y)):
                            menu = DeleteUnitsWindow(self.building, self.player, floor)
                            self.persist["menu"] = menu
                            self.bulldoze()
                            self.done = True
                            self.next = "SHOW_WINDOW"

    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.cursor.update(dt, mouse_pos)
        self.building.update(int(dt * self.speed), mouse_pos, self)
        self.buttons.update(mouse_pos)
        if self.player.cash >= 666666:
            self.done = True
            self.next = "WIN_SCREEN"
        cash = "${:,}".format(int(self.player.cash))
        if self.player_cash_label.text != cash:
            self.player_cash_label.set_text(cash)
        if self.player.cash >= 666666:
            self.done = True
            self.next = "WIN_SCREEN"
            self.persist["player"] = self.player
            self.persist["building"] = self.building
        self.tutorials.update(dt, self.building)
        
    def draw(self, surface):
        self.building.draw(surface)
        self.buttons.draw(surface)
        self.player_cash_label.draw(surface)
        self.building.calendar.draw(surface)
        self.cursor.draw(surface)
        for tut in self.tutorials:
            tut.draw(surface)