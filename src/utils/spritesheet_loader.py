"""
Cargador de spritesheets
"""

import pygame
import os
from typing import List, Tuple
from src.config import ASSETS_DIR, TILE_SIZE
from src.entities.animation import Animation, Direction


class SpriteSheetLoader:
    """Carga y procesa spritesheets"""
    
    def __init__(self, image_path: str, sprite_width: int = None, sprite_height: int = None):
        """
        Inicializa el cargador de spritesheet
        
        Args:
            image_path: Ruta al archivo de imagen (relativa a assets/)
            sprite_width: Ancho de cada sprite (si None, se detecta automáticamente)
            sprite_height: Alto de cada sprite (si None, se detecta automáticamente)
        """
        full_path = os.path.join(ASSETS_DIR, image_path)
        
        try:
            self.image = pygame.image.load(full_path).convert_alpha()
            
            # Si no se especifica tamaño, detectar automáticamente
            # Asumimos que es un grid 4x4 (16 sprites)
            if sprite_width is None or sprite_height is None:
                # Detectar tamaño automáticamente basado en el grid
                img_width = self.image.get_width()
                img_height = self.image.get_height()
                
                # Intentar detectar el grid (4 columnas, 4 filas)
                self.sprite_width = img_width // 4
                self.sprite_height = img_height // 4
                
                print(f"Spritesheet detectado: {img_width}x{img_height}, Sprite size: {self.sprite_width}x{self.sprite_height}")
            else:
                self.sprite_width = sprite_width
                self.sprite_height = sprite_height
            
            self.sheet_width = self.image.get_width() // self.sprite_width
            self.sheet_height = self.image.get_height() // self.sprite_height
            
            print(f"Grid del spritesheet: {self.sheet_width}x{self.sheet_height} sprites")
            
        except pygame.error as e:
            print(f"Error cargando spritesheet {full_path}: {e}")
            self.image = None
            self.sprite_width = sprite_width or TILE_SIZE
            self.sprite_height = sprite_height or TILE_SIZE
            self.sheet_width = 0
            self.sheet_height = 0
    
    def get_sprite(self, x: int, y: int) -> pygame.Surface:
        """
        Extrae un sprite de la posición (x, y) en el grid
        
        Args:
            x: Columna (0-indexed)
            y: Fila (0-indexed)
            
        Returns:
            Superficie del sprite con transparencia preservada
        """
        if not self.image:
            surface = pygame.Surface((self.sprite_width, self.sprite_height), pygame.SRCALPHA)
            return surface
        
        rect = pygame.Rect(
            x * self.sprite_width,
            y * self.sprite_height,
            self.sprite_width,
            self.sprite_height
        )
        # Extraer sprite y asegurar que mantiene la transparencia
        sprite = self.image.subsurface(rect).copy()
        # Asegurar que tiene canal alpha
        if not sprite.get_flags() & pygame.SRCALPHA:
            sprite = sprite.convert_alpha()
        return sprite
    
    def get_animation_frames(self, row: int, start_col: int = 0, num_frames: int = 1) -> List[pygame.Surface]:
        """
        Obtiene frames de animación de una fila
        
        Args:
            row: Fila del spritesheet (0-indexed)
            start_col: Columna inicial
            num_frames: Número de frames
            
        Returns:
            Lista de superficies
        """
        frames = []
        for i in range(num_frames):
            frames.append(self.get_sprite(start_col + i, row))
        return frames
    
    def create_player_animations(self) -> dict:
        """
        Crea las animaciones del jugador basándose en el layout del spritesheet
        
        Para un spritesheet 4x4, típicamente:
        - Row 0: Idle frames (diferentes poses)
        - Row 1: Walking frames (diferentes fases del paso)
        - Row 2: Attack frames
        - Row 3: Otros frames (jump, etc.)
        
        O alternativamente, cada fila puede ser una dirección diferente.
        
        Returns:
            Diccionario con animaciones por dirección
        """
        animations = {}
        
        if not self.image:
            # Fallback a sprites generados
            from src.utils.sprite_generator import create_player_sprite, create_player_walking_frame
            placeholder = Animation([create_player_sprite("down")], speed=0.5)
            return {
                Direction.DOWN: placeholder,
                Direction.UP: placeholder,
                Direction.LEFT: placeholder,
                Direction.RIGHT: placeholder
            }
        
        # Para side-scrolling, asumimos que:
        # - Row 0: Idle frames (col 0 = idle principal)
        # - Row 1: Walking frames (col 0, 1, 2, 3 = diferentes fases del paso)
        
        # Front/Right idle (row 0, col 0)
        front_idle = self.get_sprite(0, 0)
        
        # Intentar encontrar frames de caminar
        # Si hay múltiples columnas en la fila 1, usarlas para walking
        walking_frames = []
        if self.sheet_width >= 4 and self.sheet_height >= 2:
            # Usar fila 1 para walking (típicamente tiene 4 frames)
            for col in range(min(4, self.sheet_width)):
                walking_frame = self.get_sprite(col, 1)
                walking_frames.append(walking_frame)
        else:
            # Si no hay suficientes frames, usar solo el idle
            walking_frames = [front_idle]
        
        # Si no hay frames de caminar, usar solo idle
        if not walking_frames:
            walking_frames = [front_idle]
        
        # Animación idle: solo el frame idle, sin animación
        idle_animation = Animation([front_idle], speed=0.5)
        
        # Animación walking: ciclar entre idle y walking frames
        # Para que se vea más natural, alternamos entre idle y walking
        right_walking_frames = [front_idle] + walking_frames[:2]  # Idle + 2 frames de caminar
        animations[Direction.RIGHT] = Animation(right_walking_frames, speed=0.15)
        
        # Para idle, usar solo el frame idle (sin movimiento de manos)
        # Guardamos la animación idle por separado
        self.idle_sprite = front_idle
        
        # Left (mirando a la izquierda) - espejar sprites frontales
        left_idle = pygame.transform.flip(front_idle, True, False)
        left_walking = [pygame.transform.flip(f, True, False) for f in right_walking_frames]
        animations[Direction.LEFT] = Animation(left_walking, speed=0.15)
        
        # UP/DOWN no se usan mucho en side-scrolling, pero los definimos
        back_idle = self.get_sprite(1, 0) if self.sheet_width > 1 else front_idle
        animations[Direction.UP] = Animation([back_idle], speed=0.5)
        animations[Direction.DOWN] = Animation([front_idle], speed=0.5)
        
        return animations
    
    def get_combat_sprite(self, hand: str = "right") -> pygame.Surface:
        """
        Obtiene el sprite de combate con espada en llamas
        
        Args:
            hand: "left" o "right"
            
        Returns:
            Sprite con espada en llamas
        """
        if not self.image:
            return pygame.Surface((self.sprite_width, self.sprite_height))
        
        if hand == "left":
            return self.get_sprite(1, 2)  # Row 2, col 1
        else:
            return self.get_sprite(3, 2)  # Row 2, col 3 o Row 3, col 3

