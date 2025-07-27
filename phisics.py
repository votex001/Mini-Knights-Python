import pytmx
import pygame

# TileSprite class to represent each tile with its image, rect, and mask
class TileSprite(pygame.sprite.Sprite):
    def __init__(self, image, rect, mask):
        super().__init__()
        self.image = image
        self.rect = rect
        self.mask = mask


class Physics:
    def __init__(self, level):
        self.level = level
        self.walkable_sprites = self._get_walkable_sprites()

    # Get walkable tiles from the level
    def _get_walkable_sprites(self):
        # Create a group to hold walkable tile sprites
        sprites = pygame.sprite.Group()

        tile_width = self.level.tmx_data.tilewidth
        tile_height = self.level.tmx_data.tileheight

        for layer in self.level.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_props = self.level.tmx_data.get_tile_properties_by_gid(gid)
                    if tile_props and tile_props.get("walk") == True:
                        tile_img = self.level.tmx_data.get_tile_image_by_gid(gid)
                        if tile_img:
                            rect = pygame.Rect(x * tile_width, y * tile_height, tile_width, tile_height)
                            mask = pygame.mask.from_surface(tile_img)
                            sprite = TileSprite(tile_img, rect, mask)
                            sprites.add(sprite)
        return sprites

    # Draw walkable tiles for debugging purposes
    def draw_walkable_tiles(self, surface):
        for sprite in self.walkable_sprites:
            outline = sprite.mask.outline()
            if outline:
                shifted_outline = [(x + sprite.rect.x, y + sprite.rect.y) for x, y in outline]
                if len(shifted_outline) > 1:
                    pygame.draw.lines(surface, (255, 255, 0), True, shifted_outline, 2)
    
    # Collision detection between player and walkable tiles
    def collision_test(self, player_sprite):
        return pygame.sprite.spritecollide(player_sprite, self.walkable_sprites, False, pygame.sprite.collide_mask)

    # Move the player sprite and handle collisions
    def move(self, player_sprite, player_movement):
        # Initialize collision types
        player_sprite.rect.x += player_movement[0]
        collision_types = {"top": False, "bottom": False, "right": False, "left": False}
        # x movement
        player_sprite.rect.x += player_movement[0]
        hit_list = self.collision_test(player_sprite)
        for tile in hit_list:
            if player_movement[0] > 0:
                player_sprite.rect.right = tile.rect.left
                collision_types["right"] = True
            elif player_movement[0] < 0:
                player_sprite.rect.left = tile.rect.right
                collision_types["left"] = True
        # y movement
        player_sprite.rect.y += player_movement[1]
        hit_list = self.collision_test(player_sprite)
        for tile in hit_list:
            if player_movement[1] > 0:
                player_sprite.rect.bottom = tile.rect.top
                collision_types["bottom"] = True
                player_sprite.player_y_momentum = 0  
            elif player_movement[1] < 0:
                player_sprite.rect.top = tile.rect.bottom
                collision_types["top"] = True
        return player_sprite.rect, collision_types