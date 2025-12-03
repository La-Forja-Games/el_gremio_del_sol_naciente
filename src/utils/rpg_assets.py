"""
RPG Pixel Art Asset Library
Sistema completo para gestionar todos los assets del juego
"""

import pygame
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from src.config import ASSETS_DIR


class RPGAssetLibrary:
    """
    Biblioteca principal para gestionar todos los assets RPG pixel art
    """
    
    def __init__(self, resource_manager=None):
        """
        Inicializa la biblioteca de assets
        
        Args:
            resource_manager: ResourceManager del juego (opcional)
        """
        self.resource_manager = resource_manager
        self.base_path = ASSETS_DIR
        
        # Cachés de assets
        self._items_cache: Dict[str, Dict] = {}
        self._characters_cache: Dict[str, Dict] = {}
        self._enemies_cache: Dict[str, Dict] = {}
        self._tilesets_cache: Dict[str, pygame.Surface] = {}
        self._animations_cache: Dict[str, List[pygame.Surface]] = {}
        self._ui_cache: Dict[str, pygame.Surface] = {}
        
        # Registro de assets disponibles
        self._asset_registry = {
            'items': self._scan_items(),
            'characters': self._scan_characters(),
            'enemies': self._scan_enemies(),
            'tilesets': self._scan_tilesets(),
            'animations': self._scan_animations(),
            'ui': self._scan_ui()
        }
        
        print(f"[OK] RPG Asset Library initialized")
        print(f"  - Items: {len(self._asset_registry['items'])}")
        print(f"  - Characters: {len(self._asset_registry['characters'])}")
        print(f"  - Enemies: {len(self._asset_registry['enemies'])}")
        print(f"  - Tilesets: {len(self._asset_registry['tilesets'])}")
        print(f"  - Animations: {len(self._asset_registry['animations'])}")
        print(f"  - UI Elements: {len(self._asset_registry['ui'])}")
    
    # ==================== ITEMS ====================
    
    def _scan_items(self) -> Dict[str, List[str]]:
        """Escanea y registra todos los items disponibles"""
        items_dir = Path(self.base_path) / "sprites" / "items"
        registry = {}
        
        if not items_dir.exists():
            return registry
        
        for item_dir in items_dir.iterdir():
            if item_dir.is_dir():
                item_name = item_dir.name
                files = []
                
                # Buscar spritesheet
                spritesheet = item_dir / f"{item_name}_spritesheet.png"
                if spritesheet.exists():
                    files.append(str(spritesheet.relative_to(self.base_path)))
                
                # Buscar frames individuales
                for file in sorted(item_dir.glob(f"{item_name}_*.png")):
                    if "spritesheet" not in file.name:
                        files.append(str(file.relative_to(self.base_path)))
                
                # Buscar animación GIF
                gif = item_dir / f"{item_name}_animation.gif"
                if gif.exists():
                    files.append(str(gif.relative_to(self.base_path)))
                
                if files:
                    registry[item_name] = files
        
        return registry
    
    def get_item(self, item_name: str, frame: int = 0) -> Optional[pygame.Surface]:
        """
        Obtiene un sprite de item
        
        Args:
            item_name: Nombre del item (apple, coin, gem, etc.)
            frame: Frame de animación (0 = primer frame)
            
        Returns:
            Superficie del sprite o None
        """
        cache_key = f"{item_name}_{frame}"
        
        if cache_key in self._items_cache:
            return self._items_cache[cache_key]
        
        if item_name not in self._asset_registry['items']:
            print(f"[ERROR] Item '{item_name}' no encontrado")
            return None
        
        files = self._asset_registry['items'][item_name]
        
        # Priorizar spritesheet si existe
        spritesheet_path = None
        for f in files:
            if "spritesheet" in f:
                spritesheet_path = f
                break
        
        if spritesheet_path and self.resource_manager:
            # Cargar spritesheet y extraer frame
            sheet = self.resource_manager.load_image(spritesheet_path)
            if sheet:
                # Asumir que el spritesheet tiene frames en fila
                # Esto puede necesitar ajuste según el layout real
                frame_width = sheet.get_width() // 4  # Ajustar según necesidad
                x = (frame % 4) * frame_width
                rect = pygame.Rect(x, 0, frame_width, sheet.get_height())
                frame_surface = sheet.subsurface(rect)
                self._items_cache[cache_key] = frame_surface
                return frame_surface
        
        # Si no hay spritesheet, usar frames individuales
        if files and frame < len(files):
            file_path = files[frame]
            if self.resource_manager:
                surface = self.resource_manager.load_image(file_path)
                if surface:
                    self._items_cache[cache_key] = surface
                    return surface
        
        return None
    
    def get_item_animation(self, item_name: str) -> List[pygame.Surface]:
        """
        Obtiene todos los frames de animación de un item
        
        Args:
            item_name: Nombre del item
            
        Returns:
            Lista de superficies (frames)
        """
        if item_name not in self._asset_registry['items']:
            return []
        
        files = self._asset_registry['items'][item_name]
        frames = []
        
        # Excluir spritesheet y GIF, usar frames individuales
        for file_path in files:
            if "spritesheet" not in file_path and "animation" not in file_path:
                if self.resource_manager:
                    surface = self.resource_manager.load_image(file_path)
                    if surface:
                        frames.append(surface)
        
        return frames
    
    # ==================== CHARACTERS ====================
    
    def _scan_characters(self) -> Dict[str, List[str]]:
        """Escanea y registra todos los personajes disponibles"""
        chars_dir = Path(self.base_path) / "sprites" / "characters"
        registry = {}
        
        if not chars_dir.exists():
            return registry
        
        for char_dir in chars_dir.iterdir():
            if char_dir.is_dir():
                char_name = char_dir.name
                files = []
                
                for file in sorted(char_dir.glob("*.png")):
                    files.append(str(file.relative_to(self.base_path)))
                
                if files:
                    registry[char_name] = files
        
        return registry
    
    def get_character_sprite(self, char_name: str, animation: str = "Idle") -> Optional[pygame.Surface]:
        """
        Obtiene un sprite de personaje por animación
        
        Args:
            char_name: Nombre del personaje (knight, wizard)
            animation: Tipo de animación (Idle, Run, Attack01, etc.)
            
        Returns:
            Superficie del sprite o None
        """
        cache_key = f"{char_name}_{animation}"
        
        if cache_key in self._characters_cache:
            return self._characters_cache[cache_key]
        
        if char_name not in self._asset_registry['characters']:
            print(f"[ERROR] Character '{char_name}' no encontrado")
            return None
        
        files = self._asset_registry['characters'][char_name]
        
        # Buscar archivo que contenga el nombre de la animación
        for file_path in files:
            if animation.lower() in file_path.lower():
                if self.resource_manager:
                    surface = self.resource_manager.load_image(file_path)
                    if surface:
                        self._characters_cache[cache_key] = surface
                        return surface
        
        # Fallback: primer archivo
        if files:
            if self.resource_manager:
                surface = self.resource_manager.load_image(files[0])
                if surface:
                    return surface
        
        return None
    
    def get_character_animation(self, char_name: str, animation: str) -> List[pygame.Surface]:
        """
        Obtiene todos los frames de una animación de personaje
        
        Args:
            char_name: Nombre del personaje
            animation: Tipo de animación
            
        Returns:
            Lista de frames
        """
        if char_name not in self._asset_registry['characters']:
            return []
        
        files = self._asset_registry['characters'][char_name]
        frames = []
        
        # Buscar todos los archivos relacionados con la animación
        for file_path in files:
            if animation.lower() in file_path.lower():
                if self.resource_manager:
                    surface = self.resource_manager.load_image(file_path)
                    if surface:
                        frames.append(surface)
        
        return frames
    
    # ==================== ENEMIES ====================
    
    def _scan_enemies(self) -> Dict[str, List[str]]:
        """Escanea y registra todos los enemigos disponibles"""
        enemies_dir = Path(self.base_path) / "sprites" / "enemies"
        registry = {}
        
        if not enemies_dir.exists():
            return registry
        
        for enemy_dir in enemies_dir.iterdir():
            if enemy_dir.is_dir():
                enemy_name = enemy_dir.name
                files = []
                
                for file in sorted(enemy_dir.glob("*.png")):
                    files.append(str(file.relative_to(self.base_path)))
                
                if files:
                    registry[enemy_name] = files
        
        return registry
    
    def get_enemy_sprite(self, enemy_name: str, animation: str = "Idle") -> Optional[pygame.Surface]:
        """
        Obtiene un sprite de enemigo por animación
        
        Args:
            enemy_name: Nombre del enemigo (skeleton, slime, mushroom, boss)
            animation: Tipo de animación (Idle, Walk, Attack, etc.)
            
        Returns:
            Superficie del sprite o None
        """
        cache_key = f"{enemy_name}_{animation}"
        
        if cache_key in self._enemies_cache:
            return self._enemies_cache[cache_key]
        
        if enemy_name not in self._asset_registry['enemies']:
            print(f"[ERROR] Enemy '{enemy_name}' no encontrado")
            return None
        
        files = self._asset_registry['enemies'][enemy_name]
        
        # Buscar archivo que contenga el nombre de la animación
        for file_path in files:
            if animation.lower() in file_path.lower():
                if self.resource_manager:
                    surface = self.resource_manager.load_image(file_path)
                    if surface:
                        self._enemies_cache[cache_key] = surface
                        return surface
        
        # Fallback: primer archivo
        if files:
            if self.resource_manager:
                surface = self.resource_manager.load_image(files[0])
                if surface:
                    return surface
        
        return None
    
    # ==================== TILESETS ====================
    
    def _scan_tilesets(self) -> List[str]:
        """Escanea y registra todos los tilesets disponibles"""
        tilesets_dir = Path(self.base_path) / "tilesets"
        registry = []
        
        if not tilesets_dir.exists():
            return registry
        
        for file in tilesets_dir.glob("*.png"):
            registry.append(str(file.relative_to(self.base_path)))
        
        return registry
    
    def get_tileset(self, tileset_name: str) -> Optional[pygame.Surface]:
        """
        Obtiene un tileset
        
        Args:
            tileset_name: Nombre del tileset (con o sin extensión)
            
        Returns:
            Superficie del tileset o None
        """
        if tileset_name in self._tilesets_cache:
            return self._tilesets_cache[tileset_name]
        
        # Buscar en el registro
        for tileset_path in self._asset_registry['tilesets']:
            if tileset_name in tileset_path:
                if self.resource_manager:
                    surface = self.resource_manager.load_image(tileset_path)
                    if surface:
                        self._tilesets_cache[tileset_name] = surface
                        return surface
        
        return None
    
    # ==================== ANIMATIONS ====================
    
    def _scan_animations(self) -> List[str]:
        """Escanea y registra todas las animaciones disponibles"""
        anim_dir = Path(self.base_path) / "animations"
        registry = []
        
        if not anim_dir.exists():
            return registry
        
        for file in anim_dir.glob("*"):
            registry.append(str(file.relative_to(self.base_path)))
        
        return registry
    
    # ==================== UI ====================
    
    def _scan_ui(self) -> List[str]:
        """Escanea y registra todos los elementos de UI"""
        ui_dir = Path(self.base_path) / "ui" / "hud"
        registry = []
        
        if not ui_dir.exists():
            return registry
        
        for file in ui_dir.glob("*.png"):
            registry.append(str(file.relative_to(self.base_path)))
        
        return registry
    
    def get_ui_element(self, ui_name: str) -> Optional[pygame.Surface]:
        """
        Obtiene un elemento de UI
        
        Args:
            ui_name: Nombre del elemento UI
            
        Returns:
            Superficie del elemento o None
        """
        if ui_name in self._ui_cache:
            return self._ui_cache[ui_name]
        
        # Buscar en el registro
        for ui_path in self._asset_registry['ui']:
            if ui_name.lower() in ui_path.lower():
                if self.resource_manager:
                    surface = self.resource_manager.load_image(ui_path)
                    if surface:
                        self._ui_cache[ui_name] = surface
                        return surface
        
        return None
    
    # ==================== UTILITY METHODS ====================
    
    def list_available_items(self) -> List[str]:
        """Lista todos los items disponibles"""
        return list(self._asset_registry['items'].keys())
    
    def list_available_characters(self) -> List[str]:
        """Lista todos los personajes disponibles"""
        return list(self._asset_registry['characters'].keys())
    
    def list_available_enemies(self) -> List[str]:
        """Lista todos los enemigos disponibles"""
        return list(self._asset_registry['enemies'].keys())
    
    def list_available_tilesets(self) -> List[str]:
        """Lista todos los tilesets disponibles"""
        return [Path(p).stem for p in self._asset_registry['tilesets']]
    
    def clear_cache(self):
        """Limpia todos los cachés"""
        self._items_cache.clear()
        self._characters_cache.clear()
        self._enemies_cache.clear()
        self._tilesets_cache.clear()
        self._animations_cache.clear()
        self._ui_cache.clear()
        print("[OK] Asset caches cleared")

