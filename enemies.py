import pygame
import math
from settings import PATH, BLACK

class Enemy:
    def __init__(self):
        self.path = PATH
        self.path_index = 0
        self.x, self.y = self.path[0]
        self.base_speed = 1.5
        self.current_speed = self.base_speed
        
        self.max_hp = 30
        self.hp = self.max_hp
        self.reward = 5  
        self.active = True
        self.color = (200, 50, 50) 
        self.radius = 12

    def move(self, towers): # <-- ¡Ahora recibe la lista de torres!
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            dx, dy = target_x - self.x, target_y - self.y
            dist = math.hypot(dx, dy)
            
            # --- INTELIGENCIA ARTIFICIAL DE MOVIMIENTO ---
            # 1. Comprobar si hay una torre cerca para "huir"
            near_tower = False
            for tower in towers:
                # Si está dentro del rango de disparo de alguna torre (o a punto de entrar)
                if math.hypot(tower.x - self.x, tower.y - self.y) <= tower.range + 15:
                    near_tower = True
                    break # Solo necesitamos detectar una torre para acelerar
            
            if near_tower:
                # ¡Acelera al 180% de su velocidad para escapar!
                self.current_speed = self.base_speed * 1.8 
            elif dist < 40:
                # Frena en las curvas si no hay peligro inmediato
                self.current_speed = self.base_speed * 0.6  
            else:
                # Velocidad normal en rectas
                self.current_speed = self.base_speed * 1.3  

            if dist < self.current_speed:
                self.path_index += 1
            else:
                self.x += (dx / dist) * self.current_speed
                self.y += (dy / dist) * self.current_speed
        else:
            self.active = False # Llega a la base

    def draw(self, surface):
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius + 2)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        
        health_ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, (255, 0, 0), (self.x - 15, self.y - 25, 30, 6))
        pygame.draw.rect(surface, (0, 255, 0), (self.x - 15, self.y - 25, 30 * health_ratio, 6))
        pygame.draw.rect(surface, BLACK, (self.x - 15, self.y - 25, 30, 6), 1)

class FastEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.base_speed = 3.0
        self.current_speed = self.base_speed
        self.max_hp = 15
        self.hp = self.max_hp
        self.reward = 8  
        self.color = (255, 165, 0) 
        self.radius = 10

class TankEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.base_speed = 0.8 
        self.current_speed = self.base_speed
        self.max_hp = 120 
        self.hp = self.max_hp
        self.reward = 15 
        self.color = (100, 100, 100) 
        self.radius = 18