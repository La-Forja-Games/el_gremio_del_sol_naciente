"""
Configuración global del juego
"""

import os

# Rutas base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DATA_DIR = os.path.join(BASE_DIR, "data")
SAVES_DIR = os.path.join(BASE_DIR, "saves")

# Configuración de pantalla
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "El Gremio del Sol Naciente"

# Configuración de tiles
TILE_SIZE = 32
MAP_WIDTH = 50  # Tiles
MAP_HEIGHT = 50  # Tiles

# Colores (RGB)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)

# Estados del juego
STATE_MENU = "menu"
STATE_EXPLORATION = "exploration"
STATE_COMBAT = "combat"
STATE_INVENTORY = "inventory"
STATE_CAMP = "camp"
STATE_DIALOG = "dialog"
STATE_PAUSE = "pause"

