from random import randint
import pygame as pg

from .. import prepare


UNIT_ITEM_INFO = {

    #NAME                                 TYPE                  QLTY BONUS    MONSTER BONUSES                                                                PRICE     FLAVOR TEXT
    #                                                                                        Vmp, Ghst, Witch, Demon, Maniac, Pmpkin, Zomb, Skel, Frank


    "Candle": [                        "Lighting",                5,               [0,       0,      0,       0,          0,        10,          0,       0,      0],       25,         "Everything's creepier by candlelight."],
    "Candleabra": [                  "Lighting",               10,              [0,       0,      0,       0,          0,         0,          0,       0,      0],       40,          "Even creepier than candles."],
    "Chandelier": [                  "Lighting",                20,              [5,       5,      0,       0,          0,         0,          0,       0,      0],       70,          "An elegant, creepy answer for all your lighting needs."],

    "Coffin":                             ["Bed",                  10,               [10,       1,    0,       1,         0,         0,          2,        5,      0],      100,    "Coffins are an acceptable bed for all monsters."],
    "Casket":                            ["Bed",                  20,               [15,     2,      0,       2,         0,         0,          5,        10,    0],      160,    "More comfortable than coffins, caskets make good beds."],
    "Sarcophagus":                   ["Bed",                  40,               [20,     5,      0,       5,         0,         0,          10,      20,    0],     210,      "Vampires especially enjoy sleeping in a sarcophagus."],


    "Stone Fireplace": [          "Fireplace",                10,              [0,       0,      0,       0,          0,         0,          0,       0,      0],       120, "A simple stone fireplace."],
    "Oven":                [          "Fireplace",                10,                [0,       0,    15,       0,          0,         0,          0,       0,      0],      125,  "With space for up to three fattened children, this is an oven the whole coven will covet."],
    "Marble Fireplace": [          "Fireplace",                20,              [5,       5,      0,       0,          0,         0,          0,       0,      0],       210, "This fireplace from Malevolent Marbleworks will add a bit of spooky splendor to any room."],


    "Ouija Board": [               "Appliance",               5,                [0,      15,      0,     10,          0,         0,          0,       0,     0],       100,  ""],
    "Voodoo Doll": [               "Appliance",               5,                [0,       0,      0,       0,          0,         0,         15,       0,    10],      100,  ""],
    "Mortar and Pestle": [       "Appliance",               5,                 [0,       0,      5,        0,         0,         0,           0,       0,      5],      100, ""],
    "Cauldron": [                   "Appliance",              10,               [0,       0,      15,       0,          0,         0,          0,       0,      0],     160,  "*Eye of newt not included"],
    "Brain Storage Unit": [     "Appliance",              10,                [0,       0,      0,       0,         15,         0,         15,       0,     0],     160,  "Not just brains, the Fridgidahmer Braincrisp is perfect for storing all manner of body parts."],
    "Soiling Machine": [         "Appliance",              20,                [0,       0,      0,       0,          0,         0,          5,       0,     0],       240,  "When it comes to soiling, the Mayhemtag Soil-o-matic cleans up."],

    "Broom Closet": [            "Appliance",                5,                [0,       0,      20,     0,          0,         0,          0,       0,      0],       125, "Home is Where You Hang Your Broom"],
    "IV Stand": [                   "Appliance",               5,                [10,      0,      0,       0,          0,         0,          0,       0,     0],       125,  ""],
    "Bookcase": [                  "Appliance",               10,               [10,      0,     10,      0,          0,         0,          0,       0,     10],       150, ""],
    "Torture Table": [             "Appliance",              10,                [0,       0,      0,      10,         20,         0,          0,       0,     0],       150, ""],
    "Electric Chair": [            "Appliance",              10,               [0,       0,       0,       0,          5,         0,          0,       0,      20],      150, ""],
    "Laboratory": [                "Appliance",              10,                [5,       0,      5,       0,          0,         0,          0,       0,     20],      150, ""],
    "Altar": [                         "Appliance",              20,                [10,    10,     5,      10,          0,         0,          0,       0,      0],       300, ""],

    "Spiderweb": [                "Decoration",            5,              [0,       0,       0,       0,          0,         0,          0,       0,        0],         10,   ""],
    "Noose": [                        "Decoration",            5,              [0,      10,       0,       5,         10,        0,          0,       0,         0],       150,  ""],
    "Mirror": [                        "Decoration",            5,              [-20,   10,      0,       0,          0,         0,          0,        0,       0],        150,   "Most monsters will enjoy practicing their scary faces with this mirror."],
    "Radioactive Waste": [      "Decoration",           5,               [0,       0,        0,       0,          0,       20,        10,       0,        0],        150,  ""],
    "Venus Fly Trap": [           "Decoration",          10,              [0,       0,       0,       0,          0,        20,         0,       0,        0],        240,   ""],
    "Baby in a jar": [              "Decoration",          10,              [0,       0,       5,       5,          5,         0,          0,       0,       10],       240,   "This gruseome specimen is especially popular with Frankenfolk."],
    "Bone China": [                "Decoration",          10,              [0,       0,      0,       0,           0,         0,          0,       10,       0],       240,   ""],
    "Crystal Ball": [                "Decoration",          10,              [5,       0,     10,       0,          0,         0,          0,       0,         0],       240,   ""],
    "Stained Glass": [             "Decoration",         15,              [10,       5,      0,       5,          0,         0,          0,       0,        0],       300,   ""],
    "Throne": [                       "Decoration",         20,              [10,     0,      0,         0,          0,         0,          0,       0,        0],       360,   ""]
    }

