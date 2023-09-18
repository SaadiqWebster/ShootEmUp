import pygame,math

class Object:
    def __init__(self,x,y,width,height):
        self.x_cor = float(x)
        self.y_cor = float(y)
        self.rect = pygame.Rect(self.x_cor,self.y_cor,width,height)
        self.DESTROY = False

        self.animation_database = {}
        self.animation_play = 'LOOP'
        self.animation_offset = [0,0]
        self.current_animation = ''
        self.current_frame = 0
        self.flip = False
        self.alpha = 255

    # normalizes a passed in vector, scales the normalized vector by the speed value
    def normalize(self, vector, speed=1):
        normal = [0]*len(vector)
        if vector != [0,0] and vector != [0,0,0]:
            magnitude = math.sqrt(vector[0]**2 + vector[1]**2)
            normal = [(vector[i] / magnitude) * speed for i in range(len(vector))] 
        return normal
    
    def load_animation(self, database, id_list):
        animation_database = {}
        for animation_id in id_list:
            animation_database[animation_id] = database[animation_id]
        if animation_database:
            self.set_animation(id_list[0])
        return animation_database

    def set_animation(self, animation, frame=0, play_type='LOOP'):
        self.current_frame = frame
        self.animation_play = play_type
        self.current_animation = animation

    def update_animation(self):
        if self.animation_database and self.current_animation != '' and self.animation_play != 'STOP':
            if self.animation_play == 'ONCE':
                self.current_frame = min(self.current_frame+1, len(self.animation_database[self.current_animation])-1)
            elif self.animation_play == 'LOOP':
                self.current_frame = (self.current_frame + 1) % len(self.animation_database[self.current_animation])

    # this should be called before testing collisions
    def set_position(self):
        self.rect.x,self.rect.y = self.x_cor,self.y_cor
    
    # test collisions before updating the object
    def update(self):
        pass
    
    def draw(self):
        frame = pygame.Surface(self.rect.size)
        if self.animation_database and self.current_animation != '':
            frame = pygame.transform.flip(self.animation_database[self.current_animation][self.current_frame], self.flip, False)
            frame.set_alpha(self.alpha)
        else:
            frame.set_alpha(0)
        return frame
        #return self.rect
    
