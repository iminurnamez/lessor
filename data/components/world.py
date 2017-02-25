from random import randint, choice, uniform, random

import pygame as pg

from .. import prepare
from ..components.animation import Animation, Task
from ..components.angles import get_distance

MONSTER_INFO = {
    #NAME                        QLTY FLOOR      EXPECT QLTY         RENT LIMIT           
    "Zombie": [                         40,                      70,                 400],              
    "Skeleton": [                       50,                      80,                 500],               
    "Homocidal Maniac": [          60,                    100,                 700],
    "Pumpkin Head": [               90,                    150,                 1000],
    "Frankenfolk": [                   130,                   210,                1500],
    "Ghost": [                            160,                  280,                2000],
    "Witch": [                            195,                  380,                2400],
    "Demon": [                          235,                  460,                2700],
    "Vampire": [                        280,                  550,                5000]}
      
PAPER_INFO = {
        #NAME                         Circulation         Price         Audience
        #                                                                        Z         Sk       HM     PH    FRk      G     DMN     W      v   
        "Evil Examiner": [             66000,          150,       [23,       16,     15,     13,   11,      10,      7,     4,     1], "Your #13 Evil News Source"],
        "Undead Observer": [        50000,          200,       [40,       40,       0,      0,     0,        0,      0,        0,     20], "Raising the dead, Raising the Bar"],
        "Daily Exhumer": [            40000,          200,       [50,       50,       0,      0,     0,       0,      0,        0,       0], "Every day, digging up the truth"],
        "Graveyard Gazette": [      30000,          200,       [30,       60,       0,     0,      0,        0,      0,     10,       0], "Covering issues of grave concern"],
        "Nooseweek": [                 20000,          200,       [0,          0,      70,     0,     0,      30,      0,        0,       0], "All the noose that's fit to print"],
        "Crypt Chronicler": [          20000,          200,       [25,       30,       0,     0,      0,      25,      0,        0,      20], "Opening Dialogue, Uncovering Facts"],
        "Hades Herald": [               15000,         300,       [0,          0,       0,     0,      0,        10,    70,     10,     10], "Going to hell and back for the news you need"],
        "Vine-Dispatch": [              15000,         300,       [0,          0,       0,    100,      0,        0,      0,        0,       0], "I heard it on the Vine-Dispatch"],    
        "Redrum Reporter": [         15000,          300,       [5,         5,      65,     0,      0,        20,     5,        0,       0], "Heeere's the news"],
        "Witches' Weekly": [          15000,          300,       [0,         0,        0,     0,      0,          0,      0,      100,       0], "Keep up with what's brewing"],
        "Spectral Press": [             15000,          300,       [0,         0,        0,     0,      0,       100,      0,        0,       0],  "Transparency is our business"],
        "Transylvania Times": [    15000,          300,       [0,         0,        0,     0,      0,         0,      0,        0,    100], "Keeping a fang on the pulse of the evil world"],
        "Franken Ledger": [           15000,          300,       [0,         0,        0,     0,    100,         0,      0,        0,      0], "Keeping our teeth on the beat"]
        }

class Newspaper(object):
    ad_price_mods = [
        (1, 1),
        (2, 1.9),
        (4, 3.5),
        (13, 9),
        (26, 15),
        (52, 25)]

    def __init__(self, name, circulation, price, audience, tagline):
        self.name = name
        self.circulation = circulation
        self.price = price
        self.tagline = tagline
        self.ads = pg.sprite.Group()
        self.pool = []
        self.audience = {}
        names = ["Zombie", "Skeleton", "Homocidal Maniac",
                       "Pumpkin Head", "Frankenfolk", "Ghost",
                       "Demon", "Witch", "Vampire"]
        for n, num in zip(names, audience):
            self.pool.extend([n] * num)
            self.audience[n] = num
        
    def daily_update(self, building, visitors):
        for ad in self.ads:
            ad.update()
            chance = self.circulation * .00001
            if random() <= chance:
                visitor_type = choice(self.pool)
                self.generate_visitor(visitor_type, self.name, building, visitors)
                
    def generate_visitor(self, monster_type, paper_name, building, visitors):
        mod = randint(32, 256)
        if randint(0, 1):
            x = building.rect.left - mod
        else:
            x = building.rect.right = mod        
        start_pos = (x, building.rect.h - 91)    
        Visitor(monster_type, start_pos, self.name, building, visitors)
        
class Ad(pg.sprite.Sprite):
    def __init__(self, days, *groups):
        super(Ad, self).__init__(*groups)
        self.days = days
        
    def update(self):
        self.days -= 1
        if self.days < 1:
            self.kill()


