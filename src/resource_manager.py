"""
Gestor de recursos - carga y caché de assets
"""

import pygame
import os
from typing import Dict, Optional
from src.config import ASSETS_DIR


class ResourceManager:
    """Maneja la carga y caché de todos los recursos del juego"""
    
    def __init__(self):
        self._images: Dict[str, pygame.Surface] = {}
        self._sounds: Dict[str, pygame.mixer.Sound] = {}
        self._fonts: Dict[str, pygame.font.Font] = {}
        self._music: Dict[str, str] = {}  # Paths a archivos de música
        
    def load_image(self, path: str, use_alpha: bool = True) -> pygame.Surface:
        """
        Carga una imagen y la guarda en caché
        
        Args:
            path: Ruta relativa desde assets/ (ej: "sprites/player.png")
            use_alpha: Si True, convierte a formato con alpha
            
        Returns:
            Superficie de Pygame
        """
        full_path = os.path.join(ASSETS_DIR, path)
        
        # Si ya está en caché, devolverla
        if path in self._images:
            return self._images[path]
        
        # Cargar imagen
        try:
            image = pygame.image.load(full_path)
            if use_alpha:
                image = image.convert_alpha()
            else:
                image = image.convert()
            
            self._images[path] = image
            return image
            
        except pygame.error as e:
            print(f"Error cargando imagen {full_path}: {e}")
            # Devolver una superficie vacía como fallback
            return pygame.Surface((32, 32))
    
    def load_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        """
        Carga un sonido y lo guarda en caché
        
        Args:
            path: Ruta relativa desde assets/audio/
            
        Returns:
            Sound de Pygame o None si hay error
        """
        full_path = os.path.join(ASSETS_DIR, "audio", path)
        
        if path in self._sounds:
            return self._sounds[path]
        
        try:
            sound = pygame.mixer.Sound(full_path)
            self._sounds[path] = sound
            return sound
        except pygame.error as e:
            print(f"Error cargando sonido {full_path}: {e}")
            return None
    
    def load_font(self, name: str, size: int) -> pygame.font.Font:
        """
        Carga una fuente
        
        Args:
            name: Nombre de la fuente o path al archivo .ttf
            size: Tamaño de la fuente
            
        Returns:
            Font de Pygame
        """
        key = f"{name}_{size}"
        
        if key in self._fonts:
            return self._fonts[key]
        
        try:
            # Intentar cargar como archivo primero
            font_path = os.path.join(ASSETS_DIR, "ui", "fonts", name)
            if os.path.exists(font_path):
                font = pygame.font.Font(font_path, size)
            else:
                # Usar fuente del sistema
                font = pygame.font.Font(name, size)
            
            self._fonts[key] = font
            return font
        except Exception as e:
            print(f"Error cargando fuente {name}: {e}")
            # Fallback a fuente por defecto
            return pygame.font.Font(None, size)
    
    def load_music(self, path: str) -> str:
        """
        Registra el path de una música (las músicas se cargan diferente en Pygame)
        
        Args:
            path: Ruta relativa desde assets/audio/
            
        Returns:
            Path completo al archivo de música
        """
        full_path = os.path.join(ASSETS_DIR, "audio", path)
        self._music[path] = full_path
        return full_path
    
    def get_image(self, path: str) -> Optional[pygame.Surface]:
        """Obtiene una imagen del caché sin cargarla si no existe"""
        return self._images.get(path)
    
    def clear_cache(self):
        """Limpia todos los cachés (útil para liberar memoria)"""
        self._images.clear()
        self._sounds.clear()
        self._fonts.clear()
        self._music.clear()

