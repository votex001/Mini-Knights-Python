import pytmx
import pygame

# collisions and fall physic
class Physics:
    def __init__(self, level):
        self.level = level
        self.walkable_tiles = self._get_walkable_tiles()
        self.tiles_rects = self._get_tiles_rects()
        self.deadzonerects = []
        self.heatedrecs = []

    def _get_walkable_tiles(self):
        walkable = []
        for layer in self.level.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_props = self.level.tmx_data.get_tile_properties_by_gid(gid)
                    if tile_props and tile_props.get("walk") == True:
                        walkable.append((x, y))
        return walkable

    def _get_tiles_rects(self):
        rects = []
        tile_width = self.level.tile_width
        tile_height = self.level.tile_height
        for x, y in self.walkable_tiles:
            rects.append(pygame.Rect(x * tile_width, y * tile_height, tile_width, tile_height))
        return rects

    def draw_walkable_tiles(self, surface):
        for rect in self.tiles_rects:
            pygame.draw.rect(surface, (255, 255, 0), rect, 2)

    def collision_test(self,player_rect):
        hit_list = []
        for tile in self.tiles_rects:
            if player_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list
    
    def deathzone_touch_check(self,player_rect):
        heated =False
        tile_width = self.level.tile_width
        tile_height = self.level.tile_height
        if not self.deadzonerects:
            for layer in self.level.tmx_data.visible_layers:
                if isinstance(layer,pytmx.TiledTileLayer):
                    for x,y,gid in layer:
                        tile_props = self.level.tmx_data.get_tile_properties_by_gid(gid)
                        if tile_props and tile_props.get('deathzone') == True:
                            tiles_rect = pygame.Rect(x*tile_width,y*tile_height,tile_width,tile_height)
                            self.deadzonerects.append(tiles_rect)
        for tiles_rect in self.deadzonerects:
            if player_rect.colliderect(tiles_rect):
                heated = True
        return heated

    def exit_touch_check(self,player_rect):
        heated = False
        tile_width = self.level.tile_width
        tile_height = self.level.tile_height
        if not self.heatedrecs:
            for layer in self.level.tmx_data.visible_layers:
                if isinstance(layer,pytmx.TiledTileLayer):
                    for x,y,gid in layer:
                        tile_props = self.level.tmx_data.get_tile_properties_by_gid(gid)
                        if tile_props and tile_props.get('exit') == True:
                            tile_rect = pygame.Rect(x*tile_width,y*tile_height,tile_width,tile_height)
                            self.heatedrecs.append(tile_rect)
        for tile_rect in self.heatedrecs:                    
            if player_rect.colliderect(tile_rect):
                heated = True
        return heated

    def move(self,player_rect,player_movement):
        collision_types = {"top":False,"bottom":False,"right":False,"left":False}
        
        # X
        player_rect.x += player_movement[0] # [x,y]
        hit_list = self.collision_test(player_rect)
        for tile in hit_list:
            if player_movement[0] >0:
                player_rect.right = tile.left
                collision_types["right"] = True
            elif player_movement[0] <0:
                player_rect.left = tile.right
                collision_types["left"] = True

        # Y
        player_rect.y += player_movement[1] # [x,y]
        hit_list = self.collision_test(player_rect)
        for tile in hit_list:
            if player_movement[1]>0:
                player_rect.bottom = tile.top
                collision_types["bottom"] =True
            elif player_movement[1]<0:
                player_rect.top = tile.bottom
                collision_types["top"] = True
        return player_rect,collision_types