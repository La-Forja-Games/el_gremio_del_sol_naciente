"""
Sistema de elementos UI estilo RPG
"""

import pygame
from typing import Optional, Tuple
from src.config import ASSETS_DIR
import os


class UIElement:
    """Clase base para elementos UI"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True
    
    def render(self, screen: pygame.Surface):
        """Renderiza el elemento"""
        pass
    
    def handle_event(self, event) -> bool:
        """Maneja eventos, retorna True si el evento fue procesado"""
        return False


class UIFrame:
    """Frame decorativo estilo RPG"""
    
    def __init__(self, resource_manager, frame_type: str = "golden"):
        """
        Inicializa un frame UI
        
        Args:
            resource_manager: ResourceManager del juego
            frame_type: Tipo de frame ("golden", "grey", "simple")
        """
        self.resource_manager = resource_manager
        self.frame_type = frame_type
        self.corner_tl = None  # Top-left corner
        self.corner_tr = None  # Top-right corner
        self.corner_bl = None  # Bottom-left corner
        self.corner_br = None  # Bottom-right corner
        self.edge_h = None  # Horizontal edge
        self.edge_v = None  # Vertical edge
        self.fill = None  # Fill/background
        
        self._load_frame_parts()
    
    def _load_frame_parts(self):
        """Carga las partes del frame desde assets"""
        base_path = f"ui/frames/{self.frame_type}"
        
        # Intentar cargar partes del frame
        if self.resource_manager:
            self.corner_tl = self.resource_manager.load_image(f"{base_path}/corner_tl.png", use_alpha=True)
            self.corner_tr = self.resource_manager.load_image(f"{base_path}/corner_tr.png", use_alpha=True)
            self.corner_bl = self.resource_manager.load_image(f"{base_path}/corner_bl.png", use_alpha=True)
            self.corner_br = self.resource_manager.load_image(f"{base_path}/corner_br.png", use_alpha=True)
            self.edge_h = self.resource_manager.load_image(f"{base_path}/edge_h.png", use_alpha=True)
            self.edge_v = self.resource_manager.load_image(f"{base_path}/edge_v.png", use_alpha=True)
            self.fill = self.resource_manager.load_image(f"{base_path}/fill.png", use_alpha=False)
    
    def render(self, screen: pygame.Surface, rect: pygame.Rect):
        """
        Renderiza el frame alrededor de un rectángulo
        
        Args:
            screen: Superficie donde renderizar
            rect: Rectángulo del frame
        """
        # Si no hay assets, usar fallback simple
        if not self.corner_tl:
            pygame.draw.rect(screen, (139, 69, 19), rect, 3)  # Borde marrón/dorado
            return
        
        # Renderizar frame con assets
        corner_size = self.corner_tl.get_width()
        
        # Esquinas
        screen.blit(self.corner_tl, (rect.x, rect.y))
        screen.blit(self.corner_tr, (rect.right - corner_size, rect.y))
        screen.blit(self.corner_bl, (rect.x, rect.bottom - corner_size))
        screen.blit(self.corner_br, (rect.right - corner_size, rect.bottom - corner_size))
        
        # Bordes horizontales
        if self.edge_h:
            edge_h_height = self.edge_h.get_height()
            for x in range(rect.x + corner_size, rect.right - corner_size, self.edge_h.get_width()):
                screen.blit(self.edge_h, (x, rect.y))
                screen.blit(pygame.transform.flip(self.edge_h, False, True), (x, rect.bottom - edge_h_height))
        
        # Bordes verticales
        if self.edge_v:
            edge_v_width = self.edge_v.get_width()
            for y in range(rect.y + corner_size, rect.bottom - corner_size, self.edge_v.get_height()):
                screen.blit(self.edge_v, (rect.x, y))
                screen.blit(pygame.transform.flip(self.edge_v, True, False), (rect.right - edge_v_width, y))
        
        # Relleno
        if self.fill:
            fill_rect = pygame.Rect(rect.x + corner_size, rect.y + corner_size,
                                  rect.width - corner_size * 2, rect.height - corner_size * 2)
            # Escalar y repetir el fill si es necesario
            for x in range(fill_rect.x, fill_rect.right, self.fill.get_width()):
                for y in range(fill_rect.y, fill_rect.bottom, self.fill.get_height()):
                    screen.blit(self.fill, (x, y))


class UIButton:
    """Botón estilo RPG"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 resource_manager=None, font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.resource_manager = resource_manager
        self.state = "normal"  # normal, hover, pressed
        self.visible = True
        self.enabled = True
        
        # Sprites del botón
        self.sprite_normal = None
        self.sprite_hover = None
        self.sprite_pressed = None
        
        self._load_button_sprites()
    
    def _load_button_sprites(self):
        """Carga los sprites del botón"""
        if self.resource_manager:
            # Intentar cargar sprites personalizados
            self.sprite_normal = self.resource_manager.load_image("ui/buttons/button_normal.png", use_alpha=True)
            self.sprite_hover = self.resource_manager.load_image("ui/buttons/button_hover.png", use_alpha=True)
            self.sprite_pressed = self.resource_manager.load_image("ui/buttons/button_pressed.png", use_alpha=True)
    
    def render(self, screen: pygame.Surface):
        """Renderiza el botón"""
        if not self.visible:
            return
        
        # Determinar qué sprite usar
        sprite = None
        if self.state == "pressed" and self.sprite_pressed:
            sprite = self.sprite_pressed
        elif self.state == "hover" and self.sprite_hover:
            sprite = self.sprite_hover
        elif self.sprite_normal:
            sprite = self.sprite_normal
        
        # Renderizar sprite o fallback
        if sprite:
            # Escalar sprite al tamaño del botón
            sprite_scaled = pygame.transform.scale(sprite, (self.rect.width, self.rect.height))
            screen.blit(sprite_scaled, self.rect)
        else:
            # Fallback: botón simple
            if self.state == "pressed":
                color = (100, 100, 100)
            elif self.state == "hover":
                color = (150, 150, 150)
            else:
                color = (120, 120, 120)
            
            pygame.draw.rect(screen, color, self.rect)
            pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
        
        # Renderizar texto
        if self.text and self.font:
            text_surface = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
    
    def handle_event(self, event) -> bool:
        """Maneja eventos del botón"""
        if not self.enabled or not self.visible:
            return False
        
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.state = "hover"
            else:
                self.state = "normal"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.state = "pressed"
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.state == "pressed" and self.rect.collidepoint(event.pos):
                self.state = "hover"
                return True
        
        return False


