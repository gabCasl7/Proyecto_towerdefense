# enemies.py
import pygame
import math
from settings import PATH, BLACK

class Enemy:
    def __init__(self):
        self.path = PATH
        self.path_index = 0
        self.x, self.y = self.path[0]
        self.speed = 1.5
        self.max_hp = 30
        self.hp = self.max_hp
        self.reward = 10
        self.active = True
        self.color = (200, 50, 50) 
        self.radius = 12

    def move(self):
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            dx, dy = target_x - self.x, target_y - self.y
            dist = math.hypot(dx, dy)
            
            if dist < self.speed:
                self.path_index += 1
            else:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed
        else:
            self.active = False # Llega a la base

    def draw(self, surface):
        # Dibujar cuerpo con borde
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius + 2)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Barra de vida bonita
        health_ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, (255, 0, 0), (self.x - 15, self.y - 25, 30, 6))
        pygame.draw.rect(surface, (0, 255, 0), (self.x - 15, self.y - 25, 30 * health_ratio, 6))
        pygame.draw.rect(surface, BLACK, (self.x - 15, self.y - 25, 30, 6), 1)

class FastEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.speed = 3.0
        self.max_hp = 15
        self.hp = self.max_hp
        self.reward = 15
        self.color = (255, 165, 0) # Naranja
        self.radius = 10

class TankEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.speed = 0.8 # Muy lento
        self.max_hp = 120 # Mucha vida
        self.hp = self.max_hp
        self.reward = 30
        self.color = (100, 100, 100) # Gris oscuro
        self.radius = 18