class World(object):
    def __init__(self, building):
        self.building = building
        self.newspapers = []
        for p_name in PAPER_INFO:
            self.newspapers.append(Newspaper(p_name, *PAPER_INFO[p_name]))
        self.visitors = pg.sprite.Group()
        self.sign_pool = []
        names = ["Zombie", "Skeleton", "Homocidal Maniac",
                       "Pumpkin Head", "Frankenfolk", "Ghost",
                       "Demon", "Witch", "Vampire"]
        for n, num in zip(names, PAPER_INFO["Evil Examiner"][2]):
            self.sign_pool.extend([n] * num)
        
    def daily_update(self):
        empty = []
        for f in self.building.floors:
            for u in f.units:
                if u.tenant is None:
                    empty.append(u)
        num_empty = len(empty)
        if num_empty and (random() <= .15):
            visitor_type = choice(self.sign_pool)
            self.generate_visitor(visitor_type, "Yard Sign")
        for paper in self.newspapers:
            paper.daily_update(self.building, self.visitors)
            
    def generate_visitor(self, monster_type, paper_name):
        mod = randint(64, 256)
        if randint(0, 1):
            x = - mod
        else:
            x = prepare.SCREEN_RECT.right + mod        
        start_pos = (x, self.building.rect.h - 91)    
        Visitor(monster_type, start_pos, paper_name, self.building, self.visitors)               
        
    
    def update(self, dt):    
        self.visitors.update(dt, self.building)           
                    
    
        
class Tenant(pg.sprite.Sprite):
    def __init__(self, monster_type, gender, sentiments, unit):
        self.gender = gender
        self.monster_type = monster_type
        self.quality_floor, self.expected_quality, self.rent_limit = MONSTER_INFO[monster_type]
        self.sentiments = sentiments
        name = "".join(monster_type.lower()).replace(" ", "")
        try:
            self.image = prepare.GFX[name]
        except KeyError:
            self.image = prepare.GFX[name + self.gender]
        self.unit = unit
        self.happiness = 50
        
    def decide_to_stay(self, unit):
        quality = unit.get_quality_score(self.monster_type)
        fair_rent = unit.get_fair_rent(self.monster_type)
        qual_score = quality / float(self.expected_quality)
        price_score = fair_rent / float(unit.rent)
        total = (qual_score * .6) + (price_score * .4)
        if unit.rent > self.rent_limit:
            high = unit.rent / float(self.rent_limit)
            sentiments = [
                    (2, "Absurd Rent"), 
                    (1.5, "Very High Rent")]
            for num, s in sentiments:
                if high >= num:
                    sentiment = s
                    break
            else:
                sentiment = "High Rent"            
            self.add_sentiment(sentiment, unit.unit_num)
            self.vacate()
            return
        if quality < self.quality_floor:
            low = quality / float(self.quality_floor)
            sentiments = [
                    (.5, "Abysmal Quality"),
                    (.75, "Poor Quality")]
            for num, s in sentiments:
                if low <= num:
                    sentiment = s
                    break
                else:
                    sentiment = "Low Quality"
            self.add_sentiment("Low Quality", unit.unit_num)
            self.vacate()
            return False
        
        success = total >= uniform(0, 2)
        if success:
            if qual_score * .6 >= price_score * .4:
                self.add_sentiment("Quality Rental", unit.unit_num)
            else:
                self.add_sentiment("Price Rental", unit.unit_num)
            lease_length = (qual_score * .6) + (price_score * .4)
            self.resign_lease(unit)
            
        else:
            self.add_sentiment("Random Refusal", unit.unit_num)
    
    def vacate(self, unit):
        unit.tenant = None
        self.kill()
        
    def resign_lease(self, unit):
        unit.lease = 365
        
    def daily_update(self):
        old = self.happiness
        quality = unit.get_quality_score(self.monster_type)
        fair_rent = unit.get_fair_rent(self.monster_type)
        qual_score = quality / float(self.expected_quality)
        price_score = fair_rent / float(unit.rent)
        total = (qual_score * .6) + (price_score * .4)
        self.happiness = total * 25
        if self.happiness < 0:
            self.happiness = 0
        elif self.happiness > 100:
            self.happiness = 100
        if self.happiness != old:
            self.unit.floor.building.redraw = True
            
        
