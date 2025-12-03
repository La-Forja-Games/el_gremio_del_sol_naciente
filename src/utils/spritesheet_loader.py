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
        
        Según la documentación:
        - Fila 0: [Front Idle (sword), Back Idle, Back Idle (arms out), Front Idle (arms out)]
        - Fila 1: [Duplicado de Fila 0]
        - Fila 2: [Front Idle, Front con espada fuego (izq), Back Idle, Front con espada fuego (der)] - NO USAR (combate)
        - Fila 3: [Front Idle, Front Idle, Front Walking, Front con espada fuego (der)]
        
        Para top-down, usamos:
        - Idle: Fila 0, col 0 (Front Idle con espada normal, sin fuego)
        - Walking: Fila 3, col 2 (Front Walking, sin espada de fuego)
        - Back: Fila 0, col 1 (Back Idle)
        
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
        
        # Front/Right idle (Fila 0, col 0) - Front Idle con espada normal
        # NOTA: Este tiene espada, solo lo usamos para idle cuando está quieto
        front_idle = self.get_sprite(0, 0)
        
        # Buscar frames de caminar SIN espada
        # Según la documentación:
        # - Fila 0, col 0: Front Idle (sword) - TIENE ESPADA ❌
        # - Fila 0, col 3: Front Idle (arms out) - SIN ESPADA ✅
        # - Fila 3, col 0: Front Idle - puede tener espada ❌
        # - Fila 3, col 1: Front Idle - puede tener espada ❌
        # - Fila 3, col 2: Front Walking - puede tener espada ❌ (verificar)
        # - Fila 3, col 3: Front con espada fuego - TIENE ESPADA ❌
        
        # Usar SOLO el frame "arms out" que definitivamente NO tiene espada
        # Y crear variaciones de animación usando solo ese frame
        walking_frames = []
        
        if self.sheet_width >= 4 and self.sheet_height >= 1:
            # Fila 0, col 3: Front Idle (arms out) - SIN ESPADA (definitivo)
            frame_arms_out = self.get_sprite(3, 0)
            
            # Usar SOLO este frame sin espada para toda la animación de caminar
            # Crear una animación simple pero sin espada
            walking_frames = [frame_arms_out, frame_arms_out, frame_arms_out, frame_arms_out]
            
            print("Usando frame 'arms out' (sin espada) para caminar")
        else:
            # Si no hay col 3, intentar usar Back Idle (Fila 0, col 1) que tampoco debería tener espada frontal
            if self.sheet_width >= 2:
                back_idle_frame = self.get_sprite(1, 0)
                walking_frames = [back_idle_frame, back_idle_frame]
                print("ADVERTENCIA: Usando Back Idle como fallback (puede verse raro)")
            else:
                # Último recurso: usar idle pero mostrará espada
                print("ADVERTENCIA: No se encontraron frames sin espada, se mostrará espada")
                walking_frames = [front_idle]
        
        # Usar los frames directamente (ya están sin espada)
        right_walking_frames = walking_frames
        
        # Back idle (Fila 0, col 1) - Back Idle
        back_idle = None
        if self.sheet_width >= 2:
            back_idle = self.get_sprite(1, 0)
        else:
            back_idle = front_idle
        
        # Animación para RIGHT (mirando a la derecha/frente) - SOLO frames de caminar sin espada
        # Cuando camine, usará estos frames. Cuando esté quieto, usará el primer frame (idle)
        animations[Direction.RIGHT] = Animation(right_walking_frames, speed=0.1)
        
        # Animación para LEFT (mirando a la izquierda) - espejar los frames de caminar
        left_walking_frames = [pygame.transform.flip(f, True, False) for f in right_walking_frames]
        animations[Direction.LEFT] = Animation(left_walking_frames, speed=0.1)
        
        # Animación para DOWN (mirando hacia abajo/frente) - igual que RIGHT
        animations[Direction.DOWN] = Animation(right_walking_frames, speed=0.12)
        
        # Animación para UP (mirando hacia arriba/atrás) - usar back idle
        back_walking = back_idle  # Si no hay walking de espalda, usar idle
        up_walking_frames = [back_idle, back_walking, back_idle, back_walking]
        animations[Direction.UP] = Animation(up_walking_frames, speed=0.12)
        
        # Guardar sprite idle para referencia
        self.idle_sprite = front_idle
        
        print(f"Animaciones creadas: Idle desde (0,0), Walking desde (2,3), Back desde (1,0)")
        
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

