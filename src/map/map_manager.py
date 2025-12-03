"""
Gestor de mapas - carga y renderiza mapas de Tiled
"""

import pygame
import pytmx
import os
from typing import Optional, Dict
from src.config import DATA_DIR, TILE_SIZE


class MapManager:
    """Maneja la carga y renderizado de mapas"""
    
    def __init__(self):
        self.current_map: Optional[pytmx.TiledMap] = None
        self.map_name: Optional[str] = None
        self.collision_layer: Optional[pytmx.TiledObjectLayer] = None
        self.event_layer: Optional[pytmx.TiledObjectLayer] = None
        
    def load_map(self, map_path: str):
        """
        Carga un mapa desde un archivo .tmx
        
        Args:
            map_path: Ruta al archivo .tmx relativa a data/maps/
        """
        full_path = os.path.join(DATA_DIR, "maps", map_path)
        
        try:
            self.current_map = pytmx.load_pygame(full_path, pixelalpha=True)
            self.map_name = map_path
            
            # Buscar capas de colisión y eventos
            self.collision_layer = None
            self.event_layer = None
            
            for layer in self.current_map.objectgroups:
                if layer.name.lower() == "collision" or layer.name.lower() == "colisiones":
                    self.collision_layer = layer
                elif layer.name.lower() == "events" or layer.name.lower() == "eventos":
                    self.event_layer = layer
            
            print(f"Mapa cargado: {map_path}")
            print(f"  Dimensiones: {self.current_map.width}x{self.current_map.height} tiles")
            print(f"  Tamaño de tile: {self.current_map.tilewidth}x{self.current_map.tileheight}")
            
        except Exception as e:
            print(f"Error cargando mapa {full_path}: {e}")
            self.current_map = None
    
    def render(self, screen: pygame.Surface, camera_rect: pygame.Rect):
        """
        Renderiza el mapa visible en la pantalla
        
        Args:
            screen: Superficie donde renderizar
            camera_rect: Rectángulo de la cámara
        """
        if not self.current_map:
            return
        
        # Calcular qué tiles son visibles
        tile_width = self.current_map.tilewidth
        tile_height = self.current_map.tileheight
        
        start_x = max(0, camera_rect.x // tile_width)
        start_y = max(0, camera_rect.y // tile_height)
        end_x = min(self.current_map.width, 
                   (camera_rect.x + camera_rect.width) // tile_width + 1)
        end_y = min(self.current_map.height,
                   (camera_rect.y + camera_rect.height) // tile_height + 1)
        
        # Renderizar todas las capas de tiles
        for layer in self.current_map.visible_tile_layers:
            for y in range(start_y, end_y):
                for x in range(start_x, end_x):
                    tile = self.current_map.get_tile_image(x, y, layer)
                    if tile:
                        screen_x = x * tile_width - camera_rect.x
                        screen_y = y * tile_height - camera_rect.y
                        screen.blit(tile, (screen_x, screen_y))
    
    def check_collision(self, rect: pygame.Rect) -> bool:
        """
        Verifica si un rectángulo colisiona con objetos de colisión
        
        Args:
            rect: Rectángulo a verificar
            
        Returns:
            True si hay colisión, False si no
        """
        if not self.collision_layer:
            return False
        
        for obj in self.collision_layer:
            obj_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            if rect.colliderect(obj_rect):
                return True
        
        return False
    
    def get_map_width(self) -> int:
        """Retorna el ancho del mapa en píxeles"""
        if not self.current_map:
            return 0
        return self.current_map.width * self.current_map.tilewidth
    
    def get_map_height(self) -> int:
        """Retorna el alto del mapa en píxeles"""
        if not self.current_map:
            return 0
        return self.current_map.height * self.current_map.tileheight
    
    def get_events_at_position(self, x: float, y: float) -> list:
        """
        Obtiene eventos en una posición específica
        
        Args:
            x: Posición X
            y: Posición Y
            
        Returns:
            Lista de objetos de evento en esa posición
        """
        events = []
        if not self.event_layer:
            return events
        
        for obj in self.event_layer:
            obj_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            if obj_rect.collidepoint(x, y):
                events.append(obj)
        
        return events

