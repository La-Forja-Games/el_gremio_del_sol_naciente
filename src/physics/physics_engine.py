"""
Motor de física básico para side-scrolling
"""

import pygame
from typing import Optional
from src.config import TILE_SIZE


class PhysicsEngine:
    """Motor de física simple para plataformas 2D"""
    
    GRAVITY = 500.0  # Píxeles por segundo²
    MAX_FALL_SPEED = 400.0  # Velocidad máxima de caída
    
    @staticmethod
    def apply_gravity(velocity_y: float, dt: float) -> float:
        """
        Aplica gravedad a la velocidad vertical
        
        Args:
            velocity_y: Velocidad vertical actual
            dt: Delta time
            
        Returns:
            Nueva velocidad vertical
        """
        new_velocity = velocity_y + PhysicsEngine.GRAVITY * dt
        return min(new_velocity, PhysicsEngine.MAX_FALL_SPEED)
    
    @staticmethod
    def check_ground_collision(rect: pygame.Rect, ground_level: int) -> bool:
        """
        Verifica colisión con el suelo
        
        Args:
            rect: Rectángulo del objeto
            ground_level: Nivel del suelo en píxeles
            
        Returns:
            True si está en el suelo
        """
        return rect.bottom >= ground_level
    
    @staticmethod
    def check_platform_collision(rect: pygame.Rect, platforms: list) -> Optional[pygame.Rect]:
        """
        Verifica colisión con plataformas
        
        Args:
            rect: Rectángulo del objeto
            platforms: Lista de rectángulos de plataformas
            
        Returns:
            Rectángulo de la plataforma con la que colisiona, o None
        """
        for platform in platforms:
            if rect.colliderect(platform):
                # Verificar que está cayendo sobre la plataforma (desde arriba)
                if rect.bottom <= platform.top + 5:  # Margen pequeño
                    return platform
        return None

