import pygame
from objects import Object

class Hud(Object):
    def __init__(self, dimensions, font):
        self.font = font
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.text = font
        self.spawn_rect_width = 100
        self.spawn_rect_height = 10

    def draw(self, player_list):
        surf = pygame.Surface((self.width, self.height))
        surf.set_colorkey((0,0,0))
        
        hud_rect_y_cor = self.height-32
        pygame.draw.rect(surf,(1,0,0),pygame.Rect(0,hud_rect_y_cor,self.width,32))

        for player in player_list:
            x_offset = 1 if player.player_id == 1 else 135

            if player.state == 'DESPAWN':
                if player.lives < 0:
                    surf.blit(self.text.draw('GAME OVER',(255,255,255)), (x_offset+20, hud_rect_y_cor+10))
                else:
                    rect_width = self.spawn_rect_width * ((60-player.timer['despawn']) / 60)
                    y_cor = hud_rect_y_cor + (self.height - hud_rect_y_cor)/2
                    spawn_rect = pygame.Rect(x_offset, y_cor-(self.spawn_rect_height/2), rect_width, self.spawn_rect_height)
                    pygame.draw.rect(surf, (255,255,255), spawn_rect)
            else:
                surf.blit(self.text.draw(str(player.score),(255,255,255)), (x_offset+1, 3))

                surf.blit(self.text.draw('lives',(255,255,255)), (x_offset, hud_rect_y_cor+1))
                surf.blit(self.text.draw(str(player.lives),(255,255,255)), (x_offset+self.text.get_width('lives')+1, hud_rect_y_cor+1))

                surf.blit(self.text.draw('level',(255,255,255)), ((x_offset+self.text.get_width('lives')+10,hud_rect_y_cor+1)))
                surf.blit(self.text.draw(str(player.level),(255,255,255)), (x_offset+self.text.get_width('lives')+10+self.text.get_width('level')+1,hud_rect_y_cor))

                surf.blit(self.text.draw('exp',(255,255,255)), (x_offset,hud_rect_y_cor+11))
                surf.blit(self.text.draw(str(player.exp),(255,255,255)), (x_offset+self.text.get_width('exp')+1,hud_rect_y_cor+11))

                surf.blit(self.text.draw('power',(255,255,255)), ((x_offset+self.text.get_width('exp')+10,hud_rect_y_cor+11)))
                surf.blit(self.text.draw(str(player.meter),(255,255,255)), (x_offset+self.text.get_width('exp')+10+self.text.get_width('power')+1,hud_rect_y_cor+11))
        
        return surf
