"""
Sistema de partículas para efectos visuales
"""

import pygame
import random
from typing import List, Tuple
from src.config import TILE_SIZE


class Particle:
    """Representa una partícula individual"""
    
    def __init__(self, x: float, y: float, vx: float, vy: float, 
                 color: Tuple[int, int, int], lifetime: float, size: int = 2):
        """
        Inicializa una partícula
        
        Args:
            x, y: Posición inicial
            vx, vy: Velocidad
            color: Color RGB
            lifetime: Tiempo de vida en segundos
            size: Tamaño en píxeles
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.alpha = 255
    
    def update(self, dt: float) -> bool:
        """
        Actualiza la partícula
        
        Args:
            dt: Delta time
            
        Returns:
            True si la partícula sigue viva, False si debe ser removida
        """
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt
        
        # Fade out
        self.alpha = int(255 * (self.lifetime / self.max_lifetime))
        
        # Gravedad (para algunas partículas)
        self.vy += 50 * dt  # Gravedad suave
        
        return self.lifetime > 0
    
    def render(self, screen: pygame.Surface, camera_offset: Tuple[int, int] = (0, 0)):
        """Renderiza la partícula"""
        screen_x = int(self.x - camera_offset[0])
        screen_y = int(self.y - camera_offset[1])
        
        if 0 <= screen_x < screen.get_width() and 0 <= screen_y < screen.get_height():
            color_with_alpha = (*self.color, self.alpha)
            # Crear superficie con alpha
            particle_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color_with_alpha, (self.size, self.size), self.size)
            screen.blit(particle_surf, (screen_x - self.size, screen_y - self.size))


class ParticleSystem:
    """Sistema de partículas"""
    
    def __init__(self):
        """Inicializa el sistema de partículas"""
        self.particles: List[Particle] = []
    
    def add_explosion(self, x: float, y: float, color: Tuple[int, int, int] = (255, 200, 0), 
                     count: int = 20):
        """Agrega una explosión de partículas"""
        for _ in range(count):
            angle = random.uniform(0, 6.28)  # 0 a 2π
            speed = random.uniform(50, 150)
            vx = speed * pygame.math.Vector2(1, 0).rotate_rad(angle).x
            vy = speed * pygame.math.Vector2(1, 0).rotate_rad(angle).y
            
            particle = Particle(
                x, y, vx, vy,
                color,
                random.uniform(0.3, 0.8),
                random.randint(2, 4)
            )
            self.particles.append(particle)
    
    def add_heal_effect(self, x: float, y: float, count: int = 10):
        """Agrega efecto de curación (partículas verdes que suben)"""
        for _ in range(count):
            vx = random.uniform(-20, 20)
            vy = random.uniform(-80, -40)  # Hacia arriba
            particle = Particle(
                x + random.uniform(-10, 10),
                y + random.uniform(-10, 10),
                vx, vy,
                (100, 255, 100),
                random.uniform(0.5, 1.0),
                3
            )
            self.particles.append(particle)
    
    def add_damage_effect(self, x: float, y: float, count: int = 8):
        """Agrega efecto de daño (partículas rojas)"""
        for _ in range(count):
            vx = random.uniform(-30, 30)
            vy = random.uniform(-50, -20)
            particle = Particle(
                x + random.uniform(-5, 5),
                y + random.uniform(-5, 5),
                vx, vy,
                (255, 50, 50),
                random.uniform(0.3, 0.6),
                2
            )
            self.particles.append(particle)
    
    def add_magic_sparkles(self, x: float, y: float, color: Tuple[int, int, int] = (100, 150, 255),
                          count: int = 15):
        """Agrega chispas mágicas"""
        for _ in range(count):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(20, 60)
            vx = speed * pygame.math.Vector2(1, 0).rotate_rad(angle).x
            vy = speed * pygame.math.Vector2(1, 0).rotate_rad(angle).y
            
            particle = Particle(
                x, y, vx, vy,
                color,
                random.uniform(0.4, 0.8),
                2
            )
            self.particles.append(particle)
    
    def update(self, dt: float):
        """Actualiza todas las partículas"""
        self.particles = [p for p in self.particles if p.update(dt)]
    
    def render(self, screen: pygame.Surface, camera_offset: Tuple[int, int] = (0, 0)):
        """Renderiza todas las partículas"""
        for particle in self.particles:
            particle.render(screen, camera_offset)
    
    def clear(self):
        """Limpia todas las partículas"""
        self.particles.clear()

