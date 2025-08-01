import pygame

class Camera:
    def __init__(self,camera_surface,player_rect,screen,zoom):
        self.camera_surface = camera_surface
        self.player_rect = player_rect
        self.screen = screen
        self.zoom = zoom



    def prepare_scaled_surface(self):
        scaled_surface = pygame.transform.scale(
            self.camera_surface, 
            (self.camera_surface.get_width() * self.zoom, self.camera_surface.get_height() * self.zoom))
         

        surface_x = min(0,max((-self.player_rect.x * self.zoom) + self.screen.get_width() / 2,  -self.screen.get_width()*self.zoom +self.screen.get_width()))
        surface_y = min(0,max((-self.player_rect.y*self.zoom)+self.screen.get_height()/2,-self.screen.get_height()*self.zoom + self.screen.get_height()))
        surface_pos = (surface_x,surface_y)
        return scaled_surface,surface_pos
    