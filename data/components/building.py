import pygame as pg

from .. import prepare
from ..components.labels import Label
from ..components.scroller import Scroller
from ..components.items import YardItem, Wallpaper
from ..components.add_units_window import AddUnitsWindow
from ..components.purchase_unit_item_categories_window import PurchaseUnitItemCategoriesWindow
from ..components.delete_unit_item_window import DeleteUnitItemWindow
from ..components.visitor_info_window import VisitorInfoWindow
from ..components.sky import Sky
from ..components.calendar import Calendar
from ..components.world import World
from ..components.unit_info_window import UnitInfoWindow


class Sign(pg.sprite.Sprite):
    def __init__(self, building):
        self.image = prepare.GFX["yard_sign"]
        self.rect = self.image.get_rect(
                    midbottom=(135, building.rect.h - 160))

    def move(self, move):
        self.rect.move_ip(move)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Building(object):
    floor_width = 1032
    floor_height = 128
    path_directions = [
            "up", "up", "up", "up", "up", "up",
            "left", "left", "left", "left", "left", "left",
            "up", "up", "up", "right"]
    path_map = {
            "up": (32, -32),
            "down": (-32, 32),
            "left": (-107, 0),
            "right": (107, 0)}
    unit_costs = {
            "small": 15000,
            "medium": 24000,
            "large": 30000,
            "penthouse": 50000}

    def __init__(self):
        self.floors = []
        self.rect = pg.Rect(0, 0, 1280, 720)
        self.footprint_offset = (193, -348)
        self.top_floor = 0
        self.topleft = (0, 0)
        self.yard_items = []
        self.landscape_items = []
        self.view_rect = prepare.SCREEN_RECT.copy()

        self.make_path()
        scroll_rect = pg.Rect(self.view_rect.right - 24,
                               self.view_rect.top + 8, 16, self.view_rect.h - 16)
        self.scroller = Scroller(scroll_rect, self)
        self.vacancies = False
        self.yard_sign = Sign(self)
        self.sky = Sky()
        self.calendar = Calendar()
        self.world = World(self)
        self.make_background()
        self.image = pg.Surface(self.rect.size)
        self.make_image()
        self.redraw = False
        
    def make_image(self):
        if self.image.get_size() != self.rect.size:
            self.image = pg.Surface(self.rect.size)
        self.image.fill(self.sky.color)
        self.image.blit(self.bg, (0, self.rect.h - self.bg.get_height()))
        onscreen = self.yard_items + [x for x in self.world.visitors] + [x for x in self.floors] # if x .rect.colliderect(self.view_rect)]
        if self.vacancies:
            onscreen.append(self.yard_sign)
        for y in sorted(onscreen, key=lambda x: x.rect.bottom):
            y.draw(self.image)

    def make_background(self):
        street = prepare.GFX["street"]
        street_w, street_h = street.get_size()
        grass = prepare.GFX["grass"]
        grass_h = grass.get_size()[1]
        height = street_h + grass_h
        self.bg = pg.Surface((self.rect.w, height))
        for x in range(0, self.rect.w, street_w):
            self.bg.blit(street, (x, height - street_h))
        self.bg.blit(grass, (0, 0))
        for p_rect in self.path_rects:
            self.bg.blit(prepare.GFX["path"], p_rect.move(0, self.bg.get_height() - self.rect.h))


    def make_path(self):
        street_w, street_h = prepare.GFX["street"].get_size()
        path_img = prepare.GFX["path"]
        path_start = (439, self.rect.h - street_h)
        rect = path_img.get_rect(topleft=path_start)
        self.path_rects = [rect.copy()]
        for d in self.path_directions:
            rect.move_ip(self.path_map[d])
            self.path_rects.append(rect.copy())

    def move(self, move):
        for floor in self.floors:
            floor.move(move)
        for r in self.path_rects:
            r.move_ip(move)
        for y in self.yard_items:
            y.rect.move_ip(move)
        for v in self.world.visitors:
            v.move(move)
        self.yard_sign.rect.move_ip(move)

    def add_floor(self):
        self.top_floor += 1
        self.move((0, self.floor_height))
        self.view_rect.top = 0
        new_bottom = self.rect.bottom + self.floor_height
        self.rect = self.rect.inflate(0, self.floor_height)
        self.rect.bottom = new_bottom

        self.footprint_bottomleft = (self.footprint_offset[0],
                self.footprint_offset[1] + self.rect.bottom)
        new_floor_topleft = (self.footprint_bottomleft[0],
                self.footprint_bottomleft[1] - (self.floor_height * self.top_floor))
        floor = Floor(self.top_floor, new_floor_topleft, (self.floor_width, self.floor_height), self)
        self.floors.append(floor)
        self.redraw = True

    def get_floor_build_cost(self):
        return (self.top_floor + 1) * 1000

    def get_event(self, event, state):
        self.scroller.get_event(event)
        for floor in self.floors:
            floor.get_event(event, state)
        if event.type == pg.MOUSEBUTTONUP:
            x, y = event.pos
            y += self.view_rect.top
            for v in self.world.visitors:
                if v.rect.collidepoint((x, y)):
                    state.done = True
                    state.persist["menu"] = VisitorInfoWindow(self, state.player, v)

    def update(self, dt, mouse_pos, state):
        self.scroller.update_slider(mouse_pos)
        self.sky.update(dt)
        self.calendar.update(dt)
        self.world.update(dt)
        self.vacancies = False
        for f in self.floors:
            for u in f.units:
                if u.tenant is None:
                    self.vacancies = True
                u.update_quality_label()
        for _ in range(self.calendar.days_passed):
            self.daily_update(state.player)
        if self.redraw:
            self.make_image()
        self.redraw = False

    def daily_update(self, player):
        rent_collected = 0
        for floor in self.floors:
            for unit in floor.units:
                if unit.tenant:
                    unit.lease -= 1
                    if unit.rent_date == self.calendar.day:
                        rent_collected += unit.rent
                    if unit.lease <= 0:
                        unit.tenant.decide_to_stay(unit)
        player.cash += rent_collected
        self.world.daily_update()

    def draw(self, surface):
        surface.fill(self.sky.color)
        surf = self.image.subsurface(self.view_rect)
        surface.blit(surf, (0, 0))
        self.scroller.draw(surface)


