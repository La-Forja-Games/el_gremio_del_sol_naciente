"""
Clase base para personajes
"""

import pygame
import json
import os
from typing import Dict, Optional
from src.config import DATA_DIR, TILE_SIZE
from src.entities.animation import SpriteSheet, Direction, Animation
from src.items.equipment import Equipment


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
        self.nombre = "Personaje"  # Nombre por defecto
        
        # Stats base
        self.level = 1
        self.exp = 0
        self.base_stats = {
            "HP": 100,
            "MP": 50,
            "ATK": 10,
            "DEF": 8,
            "VEL": 10,
            "MAG": 5
        }
        self.stats = self.base_stats.copy()
        self.max_hp = self.stats["HP"]
        self.max_mp = self.stats["MP"]
        
        # Equipamiento
        self.equipment = Equipment()
        
        # Dirección y movimiento
        self.direction = Direction.RIGHT  # En side-scrolling, empieza mirando a la derecha
        self.moving = False
        self.speed = 150.0  # Píxeles por segundo (horizontal)
        
        # Física (para side-scrolling)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.on_ground = False
        self.jump_power = 300.0  # Fuerza del salto
        self.can_jump = True
        
        # Animaciones
        self.animations: Dict[Direction, Animation] = {}
        self.current_animation: Optional[Animation] = None
        
        # Sprite actual
        self.image: Optional[pygame.Surface] = None
        # El rectángulo se ajustará al tamaño del sprite cuando se cargue
        self.rect = pygame.Rect(int(x), int(y), TILE_SIZE, TILE_SIZE * 2)  # Temporal, se ajustará
        
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
                    self.base_stats = char_data.get("stats_base", self.base_stats).copy()
                    self.stats = self.base_stats.copy()
                    self.max_hp = self.stats["HP"]
                    self.max_mp = self.stats["MP"]
                    break
            
            # Recalcular stats con equipamiento
            self._recalculate_stats()
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
    
    def move(self, dx: float, dt: float):
        """
        Mueve el personaje horizontalmente (side-scrolling)
        
        Args:
            dx: Delta X (-1, 0, 1) - izquierda/derecha
            dt: Delta time
        """
        # Determinar dirección
        if dx < 0:
            self.direction = Direction.LEFT
        elif dx > 0:
            self.direction = Direction.RIGHT
        
        # Actualizar estado de movimiento
        self.moving = (dx != 0)
        
        # Calcular velocidad horizontal
        self.velocity_x = dx * self.speed
        
        # Aplicar movimiento horizontal
        self.x += self.velocity_x * dt
        
        # Actualizar rectángulo
        self.rect.x = int(self.x)
    
    def jump(self):
        """Hace que el personaje salte"""
        if self.on_ground and self.can_jump:
            self.velocity_y = -self.jump_power
            self.on_ground = False
            self.can_jump = False
    
    def apply_physics(self, dt: float, ground_level: int = None):
        """
        Aplica física al personaje (gravedad, saltos)
        
        Args:
            dt: Delta time
            ground_level: Nivel del suelo (opcional)
        """
        from src.physics.physics_engine import PhysicsEngine
        
        # Aplicar gravedad
        self.velocity_y = PhysicsEngine.apply_gravity(self.velocity_y, dt)
        
        # Aplicar movimiento vertical
        self.y += self.velocity_y * dt
        
        # Verificar colisión con el suelo
        if ground_level is not None:
            if self.rect.bottom >= ground_level:
                self.rect.bottom = ground_level
                self.y = ground_level - self.rect.height
                self.velocity_y = 0
                self.on_ground = True
                self.can_jump = True
            else:
                self.on_ground = False
        
        # Actualizar rectángulo
        self.rect.y = int(self.y)
    
    def update(self, dt: float, ground_level: int = None):
        """
        Actualiza el personaje
        
        Args:
            dt: Delta time
            ground_level: Nivel del suelo para física (opcional)
        """
        # Aplicar física si se especifica ground_level
        if ground_level is not None:
            self.apply_physics(dt, ground_level)
        
        # Si cambió la dirección, cambiar animación
        if self.direction in self.animations:
            if self.current_animation != self.animations[self.direction]:
                self.current_animation = self.animations[self.direction]
                self.current_animation.reset()
        
        # Actualizar animación (solo si se está moviendo)
        if self.current_animation:
            if self.moving:
                # Animación más rápida cuando se mueve
                self.current_animation.speed = 0.15
                self.current_animation.update(dt)
            else:
                # Cuando está quieto, mantener el primer frame (idle) SIN animar
                # Esto evita que las manos se muevan cuando está parado
                if self.current_animation.current_frame != 0:
                    self.current_animation.current_frame = 0
                    self.current_animation.time_accumulator = 0.0
                # NO llamar a update() cuando está quieto para evitar animación
            
            # Obtener el frame actual
            self.image = self.current_animation.get_current_frame()
            
            # Ajustar el rectángulo al tamaño del sprite
            if self.image:
                old_bottom = self.rect.bottom
                old_centerx = self.rect.centerx
                self.rect.width = self.image.get_width()
                self.rect.height = self.image.get_height()
                self.rect.bottom = old_bottom  # Mantener la posición del suelo
                self.rect.centerx = old_centerx  # Mantener el centro horizontal
        
        # Fricción horizontal (detener gradualmente)
        if not self.moving:
            self.velocity_x *= 0.8  # Fricción
            if abs(self.velocity_x) < 1:
                self.velocity_x = 0
    
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
            
            # Asegurar que la imagen tenga transparencia (alpha)
            # Si la imagen tiene canal alpha, blit normal lo respeta automáticamente
            # Si no, intentar convertir a alpha
            if not (self.image.get_flags() & pygame.SRCALPHA):
                # Si no tiene alpha, convertir
                self.image = self.image.convert_alpha()
            
            # Blit con transparencia (pygame maneja alpha automáticamente)
            screen.blit(self.image, (screen_x, screen_y))
            
            # Debug: dibujar rectángulo de colisión (temporal, comentar después)
            # debug_rect = pygame.Rect(screen_x, screen_y, self.rect.width, self.rect.height)
            # pygame.draw.rect(screen, (255, 0, 0), debug_rect, 1)
        else:
            # Fallback: dibujar un rectángulo visible
            screen_x = self.rect.x - camera_offset[0]
            screen_y = self.rect.y - camera_offset[1]
            pygame.draw.rect(screen, (255, 0, 0), (screen_x, screen_y, self.rect.width, self.rect.height))
            pygame.draw.circle(screen, (255, 255, 0), (screen_x + self.rect.width//2, screen_y + self.rect.height//2), 5)
    
    def get_center(self) -> tuple:
        """Retorna el centro del personaje"""
        return (self.rect.centerx, self.rect.centery)
    
    def _recalculate_stats(self):
        """Recalcula los stats totales (base + equipamiento)"""
        # Empezar con stats base
        self.stats = self.base_stats.copy()
        
        # Agregar bonos del equipamiento
        equipment_bonuses = self.equipment.get_stat_bonuses()
        for stat_name, bonus in equipment_bonuses.items():
            if stat_name in self.stats:
                self.stats[stat_name] += bonus
        
        # Actualizar HP y MP máximos
        self.max_hp = self.stats["HP"]
        self.max_mp = self.stats["MP"]
    
    def equip_item(self, item):
        """
        Equipa un item y recalcula stats
        
        Args:
            item: Item a equipar
            
        Returns:
            Item previamente equipado (si había uno)
        """
        previous_item = self.equipment.equip(item)
        self._recalculate_stats()
        return previous_item
    
    def unequip_item(self, slot_name: str):
        """
        Desequipa un item y recalcula stats
        
        Args:
            slot_name: Nombre del slot
            
        Returns:
            Item desequipado
        """
        item = self.equipment.unequip(slot_name)
        self._recalculate_stats()
        return item

