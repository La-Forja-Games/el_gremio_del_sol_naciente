"""
Sistema de cámara para side-scrolling (vista lateral 2D)
"""

import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT


class SideScrollCamera:
    """Cámara para vista lateral 2D (side-scrolling)"""
    
    def __init__(self, world_width: int, world_height: int):
        """
        Inicializa la cámara de side-scrolling
        
        Args:
            world_width: Ancho del mundo en píxeles
            world_height: Alto del mundo en píxeles
        """
        self.world_width = world_width
        self.world_height = world_height
        self.x = 0  # Posición X de la cámara
        self.y = 0  # Posición Y de la cámara (para seguir verticalmente si es necesario)
        
        # Límites de la cámara
        self.min_x = 0
        self.max_x = max(0, world_width - SCREEN_WIDTH)
        self.min_y = 0
        self.max_y = max(0, world_height - SCREEN_HEIGHT)
        
        # Smooth following (suavizado)
        self.follow_speed = 0.1
    
    def update(self, target_x: float, target_y: float = None):
        """
        Actualiza la posición de la cámara para seguir al objetivo
        
        Args:
            target_x: Posición X del objetivo
            target_y: Posición Y del objetivo (opcional, para seguir verticalmente)
        """
        # Seguir horizontalmente (centrar en el objetivo)
        target_camera_x = target_x - SCREEN_WIDTH // 2
        
        # Suavizado
        self.x += (target_camera_x - self.x) * self.follow_speed
        
        # Limitar a los bordes del mundo
        self.x = max(self.min_x, min(self.x, self.max_x))
        
        # Seguir verticalmente si se especifica (opcional, para niveles con altura)
        if target_y is not None:
            target_camera_y = target_y - SCREEN_HEIGHT // 2
            self.y += (target_camera_y - self.y) * self.follow_speed
            self.y = max(self.min_y, min(self.y, self.max_y))
        else:
            # Mantener la cámara en una altura fija (típico en side-scrolling)
            self.y = 0
    
    def apply(self, x: float, y: float) -> tuple:
        """
        Aplica el offset de la cámara a coordenadas
        
        Args:
            x: Coordenada X
            y: Coordenada Y
            
        Returns:
            Tupla (screen_x, screen_y) con las coordenadas en pantalla
        """
        return (x - self.x, y - self.y)
    
    def apply_rect(self, rect: pygame.Rect) -> pygame.Rect:
        """
        Aplica el offset de la cámara a un rectángulo
        
        Args:
            rect: Rectángulo de Pygame
            
        Returns:
            Nuevo rectángulo con offset aplicado
        """
        return rect.move(-self.x, -self.y)
    
    def get_rect(self) -> pygame.Rect:
        """Retorna el rectángulo de la cámara"""
        return pygame.Rect(self.x, self.y, SCREEN_WIDTH, SCREEN_HEIGHT)

