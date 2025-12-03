"""
Estado de exploración del juego
"""

import pygame
import random
from src.state_manager import GameState
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, STATE_PAUSE, STATE_COMBAT,
    STATE_INVENTORY, TILE_SIZE
)
from src.entities.player import Player
from src.entities.animation import Direction
from src.map.map_manager import MapManager
from src.map.map_transition import MapTransition
from src.map.tile_generator import initialize_tile_generator, TileGenerator
from src.camera import Camera


class ExplorationState(GameState):
    """Estado de exploración (movimiento por el mundo)"""
    
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.player: Player = None
        self.map_manager = MapManager()
        self.map_transition = MapTransition(self.map_manager)
        self.camera = None
        self.game = None  # Referencia al juego (se asigna desde Game)
        self.tile_generator = None  # Generador de tiles
        
        # Input
        self.keys_pressed = {}
        
        # Partículas
        from src.utils.particles import ParticleSystem
        self.particles = ParticleSystem()
        
    def enter(self):
        """Inicializa el estado de exploración"""
        # Obtener resource_manager y asset_lib del juego
        resource_manager = None
        asset_lib = None
        if self.game:
            resource_manager = self.game.resource_manager
            asset_lib = self.game.asset_lib
        
        # Inicializar tile_generator con resource_manager para usar tilesets reales
        if self.tile_generator is None:
            self.tile_generator = TileGenerator(resource_manager, asset_lib)
        
        # Crear jugador (posición inicial para top-down)
        start_x = SCREEN_WIDTH // 2  # Centro horizontal
        start_y = SCREEN_HEIGHT // 2  # Centro vertical
        self.player = Player(start_x, start_y, resource_manager=resource_manager)
        
        # Asegurar que el jugador tenga un sprite válido
        if not self.player.image:
            print("Advertencia: El jugador no tiene sprite, creando uno de emergencia")
            import pygame
            from src.config import TILE_SIZE
            self.player.image = pygame.Surface((TILE_SIZE, TILE_SIZE * 2))
            self.player.image.fill((255, 0, 0))  # Rojo para debug
            pygame.draw.circle(self.player.image, (255, 255, 255), (TILE_SIZE//2, TILE_SIZE), TILE_SIZE//3)
        
        # Cargar mapa de prueba (si existe)
        # self.map_manager.load_map("test_map.tmx")
        
        # Inicializar cámara top-down
        # Tamaño del mapa en tiles (puede ser dinámico según el mapa cargado)
        map_width_tiles = 50  # Ancho del mapa en tiles
        map_height_tiles = 50  # Alto del mapa en tiles
        self.camera = Camera(map_width_tiles, map_height_tiles)
        self.camera.update(self.player)
        
        print("Estado de exploración iniciado (vista top-down)")
    
    def update(self, dt):
        """Actualiza la lógica de exploración (top-down)"""
        # Manejar input de movimiento en 4 direcciones
        dx = 0
        dy = 0
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
        
        # Mover jugador
        if dx != 0 or dy != 0:
            # Verificar colisiones antes de mover
            test_rect = self.player.rect.copy()
            test_rect.x += dx * self.player.speed * dt
            test_rect.y += dy * self.player.speed * dt
            
            # Si no hay colisión, mover
            if not self.map_manager.check_collision(test_rect):
                # Movimiento top-down (sin física de gravedad)
                self.player.x += dx * self.player.speed * dt
                self.player.y += dy * self.player.speed * dt
                self.player.rect.x = int(self.player.x)
                self.player.rect.y = int(self.player.y)
                
                # Actualizar dirección y estado de movimiento
                if dx < 0:
                    self.player.direction = Direction.LEFT
                elif dx > 0:
                    self.player.direction = Direction.RIGHT
                elif dy < 0:
                    self.player.direction = Direction.UP
                elif dy > 0:
                    self.player.direction = Direction.DOWN
                
                self.player.moving = True
            else:
                # Detener movimiento si hay colisión
                self.player.moving = False
        else:
            self.player.moving = False
        
        # Actualizar jugador (sin física de gravedad para top-down)
        self.player.update(dt, ground_level=None)
        
        # Actualizar partículas
        self.particles.update(dt)
        
        # Actualizar cámara (top-down)
        if self.camera:
            self.camera.update(self.player)
        
        # Verificar eventos en la posición del jugador
        events = self.map_manager.get_events_at_position(
            self.player.rect.centerx,
            self.player.rect.centery
        )
        
        # Procesar eventos
        for event_obj in events:
            if event_obj.name and event_obj.name.startswith("map_"):
                # Cambio de mapa
                map_id = event_obj.name.replace("map_", "")
                spawn_point = event_obj.properties.get("spawn", "default")
                self._change_map(map_id, spawn_point)
            # TODO: Otros tipos de eventos (diálogos, combate, etc.)
    
    def handle_event(self, event):
        """Maneja eventos de entrada"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Abrir menú de pausa
                self.state_manager.push_state(STATE_PAUSE)
                return True
            elif event.key == pygame.K_i:
                # Abrir inventario
                self.state_manager.push_state(STATE_INVENTORY)
                return True
            # En top-down no hay saltos, las teclas W/UP se usan para movimiento
            elif event.key == pygame.K_e:
                # Interactuar (por ahora no hace nada)
                pass
            elif event.key == pygame.K_c:
                # Iniciar combate de prueba (temporal)
                self.state_manager.change_state(STATE_COMBAT)
                return True
        
        return False
    
    def render(self, screen):
        """Renderiza el estado de exploración (top-down)"""
        # Limpiar pantalla con color de fondo
        screen.fill((100, 150, 100))  # Verde pasto
        
        # Renderizar fondo (tiles de césped)
        self._render_background(screen)
        
        # Renderizar mapa (si existe)
        if self.camera and self.map_manager.current_map:
            self.map_manager.render(screen, self.camera.rect)
        
        # Renderizar jugador
        if self.player and self.camera:
            screen_x, screen_y = self.camera.apply(self.player)
            
            # Renderizar sprite del jugador (asegurar que existe y tiene tamaño válido)
            if self.player.image:
                # Verificar que el sprite tenga un tamaño válido
                sprite_w = self.player.image.get_width()
                sprite_h = self.player.image.get_height()
                
                if sprite_w > 0 and sprite_h > 0:
                    # Renderizar el sprite completo sin escalar (tamaño original 256x256)
                    screen.blit(self.player.image, (screen_x, screen_y))
                else:
                    # Fallback: dibujar un rectángulo visible
                    pygame.draw.rect(screen, (255, 0, 0), 
                                   (screen_x, screen_y, self.player.rect.width, self.player.rect.height))
            else:
                # Si no hay sprite, dibujar un rectángulo de debug
                pygame.draw.rect(screen, (255, 0, 0), 
                               (screen_x, screen_y, self.player.rect.width, self.player.rect.height))
                pygame.draw.circle(screen, (255, 255, 0), 
                                 (screen_x + self.player.rect.width//2, 
                                  screen_y + self.player.rect.height//2), 5)
            
            # Debug: dibujar rectángulo de colisión (descomentar para ver el área de colisión)
            # pygame.draw.rect(screen, (255, 0, 0), 
            #                 (screen_x, screen_y, self.player.rect.width, self.player.rect.height), 1)
            
            # Efecto de pasos (partículas ocasionales)
            if self.player.moving and random.random() < 0.1:
                self.particles.add_magic_sparkles(
                    self.player.rect.centerx,
                    self.player.rect.centery,
                    (200, 200, 200),
                    2
                )
        
        # Renderizar partículas
        if self.camera:
            camera_offset = (self.camera.rect.x, self.camera.rect.y)
            self.particles.render(screen, camera_offset)
        
        # Renderizar HUD básico
        from src.utils.font_helper import get_normal_font, get_small_font
        font = get_normal_font(24)
        small_font = get_small_font(18)
        
        # Información básica
        info_text = font.render("ESC: Pausa | I: Inventario", True, (255, 255, 255))
        screen.blit(info_text, (10, 10))
        
        # Stats del jugador (si existe)
        if self.player:
            hp_text = small_font.render(f"HP: {self.player.stats.get('HP', 0)}/{self.player.max_hp}", True, (255, 100, 100))
            mp_text = small_font.render(f"MP: {self.player.stats.get('MP', 0)}/{self.player.max_mp}", True, (100, 100, 255))
            screen.blit(hp_text, (10, 35))
            screen.blit(mp_text, (10, 55))
            
            level_text = small_font.render(f"Nivel: {self.player.level}", True, (255, 255, 255))
            screen.blit(level_text, (10, 75))
    
    def _render_background(self, screen):
        """Renderiza el fondo para top-down (tiles de césped)"""
        from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
        
        if not self.camera:
            return
        
        # Verificar que tile_generator esté inicializado
        if self.tile_generator is None:
            # Inicializar si no está inicializado
            resource_manager = None
            asset_lib = None
            if self.game:
                resource_manager = self.game.resource_manager
                asset_lib = self.game.asset_lib
            self.tile_generator = TileGenerator(resource_manager, asset_lib)
        
        # Renderizar tiles de césped en el área visible
        grass_tile = self.tile_generator.get_tile("grass")
        
        # Calcular qué tiles están visibles
        start_tile_x = self.camera.rect.x // TILE_SIZE
        start_tile_y = self.camera.rect.y // TILE_SIZE
        tiles_x = (SCREEN_WIDTH // TILE_SIZE) + 2
        tiles_y = (SCREEN_HEIGHT // TILE_SIZE) + 2
        
        for y in range(tiles_y):
            for x in range(tiles_x):
                tile_world_x = (start_tile_x + x) * TILE_SIZE
                tile_world_y = (start_tile_y + y) * TILE_SIZE
                tile_screen_x = tile_world_x - self.camera.rect.x
                tile_screen_y = tile_world_y - self.camera.rect.y
                
                if -TILE_SIZE < tile_screen_x < SCREEN_WIDTH and -TILE_SIZE < tile_screen_y < SCREEN_HEIGHT:
                    screen.blit(grass_tile, (tile_screen_x, tile_screen_y))
    
    def _change_map(self, map_id: str, spawn_point: str = "default"):
        """
        Cambia de mapa
        
        Args:
            map_id: ID del nuevo mapa
            spawn_point: ID del punto de spawn
        """
        spawn_pos = self.map_transition.change_map(map_id, spawn_point)
        if spawn_pos:
            self.player.x = spawn_pos[0]
            self.player.y = spawn_pos[1]
            self.player.rect.x = int(spawn_pos[0])
            self.player.rect.y = int(spawn_pos[1])
            
            # Actualizar cámara con nuevas dimensiones (top-down)
            map_width_tiles = self.map_manager.get_map_width() // TILE_SIZE if self.map_manager.get_map_width() > 0 else 50
            map_height_tiles = self.map_manager.get_map_height() // TILE_SIZE if self.map_manager.get_map_height() > 0 else 50
            self.camera = Camera(map_width_tiles, map_height_tiles)
            self.camera.update(self.player)

