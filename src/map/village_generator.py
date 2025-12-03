"""
Generador de pueblo usando tilesets disponibles
Crea un pueblo completo con lógica visual orgánica y variada
"""

import pygame
import random
import os
from typing import Dict, List, Tuple, Optional
from src.config import TILE_SIZE, ASSETS_DIR


class VillageGenerator:
    """Genera un pueblo completo usando tilesets"""
    
    def __init__(self, resource_manager):
        """
        Inicializa el generador de pueblo
        
        Args:
            resource_manager: ResourceManager para cargar tilesets
        """
        self.resource_manager = resource_manager
        self.tilesets = {}
        self.tile_cache = {}  # Cache de tiles extraídos
        self.grass_tiles = []  # Lista de tiles de grass disponibles
        self.path_tiles = []  # Lista de tiles de camino disponibles
        self.building_tiles = {}  # Diccionario de tiles de edificios por tipo
        self.tree_tiles = []  # Lista de tiles de árboles
        self.object_tiles = {}  # Diccionario de tiles de objetos por tileset
        
        # Cargar todos los tilesets
        self._load_tilesets()
        self._preload_tiles()
    
    def _load_tilesets(self):
        """Carga todos los tilesets disponibles"""
        tileset_files = [
            "base_grass.png",
            "exterior.png",
            "house_details.png",
            "legacy_Buildings.png",
            "legacy_Tiles.png",
            "legacy_Tree-Assets.png",
            "Objects.png",
            "Other_objects.png",
            "walls_floor.png",
            "ground_grass_details.png",
            "supplies_objects.png",
            "pedestals.png",
        ]
        
        for tileset_file in tileset_files:
            tileset_path = f"tilesets/{tileset_file}"
            tileset = self.resource_manager.load_image(tileset_path, use_alpha=True)
            if tileset:
                self.tilesets[tileset_file] = tileset
                print(f"[OK] Tileset cargado: {tileset_file} ({tileset.get_width()}x{tileset.get_height()})")
    
    def _preload_tiles(self):
        """Precarga tiles válidos de cada tileset para evitar repetición"""
        # Precargar tiles de grass
        if "base_grass.png" in self.tilesets:
            tileset = self.tilesets["base_grass.png"]
            tiles_x = tileset.get_width() // TILE_SIZE
            tiles_y = tileset.get_height() // TILE_SIZE
            for y in range(tiles_y):
                for x in range(tiles_x):
                    tile = self._extract_tile("base_grass.png", x, y)
                    if tile:
                        self.grass_tiles.append(tile)
        
        # Agregar tiles de ground_grass_details como variación
        if "ground_grass_details.png" in self.tilesets:
            tileset = self.tilesets["ground_grass_details.png"]
            tiles_x = min(tileset.get_width() // TILE_SIZE, 8)
            tiles_y = min(tileset.get_height() // TILE_SIZE, 8)
            for y in range(tiles_y):
                for x in range(tiles_x):
                    tile = self._extract_tile("ground_grass_details.png", x, y)
                    if tile:
                        self.grass_tiles.append(tile)
        
        # Precargar tiles de camino
        for tileset_name in ["walls_floor.png", "legacy_Tiles.png"]:
            if tileset_name in self.tilesets:
                tileset = self.tilesets[tileset_name]
                tiles_x = min(tileset.get_width() // TILE_SIZE, 12)
                tiles_y = min(tileset.get_height() // TILE_SIZE, 8)
                for y in range(tiles_y):
                    for x in range(tiles_x):
                        tile = self._extract_tile(tileset_name, x, y)
                        if tile:
                            # Filtrar tiles muy oscuros (probablemente paredes) sin numpy
                            # Muestrear algunos píxeles del tile para determinar si es claro
                            sample_points = [
                                (TILE_SIZE // 4, TILE_SIZE // 4),
                                (TILE_SIZE // 2, TILE_SIZE // 2),
                                (TILE_SIZE * 3 // 4, TILE_SIZE * 3 // 4)
                            ]
                            total_brightness = 0
                            sample_count = 0
                            for px, py in sample_points:
                                if px < tile.get_width() and py < tile.get_height():
                                    try:
                                        color = tile.get_at((px, py))
                                        # Calcular brillo promedio (RGB)
                                        brightness = (color[0] + color[1] + color[2]) / 3
                                        total_brightness += brightness
                                        sample_count += 1
                                    except:
                                        pass
                            
                            if sample_count > 0:
                                avg_brightness = total_brightness / sample_count
                                if avg_brightness > 80:  # Solo tiles claros (pisos)
                                    self.path_tiles.append(tile)
                            else:
                                # Si no se puede muestrear, agregar de todos modos
                                self.path_tiles.append(tile)
        
        # Precargar tiles de edificios
        for tileset_name in ["legacy_Buildings.png", "exterior.png", "house_details.png"]:
            if tileset_name in self.tilesets:
                tileset = self.tilesets[tileset_name]
                tiles_x = min(tileset.get_width() // TILE_SIZE, 16)
                tiles_y = min(tileset.get_height() // TILE_SIZE, 12)
                building_list = []
                for y in range(tiles_y):
                    for x in range(tiles_x):
                        tile = self._extract_tile(tileset_name, x, y)
                        if tile:
                            building_list.append(tile)
                if building_list:
                    self.building_tiles[tileset_name] = building_list
        
        # Precargar tiles de árboles
        if "legacy_Tree-Assets.png" in self.tilesets:
            tileset = self.tilesets["legacy_Tree-Assets.png"]
            tiles_x = min(tileset.get_width() // TILE_SIZE, 12)
            tiles_y = min(tileset.get_height() // TILE_SIZE, 12)
            for y in range(tiles_y):
                for x in range(tiles_x):
                    tile = self._extract_tile("legacy_Tree-Assets.png", x, y)
                    if tile:
                        self.tree_tiles.append(tile)
        
        # Precargar tiles de objetos
        for tileset_name in ["Objects.png", "Other_objects.png", "supplies_objects.png", "pedestals.png"]:
            if tileset_name in self.tilesets:
                tileset = self.tilesets[tileset_name]
                tiles_x = min(tileset.get_width() // TILE_SIZE, 16)
                tiles_y = min(tileset.get_height() // TILE_SIZE, 16)
                object_list = []
                for y in range(tiles_y):
                    for x in range(tiles_x):
                        tile = self._extract_tile(tileset_name, x, y)
                        if tile:
                            object_list.append(tile)
                if object_list:
                    self.object_tiles[tileset_name] = object_list
        
        print(f"[OK] Tiles precargados: {len(self.grass_tiles)} grass, {len(self.path_tiles)} paths, {len(self.tree_tiles)} trees")
    
    def _extract_tile(self, tileset_name: str, tile_x: int, tile_y: int) -> Optional[pygame.Surface]:
        """
        Extrae un tile de un tileset
        
        Args:
            tileset_name: Nombre del tileset
            tile_x: Posición X del tile (en tiles)
            tile_y: Posición Y del tile (en tiles)
            
        Returns:
            Superficie del tile o None
        """
        cache_key = f"{tileset_name}_{tile_x}_{tile_y}"
        if cache_key in self.tile_cache:
            return self.tile_cache[cache_key]
        
        if tileset_name not in self.tilesets:
            return None
        
        tileset = self.tilesets[tileset_name]
        x = tile_x * TILE_SIZE
        y = tile_y * TILE_SIZE
        
        if x + TILE_SIZE <= tileset.get_width() and y + TILE_SIZE <= tileset.get_height():
            try:
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                tile = tileset.subsurface(rect).copy()
                tile = tile.convert_alpha()
                self.tile_cache[cache_key] = tile
                return tile
            except:
                return None
        
        return None
    
    def _get_random_grass_tile(self) -> pygame.Surface:
        """Obtiene un tile de grass aleatorio de los precargados"""
        if self.grass_tiles:
            return random.choice(self.grass_tiles)
        # Fallback: tile verde simple
        tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        tile.fill((100, 150, 80))
        return tile
    
    def generate_village_map(self, width: int = 80, height: int = 60) -> pygame.Surface:
        """
        Genera un mapa de pueblo completo con lógica orgánica
        
        Args:
            width: Ancho del mapa en tiles
            height: Alto del mapa en tiles
            
        Returns:
            Superficie con el mapa completo
        """
        map_surface = pygame.Surface((width * TILE_SIZE, height * TILE_SIZE))
        map_surface = map_surface.convert_alpha()
        
        # Capa 1: Base de grass variada
        print("Generando base de grass variada...")
        for y in range(height):
            for x in range(width):
                grass_tile = self._get_random_grass_tile()
                map_surface.blit(grass_tile, (x * TILE_SIZE, y * TILE_SIZE))
        
        # Capa 2: Caminos orgánicos
        print("Generando caminos orgánicos...")
        self._draw_organic_paths(map_surface, width, height)
        
        # Capa 3: Casas y edificios variados
        print("Generando edificios variados...")
        self._draw_varied_buildings(map_surface, width, height)
        
        # Capa 4: Vegetación abundante y variada
        print("Generando vegetación...")
        self._draw_vegetation(map_surface, width, height)
        
        # Capa 5: Objetos decorativos
        print("Generando objetos decorativos...")
        self._draw_decorative_objects(map_surface, width, height)
        
        print(f"[OK] Pueblo generado: {width}x{height} tiles")
        return map_surface
    
    def _draw_organic_paths(self, surface: pygame.Surface, width: int, height: int):
        """Dibuja caminos orgánicos y variados"""
        if not self.path_tiles:
            return
        
        # Camino principal horizontal (centro, con variación)
        path_y = height // 2
        path_width = 3
        for y_offset in range(-path_width // 2, path_width // 2 + 1):
            for x in range(width):
                # Variar el tile de camino para evitar repetición
                path_tile = random.choice(self.path_tiles)
                surface.blit(path_tile, (x * TILE_SIZE, (path_y + y_offset) * TILE_SIZE))
        
        # Camino principal vertical (centro, con variación)
        path_x = width // 2
        for x_offset in range(-path_width // 2, path_width // 2 + 1):
            for y in range(height):
                path_tile = random.choice(self.path_tiles)
                surface.blit(path_tile, ((path_x + x_offset) * TILE_SIZE, y * TILE_SIZE))
        
        # Caminos secundarios sinuosos conectando casas
        self._draw_secondary_paths(surface, width, height)
    
    def _draw_secondary_paths(self, surface: pygame.Surface, width: int, height: int):
        """Dibuja caminos secundarios sinuosos"""
        if not self.path_tiles:
            return
        
        # Camino desde esquina superior izquierda al centro (sinuoso)
        start_x, start_y = width // 6, height // 6
        end_x, end_y = width // 2 - 2, height // 2 - 2
        
        # Algoritmo simple de línea con variación
        steps = max(abs(end_x - start_x), abs(end_y - start_y))
        for i in range(steps):
            t = i / steps if steps > 0 else 0
            # Agregar variación sinuosa
            noise = random.randint(-1, 1)
            x = int(start_x + (end_x - start_x) * t) + noise
            y = int(start_y + (end_y - start_y) * t) + noise
            if 0 <= x < width and 0 <= y < height:
                path_tile = random.choice(self.path_tiles)
                surface.blit(path_tile, (x * TILE_SIZE, y * TILE_SIZE))
        
        # Similar para otras esquinas
        for corner in [(width * 5 // 6, height // 6), (width // 6, height * 5 // 6), (width * 5 // 6, height * 5 // 6)]:
            corner_x, corner_y = corner
            steps = max(abs(width // 2 - corner_x), abs(height // 2 - corner_y))
            for i in range(steps):
                t = i / steps if steps > 0 else 0
                noise = random.randint(-1, 1)
                x = int(corner_x + (width // 2 - corner_x) * t) + noise
                y = int(corner_y + (height // 2 - corner_y) * t) + noise
                if 0 <= x < width and 0 <= y < height:
                    path_tile = random.choice(self.path_tiles)
                    surface.blit(path_tile, (x * TILE_SIZE, y * TILE_SIZE))
    
    def _draw_varied_buildings(self, surface: pygame.Surface, width: int, height: int):
        """Dibuja casas y edificios con variedad visual"""
        path_center_x = width // 2
        path_center_y = height // 2
        
        # Posiciones de casas (más distribuidas)
        house_positions = [
            (width // 8, height // 8, 5, 4, "legacy_Buildings.png"),
            (width * 7 // 8 - 5, height // 8, 5, 4, "legacy_Buildings.png"),
            (width // 8, height * 7 // 8 - 4, 5, 4, "exterior.png"),
            (width * 7 // 8 - 5, height * 7 // 8 - 4, 5, 4, "exterior.png"),
            (path_center_x - 8, path_center_y - 18, 6, 5, "legacy_Buildings.png"),
            (path_center_x + 2, path_center_y + 8, 5, 4, "exterior.png"),
            (path_center_x - 18, path_center_y - 5, 4, 4, "house_details.png"),
            (path_center_x + 14, path_center_y - 5, 4, 4, "house_details.png"),
            (width // 4, height // 3, 4, 3, "exterior.png"),
            (width * 3 // 4, height * 2 // 3, 4, 3, "exterior.png"),
        ]
        
        for house_x, house_y, house_w, house_h, tileset_name in house_positions:
            # Verificar que no esté sobre caminos principales
            if not (abs(house_x - path_center_x) < 4 and abs(house_y - path_center_y) < 4):
                self._draw_varied_house(surface, house_x, house_y, house_w, house_h, tileset_name)
    
    def _draw_varied_house(self, surface: pygame.Surface, x: int, y: int, w: int, h: int, tileset_name: str):
        """Dibuja una casa con variedad de tiles"""
        if tileset_name not in self.building_tiles or not self.building_tiles[tileset_name]:
            return
        
        building_tiles = self.building_tiles[tileset_name]
        
        # Dibujar la casa con variedad
        for ty in range(h):
            for tx in range(w):
                # Variar tiles según posición
                if tx == 0 or tx == w - 1 or ty == 0 or ty == h - 1:
                    # Bordes: usar tiles de pared (últimos tiles del tileset)
                    tile = random.choice(building_tiles[-len(building_tiles)//3:])
                else:
                    # Interior: usar tiles de techo/piso (primeros tiles)
                    tile = random.choice(building_tiles[:len(building_tiles)//2])
                
                if tile:
                    surface.blit(tile, ((x + tx) * TILE_SIZE, (y + ty) * TILE_SIZE))
        
        # Agregar detalles (puertas) si están disponibles
        if "house_details.png" in self.building_tiles:
            door_tiles = self.building_tiles["house_details.png"]
            if door_tiles:
                door_x = x + w // 2
                door_y = y + h - 1
                door_tile = random.choice(door_tiles[:len(door_tiles)//2])
                surface.blit(door_tile, (door_x * TILE_SIZE, door_y * TILE_SIZE))
    
    def _draw_vegetation(self, surface: pygame.Surface, width: int, height: int):
        """Dibuja vegetación abundante y variada"""
        if not self.tree_tiles:
            return
        
        # Árboles distribuidos orgánicamente (evitar caminos y casas)
        occupied = set()
        
        # Marcar áreas ocupadas (caminos y casas)
        path_center_x = width // 2
        path_center_y = height // 2
        for x in range(width):
            for y in range(height):
                if abs(x - path_center_x) < 3 or abs(y - path_center_y) < 3:
                    occupied.add((x, y))
        
        # Colocar árboles
        tree_count = 50  # Más árboles
        placed = 0
        attempts = 0
        max_attempts = tree_count * 10
        
        while placed < tree_count and attempts < max_attempts:
            tree_x = random.randint(2, width - 3)
            tree_y = random.randint(2, height - 3)
            
            # Verificar que no esté ocupado
            if (tree_x, tree_y) not in occupied:
                # Verificar que no esté muy cerca de otro árbol
                too_close = False
                for ox, oy in occupied:
                    if abs(tree_x - ox) < 2 and abs(tree_y - oy) < 2:
                        too_close = True
                        break
                
                if not too_close:
                    tree_tile = random.choice(self.tree_tiles)
                    surface.blit(tree_tile, (tree_x * TILE_SIZE, tree_y * TILE_SIZE))
                    occupied.add((tree_x, tree_y))
                    placed += 1
            
            attempts += 1
    
    def _draw_decorative_objects(self, surface: pygame.Surface, width: int, height: int):
        """Dibuja objetos decorativos variados"""
        occupied = set()
        path_center_x = width // 2
        path_center_y = height // 2
        
        # Marcar caminos como ocupados
        for x in range(width):
            for y in range(height):
                if abs(x - path_center_x) < 3 or abs(y - path_center_y) < 3:
                    occupied.add((x, y))
        
        # Colocar objetos de cada tileset
        for tileset_name, object_list in self.object_tiles.items():
            if not object_list:
                continue
            
            # Colocar algunos objetos aleatoriamente
            for _ in range(8):  # 8 objetos por tileset
                obj_x = random.randint(1, width - 2)
                obj_y = random.randint(1, height - 2)
                
                if (obj_x, obj_y) not in occupied:
                    obj_tile = random.choice(object_list)
                    surface.blit(obj_tile, (obj_x * TILE_SIZE, obj_y * TILE_SIZE))
                    occupied.add((obj_x, obj_y))


class VillageMapRenderer:
    """Renderiza el mapa de pueblo generado"""
    
    def __init__(self, village_surface: pygame.Surface, width: int, height: int):
        """
        Inicializa el renderizador
        
        Args:
            village_surface: Superficie con el mapa generado
            width: Ancho del mapa en tiles
            height: Alto del mapa en tiles
        """
        self.village_surface = village_surface
        self.width = width
        self.height = height
        self.map_width_px = width * TILE_SIZE
        self.map_height_px = height * TILE_SIZE
    
    def render(self, screen: pygame.Surface, camera_rect: pygame.Rect):
        """
        Renderiza el mapa visible
        
        Args:
            screen: Superficie donde renderizar
            camera_rect: Rectángulo de la cámara
        """
        # Calcular qué parte del mapa es visible
        start_x = max(0, camera_rect.x)
        start_y = max(0, camera_rect.y)
        end_x = min(self.map_width_px, camera_rect.x + camera_rect.width)
        end_y = min(self.map_height_px, camera_rect.y + camera_rect.height)
        
        # Dibujar la porción visible
        screen.blit(self.village_surface, 
                   (start_x - camera_rect.x, start_y - camera_rect.y),
                   (start_x, start_y, end_x - start_x, end_y - start_y))
    
    def check_collision(self, rect: pygame.Rect) -> bool:
        """
        Verifica colisiones (por ahora retorna False, se puede mejorar)
        
        Args:
            rect: Rectángulo a verificar
            
        Returns:
            True si hay colisión
        """
        # Por ahora, no hay colisiones (se puede agregar después)
        return False
