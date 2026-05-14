# settings.py

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
FPS = 60

# Configuración inicial del juego
START_MONEY = 150
START_LIVES = 8
WIN_WAVE = 5 

# Colores (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (34, 139, 34)       # Verde pasto
PATH_COLOR = (210, 180, 140)   # Color arena
UI_BG = (40, 40, 40)
MENU_BG = (20, 30, 50)

# Camino que seguirán los enemigos (Waypoints)
PATH = [(-50, 150), (250, 150), (250, 450), (650, 450), (650, 200), (850, 200)]