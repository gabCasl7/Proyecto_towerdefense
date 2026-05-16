import pygame
import math 
import random
from enemies import Enemy, FastEnemy, TankEnemy
from towers import Tower, SniperTower
from settings import *

class GameManager:
    def __init__(self):
        self.reset_game()
        self.map_surface = self.create_textured_map()

    def create_textured_map(self):
        """Genera un fondo con texturas de pasto y arena procedimental"""
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.fill(BG_COLOR)
        
        # 1. Textura de pasto (dibujamos 2000 hojitas)
        for _ in range(2000):
            x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
            pygame.draw.line(surface, GRASS_DARK, (x, y), (x, y-random.randint(2,6)), 2)

        # 2. Dibujar camino base
        pygame.draw.lines(surface, (150, 120, 80), False, PATH, 48)
        pygame.draw.lines(surface, PATH_COLOR, False, PATH, 40)
        
        # 3. Textura del camino (Piedrecitas y tierra)
        for _ in range(800):
            p_idx = random.randint(0, len(PATH)-2)
            x1, y1 = PATH[p_idx]
            x2, y2 = PATH[p_idx+1]
            
            # Punto aleatorio entre los dos nodos
            t = random.random()
            rx = x1 + (x2 - x1) * t + random.randint(-16, 16)
            ry = y1 + (y2 - y1) * t + random.randint(-16, 16)
            
            pygame.draw.circle(surface, DIRT_COLOR, (int(rx), int(ry)), random.randint(1, 3))

        # 4. Base Militar mejorada
        base_x, base_y = PATH[-1]
        pygame.draw.rect(surface, (80, 80, 80), (base_x-25, base_y-35, 50, 70), border_radius=5)
        pygame.draw.rect(surface, (50, 50, 50), (base_x-20, base_y-30, 40, 60))
        # Radar en la base
        pygame.draw.circle(surface, (100, 150, 255), (base_x, base_y-15), 12)
        pygame.draw.line(surface, WHITE, (base_x, base_y-15), (base_x+10, base_y-25), 2)
        
        return surface

    def reset_game(self):
        self.money = START_MONEY
        self.lives = START_LIVES
        self.wave = 1
        self.enemies = []
        self.towers = []
        self.enemies_to_spawn = 5
        self.spawn_timer = 0

    def is_valid_position(self, x, y):
        if y < 65: return False
        path_margin = 35  
        for i in range(len(PATH) - 1):
            x1, y1 = PATH[i]
            x2, y2 = PATH[i+1]
            min_x, max_x = min(x1, x2) - path_margin, max(x1, x2) + path_margin
            min_y, max_y = min(y1, y2) - path_margin, max(y1, y2) + path_margin
            if min_x <= x <= max_x and min_y <= y <= max_y: return False  
        for tower in self.towers:
            if math.hypot(tower.x - x, tower.y - y) < 30: return False  
        return True  

    def add_tower(self, x, y, tower_type):
        if not self.is_valid_position(x, y): return  
        if tower_type == "BASIC" and self.money >= 50:
            self.towers.append(Tower(x, y))
            self.money -= 50
        elif tower_type == "SNIPER" and self.money >= 100:
            self.towers.append(SniperTower(x, y))
            self.money -= 100

    def update(self):
        if self.enemies_to_spawn > 0:
            self.spawn_timer += 1
            if self.spawn_timer >= 50: 
                if self.wave % 2 == 0 and self.enemies_to_spawn % 4 == 0: self.enemies.append(TankEnemy()) 
                elif self.enemies_to_spawn % 3 == 0: self.enemies.append(FastEnemy())
                else: self.enemies.append(Enemy())
                self.enemies_to_spawn -= 1
                self.spawn_timer = 0
                
        elif len(self.enemies) == 0 and self.enemies_to_spawn == 0:
            if self.wave >= WIN_WAVE: return "WIN"
            else:
                self.wave += 1
                self.enemies_to_spawn = 5 + (self.wave * 4)

        for enemy in self.enemies[:]:
            enemy.move(self.towers)
            if not enemy.active:
                self.lives -= 1
                self.enemies.remove(enemy)
                if self.lives <= 0: return "GAME_OVER"
            elif enemy.hp <= 0:
                self.money += enemy.reward
                self.enemies.remove(enemy)

        for tower in self.towers:
            tower.update(self.enemies)
            
        return "PLAYING"

    def draw(self, surface, font):
        # Dibuja la textura generada ultrarrápido
        surface.blit(self.map_surface, (0, 0))

        for tower in self.towers: tower.draw(surface)
        for enemy in self.enemies: enemy.draw(surface)

        pygame.draw.rect(surface, UI_BG, (0, 0, WIDTH, 65))
        pygame.draw.line(surface, BLACK, (0, 65), (WIDTH, 65), 3)
        ui_text = font.render(f"❤️ Vidas: {self.lives}       💰 Oro: ${self.money}       ⚔️ Oleada: {self.wave}/{WIN_WAVE}", True, WHITE)
        surface.blit(ui_text, (20, 10))
        info_text = font.render("Controles: Click Izq -> Torre Básica ($50)  |  Click Der -> Francotirador ($100)", True, (200, 200, 200))
        surface.blit(info_text, (20, 38))