# ui.py
import pygame
from settings import WHITE, BLACK

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont("Consolas", 24, bold=True)

    def draw(self, surface):
        # Obtener posición del mouse para el efecto Hover
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

        # Dibujar botón con bordes redondeados
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10) # Borde

        # Dibujar texto centrado
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False