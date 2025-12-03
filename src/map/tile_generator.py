"""
Generador de tiles básicos
"""

import pygame
from src.config import TILE_SIZE
from src.utils.sprite_generator import (
    create_grass_tile, create_dirt_tile, create_water_tile,
    create_snow_tile, create_stone_tile
)


class TileGenerator:
    """Genera tiles básicos para mapas"""
    
    def __init__(self):
        """Inicializa el generador de tiles"""
        self._tiles = {}
        self._load_tiles()
    
    def _load_tiles(self):
        """Carga todos los tiles básicos"""
        self._tiles = {
            "grass": create_grass_tile(),
            "dirt": create_dirt_tile(),
            "water": create_water_tile(),
            "snow": create_snow_tile(),
            "stone": create_stone_tile(),
        }
    
    def get_tile(self, tile_name: str) -> pygame.Surface:
        """
        Obtiene un tile por nombre
        
        Args:
            tile_name: Nombre del tile
            
        Returns:
            Superficie del tile
        """
        return self._tiles.get(tile_name, self._tiles["grass"])


# Instancia global
tile_generator = TileGenerator()

