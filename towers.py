import pygame
import math
from settings import WHITE, BLACK

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 130
        self.damage = 10
        self.cooldown = 40
        self.timer = 0
        self.cost = 50
        self.laser_target = None
        self.laser_timer = 0 

    def draw(self, surface):
        # 1. Base de la torre (Forma de castillo de piedra)
        pygame.draw.rect(surface, (80, 80, 80), (self.x-15, self.y-15, 30, 30)) 
        pygame.draw.rect(surface, (60, 60, 60), (self.x-15, self.y+5, 30, 10))  
        pygame.draw.rect(surface, (100, 100, 100), (self.x-15, self.y-20, 8, 10))
        pygame.draw.rect(surface, (100, 100, 100), (self.x-4, self.y-20, 8, 10))
        pygame.draw.rect(surface, (100, 100, 100), (self.x+7, self.y-20, 8, 10))
        
        # Centro 
        pygame.draw.circle(surface, (40, 40, 40), (self.x, self.y), 8)

        # 2. Efecto visual de láser y cañón
        if self.laser_timer > 0 and self.laser_target:
            pygame.draw.line(surface, (200, 200, 200), (self.x, self.y), (self.x + (self.laser_target[0]-self.x)*0.3, self.y + (self.laser_target[1]-self.y)*0.3), 4)
            pygame.draw.line(surface, (0, 255, 255), (self.x, self.y), self.laser_target, 2)
            self.laser_timer -= 1

        # Rango
        mouse_pos = pygame.mouse.get_pos()
        if math.hypot(mouse_pos[0] - self.x, mouse_pos[1] - self.y) < 15:
            pygame.draw.circle(surface, WHITE, (self.x, self.y), self.range, 1)

    def update(self, enemies):
        if self.timer > 0:
            self.timer -= 1
            return
            
        for enemy in enemies:
            if math.hypot(enemy.x - self.x, enemy.y - self.y) <= self.range:
                enemy.hp -= self.damage
                self.timer = self.cooldown
                self.laser_target = (int(enemy.x), int(enemy.y))
                self.laser_timer = 5 
                break

class SniperTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 280
        self.damage = 35
        self.cooldown = 100
        self.cost = 100
        
    def draw(self, surface):
        # Base circular futurista
        pygame.draw.circle(surface, (50, 50, 50), (self.x, self.y), 16)
        pygame.draw.circle(surface, (100, 50, 150), (self.x, self.y), 12) 
        pygame.draw.polygon(surface, (180, 180, 180), [(self.x, self.y-5), (self.x-5, self.y+5), (self.x+5, self.y+5)])
        
        if self.laser_timer > 0 and self.laser_target:
            pygame.draw.line(surface, (255, 0, 0), (self.x, self.y), self.laser_target, 3)
            self.laser_timer -= 1
            
        mouse_pos = pygame.mouse.get_pos()
        if math.hypot(mouse_pos[0] - self.x, mouse_pos[1] - self.y) < 15:
            pygame.draw.circle(surface, (255, 100, 100), (self.x, self.y), self.range, 1)
