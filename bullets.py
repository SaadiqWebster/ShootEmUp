import math,random
from objects import Object

class Bullet(Object):
    def __init__(self,x,y,ang,spd,dmg=1):
        super().__init__(x,y,8,8)
        self.angle = ang
        self.speed = spd
        self.damage = dmg

    def update(self, dT):
        self.x_cor += math.sin(self.angle) * self.speed * dT
        self.y_cor += math.cos(self.angle) * self.speed * dT
