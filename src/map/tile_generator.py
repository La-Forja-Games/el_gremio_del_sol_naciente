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
    
    def __init__(self, resource_manager=None, asset_lib=None):
        """
        Inicializa el generador de tiles
        
        Args:
            resource_manager: ResourceManager para cargar imágenes
            asset_lib: RPGAssetLibrary para acceder a tilesets
        """
        self.resource_manager = resource_manager
        self.asset_lib = asset_lib
        self._tiles = {}
        self._load_tiles()
    
    def _extract_tile_from_tileset(self, tileset_surface: pygame.Surface, tile_x: int, tile_y: int) -> pygame.Surface:
        """
        Extrae un tile individual de un tileset
        
        Args:
            tileset_surface: Superficie del tileset completo
            tile_x: Posición X del tile en el tileset (en tiles)
            tile_y: Posición Y del tile en el tileset (en tiles)
            
        Returns:
            Superficie del tile extraído
        """
        if not tileset_surface:
            return None
        
        x = tile_x * TILE_SIZE
        y = tile_y * TILE_SIZE
        
        if x + TILE_SIZE <= tileset_surface.get_width() and y + TILE_SIZE <= tileset_surface.get_height():
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            return tileset_surface.subsurface(rect)
        return None
    
    def _load_grass_from_tileset(self) -> pygame.Surface:
        """Intenta cargar grass tile desde tilesets reales"""
        if not self.resource_manager:
            return None
        
        # Intentar cargar desde ground_grass_details.png
        grass_tileset = self.resource_manager.load_image("tilesets/ground_grass_details.png", use_alpha=True)
        if grass_tileset:
            # Extraer el primer tile (0, 0) o buscar un tile de grass
            # Asumimos que el tileset tiene tiles de 32x32
            tile = self._extract_tile_from_tileset(grass_tileset, 0, 0)
            if tile:
                return tile
        
        # Intentar desde legacy_Tiles.png
        legacy_tiles = self.resource_manager.load_image("tilesets/legacy_Tiles.png", use_alpha=True)
        if legacy_tiles:
            # Buscar tile de grass (generalmente en las primeras filas)
            for y in range(3):
                for x in range(5):
                    tile = self._extract_tile_from_tileset(legacy_tiles, x, y)
                    if tile:
                        # Verificar si parece grass (tiene verde)
                        # Por ahora, usar el primero que encontremos
                        return tile
        
        # Intentar desde walls_floor.png
        walls_floor = self.resource_manager.load_image("tilesets/walls_floor.png", use_alpha=True)
        if walls_floor:
            # Buscar tile de floor/grass
            tile = self._extract_tile_from_tileset(walls_floor, 0, 0)
            if tile:
                return tile
        
        return None
    
    def _load_tiles(self):
        """Carga todos los tiles básicos"""
        # Intentar cargar grass real desde tilesets
        real_grass = self._load_grass_from_tileset()
        
        # Usar grass real si está disponible, sino usar placeholder
        grass_tile = real_grass if real_grass else create_grass_tile()
        
        self._tiles = {
            "grass": grass_tile,
            "dirt": create_dirt_tile(),
            "water": create_water_tile(),
            "snow": create_snow_tile(),
            "stone": create_stone_tile(),
        }
        
        if real_grass:
            print("[OK] Grass tile cargado desde tileset")
        else:
            print("[ADVERTENCIA] Usando grass tile placeholder")
    
    def get_tile(self, tile_name: str) -> pygame.Surface:
        """
        Obtiene un tile por nombre
        
        Args:
            tile_name: Nombre del tile
            
        Returns:
            Superficie del tile
        """
        return self._tiles.get(tile_name, self._tiles["grass"])


# Instancia global (se inicializará con resource_manager cuando esté disponible)
tile_generator = None

def initialize_tile_generator(resource_manager=None, asset_lib=None):
    """Inicializa el tile_generator global con resource_manager"""
    global tile_generator
    tile_generator = TileGenerator(resource_manager, asset_lib)
    return tile_generator