class Visitor(pg.sprite.Sprite):
    def __init__(self, monster_type, start_pos, paper_name, building, *groups):
        super(Visitor, self).__init__(*groups)
        self.gender = choice(("male", "female"))
        self.monster_type = monster_type
        self.quality_floor, self.expected_quality, self.rent_limit = MONSTER_INFO[monster_type]
        name = "".join(monster_type.lower()).replace(" ", "")
        try:
            self.image = prepare.GFX[name]
        except KeyError:
            self.image = prepare.GFX[name + self.gender]
        self.rect = self.image.get_rect(midbottom=start_pos)
        self.state = "Travelling"
        sents = ["Time to check out the ad I saw in {}.",
                     "That {} ad really grabbed my attention."]
        self.sentiments = [choice(sents).format(paper_name)]
        self.animations = pg.sprite.Group()
        self.state = "Travelling"
        self.path = [x.center for x in building.path_rects[::-1]]
        self.return_path = [start_pos]
        self.return_path.extend([x.center for x in building.path_rects])
            
    def move(self, move):
        self.rect.move_ip(move)
        self.path = [(x[0] + move[0], x[1] + move[1]) for x in self.path]
        self.return_path = [(x[0] + move[0], x[1] + move[1]) for x in self.return_path]
        
    def update(self, dt, building):
        old = self.rect.midbottom
        self.animations.update(dt)
        if self.rect.midbottom != old:
            building.redraw = True
        if self.state == "Travelling":
            if not self.animations:
                if not self.path:
                    delay = randint(1000, 5000)
                    empty_units = []
                    for f in building.floors:
                        for u in f.units:
                            if u.tenant is None:
                                empty_units.append(u)
                    for eu in empty_units:
                        task = Task(self.decide_on_lease, delay, 1, args=[eu])
                        self.animations.add(task)
                        delay += randint(1000, 5000)    
                    self.state = "Looking"
                else:
                    dest = self.path.pop()
                    dist = get_distance(self.rect.midbottom, dest)
                    span = max(1, int(dist * 10))
                    ani = Animation(centerx=dest[0], bottom=dest[1], duration=span, round_values=True)
                    ani.start(self.rect)
                    self.animations.add(ani)
        elif self.state == "Looking":
            if not self.animations:
                if not self.return_path:
                    self.kill()
                self.path = self.return_path
                self.state = "Travelling"

    def decide_on_lease(self, unit):
        quality = unit.get_quality_score(self.monster_type)
        fair_rent = unit.get_fair_rent(self.monster_type)
        qual_score = quality / float(self.expected_quality)
        price_score = fair_rent / float(unit.rent)
        total = (qual_score * .6) + (price_score * .4)
        if unit.rent > self.rent_limit:
            high = unit.rent / float(self.rent_limit)
            sentiments = [
                    (2, "Absurd Rent"), 
                    (1.5, "Very High Rent")]
            for num, s in sentiments:
                if high >= num:
                    sentiment = s
                    break
            else:
                sentiment = "High Rent"            
            self.add_sentiment(sentiment, unit.unit_num)
            return False
        if quality < self.quality_floor:
            low = quality / float(self.quality_floor)
            sentiments = [
                    (.5, "Abysmal Quality"),
                    (.75, "Poor Quality")]
            for num, s in sentiments:
                if low <= num:
                    sentiment = s
                    break
                else:
                    sentiment = "Low Quality"
            self.add_sentiment("Low Quality", unit.unit_num)
            return False
        
        success = total >= uniform(0, 2)
        if success:
            if qual_score * .6 >= price_score * .4:
                self.add_sentiment("Quality Rental", unit.unit_num)
            else:
                self.add_sentiment("Price Rental", unit.unit_num)
            lease_length = (qual_score * .6) + (price_score * .4)
            tenant = Tenant(self.monster_type, self.gender, self.sentiments, unit)
            if unit.add_tenant(tenant):
                self.kill()
        else:
            self.add_sentiment("Random Refusal", unit.unit_num)
        

        
    def add_sentiment(self, sentiment, unit_num):
        sentiments = {
            "Abysmal Quality": [
                "I would never live in unit {}.",
                "{}? What a hole.",
                "I may be a monster, but I'm not living in unit {}.",
                "Unit {} isn't up to my standards."],
            "Poor Quality": [
                "I would never live in unit {}.",
                "Unit {} is a bit of dump.",
                "Unit {} isn't up to my standards."],
            "Low Quality": [
                "Unit {} is almost acceptable.",
                "Unit {} isn't up to my standards.",
                "{}? Needs some improvement before I'd live there."],
            "Absurd Rent": [
                "{}? What am I? The one percent?",
                "I looked at {}. Do they think I'm made of money?",
                "I can't afford unit {}."],
            "Very High Rent": [
                "I can't afford unit {}."],
            "High Rent": [
                "I can't afford unit {}.",
                "I'd have to get a day job to afford {}."],
            "Random Refusal": [
                "{} was ok, but I think I'll see what else I can find.",
                "I guess I'm just not in a buying mood today.",
                "I'll keep {} on my list, but I think I'll keep looking."],
            "Quality Rental": [
                "My friends will be jealous of my new place, unit {}.",
                "{} was a nice change of pace from the other dumps I looked at.",
                "I'm looking forward to meeting my neighbors."],
            "Price Rental": [
                "I just got a good deal on unit {}.",
                "I couldn't pass up the deal on {}.",
                "I'm looking forward to meeting my neighbors."]}
        self.sentiments.append(choice(sentiments[sentiment]).format(unit_num))
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)