LANDSCAPE_ITEMS = {
        "Spooky Trees": [         "Landscape",           2,               [0,     0,      0,         0,          0,         0,          0,       0,        0],       500,   ""],
        "Iron Fence":[              "Landscape",           1,               [0,     0,      0,         0,          0,         0,          0,       0,        0],       750,   ""],
        "Gravestones": [          "Landscape",           1,               [0,     0,      0,         0,          0,         0,          1,       1,        0],       1000,   ""]
        #"Mushrooms": [           "Landscape",           5,               [0,     0,      0,         0,          0,         0,          5,       5,        0],       360,   ""]
        }

WALLPAPER_INFO = {
        "Peeling": [                 "Wallpaper",            5,                [0,     0,      0,         0,          0,         0,          2,       2,        0],       50,   ""],
        "Padded": [                 "Wallpaper",            5,                [0,     0,      0,         0,          5,         0,          0,       0,        0],       50,   ""],
        "Fancy Blue": [            "Wallpaper",            10,              [0,     5,      5,         5,          0,         0,          0,       0,        0],       100,   ""],
        "Fancy Red": [             "Wallpaper",            10,              [5,     0,      0,         0,          0,         0,          0,       0,        0],       100,   ""],
        "Fancy Green": [          "Wallpaper",            10,              [0,     0,      0,         0,          0,         5,          0,       0,        0],       100,   ""],
        "Fancy Beige": [          "Wallpaper",             10,             [0,     0,      0,         0,          5,         0,          5,       5,        0],       100,   ""],
        "Fancy Yellow": [         "Wallpaper",             10,              [0,     0,      0,         0,          0,         0,          0,       0,        5],       100,   ""]
        }


class Wallpaper(object):
    def __init__(self, name):
        self.name = name
        cat, quality, bonuses, price, text = WALLPAPER_INFO[name]
        self.quality = quality
        names = ["Vampire", "Ghost", "Witch", "Demon", "Homocidal Maniac",
                       "Pumpkin Head", "Zombie", "Skeleton", "Frankenfolk"]
        self.bonuses = {n: b for n, b in zip(names, bonuses)}
        self.price = price
        self.flavor_text = text
        img_name = "".join(name.lower().replace(" ", ""))
        if img_name == "peeling":
            img_name += "{}".format(randint(1, 3))
        self.image = prepare.GFX["wallpaper-{}".format(img_name)]

    def draw(self, surface, rect):
        w = self.image.get_width()
        for x in range(rect.left, rect.right, w):
            if rect.right - x < self.image.get_width():
                r = pg.Rect(0, 0, rect.right-x, rect.h)
                surface.blit(self.image.subsurface(r), (x, rect.top))
            else:
                surface.blit(self.image, (x, rect.top))


