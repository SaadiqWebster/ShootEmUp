import pygame,os,sys,json,time

class Player_Input:
        def __init__(self, instance_id, input_map):
            self.instance_id = instance_id
            self.button_state = [False]*19
            self.button_press = [False]*19

            self.input_map = input_map
            self.action_list = self.get_list_of_actions(self.input_map)
            self.action_state = self.action_list.copy()
            self.action_press = self.action_list.copy()
        
        def get_list_of_actions(self, input_map):
            action_list = {}
            for button in input_map:
                action = input_map[button]
                if action not in action_list:
                    action_list[action] = False
            return action_list
        
        def clear_press_input(self):
            self.button_press = [False]*len(self.button_state)
            self.action_press = self.action_list.copy()
        
class Engine:
    def __init__(self, CAMERA_SIZE, CAPTION='', MAX_PLAYERS=1):
        # pygame set-up
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.mixer.set_num_channels(300)
        pygame.display.set_caption(CAPTION)
        #pygame.display.set_icon(pygame.image.load(path_to_img))
        pygame.joystick.init()
        self.joysticks = []

        # game set-up
        self.DEBUG = True
        self.CAMERA_SIZE = CAMERA_SIZE
        self.WINDOW_SIZE = CAMERA_SIZE
        self.MAX_PLAYERS = MAX_PLAYERS
        self.PATH_TO_ASSETS = 'assets'
        self.PATH_TO_CONFIG = 'config'
        self.FPS = 60

        self.window = pygame.display.set_mode(self.WINDOW_SIZE, pygame.RESIZABLE)
        self.camera = pygame.Surface(CAMERA_SIZE)
        self.clock = pygame.time.Clock()
        self.clock_last_time = time.time()
        self.clock_dT = 0
        self.settings = {'Window Size':1,'Window Border':1,'Full Screen':0,'Music Volume':5,'Sound Volume':5}
        self.apply_settings()
        self.obj_list = {'player_ships':[],'player_1_bullets':[],'player_2_bullets':[],'enemies':[],'enemy_bullets':[]}
 
        # database set-up
        self.input_map = self.load_config('input_to_button_map.json')
        self.frame_data = self.load_config('frame_data.json')
        self.tileset_database = {}
        self.sound_database = {}
        self.animation_database = {}
        self.load_databases()
        self.joysticks = {}
        self.player_list = {}

    def apply_settings(self):
        pygame.mixer.music.set_volume(self.settings['Music Volume']/10)
        self.WINDOW_SIZE = (self.CAMERA_SIZE[0]*self.settings['Window Size'], self.CAMERA_SIZE[1]*self.settings['Window Size'])
        window_mode = pygame.NOFRAME
        if self.settings['Full Screen'] == 1:
            window_mode = pygame.FULLSCREEN|pygame.SCALED
        elif self.settings['Window Border'] == 1:
            window_mode = pygame.RESIZABLE

        self.main_display = pygame.display.set_mode(self.WINDOW_SIZE, window_mode)

    def load_config(self, file):
        f=open(self.PATH_TO_CONFIG+'/'+file)
        return json.load(f)
    
    def load_databases(self):
        d = os.listdir(self.PATH_TO_ASSETS)
        for directory in d:
            if directory == 'sound':
                self.load_sound_database(self.PATH_TO_ASSETS+'/'+directory)
            elif directory == 'animation':
                self.load_animation_database(self.PATH_TO_ASSETS+'/'+directory, (0,255,0))
            elif directory == 'font':
                self.load_tileset_database(directory)
            else:
                self.load_tileset_database(directory, (0,0,0))

    def load_tileset_database(self, directory, transparent_color=None):
        self.tileset_database[directory] = {}
        f = os.listdir(self.PATH_TO_ASSETS+'/'+directory)
        for file in f:
            asset = pygame.image.load(self.PATH_TO_ASSETS+'/'+directory+'/'+file)
            if transparent_color is not None:
                asset.set_colorkey(transparent_color)
            self.tileset_database[directory][file[:-4]] = asset

    def load_sound_database(self, path):
        d = os.listdir(path)
        for directory in d:
            self.sound_database[directory] = {}
            f = os.listdir(path+'/'+directory)
            for file in f:
                if directory == 'music':
                    self.sound_database[directory][file[:-4]] = path+'/'+directory+'/'+file 
                else:
                    self.sound_database[directory][file[:-4]] = pygame.mixer.Sound(path+'/'+directory+'/'+file)
    
    def load_animation_database(self, path, transparent_color=None):
        f = os.listdir(path)
        for file in f:
            filename = file[:-4]

            spritesheet = pygame.image.load(path+'/'+file)
            frame_data = self.frame_data[filename] if filename in self.frame_data else {}
            animation = []
            
            if frame_data:
                for i in range(len(frame_data['duration'])):
                    frame = self.cut_image(spritesheet, frame_data['size'][0]*i, 0, frame_data['size'][0], frame_data['size'][1])
                    if transparent_color is not None:
                        frame.set_colorkey(transparent_color)
                    for j in range(frame_data['duration'][i]):
                        animation.append(frame)

            self.animation_database[filename] = animation

    def cut_image(self,surf,x,y,width,height):
        surf_copy = surf.copy()
        clip = pygame.Rect(x,y,width,height)
        surf_copy.set_clip(clip)
        cut = surf.subsurface(surf_copy.get_clip())
        return cut.copy()
        
    def play_music(self,sound):
        if 'music' in self.sound_database:
            pygame.mixer.music.load(self.sound_database['music'][sound])
            pygame.mixer.music.set_volume(self.settings['Music Volume']/10)
            pygame.mixer.music.play(-1)
    
    def play_sfx(self,sound):
        if 'sfx' in self.sound_database:
            self.sound_database['sfx'][sound].set_volume(self.settings['Sound Volume']/10)
            self.sound_database['sfx'][sound].play()
    
    def stop_music(self, speed=0):
            if speed > 0:
                pygame.mixer.music.fadeout(speed)
            else:
                pygame.mixer.music.stop()

    def get_tileset(self, asset_type, label):
        return self.tileset_database[asset_type][label]
    
    def get_action(self, action, player_id=-1):
        if player_id in self.player_list:
            return self.player_list[player_id].action_state[action]
        
        for player in self.player_list:
            if self.player_list[player].action_state[action]:
                return True     
        return False
    
    def get_action_press(self, action, player_id=-1):
        if player_id in self.player_list:
            return self.player_list[player_id].action_press[action]
        
        for player in self.player_list:
            if self.player_list[player].action_press[action]:
                return True     
        return False

    def get_button(self, button, player_id=-1):
        if player_id in self.player_list:
            return self.player_list[player_id].button_state[button]
        
        for player in self.player_list:
            if self.player_list[player].button_state[button]:
                return True
        return False

    def get_button_press(self, button, player_id=-1):
        if player_id in self.player_list:
            return self.player_list[player_id].button_press[button]
        
        for player in self.player_list:
            if self.player_list[player].button_press[button]:
                return True
        return False

    def get_player_input(self, instance_id):
        for player_id in self.player_list:
            if self.player_list[player_id].instance_id == instance_id:
                return player_id    
        return -1

    def set_player_input(self, player_id, controller_type, input, val):
        if controller_type in self.input_map and input in self.input_map[controller_type]:
            button = self.input_map[controller_type][input]
    
            self.player_list[player_id].button_state[button] = val
            self.player_list[player_id].button_press[button] = val
            
            if len(self.player_list[player_id].action_list) > 0 and str(button) in self.player_list[player_id].input_map:
                action = self.player_list[player_id].input_map[str(button)]
                self.player_list[player_id].action_state[action] = val
                self.player_list[player_id].action_press[action] = val
     
    def add_player_input(self, instance_id):
        if len(self.player_list) < self.MAX_PLAYERS:
            for player_id in range(1,self.MAX_PLAYERS+1):
                if player_id not in self.player_list:
                    self.player_list[player_id] = Player_Input(instance_id, self.load_config('button_to_action_map.json'))
                    return player_id
        else:
            return -1
    
    def add_object(self, obj_type, obj):
        if obj_type in self.obj_list:
            self.obj_list[obj_type].append(obj)
        else:
            self.obj_list[obj_type] = [obj]

    def add_objects(self, obj_type, _list):
        if obj_type in self.obj_list:
            self.obj_list[obj_type] += _list
        else:
            self.obj_list[obj_type] = _list
    
    def remove_object(self, obj_type, obj):
        if obj_type in self.obj_list:
            self.obj_list[obj_type].remove(obj)
        else:
            print('remove object failed. object type',obj_type,'not in object list.')

    def remove_player_input(self, player_id):
        removed_player = self.player_list.pop(player_id)
        return removed_player

    def clear_player_list(self):
        self.player_list.clear()

    def clear_object_list(self, obj_type):
        if obj_type in self.obj_list:
            self.obj_list[obj_type].clear()
        else:
            print('clear object list failed. object type',obj_type,'not in object list.')

    def test_obj_collision_rect(self, rect, obj_list):
        for obj in obj_list:
            if pygame.Rect.colliderect(rect, obj.rect):
                return obj         
        return None
    
    def test_obj_collision_mask(self, rect, obj_list):
        pass

    def read_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.quit_game()
            
            if event.type == pygame.JOYDEVICEADDED:
                self.joysticks.clear()
                for i in range(pygame.joystick.get_count()):
                    joystick = pygame.joystick.Joystick(i)
                    self.joysticks[joystick.get_instance_id()] = joystick
                print(self.joysticks)
                
            if event.type == pygame.JOYDEVICEREMOVED:
                self.joysticks.clear()
                for i in range(pygame.joystick.get_count()):
                    joystick = pygame.joystick.Joystick(i)
                    self.joysticks[joystick.get_instance_id()] = joystick

                player_id = self.get_player_input(event.instance_id)
                if player_id > 0:
                    self.remove_player_input(player_id)
        
            if event.type == pygame.KEYDOWN:
                key_control_type = 0
                if "Keyboard_1" in self.input_map and pygame.key.name(event.key) in self.input_map["Keyboard_1"]:
                    key_control_type = -1
                elif "Keyboard_2" in self.input_map and pygame.key.name(event.key) in self.input_map["Keyboard_2"]:
                    key_control_type = -2
        
                if key_control_type < 0:
                    player_id = self.get_player_input(key_control_type)
                    if player_id < 0:
                        player_id = self.add_player_input(key_control_type)
                    if player_id > 0:
                        self.set_player_input(player_id,"Keyboard_"+str(key_control_type*-1),pygame.key.name(event.key),True)
            
            if event.type == pygame.KEYUP:
                key_control_type = 0
                if "Keyboard_1" in self.input_map and pygame.key.name(event.key) in self.input_map["Keyboard_1"]:
                    key_control_type = -1
                elif "Keyboard_2" in self.input_map and pygame.key.name(event.key) in self.input_map["Keyboard_2"]:
                    key_control_type = -2

                if key_control_type < 0:
                    player_id = self.get_player_input(key_control_type)
                    if player_id > 0:
                        self.set_player_input(player_id,"Keyboard_"+str(key_control_type*-1),pygame.key.name(event.key),False)

            if event.type == pygame.JOYBUTTONDOWN:
                player_id = self.get_player_input(event.instance_id)
                if player_id < 0:
                        player_id = self.add_player_input(event.instance_id)
                if player_id > 0:
                    self.set_player_input(player_id, self.joysticks[event.instance_id].get_name(), str(event.button), True)
                
            if event.type == pygame.JOYBUTTONUP:
                player_id = self.get_player_input(event.instance_id)
                if player_id > 0:
                    self.set_player_input(player_id, self.joysticks[event.instance_id].get_name(),str(event.button), False)

            if event.type == pygame.JOYAXISMOTION:
                player_id = self.get_player_input(event.instance_id)
                if player_id < 0:
                        player_id = self.add_player_input(event.instance_id)
                if player_id > 0:
                    controller_type = self.joysticks[event.instance_id].get_name()
                    if event.axis == 0:
                        self.set_player_input(player_id,controller_type,"a-left",event.value < -0.5)
                        self.set_player_input(player_id,controller_type,"a-right",event.value > 0.5) 

                    if event.axis == 1:
                        self.set_player_input(player_id,controller_type,"a-down",event.value > 0.5)
                        self.set_player_input(player_id,controller_type,"a-up",event.value < -0.5)

            if event.type == pygame.JOYHATMOTION:
                player_id = self.get_player_input(event.instance_id)
                if player_id < 0:
                        player_id = self.add_player_input(event.instance_id)
                if player_id > 0:
                    controller_type = self.joysticks[event.instance_id].get_name()
                    self.set_player_input(player_id,controller_type,"d-left",event.value[0] < 0)
                    self.set_player_input(player_id,controller_type,"d-right",event.value[0] > 0)
                    self.set_player_input(player_id,controller_type,"d-down",event.value[1] < 0)
                    self.set_player_input(player_id,controller_type,"d-up",event.value[1] > 0)

    def game_update_start(self):
        self.camera.fill((0,0,0))
        self.clock_dT = (time.time() - self.clock_last_time) * 60 # frame-rate independence, movement locked at 60FPS
        self.clock_last_time = time.time()
        for player_id in self.player_list:
            self.player_list[player_id].clear_press_input()

    def game_update_end(self):
        self.window.blit(pygame.transform.scale(self.camera, self.WINDOW_SIZE), ((self.window.get_width()/2)-(self.WINDOW_SIZE[0]/2), (self.window.get_height()/2)-(self.WINDOW_SIZE[1]/2)))
        pygame.display.update()
        self.clock.tick(self.FPS)
   
    def game_update_objects(self):
        for obj_type in self.obj_list:
            for obj in self.obj_list[obj_type]:
                obj.set_position()

                if obj_type == 'player_ships':
                    collisions = {}
                    enemy_collision = self.test_obj_collision_rect(obj.rect,self.obj_list['enemies'])
                    bullet_collision = self.test_obj_collision_rect(obj.rect,self.obj_list['enemy_bullets'])
                    if enemy_collision is not None:
                        self.remove_object('enemies', enemy_collision)
                        collisions['enemies'] = enemy_collision
                    if bullet_collision is not None:
                        self.remove_object('enemy_bullets', bullet_collision)
                        collisions['enemy_bullets'] = bullet_collision    
                    
                    obj.update(self.player_list[obj.player_id].action_state, collisions, self.clock_dT)
                    player_bullets = obj.get_bullets()
                    if player_bullets:
                        self.add_objects('player_'+str(obj.player_id)+'_bullets',player_bullets)
                        #self.play_sound('cursor')

                elif obj_type == 'enemies':
                    for ship in self.obj_list['player_ships']:
                        bullet = self.test_obj_collision_rect(obj.rect,self.obj_list['player_'+str(ship.player_id)+'_bullets'])
                        if bullet is not None:
                            self.remove_object('player_'+str(ship.player_id)+'_bullets', bullet)
                            obj.hit(bullet.damage)
                            ship.increase_exp(bullet.damage)
                    
                    obj.update(self.clock_dT)
                    self.add_objects('enemy_bullets',obj.get_bullets())
                else:
                    obj.update(self.clock_dT)

                if obj.rect.x < 0 - (self.CAMERA_SIZE[0]/2) or obj.rect.x > self.CAMERA_SIZE[0] + (self.CAMERA_SIZE[0]/2) or obj.rect.y < 0 - (self.CAMERA_SIZE[1]/4) or obj.rect.y > self.CAMERA_SIZE[1] + (self.CAMERA_SIZE[1]/4):
                    obj.DESTROY = True

                if obj.DESTROY:
                    self.remove_object(obj_type, obj)

    def game_draw_objects(self):
        for obj_type in self.obj_list:
            for obj in self.obj_list[obj_type]:
                self.game_draw_to_screen(obj.draw(), (obj.rect.x+obj.animation_offset[0], obj.rect.y+obj.animation_offset[1]))
                if obj_type == 'player_ships':
                    for subship in obj.subships:
                        self.game_draw_to_screen(subship.draw(), (subship.rect.x+subship.animation_offset[0], subship.rect.y+subship.animation_offset[1]))
                        # eventually you can comment or delete this if statement, since subships do nothing on collision it is not needed to display
                        if self.DEBUG:
                            rect_color = (0,255,255)
                            pygame.draw.rect(self.camera,rect_color,subship.rect)

                if self.DEBUG:
                    rect_color = (255,255,255)
                    if obj_type == 'player_ships':
                        rect_color = (0,255,0)
                    if obj_type == 'player_0_bullets' or obj_type == 'player_1_bullets':
                        rect_color = (255,255,0)
                    if obj_type == 'enemies':
                        rect_color = (255,0,0)    
                    if obj_type == 'enemy_bullets':
                        rect_color = (255,0,0)
                    pygame.draw.rect(self.camera,rect_color,obj.rect,1)

    def game_draw_to_screen(self, surf, cor, justification='left'):
        if justification == 'left':
            self.camera.blit(surf,cor)
        if justification == 'right':
            self.camera.blit(surf, (cor[0]-surf.get_width(), cor[1]))
        if justification == 'center':
            self.camera.blit(surf, (cor[0]-surf.get_width()/2, cor[1]-surf.get_height()/2))

    def quit_game(self):
            pygame.quit()
            sys.exit()
        