"""
Script de prueba rápida para verificar imports
"""

import sys
import io

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Verificando imports...")

try:
    import pygame
    print("✅ pygame importado correctamente")
except ImportError as e:
    print(f"❌ Error importando pygame: {e}")
    exit(1)

try:
    from src.game import Game
    print("✅ Game importado correctamente")
except ImportError as e:
    print(f"❌ Error importando Game: {e}")
    exit(1)

try:
    from src.entities.player import Player
    print("✅ Player importado correctamente")
except ImportError as e:
    print(f"❌ Error importando Player: {e}")
    exit(1)

try:
    from src.map.map_manager import MapManager
    print("✅ MapManager importado correctamente")
except ImportError as e:
    print(f"❌ Error importando MapManager: {e}")
    exit(1)

try:
    from src.states.exploration_state import ExplorationState
    print("✅ ExplorationState importado correctamente")
except ImportError as e:
    print(f"❌ Error importando ExplorationState: {e}")
    exit(1)

print("\n✅ Todos los imports están correctos!")
print("El juego debería ejecutarse sin problemas.")

