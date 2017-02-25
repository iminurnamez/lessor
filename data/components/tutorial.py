import pygame as pg

from .. import prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.animation import Animation

def floor_check(building):
    if len(building.floors) > 0:
        return True
    return False
    
def unit_check(building):
    for floor in building.floors:
        if len(floor.units) > 0:
            return True
    return False
    
def item_check(building):
    for floor in building.floors:
        for unit in floor.units:
            for slot in unit.item_slots:
                if slot.item is not None:
                    return True
    return False
    
def ad_check(building):
    for n in building.world.newspapers:
        if n.ads:
            return True
    return False

def rent_check(building):
    for floor in building.floors:
        for unit in floor.units:
            if unit.rent != unit.next_rent:
                return True
    return False
    
    
class TutorialGoal(object):
    def __init__(self, msg, arrow_info, goal_check):
        self.label = Label(msg, {"midtop": (prepare.SCREEN_RECT.centerx, 16)},
                                  font_size=16, text_color="antiquewhite")
        self.goal_check = goal_check
        self.animations = pg.sprite.Group()
        self.arrow_image = None
        if arrow_info:
            direction, pos = arrow_info
            self.arrow_image = prepare.GFX["arrow-{}".format(direction)]
            self.arrow_rect = self.arrow_image.get_rect()
            if direction == "left":
                self.arrow_rect.midleft = pos
                self.pos = pos
                self.other_pos = (pos[0] + 16, pos[1])
            elif direction == "right":
                self.arrow_rect.midright = pos
                self.pos = pos
                self.other_pos = (pos[0] - 16, pos[1])
            elif direction == "up":
                self.pos = pos
                self.arrow_rect.midtop = pos
                self.other_pos = (pos[0], pos[1] + 16)
            else:
                self.pos = pos
                self.arrow_rect.midbottom = pos
                self.other_pos = (pos[0], pos[1] - 16)
                self.other_pos = (pos[0], pos[1] - 16)
            self.make_anis()
        
    def make_anis(self):
        d= 200
        ani = Animation(x=self.other_pos[0], duration=d, round_values=True)
        ani2 = Animation(x=self.pos[0], duration=d, delay=d, round_values=True)
        ani.start(self.arrow_rect)
        ani2.start(self.arrow_rect)
        ani2.callback = self.make_anis
        self.animations.add(ani, ani2)
        
    def update(self, dt):
        self.animations.update(dt)
        
        
    def draw(self, surface):
        self.label.draw(surface)
        if self.arrow_image:
            surface.blit(self.arrow_image, self.arrow_rect)

            
class Tutorial(pg.sprite.Sprite):
    def __init__(self, *groups):
        super(Tutorial, self).__init__(*groups)
        self.goal_info = [
                ["Click the build button to add a floor", ["left", (96,112)], floor_check],
                ["Click an empty floor to add units", [], unit_check],
                ["Click on a unit to open the unit info window to change the unit's rent", [], rent_check],
                ["Click a unit or an empty item slot to buy an item", [], item_check],
                ["Cick the classifieds button to place an ad", ["left", (96, 296)], ad_check]]
                           
        self.goals = []
        for msg, arrow_info, goal_check in self.goal_info:
            goal = TutorialGoal(msg, arrow_info, goal_check)
            self.goals.append(goal)
        self.goals = iter(self.goals)
        self.goal = next(self.goals)        
    
    def update(self, dt, building):
        self.goal.update(dt)
        if self.goal.goal_check(building):
            try:
                self.goal = next(self.goals)
            except StopIteration:
                self.kill()
                
    def draw(self, surface):
        self.goal.draw(surface)    