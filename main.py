# main.py
import pygame
import sys
from game_manager import GameManager
from ui import Button
from settings import WIDTH, HEIGHT, FPS, BG_COLOR, MENU_BG, WHITE

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tower Defense Pro - Proyecto Universitario")
    clock = pygame.time.Clock()
    
    font_title = pygame.font.SysFont("Consolas", 48, bold=True)
    font_ui = pygame.font.SysFont("Consolas", 16, bold=True)

    # Inicializar el gestor del juego
    game = GameManager()
    
    # Crear Botones
    btn_start = Button(WIDTH//2 - 100, HEIGHT//2 - 30, 200, 50, "JUGAR", (50, 150, 50), (80, 200, 80))
    btn_quit = Button(WIDTH//2 - 100, HEIGHT//2 + 40, 200, 50, "SALIR", (200, 50, 50), (255, 80, 80))
    btn_restart = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50, "REINICIAR", (50, 100, 200), (80, 150, 255))

    state = "MENU" # Estados: MENU, PLAYING, GAME_OVER, WIN
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if state == "MENU":
                if btn_start.is_clicked(event):
                    game.reset_game()
                    state = "PLAYING"
                if btn_quit.is_clicked(event):
                    running = False
                    
            elif state == "PLAYING":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if event.button == 1:
                        game.add_tower(x, y, "BASIC")
                    elif event.button == 3:
                        game.add_tower(x, y, "SNIPER")
                        
            elif state in ["GAME_OVER", "WIN"]:
                if btn_restart.is_clicked(event):
                    game.reset_game()
                    state = "PLAYING"

        # ---------------- LÓGICA Y DIBUJO ---------------- #
        if state == "MENU":
            screen.fill(MENU_BG)
            title = font_title.render("TOWER DEFENSE", True, WHITE)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
            btn_start.draw(screen)
            btn_quit.draw(screen)

        elif state == "PLAYING":
            screen.fill(BG_COLOR)
            new_state = game.update()
            if new_state != "PLAYING":
                state = new_state
            game.draw(screen, font_ui)

        elif state == "GAME_OVER":
            screen.fill((50, 10, 10))
            msg = font_title.render("¡DERROTA! LA BASE CAYÓ", True, (255, 50, 50))
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 200))
            btn_restart.draw(screen)

        elif state == "WIN":
            screen.fill((10, 50, 10))
            msg = font_title.render("¡VICTORIA! SOBREVIVISTE", True, (50, 255, 50))
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 200))
            btn_restart.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()