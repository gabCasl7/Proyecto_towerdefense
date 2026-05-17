import pygame
import sys
import random
from game_manager import GameManager
from ui import Button
from settings import WIDTH, HEIGHT, FPS, BG_COLOR, MENU_BG, WHITE

def draw_menu_background(surface):
    """Ilustración de fondo para el menú principal"""
    surface.fill(MENU_BG)
    # Estrellas en el fondo
    for _ in range(50):
        pygame.draw.circle(surface, (150, 150, 150), (random.randint(0, WIDTH), random.randint(0, HEIGHT)), 1)
        
    # Silueta de un castillo gigante a la izquierda
    pygame.draw.rect(surface, (15, 20, 35), (50, HEIGHT-200, 150, 200))
    pygame.draw.rect(surface, (15, 20, 35), (30, HEIGHT-250, 40, 60))
    pygame.draw.rect(surface, (15, 20, 35), (180, HEIGHT-250, 40, 60))
    
    # Siluetas de tanques atacando a la derecha
    pygame.draw.rect(surface, (30, 20, 20), (WIDTH-200, HEIGHT-60, 80, 30), border_radius=5)
    pygame.draw.rect(surface, (30, 20, 20), (WIDTH-170, HEIGHT-70, 40, 20))
    pygame.draw.line(surface, (30, 20, 20), (WIDTH-170, HEIGHT-65), (WIDTH-220, HEIGHT-80), 6)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tower Defense Pro - Proyecto POO")
    clock = pygame.time.Clock()
    
    font_title = pygame.font.SysFont("Consolas", 55, bold=True)
    font_ui = pygame.font.SysFont("Consolas", 16, bold=True)

    game = GameManager()
    
    btn_start = Button(WIDTH//2 - 100, HEIGHT//2 - 20, 200, 50, "JUGAR", (50, 150, 50), (80, 200, 80))
    btn_quit = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50, "SALIR", (200, 50, 50), (255, 80, 80))
    btn_restart = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50, "REINICIAR", (50, 100, 200), (80, 150, 255))

    state = "MENU" 
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if state == "MENU":
                if btn_start.is_clicked(event):
                    game.reset_game()
                    state = "PLAYING"
                if btn_quit.is_clicked(event): running = False
            elif state == "PLAYING":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if event.button == 1: game.add_tower(x, y, "BASIC")
                    elif event.button == 3: game.add_tower(x, y, "SNIPER")
            elif state in ["GAME_OVER", "WIN"]:
                if btn_restart.is_clicked(event):
                    game.reset_game()
                    state = "PLAYING"

        if state == "MENU":
            draw_menu_background(screen)
            title = font_title.render("TOWER DEFENSE", True, (255, 215, 0)) # Título en dorado
            # Sombra del texto
            screen.blit(font_title.render("TOWER DEFENSE", True, (0,0,0)), (WIDTH//2 - title.get_width()//2 + 3, 103))
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
            btn_start.draw(screen)
            btn_quit.draw(screen)

        elif state == "PLAYING":
            screen.fill(BG_COLOR)
            new_state = game.update()
            if new_state != "PLAYING": state = new_state
            game.draw(screen, font_ui)

        elif state == "GAME_OVER":
            screen.fill((50, 10, 10)) 
            msg = font_title.render("¡DERROTA! eres un noob!", True, (255, 50, 50))
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 200))
            btn_restart.draw(screen)

        elif state == "WIN":
            screen.fill((10, 50, 10)) 
            msg = font_title.render("¡VICTORIA! eres un crack!", True, (50, 255, 50))
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 200))
            btn_restart.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()