class ProgressBar:
    """Barra de progreso estilo RPG (HP, MP, EXP)"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 resource_manager=None, bar_type: str = "health"):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = 100  # 0-100
        self.max_value = 100
        self.resource_manager = resource_manager
        self.bar_type = bar_type  # health, mana, exp
        
        # Sprites
        self.bg_sprite = None
        self.fill_sprite = None
        
        self._load_bar_sprites()
    
    def _load_bar_sprites(self):
        """Carga los sprites de la barra"""
        if self.resource_manager:
            self.bg_sprite = self.resource_manager.load_image(f"ui/bars/{self.bar_type}_bg.png", use_alpha=True)
            self.fill_sprite = self.resource_manager.load_image(f"ui/bars/{self.bar_type}_fill.png", use_alpha=True)
    
    def render(self, screen: pygame.Surface):
        """Renderiza la barra de progreso"""
        # Color según tipo
        if self.bar_type == "health":
            fill_color = (200, 0, 0)  # Rojo
        elif self.bar_type == "mana":
            fill_color = (0, 100, 200)  # Azul
        elif self.bar_type == "exp":
            fill_color = (0, 200, 0)  # Verde
        else:
            fill_color = (150, 150, 150)  # Gris
        
        # Renderizar fondo
        if self.bg_sprite:
            bg_scaled = pygame.transform.scale(self.bg_sprite, (self.rect.width, self.rect.height))
            screen.blit(bg_scaled, self.rect)
        else:
            pygame.draw.rect(screen, (50, 50, 50), self.rect)
            pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)
        
        # Calcular ancho del fill
        fill_width = int((self.value / self.max_value) * self.rect.width)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            
            # Renderizar fill
            if self.fill_sprite:
                fill_scaled = pygame.transform.scale(self.fill_sprite, (fill_rect.width, fill_rect.height))
                screen.blit(fill_scaled, fill_rect)
            else:
                pygame.draw.rect(screen, fill_color, fill_rect)
                pygame.draw.rect(screen, (255, 255, 255), fill_rect, 1)

