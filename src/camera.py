"""
Sistema de cámara para seguir al jugador
"""

import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


class Camera:
    """Maneja el desplazamiento de la cámara para seguir al jugador"""
    
    def __init__(self, map_width: int, map_height: int):
        """
        Inicializa la cámara
        
        Args:
            map_width: Ancho del mapa en tiles
            map_height: Alto del mapa en tiles
        """
        self.map_width = map_width * TILE_SIZE
        self.map_height = map_height * TILE_SIZE
        self.rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        
    def update(self, target):
        """
        Actualiza la posición de la cámara para seguir al objetivo
        
        Args:
            target: Objeto con atributos x, y (normalmente el jugador)
        """
        # Centrar la cámara en el objetivo
        x = target.x - SCREEN_WIDTH // 2
        y = target.y - SCREEN_HEIGHT // 2
        
        # Limitar la cámara a los bordes del mapa
        x = max(0, min(x, self.map_width - SCREEN_WIDTH))
        y = max(0, min(y, self.map_height - SCREEN_HEIGHT))
        
        self.rect.x = x
        self.rect.y = y
    
    def apply(self, entity):
        """
        Aplica el offset de la cámara a una entidad para renderizarla
        
        Args:
            entity: Objeto con atributos x, y, rect (opcional)
            
        Returns:
            Tupla (x, y) con las coordenadas ajustadas
        """
        if hasattr(entity, 'rect'):
            return (entity.rect.x - self.rect.x, entity.rect.y - self.rect.y)
        else:
            return (entity.x - self.rect.x, entity.y - self.rect.y)
    
    def apply_rect(self, rect: pygame.Rect) -> pygame.Rect:
        """
        Aplica el offset de la cámara a un rectángulo
        
        Args:
            rect: Rectángulo de Pygame
            
        Returns:
            Nuevo rectángulo con offset aplicado
        """
        return rect.move(-self.rect.x, -self.rect.y)

