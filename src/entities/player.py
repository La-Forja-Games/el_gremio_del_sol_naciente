"""
Clase del jugador
"""

from src.entities.character import Character
from src.entities.animation import Direction


class Player(Character):
    """Clase del jugador principal (El Heredero)"""
    
    def __init__(self, x: float, y: float, resource_manager=None):
        """
        Inicializa el jugador
        
        Args:
            x: Posición X inicial
            y: Posición Y inicial
            resource_manager: Instancia de ResourceManager
        """
        super().__init__(x, y, character_id=1, resource_manager=resource_manager)
        
        # Cargar sprite del jugador (por ahora usaremos un placeholder)
        # Cuando tengamos el sprite real, descomentar:
        # self.load_sprite("sprites/player.png")
        
        # Por ahora, crear un sprite simple
        self._create_placeholder_sprite()
    
    def _create_placeholder_sprite(self):
        """Crea un sprite placeholder temporal"""
        import pygame
        from src.config import TILE_SIZE
        
        # Crear un sprite simple de color
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((0, 100, 200))  # Azul
        
        # Dibujar un círculo para representar al jugador
        pygame.draw.circle(self.image, (255, 255, 255), 
                         (TILE_SIZE // 2, TILE_SIZE // 2), 
                         TILE_SIZE // 3)
        
        # Crear animaciones placeholder (todas iguales por ahora)
        from src.entities.animation import Animation
        placeholder_anim = Animation([self.image])
        self.animations = {
            Direction.DOWN: placeholder_anim,
            Direction.UP: placeholder_anim,
            Direction.LEFT: placeholder_anim,
            Direction.RIGHT: placeholder_anim
        }
        self.current_animation = placeholder_anim

