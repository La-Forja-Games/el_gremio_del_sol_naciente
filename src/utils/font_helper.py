"""
Helper para cargar fuentes góticas/medievales épicas
"""

import pygame
import os
from src.config import ASSETS_DIR, EPIC_FONTS, SYSTEM_EPIC_FONTS


def get_epic_font(size: int, bold: bool = False) -> pygame.font.Font:
    """
    Obtiene la fuente BLKCHCRY para el juego
    
    Args:
        size: Tamaño de la fuente
        bold: Si True, intenta usar una fuente en negrita
        
    Returns:
        Font de Pygame con la fuente BLKCHCRY
    """
    from src.config import MAIN_FONT
    
    # Primero intentar cargar BLKCHCRY desde archivo personalizado
    # Buscar directamente en la carpeta de fuentes
    fonts_dir = os.path.join(ASSETS_DIR, "ui", "fonts")
    
    # Lista de nombres posibles para el archivo
    possible_names = ["BLKCHCRY.TTF", "blkchcry.ttf", "BLKCHCRY.ttf", "Blkchcry.ttf"]
    
    for font_name in possible_names:
        font_path = os.path.join(fonts_dir, font_name)
        if os.path.exists(font_path):
            try:
                font = pygame.font.Font(font_path, size)
                if bold:
                    font.set_bold(True)
                print(f"[OK] Fuente BLKCHCRY cargada desde archivo: {font_path}")
                return font
            except Exception as e:
                print(f"[ERROR] Error cargando fuente {font_path}: {e}")
                continue
    
    # También intentar desde EPIC_FONTS (por si acaso)
    for font_path in EPIC_FONTS:
        # Remover "assets/" del inicio si existe
        if font_path.startswith("assets/"):
            relative_path = font_path[7:]  # Remover "assets/"
        else:
            relative_path = font_path
        
        full_path = os.path.join(ASSETS_DIR, relative_path)
        
        if os.path.exists(full_path):
            try:
                font = pygame.font.Font(full_path, size)
                if bold:
                    font.set_bold(True)
                print(f"[OK] Fuente BLKCHCRY cargada desde archivo: {full_path}")
                return font
            except Exception as e:
                print(f"[ERROR] Error cargando fuente {full_path}: {e}")
                continue
    
    # Intentar cargar BLKCHCRY como fuente del sistema
    try:
        font = pygame.font.SysFont(MAIN_FONT, size, bold=bold)
        # Verificar que la fuente se cargó correctamente
        test_surface = font.render("Test", True, (255, 255, 255))
        if test_surface:
            print(f"[OK] Fuente BLKCHCRY cargada desde sistema")
            return font
    except Exception as e:
        print(f"[ERROR] Error cargando fuente BLKCHCRY del sistema: {e}")
    
    # Si BLKCHCRY no está disponible, intentar otras fuentes del sistema
    for font_name in SYSTEM_EPIC_FONTS:
        if font_name == MAIN_FONT:
            continue  # Ya intentamos BLKCHCRY
        try:
            font = pygame.font.SysFont(font_name, size, bold=bold)
            test_surface = font.render("Test", True, (255, 255, 255))
            if test_surface:
                print(f"Usando fuente alternativa: {font_name}")
                return font
        except Exception:
            continue
    
    # Último recurso: usar fuente por defecto pero en negrita si se solicita
    print("ADVERTENCIA: No se encontró BLKCHCRY, usando fuente por defecto")
    font = pygame.font.Font(None, size)
    if bold:
        font.set_bold(True)
    return font


def get_title_font(size: int = 72) -> pygame.font.Font:
    """Obtiene una fuente épica para títulos"""
    return get_epic_font(size, bold=True)


def get_normal_font(size: int = 24) -> pygame.font.Font:
    """Obtiene una fuente épica para texto normal"""
    return get_epic_font(size, bold=False)


def get_small_font(size: int = 18) -> pygame.font.Font:
    """Obtiene una fuente épica para texto pequeño"""
    return get_epic_font(size, bold=False)

