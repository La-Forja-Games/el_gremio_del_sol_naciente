"""
Sistema de animaciones para sprites
"""

import pygame
from typing import List, Dict
from enum import Enum


class Direction(Enum):
    """Direcciones de movimiento"""
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3


class Animation:
    """Maneja una animación de un sprite"""
    
    def __init__(self, frames: List[pygame.Surface], speed: float = 0.1):
        """
        Inicializa una animación
        
        Args:
            frames: Lista de superficies (frames) de la animación
            speed: Velocidad de la animación (segundos por frame)
        """
        self.frames = frames
        self.speed = speed
        self.current_frame = 0
        self.time_accumulator = 0.0
        
    def update(self, dt: float):
        """
        Actualiza la animación
        
        Args:
            dt: Delta time en segundos
        """
        self.time_accumulator += dt
        if self.time_accumulator >= self.speed:
            self.time_accumulator = 0.0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def get_current_frame(self) -> pygame.Surface:
        """Retorna el frame actual de la animación"""
        return self.frames[self.current_frame]
    
    def reset(self):
        """Reinicia la animación al primer frame"""
        self.current_frame = 0
        self.time_accumulator = 0.0


class SpriteSheet:
    """Maneja un spritesheet y extrae frames para animaciones"""
    
    def __init__(self, image: pygame.Surface, tile_width: int, tile_height: int):
        """
        Inicializa un spritesheet
        
        Args:
            image: Superficie del spritesheet completo
            tile_width: Ancho de cada tile/frame
            tile_height: Alto de cada tile/frame
        """
        self.image = image
        self.tile_width = tile_width
        self.tile_height = tile_height
        
        # Calcular dimensiones del spritesheet
        self.sheet_width = image.get_width() // tile_width
        self.sheet_height = image.get_height() // tile_height
    
    def get_image(self, x: int, y: int) -> pygame.Surface:
        """
        Extrae un frame específico del spritesheet
        
        Args:
            x: Posición X en tiles (0-indexed)
            y: Posición Y en tiles (0-indexed)
            
        Returns:
            Superficie del frame extraído
        """
        rect = pygame.Rect(
            x * self.tile_width,
            y * self.tile_height,
            self.tile_width,
            self.tile_height
        )
        return self.image.subsurface(rect)
    
    def get_animation(self, row: int, start_col: int = 0, num_frames: int = 1) -> Animation:
        """
        Crea una animación desde una fila del spritesheet
        
        Args:
            row: Fila del spritesheet (0-indexed)
            start_col: Columna inicial (0-indexed)
            num_frames: Número de frames en la animación
            
        Returns:
            Objeto Animation
        """
        frames = []
        for i in range(num_frames):
            frames.append(self.get_image(start_col + i, row))
        return Animation(frames)
    
    def get_animations_by_direction(self, row: int, frames_per_direction: int = 1) -> Dict[Direction, Animation]:
        """
        Crea animaciones para las 4 direcciones desde filas consecutivas
        
        Args:
            row: Fila inicial (0-indexed)
            frames_per_direction: Número de frames por dirección
            
        Returns:
            Diccionario con animaciones por dirección
        """
        animations = {}
        directions = [Direction.DOWN, Direction.UP, Direction.LEFT, Direction.RIGHT]
        
        for i, direction in enumerate(directions):
            anim = self.get_animation(row + i, 0, frames_per_direction)
            animations[direction] = anim
        
        return animations

