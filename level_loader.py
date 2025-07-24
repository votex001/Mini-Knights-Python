import pytmx
from pytmx.util_pygame import load_pygame



class SelectLevel:
    def __init__(self,path,surface):
        self.surface = surface
        self.tmx_data = load_pygame(path)
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight
        self.spawn_pos = None
    

    def get_spawn(self):
        for obj in self.tmx_data.objects:
            if obj.properties.get("spawn") == True:
                # self.spawn_pos = (obj.x-(obj.width),obj.y-(obj.height))
                self.spawn_pos = (obj.x,obj.y)
                # self.spawn_pos = (0,0)
        return self.spawn_pos
               
            
    def draw(self):
        # draw bg
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer,pytmx.TiledImageLayer):
                image = layer.image
                self.surface.blit(image,(0,0))

        # draw tiles
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer,pytmx.TiledTileLayer):
                for x,y,gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        self.surface.blit(tile,(x*self.tile_width,y*self.tile_height))
        