from random import randint, choice

from ..tools import lerp


class Sky(object):
    def __init__(self):
        self.colors = [(77, 21, 164), (164, 120, 21),
                           (21, 164, 127), (21, 164, 77), 
                           (85, 162, 33), (164, 162, 21),
                           (164, 58, 21)]
        self.last_color = choice(self.colors)
        self.next_color = choice(self.colors)
        self.time_range = (10000, 40000)
        self.change_time = randint(*self.time_range)
        self.timer = 0
        self.color = lerp(self.last_color, self.next_color,
                                self.timer / float(self.change_time))
        
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.change_time:
            self.timer = 0
            self.change_time = randint(*self.time_range)
            self.last_color = self.next_color
            self.next_color = choice(self.colors)
        self.color = lerp(self.last_color, self.next_color,
                                self.timer / float(self.change_time))      