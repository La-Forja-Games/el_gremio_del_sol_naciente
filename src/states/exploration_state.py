"""
Estado de exploración del juego
"""

import pygame
from src.state_manager import GameState
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, STATE_PAUSE, STATE_COMBAT,
    TILE_SIZE
)
from src.entities.player import Player
from src.map.map_manager import MapManager
from src.map.map_transition import MapTransition
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
        
        # Input
        self.keys_pressed = {}
        
    def enter(self):
        """Inicializa el estado de exploración"""
        # Obtener resource_manager del juego
        resource_manager = None
        if self.game:
            resource_manager = self.game.resource_manager
        
        # Crear jugador
        start_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2
        self.player = Player(start_x, start_y, resource_manager=resource_manager)
        
        # Cargar mapa de prueba (si existe)
        # self.map_manager.load_map("test_map.tmx")
        
        # Inicializar cámara con dimensiones del mapa
        map_width = self.map_manager.get_map_width() // TILE_SIZE if self.map_manager.get_map_width() > 0 else 50
        map_height = self.map_manager.get_map_height() // TILE_SIZE if self.map_manager.get_map_height() > 0 else 50
        self.camera = Camera(map_width, map_height)
        self.camera.update(self.player)
        
        print("Estado de exploración iniciado")
    
    def update(self, dt):
        """Actualiza la lógica de exploración"""
        # Manejar input de movimiento
        dx = 0
        dy = 0
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        
        # Normalizar movimiento diagonal
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/sqrt(2) para mantener velocidad constante
            dy *= 0.707
        
        # Mover jugador
        if dx != 0 or dy != 0:
            # Verificar colisiones antes de mover
            test_rect = self.player.rect.copy()
            test_rect.x += dx * self.player.speed * dt
            test_rect.y += dy * self.player.speed * dt
            
            # Si no hay colisión, mover
            if not self.map_manager.check_collision(test_rect):
                self.player.move(dx, dy, dt)
            else:
                # Intentar mover solo en X o solo en Y
                test_rect_x = self.player.rect.copy()
                test_rect_x.x += dx * self.player.speed * dt
                if not self.map_manager.check_collision(test_rect_x):
                    self.player.move(dx, 0, dt)
                else:
                    test_rect_y = self.player.rect.copy()
                    test_rect_y.y += dy * self.player.speed * dt
                    if not self.map_manager.check_collision(test_rect_y):
                        self.player.move(0, dy, dt)
        
        # Actualizar jugador
        self.player.update(dt)
        
        # Actualizar cámara
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
            elif event.key == pygame.K_e:
                # Interactuar (por ahora no hace nada)
                pass
        
        return False
    
    def render(self, screen):
        """Renderiza el estado de exploración"""
        # Limpiar pantalla con color de fondo
        screen.fill((50, 50, 50))  # Gris oscuro
        
        # Renderizar mapa
        if self.camera:
            self.map_manager.render(screen, self.camera.rect)
        
        # Renderizar jugador
        if self.player and self.camera:
            camera_offset = (self.camera.rect.x, self.camera.rect.y)
            self.player.render(screen, camera_offset)
        
        # Renderizar HUD básico (por ahora solo un indicador)
        font = pygame.font.Font(None, 24)
        text = font.render("Exploración - ESC para pausar", True, (255, 255, 255))
        screen.blit(text, (10, 10))
    
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
            
            # Actualizar cámara con nuevas dimensiones
            map_width = self.map_manager.get_map_width() // TILE_SIZE if self.map_manager.get_map_width() > 0 else 50
            map_height = self.map_manager.get_map_height() // TILE_SIZE if self.map_manager.get_map_height() > 0 else 50
            self.camera = Camera(map_width, map_height)
            self.camera.update(self.player)

