import pygame,math
import bullets as b
from objects import Object

class SubShip(Object):
    def __init__(self,x,y):
        super().__init__(x,y,10,10)

    def update(self, x_pos, y_pos):
        self.x_cor += (x_pos-self.x_cor) / 3
        self.y_cor += (y_pos-self.y_cor) / 3
        self.set_position()

class PlayerShip(Object):
    def __init__(self,x,y, player_id, pos_limit, animation_database):
        super().__init__(x,y,20,20)
        self.spawn_pos = [float(x),float(y)]
        self.pos_limit = pos_limit
        self.player_id = player_id
        self.bullets = []
        self.subships = []
        self.subship_offsets = [(-13,17),(23,17),(-26,21),(36,21)]
        self.score = 0
        self.lives = 2
        self.exp = 0
        self.level = 1
        self.meter = 0
        self.bombs = 3
        self.state = 'SPAWN'
        self.timer = {
            'iframes':0,
            'bullet_cooldown':0,
            'spawn':30,
            'despawn':0
            }
        self.animation_list = ['bird_animation']
        self.animation_database = self.load_animation(animation_database,self.animation_list)
        self.animation_offset = [2,2]

    def increase_exp(self, amount):
        if self.level < 3:
            self.exp += amount
            if self.exp >= 20:
                self.exp = 0
                self.level += 1
                self.subships.append(SubShip(self.x_cor,self.y_cor))
                self.subships.append(SubShip(self.x_cor,self.y_cor))
    
    def get_bullets(self):
        bullet_list = self.bullets.copy()
        self.bullets.clear()
        return bullet_list

    def shoot_bullet(self,x,y):
        bullet = b.Bullet(x,y,math.pi,32)
        self.bullets.append(bullet)

    def set_position(self):
        if self.state == 'ACTIVE':
            self.x_cor = float(min(max(0, self.x_cor), self.pos_limit[0]-self.rect.width))
            self.y_cor = float(min(max(0, self.y_cor), self.pos_limit[1]-self.rect.height))
        super().set_position()

    def update_timers(self, dT):
        for t in self.timer:
            self.timer[t] = max(0,self.timer[t]-1*dT) # this dT multiplication might not be correct :/
        #print(self.timer)

    def read_input(self, _input, dT):
        vel = [0,0]
        movement_speed = 2.5 * dT
        if _input["up"]:
            vel[1] = -1
        if _input["down"]:
            vel[1] = 1
        if _input["left"]:
            vel[0] = -1
        if _input["right"]:
            vel[0] = 1    
        
        vel = self.normalize(vel, movement_speed)
        self.x_cor += vel[0]
        self.y_cor += vel[1]

        if _input["shoot 2"]:
            self.subship_offsets = [(3,-8),(12,-8),(-6,-8),(21,-8)]
        elif _input["shoot 1"]:
            self.subship_offsets = [(-13,17),(23,17),(-26,21),(36,21)]
        else:
            self.subship_offsets = [(-12,17),(21,17),(-20,21),(29,21)]
            
        if (_input["shoot 1"] or _input["shoot 2"] or _input["shoot 3"]) and self.timer['bullet_cooldown'] <= 0:
                self.shoot_bullet(self.x_cor+8,self.y_cor-6)
                for subship in self.subships:
                    self.shoot_bullet(subship.x_cor+2,subship.y_cor-6)
                self.timer['bullet_cooldown'] = 2

    def update(self, _input, collisions, dT):
        self.update_timers(dT)

        if self.state == 'SPAWN':
            if self.timer['spawn'] <= 0:
                self.state = 'ACTIVE'
                self.timer['iframes'] = 60
            else:
                self.y_cor -= 3 * dT

        if self.state == 'ACTIVE':
            if len(collisions) > 0 and self.timer['iframes'] <= 0:
                self.lives -= 1
                self.level = 1
                self.exp = 0
                self.meter = 0
                self.subships.clear()
                self.x_cor = self.spawn_pos[0]
                self.y_cor = self.spawn_pos[1]
                self.state = 'DESPAWN'
                self.timer['despawn'] = 60

            elif len(_input) > 0:
                self.read_input(_input, dT)
        
        if self.state == 'DESPAWN':
            if self.lives >= 0 and self.timer['despawn'] <= 0:
                self.state = 'SPAWN'
                self.timer['spawn'] = 30

        for i in range(len(self.subships)):
            self.subships[i].update(self.x_cor+self.subship_offsets[i][0],self.y_cor+self.subship_offsets[i][1])

        self.update_animation()