class Floor(object):
    num_units = {
        "small": 4,
        "medium": 3,
        "large": 2,
        "penthouse": 1
        }

    def __init__(self, level, topleft, size, building):
        self.level = level
        self.rect = pg.Rect(topleft, size)
        self.units = []
        self.unimproved = True
        self.building = building

    def add_units(self, unit_size):
        unit_size = unit_size.lower()
        self.units = []
        num = self.num_units[unit_size.lower()]
        w = self.rect.w // num
        letters = "ABCD"
        for x, letter in zip(range(num), letters):
            left = self.rect.left + (x * w)
            unit_num = "{}{}".format(self.level, letter)
            unit = Unit((left, self.rect.top), (w, self.rect.h), unit_size, unit_num, self)
            self.units.append(unit)
        self.unimproved = False
        self.building.redraw = True


    def remove_units(self):
        self.units = []
        self.unimproved = True
        self.building.redraw = True

    def move(self, move):
        self.rect.move_ip(move)
        for unit in self.units:
            unit.move(move)

    def save_to_dict(self):
        d = {}
        d["units"] = []
        for unit in self.units:
            d["units"].append(unit.save_to_dict())
        d["rect"] = [self.rect.topleft, self.rect.size]
        d["level"] = self.level
        d["unimproved"] = self.unimproved

    def get_event(self, event, state):
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            x = event.pos[0] + self.building.view_rect.left
            y = event.pos[1] + self.building.view_rect.top
            if self.unimproved:
                if self.rect.collidepoint((x, y)):
                    state.done = True
                    state.next = "SHOW_WINDOW"
                    state.persist["menu"] = AddUnitsWindow(self.building, state.player, self)
            for unit in self.units:
                if unit.get_event(event, state):
                    break
            #else:
            #    if self.rect.collidepoint((x, y)):
            #        state.done = True
            #        state.next = "SHOW_WINDOW"
            #        state.persist["menu"] = FloorInfoWindow()


    def draw(self, surface):
        if self.unimproved:
            surface.blit(prepare.GFX["emptyfloor"], self.rect)
        for unit in self.units:
            unit.draw(surface)


