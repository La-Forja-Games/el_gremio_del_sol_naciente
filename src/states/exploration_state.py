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
        self.village_renderer = None  # Renderizador del pueblo generado
        self.map_background = None  # Fondo PNG del mapa
        self.map_background_size = (0, 0)  # Tamaño del fondo PNG
        self.simple_map_data = None  # Datos del mapa simple (grass + house)
        self.house_tile = None  # Tile de la casa
        
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
        
        # Intentar cargar mapa map_01.tmx primero
        map_loaded = False
        map_file = "map_01.tmx"
        if self.map_manager.load_map(map_file):
            map_loaded = True
            print(f"[OK] Mapa {map_file} cargado")
        else:
            # Intentar con diferentes nombres
            for alt_name in ["map_01.tmx", "map01.tmx", "Map_01.tmx"]:
                if self.map_manager.load_map(alt_name):
                    map_loaded = True
                    print(f"[OK] Mapa {alt_name} cargado")
                    break
        
        # Si no hay .tmx, crear mapa simple (base_grass + house)
        if not map_loaded and resource_manager:
            # Crear mapa simple: base_grass con una casa en la esquina superior izquierda
            self._create_simple_map(resource_manager)
        else:
            self.map_background = None
            self.simple_map_data = None
        
        # Crear jugador (posición inicial para top-down)
        # Colocar en el centro del mapa
        if map_loaded and self.map_manager.current_map:
            # Usar el mapa cargado
            map_width_px = self.map_manager.get_map_width()
            map_height_px = self.map_manager.get_map_height()
            start_x = map_width_px // 2
            start_y = map_height_px // 2
        elif self.simple_map_data:
            # Usar mapa simple (centro)
            map_width_px = self.simple_map_data['width'] * TILE_SIZE
            map_height_px = self.simple_map_data['height'] * TILE_SIZE
            start_x = map_width_px // 2
            start_y = map_height_px // 2
        elif self.map_background:
            # Usar mapa PNG (centro de la imagen)
            start_x = self.map_background_size[0] // 2
            start_y = self.map_background_size[1] // 2
        elif self.village_renderer:
            # Usar pueblo generado
            start_x = self.village_renderer.map_width_px // 2
            start_y = self.village_renderer.map_height_px // 2
        else:
            # Fallback: centro de pantalla
            start_x = SCREEN_WIDTH // 2
            start_y = SCREEN_HEIGHT // 2
        
        self.player = Player(start_x, start_y, resource_manager=resource_manager)
        
        # Asegurar que el jugador tenga un sprite válido
        if not self.player.image:
            print("Advertencia: El jugador no tiene sprite, creando uno de emergencia")
            self.player.image = pygame.Surface((TILE_SIZE, TILE_SIZE * 2))
            self.player.image.fill((255, 0, 0))  # Rojo para debug
            pygame.draw.circle(self.player.image, (255, 255, 255), (TILE_SIZE//2, TILE_SIZE), TILE_SIZE//3)
        
        # Inicializar cámara top-down
        # Tamaño del mapa en tiles
        if map_loaded and self.map_manager.current_map:
            map_width_tiles = self.map_manager.current_map.width
            map_height_tiles = self.map_manager.current_map.height
        elif self.simple_map_data:
            map_width_tiles = self.simple_map_data['width']
            map_height_tiles = self.simple_map_data['height']
        elif self.map_background:
            # Convertir píxeles a tiles para el mapa PNG
            map_width_tiles = self.map_background_size[0] // TILE_SIZE
            map_height_tiles = self.map_background_size[1] // TILE_SIZE
        elif self.village_renderer:
            map_width_tiles = self.village_renderer.width
            map_height_tiles = self.village_renderer.height
        else:
            map_width_tiles = 50
            map_height_tiles = 50
        
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
        
        # Prioridad: Renderizar mapa de Tiled (map_01.tmx) si existe
        if self.camera and self.map_manager.current_map:
            self.map_manager.render(screen, self.camera.rect)
        elif self.simple_map_data and self.camera:
            # Renderizar mapa simple (base_grass + house)
            self._render_simple_map(screen)
        elif self.map_background and self.camera:
            # Renderizar mapa PNG directamente
            # Calcular qué parte del mapa es visible
            start_x = max(0, self.camera.rect.x)
            start_y = max(0, self.camera.rect.y)
            end_x = min(self.map_background_size[0], self.camera.rect.x + self.camera.rect.width)
            end_y = min(self.map_background_size[1], self.camera.rect.y + self.camera.rect.height)
            
            # Dibujar la porción visible del mapa PNG
            screen.blit(self.map_background, 
                       (start_x - self.camera.rect.x, start_y - self.camera.rect.y),
                       (start_x, start_y, end_x - start_x, end_y - start_y))
        elif self.village_renderer and self.camera:
            # Fallback: renderizar pueblo generado
            self.village_renderer.render(screen, self.camera.rect)
        else:
            # Fallback: renderizar fondo (tiles de césped)
            self._render_background(screen)
        
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
    
    def _create_simple_map(self, resource_manager):
        """Crea un mapa simple: base_grass con una casa en la esquina superior izquierda"""
        # Asegurar que tile_generator esté inicializado
        if self.tile_generator is None:
            asset_lib = None
            if self.game:
                asset_lib = self.game.asset_lib
            self.tile_generator = TileGenerator(resource_manager, asset_lib)
        
        # Tamaño del mapa en tiles (50x50 por defecto)
        map_width = 50
        map_height = 50
        
        # Cargar grass tile desde base_grass
        grass_tile = self.tile_generator.get_tile("grass")
        
        # Inicializar house_tile como None
        self.house_tile = None
        
        # Intentar cargar house tile desde legacy_Buildings
        try:
            house_tileset = resource_manager.load_image("tilesets/legacy_Buildings.png", use_alpha=True)
            if house_tileset and self.tile_generator:
                # Extraer un tile de casa (probablemente en las primeras filas/columnas)
                # Intentar diferentes posiciones hasta encontrar un tile válido
                for y in range(3):
                    for x in range(5):
                        house_tile = self.tile_generator._extract_tile_from_tileset(house_tileset, x, y)
                        if house_tile:
                            self.house_tile = house_tile
                            print(f"[OK] Casa cargada desde legacy_Buildings.png (tile {x},{y})")
                            break
                    if self.house_tile:
                        break
        except Exception as e:
            print(f"[WARNING] Error cargando casa desde legacy_Buildings: {e}")
        
        # Si no se encontró casa, intentar desde house_details
        if not self.house_tile:
            try:
                house_details = resource_manager.load_image("tilesets/house_details.png", use_alpha=True)
                if house_details and self.tile_generator:
                    house_tile = self.tile_generator._extract_tile_from_tileset(house_details, 0, 0)
                    if house_tile:
                        self.house_tile = house_tile
                        print("[OK] Casa cargada desde house_details.png")
            except Exception as e:
                print(f"[WARNING] Error cargando casa desde house_details: {e}")
        
        # Guardar datos del mapa
        self.simple_map_data = {
            'width': map_width,
            'height': map_height,
            'grass_tile': grass_tile,
            'house_pos': (0, 0)  # Casa en la esquina superior izquierda
        }
        
        print(f"[OK] Mapa simple creado: {map_width}x{map_height} tiles (base_grass + house)")
    
    def _render_simple_map(self, screen):
        """Renderiza el mapa simple (base_grass + house)"""
        if not self.simple_map_data:
            return
        
        map_width = self.simple_map_data['width']
        map_height = self.simple_map_data['height']
        grass_tile = self.simple_map_data['grass_tile']
        house_pos = self.simple_map_data['house_pos']
        
        # Calcular qué tiles son visibles
        start_tile_x = max(0, self.camera.rect.x // TILE_SIZE)
        start_tile_y = max(0, self.camera.rect.y // TILE_SIZE)
        end_tile_x = min(map_width, (self.camera.rect.x + self.camera.rect.width) // TILE_SIZE + 1)
        end_tile_y = min(map_height, (self.camera.rect.y + self.camera.rect.height) // TILE_SIZE + 1)
        
        # Renderizar grass tiles
        for y in range(start_tile_y, end_tile_y):
            for x in range(start_tile_x, end_tile_x):
                tile_world_x = x * TILE_SIZE
                tile_world_y = y * TILE_SIZE
                
                # Convertir coordenadas del mundo a pantalla
                tile_screen_x = tile_world_x - self.camera.rect.x
                tile_screen_y = tile_world_y - self.camera.rect.y
                
                # Renderizar grass
                screen.blit(grass_tile, (tile_screen_x, tile_screen_y))
        
        # Renderizar casa en la esquina superior izquierda (si está visible)
        house_x, house_y = house_pos
        if (start_tile_x <= house_x < end_tile_x and 
            start_tile_y <= house_y < end_tile_y and 
            self.house_tile):
            house_world_x = house_x * TILE_SIZE
            house_world_y = house_y * TILE_SIZE
            house_screen_x = house_world_x - self.camera.rect.x
            house_screen_y = house_world_y - self.camera.rect.y
            screen.blit(self.house_tile, (house_screen_x, house_screen_y))
    
    def _render_background(self, screen):
        """Renderiza el fondo para top-down (tiles de césped)"""
        # SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE ya están importados arriba
        
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

