import pygame
from pygame.locals import * 

class Player:
    def __init__(self,path,spawn_pos,physics,surface):
        # Default Settings
        self.SPEED = 2
        self.JUMP_LEFT = 2
        self.JUMP_HEIGHT = 4

        self.surface= surface
        self.physics = physics

        # player Img and Rect
        self.img = pygame.image.load(path).convert_alpha()
        self.rect = self.img.get_rect()


        # on init spawn Player
        self.spawn_pos = spawn_pos
        self.spawn()

        # player movement
        self.players_jumps = self.JUMP_LEFT
        self.moving_right = False
        self.moving_left = False
        self.player_y_momentum = 0

    # spawn player on spawn pos
    def spawn(self):
        # for test draw player rect
        # pygame.draw.rect(surface,(0,255,255),self.rect)

        self.x, self.y = self.spawn_pos if self.spawn_pos else (0, 0)
        self.rect.topleft = (self.x, self.y)
        self.surface.blit(self.img, self.rect)

    # listen to player moves
    def handle_input(self,events):
        player_movement =[0,0]
        if self.moving_right:
            player_movement[0] += self.SPEED
        if self.moving_left:
            player_movement[0] -= self.SPEED
        player_movement[1] += self.player_y_momentum
        self.player_y_momentum += 0.2
        if self.player_y_momentum > 3:
            self.player_y_momentum = 3

        player_rect,collisions = self.physics.move(self.rect,player_movement)
        if collisions['bottom']:
            self.players_jumps = self.JUMP_LEFT
        if collisions['top']:
            self.player_y_momentum = 1
        self.surface.blit(self.img,player_rect)


        for event in events: # event loop
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.moving_right = True
                if event.key == K_LEFT:
                    self.moving_left = True
                if event.key == K_UP:
                   if self.players_jumps >0:
                    self.player_y_momentum = -self.JUMP_HEIGHT
                    self.players_jumps -=1
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.moving_right = False
                if event.key == K_LEFT:
                    self.moving_left = False
        

       