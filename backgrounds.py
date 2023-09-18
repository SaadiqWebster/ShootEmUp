import pygame
from objects import Object

class Background(Object):
    def __init__(self, size, background_database):
        super().__init__(0,0,0,0)
        self.surf = pygame.Surface(size)
        self.surf.set_colorkey((0,0,0))
        self.animation_list = ['test_layer1','test_layer2']
        self.assets_database = self.load_animation(background_database,self.animation_list)
        self.layer_position = {
            0:[0,0],
            1:[0,0]
        }
    
    def update(self):
        self.layer_position[0][1] = (self.layer_position[0][1] + 4) % self.surf.get_height()
        self.layer_position[1][1] = (self.layer_position[1][1] + 7) % self.surf.get_height()

    def draw(self):
        self.surf.fill((107,193,255))
        for layer in self.layer_position:
            self.surf.blit(self.assets_database[self.animation_list[layer]], (self.layer_position[layer][0], self.layer_position[layer][1]))
            self.surf.blit(self.assets_database[self.animation_list[layer]], (self.layer_position[layer][0], self.layer_position[layer][1]-self.surf.get_height()))
            self.surf.blit(self.assets_database[self.animation_list[layer]], (self.layer_position[layer][0], self.layer_position[layer][1]+self.surf.get_height()))
        return self.surf
