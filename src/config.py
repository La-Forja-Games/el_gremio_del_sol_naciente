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
STATE_LOADING = "loading"
STATE_MENU = "menu"
STATE_EXPLORATION = "exploration"
STATE_COMBAT = "combat"
STATE_INVENTORY = "inventory"
STATE_CAMP = "camp"
STATE_DIALOG = "dialog"
STATE_PAUSE = "pause"

# Configuración de fuentes
# Fuente principal: BLKCHCRY
MAIN_FONT = "BLKCHCRY"

# Fuentes personalizadas a intentar (en orden de preferencia)
EPIC_FONTS = [
    "ui/fonts/BLKCHCRY.TTF",  # Fuente BLKCHCRY personalizada (si existe)
    "ui/fonts/blkchcry.ttf",  # Variante en minúsculas
    "ui/fonts/BLKCHCRY.ttf",  # Variante mixta
]

# Fuentes del sistema a intentar como fallback
SYSTEM_EPIC_FONTS = [
    "BLKCHCRY",  # Fuente principal
    "Arial Black",  # Negrita y épica
    "Impact",  # Fuente impactante
    "Courier New",  # Estilo retro
    "Times New Roman",  # Clásica
]

# Configuración de fuentes
# Fuentes épicas a intentar (en orden de preferencia)
EPIC_FONTS = [
    "assets/ui/fonts/pixel.ttf",  # Fuente pixel art personalizada (si existe)
    "assets/ui/fonts/medieval.ttf",  # Fuente medieval personalizada (si existe)
    "assets/ui/fonts/fantasy.ttf",  # Fuente fantasy personalizada (si existe)
]

# Fuentes del sistema góticas/medievales a intentar como fallback
SYSTEM_EPIC_FONTS = [
    "Algerian",  # Fuente gótica/medieval
    "Old English Text MT",  # Estilo gótico antiguo
    "Blackletter",  # Estilo gótico
    "Goudy Old Style",  # Estilo antiguo elegante
    "Times New Roman",  # Clásica como fallback
    "Arial Black",  # Negrita como último recurso
]

