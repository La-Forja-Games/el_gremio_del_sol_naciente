"""
Clase del jugador
"""

from src.entities.character import Character
from src.entities.animation import Direction
from src.items.inventory import Inventory
from src.config import TILE_SIZE


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
        
        # Nombre del jugador
        self.nombre = "El Heredero"
        
        # Inventario
        self.inventory = Inventory(max_slots=40)
        
        # Cargar sprite del jugador (por ahora usaremos un placeholder)
        # Cuando tengamos el sprite real, descomentar:
        # self.load_sprite("sprites/player.png")
        
        # Por ahora, crear un sprite simple
        self._create_placeholder_sprite()
    
    def _create_placeholder_sprite(self):
        """Crea un sprite placeholder temporal o carga desde spritesheet"""
        from src.utils.spritesheet_loader import SpriteSheetLoader
        from src.entities.animation import Animation
        from src.config import TILE_SIZE as TILE_SIZE_LOCAL  # Import local para evitar conflictos
        
        # Intentar cargar el spritesheet del jugador
        spritesheet_path = "sprites/player.png"  # Ruta esperada del spritesheet
        # No especificar tamaño, dejar que se detecte automáticamente
        loader = SpriteSheetLoader(spritesheet_path)
        
        if loader.image:
            # Cargar animaciones desde el spritesheet
            self.animations = loader.create_player_animations()
            # Sprite inicial (front idle - row 0, col 0)
            initial_sprite = loader.get_sprite(0, 0)
            # Asegurar transparencia
            if initial_sprite:
                self.image = initial_sprite.copy()
            else:
                self.image = initial_sprite
            # Usar animación RIGHT por defecto (para side-scrolling)
            self.current_animation = self.animations.get(Direction.RIGHT, 
                                                         self.animations.get(Direction.DOWN, None))
            if self.current_animation:
                # Empezar en el primer frame (idle, sin movimiento)
                self.current_animation.current_frame_index = 0
                self.current_animation.timer = 0
                # Establecer la imagen inicial
                if self.current_animation.frames:
                    self.image = self.current_animation.frames[0].copy()
            # Ajustar rectángulo al tamaño del sprite
            if self.image:
                sprite_w = self.image.get_width()
                sprite_h = self.image.get_height()
                self.rect.width = sprite_w
                self.rect.height = sprite_h
                # Ajustar posición Y para que los pies estén en el suelo
                self.rect.bottom = int(self.y + sprite_h)
                self.y = self.rect.bottom - sprite_h
                print(f"Spritesheet del jugador cargado correctamente - Tamaño: {sprite_w}x{sprite_h}")
                print(f"Posición del jugador: ({self.x}, {self.y})")
        else:
            # Fallback a sprites generados
            from src.utils.sprite_generator import create_player_sprite, create_player_walking_frame
            
            direction_map = {
                Direction.DOWN: "down",
                Direction.UP: "up",
                Direction.LEFT: "left",
                Direction.RIGHT: "right"
            }
            
            self.animations = {}
            for direction, dir_name in direction_map.items():
                frames = [
                    create_player_sprite(dir_name),
                    create_player_walking_frame(dir_name, 0),
                    create_player_sprite(dir_name),
                    create_player_walking_frame(dir_name, 1),
                ]
                anim = Animation(frames, speed=0.15)
                self.animations[direction] = anim
            
            self.image = create_player_sprite("down")
            self.current_animation = self.animations[Direction.DOWN]
            print("Usando sprites generados (spritesheet no encontrado)")
        
        # Asegurar que siempre hay un sprite
        if not self.image:
            import pygame
            from src.config import TILE_SIZE as TILE_SIZE_LOCAL
            self.image = pygame.Surface((TILE_SIZE_LOCAL, TILE_SIZE_LOCAL))
            self.image.fill((0, 100, 200))  # Azul de emergencia
            pygame.draw.circle(self.image, (255, 255, 255), (TILE_SIZE_LOCAL//2, TILE_SIZE_LOCAL//2), TILE_SIZE_LOCAL//3)

