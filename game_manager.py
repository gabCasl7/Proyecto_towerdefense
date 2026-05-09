# game_manager.py
import pygame
from enemies import Enemy, FastEnemy, TankEnemy
from towers import Tower, SniperTower
from settings import *

class GameManager:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.money = START_MONEY
        self.lives = START_LIVES
        self.wave = 1
        self.enemies = []
        self.towers = []
        self.enemies_to_spawn = 5
        self.spawn_timer = 0

    def add_tower(self, x, y, tower_type):
        # Evitar construir sobre el panel superior
        if y < 50: return 
        
        if tower_type == "BASIC" and self.money >= 50:
            self.towers.append(Tower(x, y))
            self.money -= 50
        elif tower_type == "SNIPER" and self.money >= 100:
            self.towers.append(SniperTower(x, y))
            self.money -= 100

    def update(self):
        # 1. Spawner de enemigos
        if self.enemies_to_spawn > 0:
            self.spawn_timer += 1
            if self.spawn_timer >= 50: 
                # Lógica de oleadas
                if self.wave % 2 == 0 and self.enemies_to_spawn % 4 == 0:
                    self.enemies.append(TankEnemy()) # Sale un tanque de vez en cuando en oleadas pares
                elif self.enemies_to_spawn % 3 == 0:
                    self.enemies.append(FastEnemy())
                else:
                    self.enemies.append(Enemy())
                self.enemies_to_spawn -= 1
                self.spawn_timer = 0
                
        elif len(self.enemies) == 0 and self.enemies_to_spawn == 0:
            if self.wave >= WIN_WAVE:
                return "WIN"
            else:
                self.wave += 1
                self.enemies_to_spawn = 5 + (self.wave * 4)

        # 2. Actualizar entidades
        for enemy in self.enemies[:]:
            enemy.move()
            if not enemy.active:
                self.lives -= 1
                self.enemies.remove(enemy)
                if self.lives <= 0:
                    return "GAME_OVER"
            elif enemy.hp <= 0:
                self.money += enemy.reward
                self.enemies.remove(enemy)

        for tower in self.towers:
            tower.update(self.enemies)
            
        return "PLAYING"

    def draw(self, surface, font):
        # Dibujar Camino con borde
        pygame.draw.lines(surface, (150, 120, 80), False, PATH, 46)
        pygame.draw.lines(surface, PATH_COLOR, False, PATH, 40)
        
        # Dibujar "Base" al final del camino
        base_x, base_y = PATH[-1]
        pygame.draw.rect(surface, (80, 80, 80), (base_x-20, base_y-30, 40, 60))
        pygame.draw.polygon(surface, (50, 50, 200), [(base_x-25, base_y-30), (base_x+25, base_y-30), (base_x, base_y-50)])

        for tower in self.towers:
            tower.draw(surface)
            
        for enemy in self.enemies:
            enemy.draw(surface)

        # Dibujar Panel Superior (UI)
        pygame.draw.rect(surface, UI_BG, (0, 0, WIDTH, 45))
        pygame.draw.line(surface, BLACK, (0, 45), (WIDTH, 45), 3)
        
        ui_text = font.render(f"❤️ Vidas: {self.lives}  |  💰 Oro: ${self.money}  |  ⚔️ Oleada: {self.wave}/{WIN_WAVE}", True, WHITE)
        surface.blit(ui_text, (15, 12))
        
        info_text = font.render("Click Izq: Torre Básica ($50) | Click Der: Francotirador ($100)", True, (200, 200, 200))
        surface.blit(info_text, (WIDTH - 550, 12))