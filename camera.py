import pygame
from settings import *

class Camera:
    def __init__(self,camera_surface,player,screen):
        self.camera_surface = camera_surface
        self.player = player
        self.screen = screen
        self.zoom = ZOOM
        self.camera_pos = [0,0]
       


    def prepare_scaled_surface(self):
        # zoom map
        scaled_surface = pygame.transform.scale(
            self.camera_surface, 
            (self.camera_surface.get_width() * self.zoom, self.camera_surface.get_height() * self.zoom))
        
        # if to put this params on camera player will be on the center 
        player_pos_x = (-self.player.rect.x * self.zoom) + self.screen.get_width() / 2
        player_pos_y = (-self.player.rect.y*self.zoom)+self.screen.get_height()/2

        # dif between cam and player
        dif_x = player_pos_x - self.camera_pos[0]
        dif_y = player_pos_y - self.camera_pos[1]


        # after this num camera pos = player pos
        min_px = 1.0
       
        # to makes move camera smooth
        smooth_factor = 0.1



        # x
        if abs(dif_x) < min_px:
            self.camera_pos[0] = player_pos_x
        else:
            self.camera_pos[0] += dif_x * smooth_factor

        # y
        if abs(dif_y) < min_px:
            self.camera_pos[1] = player_pos_y
        else:
            self.camera_pos[1] += dif_y * smooth_factor
            
         
        # max and min camera pos
        self.camera_pos[0] = min(0,max(self.camera_pos[0],  -scaled_surface.get_width() +self.screen.get_width()))
        self.camera_pos[1] = min(0,max(self.camera_pos[1],  -scaled_surface.get_height() +self.screen.get_height()))
        return scaled_surface,self.camera_pos
    