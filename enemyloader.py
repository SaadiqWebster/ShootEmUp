import enemies as e

class EnemyLoader():
    def __init__(self, enemy_chart):
        self.timer = 0
        self.trigger_stack = []
        self.enemy_stack = []
        self.load_enemy_chart(enemy_chart)

    def load_enemy_chart(self, chart):
        for trigger in chart:            
            enemy = None
            attributes = chart[trigger]
            
            if attributes[0] == "enemy":
                enemy = e.Enemy(attributes[1],attributes[2])

            self.enemy_stack.append(enemy)
            self.trigger_stack.append(int(trigger))

    def update(self):
        self.timer += 1

    def pop(self):
        enemy_spawn = []
        while len(self.trigger_stack) > 0 and self.timer >= self.trigger_stack[0]:
            self.trigger_stack.pop(0)
            enemy_spawn.append(self.enemy_stack.pop(0))
        return enemy_spawn

