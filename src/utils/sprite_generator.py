"""
Generador de sprites básicos en pixel art
"""

import pygame
from src.config import TILE_SIZE


def create_player_sprite(direction: str = "down") -> pygame.Surface:
    """Crea un sprite básico del jugador (El Heredero)"""
    sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
    sprite.set_colorkey((0, 0, 0))  # Transparente
    
    # Cuerpo (poncho gris oscuro con detalle)
    pygame.draw.rect(sprite, (60, 60, 60), (8, 12, 16, 16))
    # Borde del poncho
    pygame.draw.rect(sprite, (40, 40, 40), (8, 12, 16, 16), 1)
    # Emblema del sol en el pecho
    pygame.draw.circle(sprite, (255, 200, 0), (16, 20), 4)
    pygame.draw.circle(sprite, (255, 150, 0), (16, 20), 2)
    
    # Cabeza
    pygame.draw.rect(sprite, (255, 220, 177), (10, 4, 12, 10))
    # Cabello marrón
    pygame.draw.rect(sprite, (101, 67, 33), (10, 4, 12, 6))
    # Ojos
    pygame.draw.rect(sprite, (50, 50, 50), (12, 7, 2, 2))
    pygame.draw.rect(sprite, (50, 50, 50), (18, 7, 2, 2))
    
    # Facón (según dirección)
    if direction == "right":
        pygame.draw.rect(sprite, (200, 200, 200), (22, 16, 2, 8))
        pygame.draw.rect(sprite, (150, 100, 50), (24, 18, 1, 4))  # Empuñadura
    elif direction == "left":
        pygame.draw.rect(sprite, (200, 200, 200), (6, 16, 2, 8))
        pygame.draw.rect(sprite, (150, 100, 50), (5, 18, 1, 4))
    else:
        pygame.draw.rect(sprite, (200, 200, 200), (22, 16, 2, 8))
        pygame.draw.rect(sprite, (150, 100, 50), (24, 18, 1, 4))
    
    # Botas
    pygame.draw.rect(sprite, (80, 50, 20), (10, 26, 6, 6))
    pygame.draw.rect(sprite, (80, 50, 20), (18, 26, 6, 6))
    # Suela de las botas
    pygame.draw.rect(sprite, (50, 30, 10), (10, 30, 6, 2))
    pygame.draw.rect(sprite, (50, 30, 10), (18, 30, 6, 2))
    
    return sprite


def create_player_walking_frame(direction: str = "down", frame: int = 0) -> pygame.Surface:
    """Crea un frame de caminata del jugador"""
    sprite = create_player_sprite(direction)
    
    # Animación de piernas (alternar posición)
    if frame % 2 == 0:
        # Pierna izquierda adelante
        pygame.draw.rect(sprite, (80, 50, 20), (10, 26, 4, 6))
        pygame.draw.rect(sprite, (80, 50, 20), (20, 28, 4, 4))
    else:
        # Pierna derecha adelante
        pygame.draw.rect(sprite, (80, 50, 20), (18, 26, 4, 6))
        pygame.draw.rect(sprite, (80, 50, 20), (10, 28, 4, 4))
    
    return sprite


def create_enemy_sprite(color=(200, 0, 0), enemy_type: str = "spirit") -> pygame.Surface:
    """Crea un sprite básico de enemigo"""
    sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
    sprite.set_colorkey((0, 0, 0))
    
    if enemy_type == "spirit":
        # Espíritu (forma etérea)
        pygame.draw.ellipse(sprite, color, (6, 8, 20, 20))
        # Brillo interno
        pygame.draw.ellipse(sprite, tuple(min(255, c + 50) for c in color), (10, 12, 12, 12))
        # Ojos brillantes
        pygame.draw.rect(sprite, (255, 255, 255), (12, 14, 2, 2))
        pygame.draw.rect(sprite, (255, 255, 255), (18, 14, 2, 2))
        # Partículas flotantes
        for i in range(3):
            pygame.draw.circle(sprite, color, (8 + i*8, 6), 1)
    else:
        # Bestia normal
        # Cuerpo
        pygame.draw.rect(sprite, color, (8, 10, 16, 18))
        pygame.draw.rect(sprite, tuple(max(0, c - 30) for c in color), (8, 10, 16, 18), 1)
        # Cabeza
        pygame.draw.rect(sprite, (150, 100, 100), (10, 4, 12, 8))
        # Ojos rojos
        pygame.draw.rect(sprite, (255, 0, 0), (12, 6, 2, 2))
        pygame.draw.rect(sprite, (255, 0, 0), (18, 6, 2, 2))
        # Patas
        pygame.draw.rect(sprite, color, (10, 26, 4, 6))
        pygame.draw.rect(sprite, color, (18, 26, 4, 6))
    
    return sprite


def create_grass_tile() -> pygame.Surface:
    """Crea un tile de césped"""
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    
    # Base verde
    tile.fill((100, 150, 80))
    
    # Variaciones de verde para textura
    for i in range(0, TILE_SIZE, 4):
        for j in range(0, TILE_SIZE, 4):
            if (i + j) % 8 == 0:
                pygame.draw.rect(tile, (120, 170, 100), (i, j, 2, 2))
    
    # Pequeñas flores blancas
    pygame.draw.circle(tile, (255, 255, 255), (8, 8), 1)
    pygame.draw.circle(tile, (255, 255, 255), (24, 16), 1)
    
    return tile


