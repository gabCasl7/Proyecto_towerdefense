import pygame
import math
from settings import PATH, BLACK

class Enemy:
    def __init__(self):
        self.path = PATH
        self.path_index = 0
        self.x, self.y = self.path[0]
        # Variables de velocidad inteligente
        self.base_speed = 2.0
        self.current_speed = self.base_speed
        
        self.max_hp = 45
        self.hp = self.max_hp
        self.reward = 5  # ORO REDUCIDO (antes 10)
        self.active = True
        self.color = (200, 50, 50) 
        self.radius = 12

    def move(self):
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            dx, dy = target_x - self.x, target_y - self.y
            dist = math.hypot(dx, dy)
            
            # --- INTELIGENCIA DE MOVIMIENTO ---
            # Si están a menos de 40 píxeles del siguiente punto (una curva), frenan.
            # Si están lejos (una recta), aceleran.
            if dist < 40:
                self.current_speed = self.base_speed * 0.6  # Frena en la curva
            else:
                self.current_speed = self.base_speed * 1.3  # Acelera en la recta

            if dist < self.current_speed:
                self.path_index += 1
            else:
                self.x += (dx / dist) * self.current_speed
                self.y += (dy / dist) * self.current_speed
        else:
            self.active = False # Llega a la base

    def draw(self, surface):
        # Dibujar cuerpo con borde
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius + 2)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Barra de vida
        health_ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, (255, 0, 0), (self.x - 15, self.y - 25, 30, 6))
        pygame.draw.rect(surface, (0, 255, 0), (self.x - 15, self.y - 25, 30 * health_ratio, 6))
        pygame.draw.rect(surface, BLACK, (self.x - 15, self.y - 25, 30, 6), 1)

class FastEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.base_speed = 3.0
        self.current_speed = self.base_speed
        self.max_hp = 25 
        self.hp = self.max_hp
        self.reward = 8  # ORO REDUCIDO (antes 15)
        self.color = (255, 165, 0) # Naranja
        self.radius = 10

class TankEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.base_speed = 1.0# Muy lento
        self.current_speed = self.base_speed
        self.max_hp = 120 # Mucha vida
        self.hp = self.max_hp
        self.reward = 15 # ORO REDUCIDO (antes 30)
        self.color = (100, 100, 100) # Gris oscuro
        self.radius = 18