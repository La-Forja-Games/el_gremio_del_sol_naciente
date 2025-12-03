"""
Clase base para personajes
"""

import pygame
import json
import os
from typing import Dict, Optional
from src.config import DATA_DIR, TILE_SIZE
from src.entities.animation import SpriteSheet, Direction, Animation


class Character:
    """Clase base para todos los personajes (jugadores, NPCs, enemigos)"""
    
    def __init__(self, x: float, y: float, character_id: int = None, resource_manager=None):
        """
        Inicializa un personaje
        
        Args:
            x: Posición X inicial
            y: Posición Y inicial
            character_id: ID del personaje (para cargar datos de JSON)
            resource_manager: Instancia de ResourceManager
        """
        self.x = x
        self.y = y
        self.character_id = character_id
        self.resource_manager = resource_manager
        
        # Stats base
        self.level = 1
        self.exp = 0
        self.stats = {
            "HP": 100,
            "MP": 50,
            "ATK": 10,
            "DEF": 8,
            "VEL": 10,
            "MAG": 5
        }
        self.max_hp = self.stats["HP"]
        self.max_mp = self.stats["MP"]
        
        # Dirección y movimiento
        self.direction = Direction.DOWN
        self.moving = False
        self.speed = 100.0  # Píxeles por segundo
        
        # Animaciones
        self.animations: Dict[Direction, Animation] = {}
        self.current_animation: Optional[Animation] = None
        
        # Sprite actual
        self.image: Optional[pygame.Surface] = None
        self.rect = pygame.Rect(int(x), int(y), TILE_SIZE, TILE_SIZE)
        
        # Cargar datos si se proporciona un ID
        if character_id and resource_manager:
            self._load_character_data(character_id)
    
    def _load_character_data(self, character_id: int):
        """Carga los datos del personaje desde JSON"""
        try:
            char_file = os.path.join(DATA_DIR, "characters", "character_base.json")
            with open(char_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Buscar el personaje por ID
            for char_data in data.get("characters", []):
                if char_data.get("id") == character_id:
                    self.stats = char_data.get("stats_base", self.stats).copy()
                    self.max_hp = self.stats["HP"]
                    self.max_mp = self.stats["MP"]
                    break
        except Exception as e:
            print(f"Error cargando datos del personaje {character_id}: {e}")
    
    def load_sprite(self, sprite_path: str, tile_width: int = TILE_SIZE, tile_height: int = TILE_SIZE):
        """
        Carga el spritesheet del personaje
        
        Args:
            sprite_path: Ruta al spritesheet relativa a assets/
            tile_width: Ancho de cada tile
            tile_height: Alto de cada tile
        """
        if not self.resource_manager:
            return
        
        sprite_image = self.resource_manager.load_image(sprite_path)
        spritesheet = SpriteSheet(sprite_image, tile_width, tile_height)
        
        # Crear animaciones para las 4 direcciones
        # Asumimos que el spritesheet tiene 4 filas (una por dirección)
        # y al menos 1 columna (frame) por dirección
        self.animations = spritesheet.get_animations_by_direction(0, frames_per_direction=1)
        self.current_animation = self.animations[self.direction]
        
        # Actualizar imagen inicial
        self.image = self.current_animation.get_current_frame()
    
    def move(self, dx: float, dy: float, dt: float):
        """
        Mueve el personaje
        
        Args:
            dx: Delta X (-1, 0, 1)
            dy: Delta Y (-1, 0, 1)
            dt: Delta time
        """
        # Determinar dirección
        if dy > 0:
            self.direction = Direction.DOWN
        elif dy < 0:
            self.direction = Direction.UP
        elif dx < 0:
            self.direction = Direction.LEFT
        elif dx > 0:
            self.direction = Direction.RIGHT
        
        # Actualizar estado de movimiento
        self.moving = (dx != 0 or dy != 0)
        
        # Calcular movimiento
        move_distance = self.speed * dt
        self.x += dx * move_distance
        self.y += dy * move_distance
        
        # Actualizar rectángulo
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def update(self, dt: float):
        """
        Actualiza el personaje
        
        Args:
            dt: Delta time
        """
        # Actualizar animación
        if self.current_animation:
            self.current_animation.update(dt)
            self.image = self.current_animation.get_current_frame()
        
        # Si cambió la dirección, cambiar animación
        if self.direction in self.animations:
            if self.current_animation != self.animations[self.direction]:
                self.current_animation = self.animations[self.direction]
                self.current_animation.reset()
    
    def render(self, screen: pygame.Surface, camera_offset: tuple = (0, 0)):
        """
        Renderiza el personaje
        
        Args:
            screen: Superficie donde renderizar
            camera_offset: Offset de la cámara (x, y)
        """
        if self.image:
            screen_x = self.rect.x - camera_offset[0]
            screen_y = self.rect.y - camera_offset[1]
            screen.blit(self.image, (screen_x, screen_y))
        else:
            # Fallback: dibujar un rectángulo
            rect = self.rect.copy()
            rect.x -= camera_offset[0]
            rect.y -= camera_offset[1]
            pygame.draw.rect(screen, (255, 0, 0), rect)
    
    def get_center(self) -> tuple:
        """Retorna el centro del personaje"""
        return (self.rect.centerx, self.rect.centery)

