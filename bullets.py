import math
from objects import Object

class Bullet(Object):
    def __init__(self,tile,x,y,ang,spd,dmg=1):
        super().__init__(x,y,tile.get_width(),tile.get_height())
        self.angle = ang
        self.speed = spd
        self.damage = dmg
        self.tile = tile

    def update(self, dT):
        self.x_cor += math.sin(self.angle) * self.speed * dT
        self.y_cor += math.cos(self.angle) * self.speed * dT

    def draw(self):
        return self.tile

