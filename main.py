import pygame, math
import engine as e, font as f
import backgrounds as b, hud as h
import player as p, enemyloader as l

engine = e.Engine((160, 284),'Shoot-em-Up', 2)
text = f.Font(engine.get_tileset('font','font_classic'),1)

def MainMenu():
    menuselect = 0
    
    Run = True
    while Run:
        # INPUTS AND EVENTS
        engine.read_events()
        if engine.get_action_press('up') or engine.get_action_press('left'):
            menuselect = (menuselect - 1) % 3
        if engine.get_action_press('down') or engine.get_action_press('right'):
            menuselect = (menuselect + 1) % 3
        if engine.get_action_press("start") or engine.get_action_press("shoot 1"):
            if menuselect == 2:
                Run = False
            elif menuselect == 1:
                Options()
            elif menuselect == 0:
                ShipSelect()

                level = 1
                while level <= 4:
                    LevelIntro(level)
                    Gameplay(level)
                    level += 1

        # UPDATE
        engine.game_update_start()
        
        # DRAW
        options = ['START GAME','OPTIONS','EXIT GAME']
        y_offset = -10
        for i in range(len(options)):
            font_color = (255,255,13) if menuselect == i else (255,255,255)
            engine.game_draw_to_screen(text.draw(options[i], font_color), ((engine.CAMERA_SIZE[0]/2), (engine.CAMERA_SIZE[1]/2)+y_offset), 'center')
            y_offset += 10

        # END
        engine.game_update_end()

def ShipSelect():
    engine.clear_player_list()
    ready_meter = [0]*engine.MAX_PLAYERS

    Run = True
    while Run:
        
        engine.read_events()
        
        for player_id in range(1,engine.MAX_PLAYERS+1):
            if player_id in engine.player_list:
                fill_speed = 1 if len(engine.player_list) < 2 else 1.5
                if engine.get_action('start', player_id):
                    ready_meter[player_id-1] = min(ready_meter[player_id-1]+fill_speed, 100)
                else:
                    ready_meter[player_id-1] = max(ready_meter[player_id-1]-fill_speed, 0)
            else:
                ready_meter[player_id-1] = 0

        engine.game_update_start()
        
        if len(engine.player_list) < 2 and (ready_meter[0] == 100 or ready_meter[1] == 100):
                Run = False
        elif ready_meter[0] == 100 and ready_meter[1] == 100:
                Run = False

        engine.game_draw_to_screen(text.draw('Player 1',(255,255,255)), (engine.CAMERA_SIZE[0]*1/4, (engine.CAMERA_SIZE[1]/2)-10), 'center')
        engine.game_draw_to_screen(text.draw('Player 2',(255,255,255)), (engine.CAMERA_SIZE[0]*3/4, (engine.CAMERA_SIZE[1]/2)-10), 'center')
        
        for i in range(1,engine.MAX_PLAYERS+1):
            x_offset = 0 if i == 1 else engine.CAMERA_SIZE[0]/2
            if i in engine.player_list:
                engine.game_draw_to_screen(text.draw('Ready!', (255,255,13)), (engine.CAMERA_SIZE[0]*1/4+x_offset, (engine.CAMERA_SIZE[1]/2)+5), 'center')
            else:
                engine.game_draw_to_screen(text.draw('Press Any Button', (255,255,255)), (engine.CAMERA_SIZE[0]*1/4+x_offset, (engine.CAMERA_SIZE[1]/2)+5), 'center')
        
        max_width = math.ceil(engine.CAMERA_SIZE[0]*8/10) if len(engine.player_list) < 2 else math.ceil(engine.CAMERA_SIZE[0]*(4/10))
        player1meter_surf = pygame.Surface((max_width*ready_meter[0]/100, 10))
        player2meter_surf = pygame.Surface((max_width*ready_meter[1]/100, 10))
        player1meter_surf.fill((255,255,255))
        player2meter_surf.fill((255,255,255))
        engine.game_draw_to_screen(player1meter_surf, (engine.CAMERA_SIZE[0]*1/10, (engine.CAMERA_SIZE[1]/2)+30), 'left')
        engine.game_draw_to_screen(player2meter_surf, (engine.CAMERA_SIZE[0]*9/10, (engine.CAMERA_SIZE[1]/2)+30), 'right')
        
        engine.game_update_end()
    
    for player_id in engine.player_list:
        if len(engine.player_list) < 2:
            x_offset = 1/2
        elif player_id == 1:
            x_offset = 3/10
        else:
            x_offset = 7/10
        engine.add_object('player_ships', p.PlayerShip((engine.CAMERA_SIZE[0]*x_offset)-10, engine.CAMERA_SIZE[1], player_id, (engine.CAMERA_SIZE[0],engine.CAMERA_SIZE[1]-32), engine.animation_database, engine.tileset_database['tile']))

def Options():
    pass

def LevelIntro(level):
    pass

def Gameplay(level):
    enemyloader = l.EnemyLoader(engine.load_config('levelchart_lvl'+str(level)+'.json'))
    background = b.SkyBackground(engine.CAMERA_SIZE,engine.tileset_database)
    hud = h.Hud(engine.CAMERA_SIZE, text)

    Run = True
    while Run:
        # INPUTS & EVENTS
        engine.read_events()

        # UPDATE
        enemyloader.update()
        enemy_spawn = enemyloader.pop()
        engine.add_objects('enemies', enemy_spawn)

        engine.game_update_start()
        engine.game_update_objects()

        background.update()

        # DRAW
        engine.game_draw_to_screen(background.draw(),(0,0))
        engine.game_draw_objects()
        engine.game_draw_to_screen(hud.draw(engine.obj_list['player_ships']),(0,0))


        # END
        engine.game_update_end()



if __name__ == "__main__":
    MainMenu()
    engine.quit_game()

