import pygame
from pygame.locals import *
from animation import Animation
import time
class Player(pygame.sprite.Sprite):
    def __init__(self, imgs_path,imgs_map, spawn_pos, physics, surface):
        super().__init__()
        # player params
        self.SPEED = 5
        self.JUMP_LEFT = 2
        self.JUMP_HEIGHT = 8
        self.Fall_SPEED = 0.4
        self.MAX_FALL_SPEED = 5
        self.DAMAGE = 5


        # dead animation
        self.player_is_alive = False
        #for after dies control connection use this
        self.after_dead_anim = False

        # map surface
        self.surface= surface

        # collision physic
        self.physics = physics

        self.last_move_side = "right"

        # player Img and Rect
        self.animation = Animation(imgs_path,imgs_map)
        self.img,self.rect_img,_ = self.animation.next_frame('idle',self.last_move_side)
        self.rect = self.rect_img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.jump_animation = False

        # on init spawn Player
        self.spawn_pos = spawn_pos
        self.spawn()

        # player movement
        self.players_jumps = self.JUMP_LEFT
        self.moving_right = False
        self.moving_left = False
        self.attack = False
        self.player_y_momentum = 0

    def reload_player_vue(self):
        self.img,self.rect_img,_ = self.animation.next_frame('idle',self.last_move_side)
        self.rect = self.rect_img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.rect.topleft = (self.x, self.y)
        self.surface.blit(self.img, self.rect)


    def spawn(self):
        self.x, self.y = self.spawn_pos if self.spawn_pos else (0, 0)
        self.reload_player_vue()
        self.player_is_alive = True
        self.after_dead_anim = False

    def update_animation(self):
        if self.player_is_alive:
            # anim side priority
            if self.moving_left:
                self.last_move_side = "left"
            elif self.moving_right:
                self.last_move_side = "right"
                
            if self.attack:
                self.img,_,last_frame = self.animation.next_frame("attack",self.last_move_side)
                if last_frame:
                    self.attack = False
            elif self.jump_animation:
                self.img,_,last_frame = self.animation.next_frame("jump",self.last_move_side)
                if last_frame:
                    self.jump_animation = False
            elif  self.moving_right:
                self.img,_,_ = self.animation.next_frame("run",self.last_move_side)
            elif self.moving_left:
                self.img,_,_ = self.animation.next_frame("run",self.last_move_side)
            else:
                self.img,_,_ = self.animation.next_frame("idle",self.last_move_side)
        else:
            if self.img:
                self.img,_,last_frame = self.animation.next_frame("die",self.last_move_side,True)
                img_rect = self.img.get_rect()
                img_rect.midbottom = self.rect.midbottom
                self.rect = img_rect
                if last_frame:
                    self.animation.reset_animation("die")
                    self.after_dead_anim = True
                    time.sleep(3)
                    self.spawn()
    # if player dies
    def die(self):
            self.player_is_alive = False
            self.reset_moves()       

    # reset player movement
    def reset_moves(self):
        self.moving_right = self.moving_left = self.attack = False 


    # listen to player moves
    def handle_input(self,events):    
        player_movement =[0,0]
        if self.moving_right:
            player_movement[0] += self.SPEED
        if self.moving_left:
            player_movement[0] -= self.SPEED
        player_movement[1] += self.player_y_momentum
        self.player_y_momentum += self.Fall_SPEED
        if self.player_y_momentum > self.MAX_FALL_SPEED:
            self.player_y_momentum = self.MAX_FALL_SPEED

        player_rect, collisions,player_damaged_by_deathzone = self.physics.move(self.rect, player_movement)
        if player_damaged_by_deathzone:
            self.die()
        if collisions['bottom']:
            self.players_jumps = self.JUMP_LEFT
            self.jump_animation = False
        if collisions['top']:
            self.player_y_momentum = 1
        if self.img:
            self.surface.blit(self.img,player_rect)

        self.update_animation()

        for event in events: # event loop
            if event.type == KEYDOWN:
                # can move only if alive
                if self.player_is_alive:
                    if event.key == K_x:
                        self.attack = True
                    if event.key == K_d:
                        self.moving_right = True
                    if event.key == K_a:
                        self.moving_left = True
                    if event.key == K_w:
                        if self.players_jumps >0:
                            self.animation.reset_animation("jump")
                            self.jump_animation = True
                            self.player_y_momentum = -self.JUMP_HEIGHT
                            self.players_jumps -=1
            if event.type == KEYUP:
                if event.key == K_d:
                    self.moving_right = False
                if event.key == K_a:
                    self.moving_left = False
        

       