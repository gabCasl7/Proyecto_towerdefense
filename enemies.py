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

    def move(self, towers):
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            dx, dy = target_x - self.x, target_y - self.y
            dist = math.hypot(dx, dy)
            
            near_tower = False
            for tower in towers:
                if math.hypot(tower.x - self.x, tower.y - self.y) <= tower.range + 15:
                    near_tower = True
                    break 
            
            if near_tower: self.current_speed = self.base_speed * 1.8 
            elif dist < 40: self.current_speed = self.base_speed * 0.6  
            else: self.current_speed = self.base_speed * 1.3  

            if dist < self.current_speed:
                self.path_index += 1
            else:
                self.x += (dx / dist) * self.current_speed
                self.y += (dy / dist) * self.current_speed
        else:
            self.active = False 

    def draw(self, surface):
        # DIBUJO DE SOLDADITO BÁSICO
        # Cuerpo y mochila
        pygame.draw.rect(surface, (30, 80, 30), (self.x-8, self.y-8, 16, 16), border_radius=3)
        pygame.draw.rect(surface, (80, 60, 40), (self.x-10, self.y-5, 4, 10)) # Mochila
        # Cabeza (Casco)
        pygame.draw.circle(surface, (50, 100, 50), (int(self.x+2), int(self.y)), 6)
        pygame.draw.circle(surface, (255, 200, 150), (int(self.x+4), int(self.y)), 3) # Cara
        
        self.draw_health(surface)

    def draw_health(self, surface):
        health_ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, (255, 0, 0), (self.x - 15, self.y - 20, 30, 4))
        pygame.draw.rect(surface, (0, 255, 0), (self.x - 15, self.y - 20, 30 * health_ratio, 4))

class FastEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.base_speed = 3.0
        self.current_speed = self.base_speed
        self.max_hp = 15
        self.hp = self.max_hp
        self.reward = 8  

    def draw(self, surface):
        # DIBUJO DE SCOUT / BUGGY LIGERO
        # Llantas negras
        pygame.draw.rect(surface, BLACK, (self.x-10, self.y-12, 6, 6))
        pygame.draw.rect(surface, BLACK, (self.x+4, self.y-12, 6, 6))
        pygame.draw.rect(surface, BLACK, (self.x-10, self.y+6, 6, 6))
        pygame.draw.rect(surface, BLACK, (self.x+4, self.y+6, 6, 6))
        # Chasis amarillo
        pygame.draw.rect(surface, (255, 200, 0), (self.x-8, self.y-10, 16, 20), border_radius=2)
        pygame.draw.rect(surface, (100, 150, 255), (self.x-4, self.y-5, 8, 8)) # Parabrisas
        
        self.draw_health(surface)

class TankEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.base_speed = 0.8 
        self.current_speed = self.base_speed
        self.max_hp = 120 
        self.hp = self.max_hp
        self.reward = 15 

    def draw(self, surface):
        # DIBUJO DE TANQUE PESADO
        # Orugas grises
        pygame.draw.rect(surface, (50, 50, 50), (self.x-15, self.y-18, 30, 8), border_radius=2)
        pygame.draw.rect(surface, (50, 50, 50), (self.x-15, self.y+10, 30, 8), border_radius=2)
        # Chasis central oscuro
        pygame.draw.rect(surface, (80, 90, 80), (self.x-12, self.y-14, 24, 28))
        # Torreta verde oscura
        pygame.draw.circle(surface, (40, 60, 40), (int(self.x), int(self.y)), 10)
        pygame.draw.rect(surface, (30, 30, 30), (self.x+5, self.y-3, 15, 6)) # Cañón
        
        self.draw_health(surface)