import pygame,math,random
import bullets as b
from objects import Object

class Enemy(Object):
    def __init__(self,x,y):
        super().__init__(x,y,24,24)
        self.bullets = []
        self.health = 100
        self.iframes = False
        self.timer = {
            'iframes':0,
            'bullet_cooldown':0
            }

    # -- not frame independent
    def update_timers(self):
        for t in self.timer:
            self.timer[t] = max(0,self.timer[t]-1)

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.DESTROY = True

    def get_bullets(self):
        bullet_list = self.bullets.copy()
        self.bullets.clear()
        return bullet_list
    
    def shoot_bullet(self,x,y,angle,speed,num=1):
        for i in range(num):
            bullet = pygame.Surface((8,8))
            bullet.fill((255,255,255))
            bullet = b.Bullet(bullet, x, y, angle+((1/num)*2*math.pi*i), speed)
            self.bullets.append(bullet)

    def update(self, dT):
        self.update_timers()
        self.y_cor += 1 * dT

        if self.y_cor > 390:
             self.y_cor = -10
             self.x_cor = random.random()*248
        
        if self.timer['bullet_cooldown'] <= 0:
            self.shoot_bullet(self.x_cor+8,self.y_cor+6,0,4,1)
            self.timer['bullet_cooldown'] = 10