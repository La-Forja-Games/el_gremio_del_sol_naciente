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
from src.map.map_manager import MapManager
from src.map.map_transition import MapTransition
from src.map.tile_generator import tile_generator
from src.camera_side_scroll import SideScrollCamera


class ExplorationState(GameState):
    """Estado de exploración (movimiento por el mundo)"""
    
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.player: Player = None
        self.map_manager = MapManager()
        self.map_transition = MapTransition(self.map_manager)
        self.camera = None
        self.game = None  # Referencia al juego (se asigna desde Game)
        
        # Input
        self.keys_pressed = {}
        
        # Partículas
        from src.utils.particles import ParticleSystem
        self.particles = ParticleSystem()
        
    def enter(self):
        """Inicializa el estado de exploración"""
        # Nivel del suelo (para física) - Definir PRIMERO
        self.ground_level = SCREEN_HEIGHT - 100
        
        # Obtener resource_manager del juego
        resource_manager = None
        if self.game:
            resource_manager = self.game.resource_manager
        
        # Crear jugador (posición inicial para side-scrolling)
        start_x = 100  # Empezar a la izquierda
        # La Y se ajustará cuando se cargue el sprite para que los pies estén en el suelo
        start_y = SCREEN_HEIGHT - 150  # Temporal, se ajustará
        self.player = Player(start_x, start_y, resource_manager=resource_manager)
        
        # Ajustar posición Y después de cargar el sprite para que esté en el suelo
        if self.player.image:
            self.player.rect.bottom = self.ground_level
            self.player.y = self.player.rect.bottom - self.player.rect.height
        
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
        
        # Inicializar cámara side-scrolling
        world_width = 2000  # Ancho del mundo (puede ser dinámico según el mapa)
        world_height = SCREEN_HEIGHT
        self.camera = SideScrollCamera(world_width, world_height)
        self.camera.update(self.player.x, self.player.y)
        
        print("Estado de exploración iniciado")
    
    def update(self, dt):
        """Actualiza la lógica de exploración (side-scrolling)"""
        # Manejar input de movimiento horizontal
        dx = 0
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        
        # Mover jugador horizontalmente
        if dx != 0:
            # Verificar colisiones horizontales antes de mover
            test_rect = self.player.rect.copy()
            test_rect.x += dx * self.player.speed * dt
            
            # Si no hay colisión, mover
            if not self.map_manager.check_collision(test_rect):
                self.player.move(dx, dt)
            else:
                # Detener movimiento si hay colisión
                self.player.velocity_x = 0
        
        # Actualizar jugador (con física)
        self.player.update(dt, self.ground_level)
        
        # Actualizar partículas
        self.particles.update(dt)
        
        # Actualizar cámara (side-scrolling)
        if self.camera:
            self.camera.update(self.player.x, self.player.y)
        
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
            elif event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                # Saltar
                self.player.jump()
                return True
            elif event.key == pygame.K_e:
                # Interactuar (por ahora no hace nada)
                pass
            elif event.key == pygame.K_c:
                # Iniciar combate de prueba (temporal)
                self.state_manager.change_state(STATE_COMBAT)
                return True
        
        return False
    
    def render(self, screen):
        """Renderiza el estado de exploración (side-scrolling)"""
        # Limpiar pantalla con color de fondo (cielo)
        screen.fill((135, 206, 235))  # Azul cielo
        
        # Renderizar suelo y fondo
        self._render_background(screen)
        
        # Renderizar mapa (si existe)
        if self.camera and self.map_manager.current_map:
            self.map_manager.render(screen, self.camera.get_rect())
        
        # Renderizar jugador
        if self.player and self.camera:
            screen_x, screen_y = self.camera.apply(self.player.rect.x, self.player.rect.y)
            
            # Renderizar sprite del jugador (asegurar que existe y tiene tamaño válido)
            if self.player.image:
                # Verificar que el sprite tenga un tamaño válido
                sprite_w = self.player.image.get_width()
                sprite_h = self.player.image.get_height()
                
                if sprite_w > 0 and sprite_h > 0:
                    # Renderizar el sprite completo sin escalar (tamaño original)
                    screen.blit(self.player.image, (screen_x, screen_y))
                    
                    # Debug: mostrar información del sprite (temporal)
                    # font = pygame.font.Font(None, 16)
                    # debug_text = font.render(f"Sprite: {sprite_w}x{sprite_h}", True, (255, 255, 0))
                    # screen.blit(debug_text, (screen_x, screen_y - 20))
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
                    self.player.rect.bottom,
                    (200, 200, 200),
                    2
                )
        
        # Renderizar partículas
        if self.camera:
            camera_offset = (self.camera.x, self.camera.y)
            self.particles.render(screen, camera_offset)
        
        # Renderizar HUD básico
        font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 18)
        
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
        """Renderiza el fondo y suelo para side-scrolling"""
        from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
        
        # Renderizar suelo
        ground_y = self.ground_level
        screen_ground_y = ground_y - self.camera.y if self.camera else ground_y
        
        # Suelo (césped)
        grass_tile = tile_generator.get_tile("grass")
        num_tiles = (SCREEN_WIDTH // TILE_SIZE) + 2
        
        for i in range(num_tiles):
            tile_x = (i * TILE_SIZE) - (self.camera.x % TILE_SIZE) if self.camera else (i * TILE_SIZE)
            if screen_ground_y < SCREEN_HEIGHT:
                screen.blit(grass_tile, (tile_x, screen_ground_y))
        
        # Línea del suelo (opcional, para debug)
        # pygame.draw.line(screen, (0, 255, 0), (0, screen_ground_y + TILE_SIZE), (SCREEN_WIDTH, screen_ground_y + TILE_SIZE), 2)
        
        # Renderizar algunas nubes de fondo (decoración)
        if self.camera:
            for i in range(3):
                cloud_x = 200 + i * 400 - (self.camera.x * 0.3)  # Movimiento parallax
                cloud_y = 50 + i * 30
                if -100 < cloud_x < SCREEN_WIDTH + 100:
                    pygame.draw.ellipse(screen, (255, 255, 255), (cloud_x, cloud_y, 60, 30))
                    pygame.draw.ellipse(screen, (255, 255, 255), (cloud_x + 20, cloud_y - 10, 50, 25))
                    pygame.draw.ellipse(screen, (255, 255, 255), (cloud_x + 40, cloud_y, 40, 20))
    
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
            
            # Actualizar cámara con nuevas dimensiones (side-scrolling)
            map_width = self.map_manager.get_map_width() if self.map_manager.get_map_width() > 0 else 2000
            map_height = SCREEN_HEIGHT
            self.camera = SideScrollCamera(map_width, map_height)
            self.camera.update(self.player.x, self.player.y)

