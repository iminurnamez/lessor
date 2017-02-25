import pygame as pg

from .. import prepare



class SliderTab(object):
    def __init__(self, topleft):
        self.image = prepare.GFX["slider_tab"]
        self.rect = self.image.get_rect(topleft=topleft)
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    
class Scroller(object):
    def __init__(self, rect, building):
        self.building = building
        self.slider_rect = rect
        self.frame_rect = FrameRect(self.slider_rect)
        self.slider_tab = SliderTab(self.slider_rect.topleft)
        self.tab_slide_amount = 16 #tab_slide_amount
        self.scroll_amount = 16 #scroll_amount
        self.slide_area = self.slider_rect.h - self.slider_tab.rect.h
        self.slider_fill_color = (49, 18, 65)
        self.grabbed = False
        
    def slide(self, direction):
        old = self.slider_tab.rect.top
        move = direction * self.tab_slide_amount
        self.slider_tab.rect.move_ip((0, move))
        self.slider_tab.rect.clamp_ip(self.slider_rect)
        self.set_panel_pos()
    
    def update_slider(self, mouse_pos):
        if self.grabbed:
            y = mouse_pos[1] - self.grab_point
            self.slider_tab.rect.top = y
            self.slider_tab.rect.clamp_ip(self.slider_rect)
            self.set_panel_pos()

    def set_slider_pos(self):
        slide_area = self.building.rect.h - self.building.view_rect.h
        try:
            percent = self.building.view_rect.top / float(slide_area)
            self.slider_tab.rect.top = self.slider_rect.top + (self.slide_area * percent)
        except ZeroDivisionError:
            self.slider_tab.rect.top = self.slider_rect.top

    def set_panel_pos(self):
        slide_area = self.building.rect.h - self.building.view_rect.h
        percent = (self.slider_tab.rect.top - self.slider_rect.top) / float(self.slide_area)
        old_top = self.building.view_rect.top
        new_top = percent * slide_area
        self.scroll(new_top - old_top)
        
    def scroll(self, amount):
        old_top = self.building.view_rect.top
        self.building.view_rect.top += amount
        if self.building.view_rect.top < 0:
            self.building.view_rect.top = 0
        elif self.building.view_rect.bottom > self.building.rect.bottom:
            self.building.view_rect.bottom = self.building.rect.bottom
            
    def check_scroll_events(self, event):    
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.slider_tab.rect.collidepoint(event.pos):
                    x, y = event.pos
                    self.grabbed = True
                    self.grab_point = y - self.slider_tab.rect.top
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                if self.grabbed:
                    self.grabbed = False
                    old_top = self.slider_tab.rect.top
                    new_top = event.pos[1] - self.grab_point
                    diff = new_top - old_top
                    self.slide(diff)
                elif self.slider_rect.collidepoint(event.pos):
                    x, y = event.pos
                    self.slider_tab.rect.centery = y
                    self.slider_tab.rect.clamp_ip(self.slider_rect)
                    self.set_panel_pos()
            elif event.button in (4, 5):
                view_rect = self.building.view_rect.copy()
                view_rect.topleft = (0, 0)
                panel_collide = view_rect.collidepoint(event.pos)
                if panel_collide:
                    if event.button == 4:
                        self.scroll(self.scroll_amount * -1)
                        self.set_slider_pos()
                    elif event.button == 5:
                        self.scroll(self.scroll_amount)
                        self.set_slider_pos()
                elif self.slider_rect.collidepoint(event.pos):
                    if event.button == 4:
                        self.slide(-1)
                        self.set_panel_pos()
                    elif event.button == 5:
                        self.slide(1)
                        self.set_panel_pos()
    
    def get_event(self, event):
        self.check_scroll_events(event)
        
    def draw(self, surface):
        pg.draw.rect(surface, self.slider_fill_color, self.slider_rect)
        self.frame_rect.draw(surface)
        self.slider_tab.draw(surface)

        
class FrameRect(object):
    def __init__(self, rect):
        self.rect = rect.inflate(16, 16)
        left = prepare.GFX["frame_left"]
        top = pg.transform.rotate(left, 270)
        tiles_high = self.rect.height // 8
        tiles_wide = self.rect.width // 8
        self.left_img = pg.Surface((8, self.rect.height))
        for y in range(0, self.rect.height, 8):
            self.left_img.blit(left, (0, y))
        self.top_img = pg.Surface((self.rect.width - 14, 8))
        for x in range(0, self.rect.width, 8):
            self.top_img.blit(top, (x, 0))
        self.right_img = pg.transform.flip(self.left_img, True, False)
        self.bottom_img = pg.transform.flip(self.top_img, False, True)
        self.corner_imgs = [
                pg.transform.rotate(prepare.GFX["frame_topleft"], x * 90)
                for x in range(4)]
        self.corners = [self.rect.topleft, (self.rect.left, self.rect.bottom - 16),
                              (self.rect.right - 16, self.rect.bottom - 16),
                              (self.rect.right - 16, self.rect.top)]

    def draw(self, surface):
        surface.blit(self.left_img, self.rect.topleft)
        surface.blit(self.right_img, (self.rect.right - 8, self.rect.top))
        surface.blit(self.top_img, (self.rect.left + 7, self.rect.top))
        surface.blit(self.bottom_img,
                         (self.rect.left + 7, self.rect.bottom - 8))
        for img, corner in zip(self.corner_imgs, self.corners):
            surface.blit(img, corner)