def create_dirt_tile() -> pygame.Surface:
    """Crea un tile de tierra"""
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    
    # Base marrón
    tile.fill((139, 90, 43))
    
    # Textura
    for i in range(0, TILE_SIZE, 3):
        for j in range(0, TILE_SIZE, 3):
            if (i + j) % 6 == 0:
                pygame.draw.rect(tile, (120, 75, 35), (i, j, 2, 1))
    
    return tile


def create_water_tile() -> pygame.Surface:
    """Crea un tile de agua"""
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    
    # Base azul
    tile.fill((50, 100, 200))
    
    # Ondas
    for i in range(0, TILE_SIZE, 4):
        pygame.draw.line(tile, (70, 120, 220), (i, TILE_SIZE // 2), 
                         (i + 2, TILE_SIZE // 2 + 2), 1)
    
    return tile


def create_snow_tile() -> pygame.Surface:
    """Crea un tile de nieve"""
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    
    # Base blanca
    tile.fill((240, 240, 255))
    
    # Textura de nieve
    for i in range(0, TILE_SIZE, 2):
        for j in range(0, TILE_SIZE, 2):
            if (i + j) % 4 == 0:
                pygame.draw.rect(tile, (255, 255, 255), (i, j, 1, 1))
    
    return tile


def create_stone_tile() -> pygame.Surface:
    """Crea un tile de piedra"""
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    
    # Base gris
    tile.fill((120, 120, 120))
    
    # Textura de piedra
    pygame.draw.rect(tile, (100, 100, 100), (0, 0, TILE_SIZE, 2))
    pygame.draw.rect(tile, (100, 100, 100), (0, 0, 2, TILE_SIZE))
    pygame.draw.rect(tile, (140, 140, 140), (TILE_SIZE - 2, 0, 2, TILE_SIZE))
    pygame.draw.rect(tile, (140, 140, 140), (0, TILE_SIZE - 2, TILE_SIZE, 2))
    
    return tile


def create_tree_sprite() -> pygame.Surface:
    """Crea un sprite de árbol"""
    sprite = pygame.Surface((TILE_SIZE, TILE_SIZE * 2))
    sprite.set_colorkey((0, 0, 0))
    
    # Tronco
    pygame.draw.rect(sprite, (101, 67, 33), (12, 20, 8, 12))
    # Textura del tronco
    pygame.draw.line(sprite, (80, 50, 20), (14, 22), (14, 30), 1)
    pygame.draw.line(sprite, (80, 50, 20), (18, 22), (18, 30), 1)
    
    # Copa (verde oscuro con capas)
    pygame.draw.ellipse(sprite, (34, 139, 34), (4, 4, 24, 20))
    pygame.draw.ellipse(sprite, (0, 100, 0), (6, 6, 20, 16))
    # Detalles de hojas
    for i in range(3):
        pygame.draw.circle(sprite, (50, 150, 50), (8 + i*8, 10), 2)
    
    return sprite


def create_campfire_sprite() -> pygame.Surface:
    """Crea un sprite de fogata"""
    sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
    sprite.set_colorkey((0, 0, 0))
    
    # Leña
    pygame.draw.rect(sprite, (101, 67, 33), (10, 20, 12, 8))
    pygame.draw.line(sprite, (80, 50, 20), (12, 20), (16, 28), 2)
    pygame.draw.line(sprite, (80, 50, 20), (20, 20), (16, 28), 2)
    
    # Fuego (naranja/amarillo)
    pygame.draw.polygon(sprite, (255, 150, 0), [(16, 18), (12, 22), (16, 20), (20, 22)])
    pygame.draw.polygon(sprite, (255, 200, 0), [(16, 19), (13, 21), (16, 20), (19, 21)])
    pygame.draw.circle(sprite, (255, 255, 0), (16, 20), 2)
    
    return sprite


def create_chest_sprite(open: bool = False) -> pygame.Surface:
    """Crea un sprite de cofre"""
    sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
    sprite.set_colorkey((0, 0, 0))
    
    # Cofre cerrado
    pygame.draw.rect(sprite, (139, 90, 43), (8, 16, 16, 12))
    # Bandas metálicas
    pygame.draw.rect(sprite, (150, 150, 150), (8, 18, 16, 2))
    pygame.draw.rect(sprite, (150, 150, 150), (8, 24, 16, 2))
    # Cerradura
    pygame.draw.circle(sprite, (200, 200, 0), (16, 22), 3)
    
    if open:
        # Tapa abierta
        pygame.draw.polygon(sprite, (120, 75, 35), [(8, 16), (24, 16), (20, 12), (12, 12)])
        # Interior oscuro
        pygame.draw.rect(sprite, (30, 20, 10), (10, 18, 12, 8))
    
    return sprite


def create_rock_sprite() -> pygame.Surface:
    """Crea un sprite de roca"""
    sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
    sprite.set_colorkey((0, 0, 0))
    
    # Roca gris
    pygame.draw.ellipse(sprite, (100, 100, 100), (4, 8, 24, 20))
    pygame.draw.ellipse(sprite, (80, 80, 80), (6, 10, 20, 16))
    # Sombras
    pygame.draw.ellipse(sprite, (60, 60, 60), (8, 12, 16, 12))
    
    return sprite

