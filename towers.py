# towers.py
import pygame
import math
from settings import WHITE

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 130
        self.damage = 10
        self.cooldown = 40
        self.timer = 0
        self.cost = 50
        self.color = (50, 150, 255)
        self.laser_target = None
        self.laser_timer = 0 # Para animar el disparo

    def draw(self, surface):
        # Dibujar base
        pygame.draw.rect(surface, (40, 40, 40), (self.x-15, self.y-15, 30, 30), border_radius=5)
        pygame.draw.circle(surface, self.color, (self.x, self.y), 12)
        
        # Efecto visual de láser
        if self.laser_timer > 0 and self.laser_target:
            pygame.draw.line(surface, (0, 255, 255), (self.x, self.y), self.laser_target, 3)
            self.laser_timer -= 1

        # Si el mouse está encima, mostrar el rango
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
                self.laser_timer = 5 # El láser dura 5 frames
                break

class SniperTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 280
        self.damage = 35
        self.cooldown = 100
        self.cost = 100
        self.color = (180, 50, 255) # Morado
        
    def draw(self, surface):
        super().draw(surface)
        if self.laser_timer > 0 and self.laser_target:
            # El francotirador tiene un láser rojo más grueso
            pygame.draw.line(surface, (255, 0, 0), (self.x, self.y), self.laser_target, 4)
