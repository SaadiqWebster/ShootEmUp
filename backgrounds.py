import pygame
from objects import Object

class LevelBackground(Object):
    def __init__(self, size, background_database, asset_list):
        super().__init__(0,0,0,0)
        self.surf = pygame.Surface(size)
        self.surf.set_colorkey((0,0,0))
        self.fill_color = (0,0,0)
        self.asset_list = asset_list
        self.asset_database = self.load_from_database(background_database, asset_list)
        self.layer_position = {i:[0,0] for i in range(len(asset_list))}
        self.layer_speed = {i:0 for i in range(len(asset_list))}
        print(self.asset_database, self.layer_position, self.layer_speed)

    def update(self):
        for layer in self.layer_position:   
            self.layer_position[layer][1] = (self.layer_position[layer][1] + self.layer_speed[layer]) % self.surf.get_height()

    def draw(self):
        self.surf.fill(self.fill_color)
        for layer in self.layer_position:
            self.surf.blit(self.asset_database[self.asset_list[layer]], (self.layer_position[layer][0], self.layer_position[layer][1]))
            self.surf.blit(self.asset_database[self.asset_list[layer]], (self.layer_position[layer][0], self.layer_position[layer][1]-self.surf.get_height()))
            self.surf.blit(self.asset_database[self.asset_list[layer]], (self.layer_position[layer][0], self.layer_position[layer][1]+self.surf.get_height()))
        return self.surf

class SkyBackground(LevelBackground):
    def __init__(self, size, tileset_database):
        self.asset_list = ['test_layer1','test_layer2']
        super().__init__(size, tileset_database['background'], self.asset_list)
        
        self.fill_color = (60, 129, 219)
        #self.
    
