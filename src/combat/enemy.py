"""
Clase base para enemigos
"""

import json
import os
import pygame
from typing import Dict, Optional, List
from src.config import DATA_DIR, TILE_SIZE
from src.entities.character import Character
from src.entities.animation import Direction


class Enemy(Character):
    """Clase base para enemigos"""
    
    def __init__(self, x: float, y: float, enemy_id: int, resource_manager=None):
        """
        Inicializa un enemigo
        
        Args:
            x: Posición X inicial
            y: Posición Y inicial
            enemy_id: ID del enemigo (para cargar datos de JSON)
            resource_manager: Instancia de ResourceManager
        """
        super().__init__(x, y, character_id=None, resource_manager=resource_manager)
        self.enemy_id = enemy_id
        
        # Cargar datos del enemigo
        self._load_enemy_data(enemy_id)
        
        # Información del enemigo
        self.nombre = "Enemigo"
        self.tipo = "Normal"
        self.elemento = None
        self.exp_reward = 0
        self.loot_table = []
        self.habilidades = []
        
        # AI
        self.ai_type = "basic"  # basic, aggressive, defensive, etc.
        
        # Sprite placeholder
        self._create_placeholder_sprite()
    
    def _load_enemy_data(self, enemy_id: int):
        """Carga los datos del enemigo desde JSON"""
        try:
            enemy_file = os.path.join(DATA_DIR, "enemies", "enemies_base.json")
            with open(enemy_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Buscar el enemigo por ID
            for enemy_data in data.get("enemies", []):
                if enemy_data.get("id") == enemy_id:
                    self.nombre = enemy_data.get("nombre", "Enemigo")
                    self.tipo = enemy_data.get("tipo", "Normal")
                    self.elemento = enemy_data.get("elemento", None)
                    self.exp_reward = enemy_data.get("exp_reward", 0)
                    self.loot_table = enemy_data.get("loot_table", [])
                    self.habilidades = enemy_data.get("habilidades", [])
                    
                    # Cargar stats
                    stats = enemy_data.get("stats", {})
                    self.base_stats = {
                        "HP": stats.get("HP", 50),
                        "MP": stats.get("MP", 20),
                        "ATK": stats.get("ATK", 10),
                        "DEF": stats.get("DEF", 5),
                        "VEL": stats.get("VEL", 8),
                        "MAG": stats.get("MAG", 5)
                    }
                    self.stats = self.base_stats.copy()
                    self.max_hp = self.stats["HP"]
                    self.max_mp = self.stats["MP"]
                    break
        except Exception as e:
            print(f"Error cargando datos del enemigo {enemy_id}: {e}")
    
    def _create_placeholder_sprite(self):
        """Crea un sprite placeholder temporal"""
        from src.utils.sprite_generator import create_enemy_sprite
        from src.entities.animation import Animation
        
        # Color según el tipo de enemigo
        if self.elemento == "Hielo":
            color = (150, 200, 255)  # Azul claro
            enemy_type = "spirit"
        elif self.elemento == "Fuego":
            color = (255, 100, 50)  # Naranja/rojo
            enemy_type = "spirit"
        else:
            color = (200, 0, 0)  # Rojo por defecto
            enemy_type = "beast"
        
        # Crear sprites con animación (pulsación para espíritus)
        if enemy_type == "spirit":
            frames = []
            for i in range(4):
                # Variar el tamaño para efecto de pulsación
                frame = create_enemy_sprite(color, enemy_type)
                if i % 2 == 1:
                    # Frame más grande (pulsación)
                    frame_scaled = pygame.transform.scale(frame, (TILE_SIZE + 2, TILE_SIZE + 2))
                    frame = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    frame.set_colorkey((0, 0, 0))
                    frame.blit(frame_scaled, (-1, -1))
                frames.append(frame)
            anim = Animation(frames, speed=0.2)
            self.image = frames[0]
        else:
            # Animación simple para bestias
            sprite = create_enemy_sprite(color, enemy_type)
            anim = Animation([sprite], speed=0.3)
            self.image = sprite
        
        # Crear animaciones para todas las direcciones
        self.animations = {
            Direction.DOWN: anim,
            Direction.UP: anim,
            Direction.LEFT: anim,
            Direction.RIGHT: anim
        }
        self.current_animation = anim

