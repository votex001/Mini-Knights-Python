import pygame
from pygame.locals import *
from animation import Animation

class Player(pygame.sprite.Sprite):
    def __init__(self, imgs_path,imgs_map, spawn_pos, physics, surface):
        super().__init__()
        self.SPEED = 5
        self.JUMP_LEFT = 2
        self.JUMP_HEIGHT = 8
        self.Fall_SPEED = 0.4
        self.MAX_FALL_SPEED = 5

        self.surface= surface
        self.physics = physics
        self.last_move_side = "right"

        # player Img and Rect
        self.animation = Animation(imgs_path,imgs_map)
        self.img,self.rect_img,_ = self.animation.next_frame('idle',self.last_move_side)
        self.rect = self.rect_img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)

        # on init spawn Player
        self.spawn_pos = spawn_pos
        self.spawn()

        # player movement
        self.players_jumps = self.JUMP_LEFT
        self.moving_right = False
        self.moving_left = False
        self.attack = False
        self.player_y_momentum = 0

    def spawn(self):
        self.x, self.y = self.spawn_pos if self.spawn_pos else (0, 0)
        self.rect.topleft = (self.x, self.y)
        self.surface.blit(self.img, self.rect)

    def update_animation(self):
        # anim side priority
        if self.moving_left:
            self.last_move_side = "left"
        elif self.moving_right:
            self.last_move_side = "right"
            
        if self.attack:
            self.img,_,last_frame = self.animation.next_frame("attack",self.last_move_side)
            if last_frame:
                self.attack = False
        elif self.player_y_momentum < 0:
            self.img,_,_ = self.animation.next_frame("jump",self.last_move_side)
        elif  self.moving_right:
            self.img,_,_ = self.animation.next_frame("run",self.last_move_side)
        elif self.moving_left:
            self.img,_,_ = self.animation.next_frame("run",self.last_move_side)
        else:
            self.img,_,_ = self.animation.next_frame("idle",self.last_move_side)
        
        # old_center = self.rect.center  # сохраняем позицию
        # self.rect = self.rect_img.get_rect()
        # self.rect.center = old_center  # восстанавливаем позицию
        # self.mask = pygame.mask.from_surface(self.rect_img)



    # listen to player moves
    def handle_input(self,events):
        self.update_animation()
        player_movement =[0,0]
        if self.moving_right:
            player_movement[0] += self.SPEED
        if self.moving_left:
            player_movement[0] -= self.SPEED
        player_movement[1] += self.player_y_momentum
        self.player_y_momentum += self.Fall_SPEED
        if self.player_y_momentum > self.MAX_FALL_SPEED:
            self.player_y_momentum = self.MAX_FALL_SPEED

        player_rect, collisions = self.physics.move(self.rect, player_movement)
        if collisions['bottom']:
            self.players_jumps = self.JUMP_LEFT
        if collisions['top']:
            self.player_y_momentum = 1
        self.surface.blit(self.img,player_rect)


        for event in events: # event loop
            if event.type == KEYDOWN:
                if event.key == K_x:
                    self.attack = True
                if event.key == K_d:
                    self.moving_right = True
                if event.key == K_a:
                    self.moving_left = True
                if event.key == K_w:
                   if self.players_jumps >0:
                    self.player_y_momentum = -self.JUMP_HEIGHT
                    self.players_jumps -=1
            if event.type == KEYUP:
                if event.key == K_d:
                    self.moving_right = False
                if event.key == K_a:
                    self.moving_left = False
        

       