class LandscapeItem(object):
    def __init__(self, name, quality, bonuses, price, flavor_text):
        self.name = name
        self.quality = quality
        names = ["Vampire", "Ghost", "Witch", "Demon", "Homocidal Maniac",
                       "Pumpkin Head", "Zombie", "Skeleton", "Frankenfolk"]
        self.bonuses = {n: b for n, b in zip(names, bonuses)}
        self.price = price
        self.flavor_text = flavor_text


class Trees(LandscapeItem):
    tree_spots = {
            1: (-15, -447),
            2: (636, -159),
            4: (216, -130),
            5: (1055, -157)}
    def __init__(self, building):
        super(Trees, self).__init__("Spooky Trees", *LANDSCAPE_ITEMS["Spooky Trees"][1:])
        self.add_trees(building)
        building.landscape_items.append(self)
        building.redraw = True

    def add_trees(self, building):
        for num, spot in self.tree_spots.items():
            img = prepare.GFX["tree{}".format(num)]
            left = spot[0] #+ building.rect.left
            bottom = building.rect.bottom + spot[1]
            rect = img.get_rect(bottomleft=(left, bottom))
            tree = YardItem(img, rect.topleft)
            building.yard_items.append(tree)


class Fence(LandscapeItem):
    def __init__(self, building):
        super(Fence, self).__init__("Iron Fence", *LANDSCAPE_ITEMS["Iron Fence"][1:])
        self.add_fence(building)
        building.landscape_items.append(self)
        building.redraw = True

    def add_fence(self, building):
            r_fence = prepare.GFX["fence"]
            l_fence = pg.transform.flip(r_fence, True, False)
            w, h = r_fence.get_size()
            left_fence_spots = [(x, building.rect.bottom - (114 + h))
                                         for x in range(214, -w + 2, -(w - 2))]
            right_fence_spots = [(x, building.rect.bottom - (114 + h))
                                           for x in [597 + ((w-2) * x) for x in range(6)]]
            for ls in left_fence_spots:
                building.yard_items.append(YardItem(l_fence, ls))
            for rs in right_fence_spots:
                building.yard_items.append(YardItem(r_fence, rs))


class Gravestones(LandscapeItem):
    grave_spots = [(109, -498), (434, -239), (891, -212),
                           (1204, -323), (57, -294)]
    def __init__(self, building):
        super(Gravestones, self).__init__("Gravestones", *LANDSCAPE_ITEMS["Gravestones"][1:])
        self.add_gravestones(building)
        building.landscape_items.append(self)
        building.redraw = True

    def add_gravestones(self, building):
        for x, y in self.grave_spots:
            grave = YardItem(prepare.GFX["gravestone"],
                                       (x, building.rect.bottom + y))
            building.yard_items.append(grave)


class Mushrooms(LandscapeItem):
    def __init__(self, building):
        super(Mushrooms, self).__init__("Mushrooms", *LANDSCAPE_ITEMS["Mushrooms"][1:])


class YardItem(object):
    def __init__(self, image, topleft):
        self.image = image
        self.rect = self.image.get_rect(topleft=topleft)

    def draw(self, surface):
        surface.blit(self.image, self.rect)




class UnitItem(object):
    def __init__(self, name):
        self.name = name
        item_type, quality, bonuses, price, text = UNIT_ITEM_INFO[name]
        self.item_type = item_type
        self.quality = quality
        names = ["Vampire", "Ghost", "Witch", "Demon", "Homocidal Maniac",
                       "Pumpkin Head", "Zombie", "Skeleton", "Frankenfolk"]
        self.bonuses = {n: b for n, b in zip(names, bonuses)}
        self.flavor_text = text
        self.image = prepare.GFX["".join(self.name.lower().replace(" ", ""))]


class Tenant(object):
    def __init__(self, monster_type):
        self.monster_type = monster_type
        name = "".join(self.monster_type.lower())
        if self.monster_type in ("Frankenfolk", "Pumpkin Head", "Homicidal Maniac", "Zombie"):
            name += choice(("male", "female"))
        self.image = prepare.GFX[name]

        #self.price_range =
        #self.quality_req =

class Visitor(Tenant):
    def __init__(self, monster_type):
        pass


class Advertiser(object):
    def __init__(self, circulation, population, bonuses):
        self.circulation = circulation
        self.bonuses = bonuses

    def daily_update(self):
        pass