class ItemSlot(object):
    def __init__(self, unit, topleft, item=None):
        self.unit = unit
        self.rect = pg.Rect(topleft, (32, 32))
        if item is not None:
            self.add_item(item)
        else:
            self.item = None
            self.item_rect = None

    def move(self, move):
        self.rect.move_ip(move)
        if self.item_rect:
            self.item_rect.move_ip(move)

    def remove_item(self):
        self.item = None
        self.item_rect = None
        self.unit.floor.building.redraw = True

    def add_item(self, item):
        self.item = item
        self.item_rect = self.item.image.get_rect(center=self.rect.center)
        self.unit.floor.building.redraw = True

    def draw(self, surface):
        if self.item:
            surface.blit(self.item.image, self.item_rect)


class Unit(object):
    item_slot_offsets = {
        "penthouse": [
            (3, 59), (37, 59), (71, 59), (105, 59),
            (3, 93), (37, 93), (71, 93), (105, 93),
            (895, 59), (929, 59), (963, 59), (997, 59),
            (895, 93), (929, 93), (963, 93), (997, 93)],
        "large": [
            (3, 59), (37, 59), (71, 59),
            (3, 93), (37, 93), (71, 93),
            (413, 59), (447, 59), (481, 59),
            (413, 93), (447, 93), (481, 93)],
        "medium": [
            (3, 59), (37, 59),
            (3, 93), (37, 93),
            (275, 59), (309, 59),
            (275, 93), (309, 93)],
        "small": [
            (3, 59),
            (3, 93),
            (223, 59),
            (223, 93)]
    }
    item_limits = {
            "small": {"Appliance": 1},
            "medium": {"Appliance": 2},
            "large": {"Appliance": 4},
            "penthouse": {"Appliance": 8}
    }
    base_quality = {
            "small": 50,
            "medium": 100,
            "large": 200,
            "penthouse": 400
    }
    price_mods = {
        "small": 3.0,
        "medium": 3.5,
        "large": 4.0,
        "penthouse": 5.0}
    default_rents = {
        "small": 150,
        "medium": 350,
        "large": 800,
        "penthouse": 2000}
    star_spots = {
        "small": (71, 33),
        "medium": (109, 33), 
        "large": (169, 33),
        "penthouse": (315, 33)}
    happy_face = prepare.GFX["face-happy"]
    neutral_face = prepare.GFX["face-neutral"]
    sad_face = prepare.GFX["face-sad"]
    blank_face = prepare.GFX["face-blank"]
    def __init__(self, topleft, size, unit_size, unit_num, floor):
        self.rect = pg.Rect(topleft, size)
        self.unit_size = unit_size
        self.unit_num = unit_num
        self.floor = floor
        self.tenant = None
        self.tenant_rect = pg.Rect(0, 0, 68, 116)
        self.tenant_rect.midbottom = self.rect.midbottom
        self.wallpaper = Wallpaper("Fancy Blue")
        self.frame = prepare.GFX["roomframe-{}".format(self.unit_size)]
        self.make_item_slots()
        self.rent = self.next_rent = self.get_fair_rent()
        self.star = prepare.GFX["star"]
        sx, sy = self.star_spots[self.unit_size]
        self.star_rect = self.star.get_rect(midbottom=(self.rect.x + sx, self.rect.y + sy))
        self.smiley = self.blank_face
        self.smiley_rect = self.smiley.get_rect(midbottom=(self.rect.right - sx, self.rect.top + sy))
        self.labels = pg.sprite.Group()
        self.quality_label = Label("{}".format(int(self.get_quality_score())),
                                            {"midtop": self.star_rect.midbottom},
                                            self.labels, font_size=16)
        
    def update_quality_label(self):
        old = self.quality_label.text
        old_smiley = self.smiley
        monster = None if not self.tenant else self.tenant.monster_type
        qual = self.get_quality_score(monster)
        t = "{}".format(qual)
        if t != old:
            self.quality_label.set_text(t)
            self.floor.building.redraw = True
        if self.tenant:
            if self.tenant.happiness <= 30:
                self.smiley = self.sad_face
            elif self.tenant.happiness >= 70:
                self.smiley = self.happy_face
            else:
                self.smiley = self.neutral_face
        else:
            self.smiley = self.blank_face
        if old_smiley != self.smiley:
            self.floor.building.redraw = True
            
    def get_fair_rent(self, monster=None):
        quality = self.get_quality_score(monster)
        fair_price = self.price_mods[self.unit_size] * quality
        return fair_price

    def get_quality_score(self, monster=None):
        score = self.base_quality[self.unit_size]
        score += self.wallpaper.quality
        if monster:
            score += self.wallpaper.bonuses[monster]
        for land in self.floor.building.landscape_items:
            score += land.quality
            if monster:
                score += land.bonuses[monster]
        for slot in self.item_slots:
            if slot.item:
                score += slot.item.quality
                if monster:
                    score += slot.item.bonuses[monster]
        return score

    def move(self, move):
        self.rect.move_ip(move)
        self.tenant_rect.move_ip(move)
        for item_slot in self.item_slots:
            item_slot.move(move)
        self.star_rect.move_ip(move)
        self.quality_label.rect.move_ip(move)        
        self.quality_label.rect_attr = {"midtop": self.star_rect.midbottom}
        self.smiley_rect.move_ip(move)
        
    def make_item_slots(self):
        self.item_slots = []
        for spot in self.item_slot_offsets[self.unit_size]:
            x, y = spot[0] + self.rect.left, spot[1] + self.rect.top
            slot = ItemSlot(self, (x, y))
            self.item_slots.append(slot)

    def add_tenant(self, tenant):
        if self.tenant is not None:
            return False
        self.tenant = tenant
        self.rent_date = self.floor.building.calendar.day
        self.lease = 365
        self.floor.building.redraw = True
        return True
        
    def get_event(self, event, state):
        if event.type == pg.MOUSEBUTTONUP:
            x = self.floor.building.view_rect.left + event.pos[0]
            y = self.floor.building.view_rect.top + event.pos[1]
            for item_slot in self.item_slots:
                if item_slot.rect.collidepoint((x, y)):
                    if item_slot.item:
                        state.persist["menu"] = DeleteUnitItemWindow(self.floor.building, state.player, item_slot)
                    else:
                        state.persist["menu"] = PurchaseUnitItemCategoriesWindow(self.floor.building, state.player, item_slot, self)
                    state.done = True
                    state.next = "SHOW_WINDOW"
                    return True
            if self.rect.collidepoint((x, y)):
                state.done = True
                state.next = "SHOW_WINDOW"
                state.persist["menu"] = UnitInfoWindow(self.floor.building, state.player, self)

    def load_from_dict(self, d):
        if d["tenant"] is not None:
            self.tenant = Tenant(d["tenant"])


    def save_to_dict(self):
        d = {}
        d["items"] = []
        for item in self.items:
            pass
        if self.tenant is not None:
            d["tenant"] = self.tenant.save_to_dict()
        else:
            d["tenant"] = None

    def draw(self, surface):
        if self.wallpaper:
            self.wallpaper.draw(surface, self.rect)
        else:
            pg.draw.rect(surface, pg.Color("gray20"), self.rect)
        surface.blit(self.frame, self.rect)
        for item_slot in self.item_slots:
            item_slot.draw(surface)
        if self.tenant:
            surface.blit(self.tenant.image, self.tenant_rect)
            #smiley face
        surface.blit(self.star, self.star_rect)
        self.quality_label.draw(surface)
        surface.blit(self.smiley, self.smiley_rect)        