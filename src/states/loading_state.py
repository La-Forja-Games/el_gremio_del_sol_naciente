"""
Estado de carga - Pantalla de loading estilo EA Games
"""

import pygame
import math
from src.state_manager import GameState
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, STATE_MENU


class LoadingState(GameState):
    """Pantalla de loading con logo animado estilo EA Games"""
    
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.logo = None
        self.logo_scale = 0.0
        self.logo_alpha = 0
        self.progress = 0.0
        self.loading_dots = 0
        self.dot_timer = 0.0
        self.fade_alpha = 255
        self.loading_complete = False
        self.min_loading_time = 2.5  # Tiempo mínimo de carga (segundos)
        self.loading_start_time = 0.0
        self.game = None
        self.font = None
        self.epic_font = None
        self.sparks = []  # Lista de chispitas para el fondo
        self._init_sparks()
    
    def enter(self):
        """Inicializa el estado de loading"""
        print("[DEBUG] LoadingState.enter() llamado")
        
        # Cargar fuentes primero
        from src.utils.font_helper import get_normal_font, get_epic_font
        self.font = get_normal_font(28)
        self.epic_font = get_epic_font(32)
        
        # Cargar logo
        if self.game and self.game.resource_manager:
            print("[DEBUG] Intentando cargar logo...")
            self.logo = self.game.resource_manager.load_image("ui/logo.png", use_alpha=True)
            if self.logo:
                # Escalar logo a un tamaño mucho más grande (mantener aspect ratio)
                logo_width, logo_height = self.logo.get_size()
                # Logo mucho más grande - usar 70% del ancho de pantalla
                max_width = int(SCREEN_WIDTH * 0.7)
                max_height = int(SCREEN_HEIGHT * 0.6)
                scale = min(max_width / logo_width, max_height / logo_height)
                new_width = int(logo_width * scale)
                new_height = int(logo_height * scale)
                self.logo = pygame.transform.smoothscale(self.logo, (new_width, new_height))
                print(f"[OK] Logo cargado: {new_width}x{new_height}")
            else:
                print("[WARNING] Logo no se pudo cargar")
        else:
            print(f"[WARNING] game o resource_manager no disponible")
        
        # Inicializar variables de animación
        self.logo_scale = 0.0
        self.logo_alpha = 0
        self.progress = 0.0
        self.loading_dots = 0
        self.dot_timer = 0.0
        self.fade_alpha = 255
        self.loading_complete = False
        self.loading_start_time = pygame.time.get_ticks() / 1000.0
        print(f"[DEBUG] LoadingState inicializado. Tiempo inicio: {self.loading_start_time}")
    
    def _init_sparks(self):
        """Inicializa las chispitas del fondo"""
        import random
        self.sparks = []
        for _ in range(50):  # 50 chispitas
            spark = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(1, 3),
                'brightness': random.randint(100, 255),
                'speed': random.uniform(0.2, 0.8),
                'color': random.choice([
                    (255, 200, 100),  # Dorado
                    (255, 150, 50),   # Naranja
                    (255, 100, 0),    # Naranja oscuro
                    (255, 255, 200),  # Amarillo claro
                ])
            }
            self.sparks.append(spark)
    
    def exit(self):
        """Limpia recursos al salir"""
        pass
    
    def handle_event(self, event):
        """Maneja eventos (no hace nada en loading)"""
        pass
    
    def update(self, dt):
        """Actualiza la animación de loading"""
        # Asegurar que dt sea válido
        if dt <= 0:
            dt = 0.016  # ~60 FPS
        
        current_time = pygame.time.get_ticks() / 1000.0
        elapsed = current_time - self.loading_start_time
        
        # Animación de entrada del logo (escala y fade in)
        if elapsed < 1.0:
            # Escala: de 0 a 1 con efecto bounce
            t = elapsed / 1.0
            self.logo_scale = 1.0 - math.pow(1.0 - t, 3)  # Ease out cubic
            if self.logo_scale > 1.0:
                self.logo_scale = 1.0
            
            # Alpha: fade in
            self.logo_alpha = int(255 * t)
        else:
            self.logo_scale = 1.0
            self.logo_alpha = 255
        
        # Progreso de carga (simulado) - Asegurar que siempre avance
        if elapsed < self.min_loading_time:
            # Progreso suave hasta el tiempo mínimo
            self.progress = min(0.95, elapsed / self.min_loading_time)
        else:
            # Completar carga - asegurar que llegue al 100%
            remaining = 1.0 - self.progress
            if remaining > 0:
                # Avanzar más rápido al final
                self.progress = min(1.0, self.progress + dt * 2.0)
            else:
                self.progress = 1.0
            
            # Cuando llegue al 100%, iniciar fade out
            if self.progress >= 1.0 and not self.loading_complete:
                self.loading_complete = True
                print("[DEBUG] Carga completada, iniciando fade out")
            
            # Fade out después de completar
            if self.loading_complete:
                # Pequeño delay antes del fade out
                if elapsed > self.min_loading_time + 0.5:
                    self.fade_alpha = max(0, self.fade_alpha - int(255 * dt * 2))
                    
                    # Cambiar al menú cuando el fade out termine
                    if self.fade_alpha <= 0:
                        print("[DEBUG] Cambiando al menú principal")
                        try:
                            self.state_manager.change_state(STATE_MENU)
                        except Exception as e:
                            print(f"[ERROR] Error al cambiar de estado: {e}")
        
        # Actualizar chispitas
        import random
        for spark in self.sparks:
            spark['y'] -= spark['speed'] * dt * 60  # Mover hacia arriba
            spark['brightness'] = (spark['brightness'] + 2) % 255  # Parpadeo
            
            # Si sale de la pantalla, reiniciar abajo
            if spark['y'] < 0:
                spark['y'] = SCREEN_HEIGHT
                spark['x'] = random.randint(0, SCREEN_WIDTH)
        
        # Animación de puntos de loading
        self.dot_timer += dt
        if self.dot_timer >= 0.5:
            self.dot_timer = 0.0
            self.loading_dots = (self.loading_dots + 1) % 4
    
    def render(self, screen):
        """Renderiza la pantalla de loading estilo EA Games"""
        # Fondo negro
        screen.fill((0, 0, 0))
        
        # Renderizar chispitas de fondo
        for spark in self.sparks:
            alpha = spark['brightness']
            color = tuple(min(255, int(c * alpha / 255)) for c in spark['color'])
            size = spark['size']
            pygame.draw.circle(screen, color, (int(spark['x']), int(spark['y'])), size)
        
        # Renderizar logo con animación
        if self.logo:
            # Calcular posición centrada
            logo_width = int(self.logo.get_width() * max(0.1, self.logo_scale))
            logo_height = int(self.logo.get_height() * max(0.1, self.logo_scale))
            logo_x = (SCREEN_WIDTH - logo_width) // 2
            logo_y = SCREEN_HEIGHT // 3 - logo_height // 2
            
            # Crear superficie escalada con alpha
            if self.logo_scale < 1.0 and self.logo_scale > 0:
                scaled_logo = pygame.transform.smoothscale(
                    self.logo, 
                    (logo_width, logo_height)
                )
            else:
                scaled_logo = self.logo
            
            # Aplicar alpha (mínimo 50 para que siempre sea visible)
            if self.logo_alpha < 255:
                scaled_logo = scaled_logo.copy()
                scaled_logo.set_alpha(max(50, self.logo_alpha))
            
            screen.blit(scaled_logo, (logo_x, logo_y))
        else:
            # Fallback: mostrar texto si no hay logo
            if self.epic_font:
                fallback_text = self.epic_font.render("EL GREMIO DEL SOL NACIENTE", True, (255, 200, 100))
                fallback_rect = fallback_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
                screen.blit(fallback_text, fallback_rect)
        
        # Barra de progreso estilo EA Games (más grande y colorida)
        bar_width = int(SCREEN_WIDTH * 0.6)
        bar_height = 8
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = int(SCREEN_HEIGHT * 0.75)
        
        # Fondo de la barra (negro con borde)
        pygame.draw.rect(screen, (20, 20, 20), 
                        (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(screen, (60, 60, 60), 
                        (bar_x, bar_y, bar_width, bar_height))
        
        # Barra de progreso (colores vibrantes estilo fuego)
        # Siempre mostrar al menos un pequeño indicador
        progress_width = max(5, int(bar_width * max(0.01, self.progress)))
        if progress_width > 0:
            progress_rect = pygame.Rect(bar_x, bar_y, progress_width, bar_height)
            
            # Colores vibrantes de fuego (naranja brillante a dorado)
            if self.progress < 0.5:
                # Primera mitad: naranja rojizo brillante
                r = 255
                g = int(100 + self.progress * 100)
                b = int(30 + self.progress * 20)
            else:
                # Segunda mitad: naranja dorado brillante
                r = 255
                g = int(180 + (self.progress - 0.5) * 75)
                b = int(50 + (self.progress - 0.5) * 50)
            
            color = (r, g, b)
            
            # Dibujar barra de progreso con gradiente simulado
            pygame.draw.rect(screen, color, progress_rect)
            
            # Efecto de fuego en la barra (llamas pequeñas)
            import random
            import math
            flame_count = int(progress_width / 10)  # Una llama cada 10 píxeles
            for i in range(flame_count):
                flame_x = bar_x + (i * 10) + random.randint(-2, 2)
                flame_y = bar_y - random.randint(0, 3)
                
                # Dibujar pequeñas llamas
                flame_points = [
                    (flame_x, bar_y),
                    (flame_x - 2, flame_y),
                    (flame_x, flame_y - 2),
                    (flame_x + 2, flame_y),
                ]
                flame_color = (255, random.randint(150, 200), random.randint(50, 100))
                pygame.draw.polygon(screen, flame_color, flame_points)
            
            # Brillo superior (línea blanca/naranja clara)
            if progress_width > 3:
                highlight_color = (255, 220, 150)
                pygame.draw.line(screen, highlight_color, 
                               (bar_x + 1, bar_y + 1), 
                               (bar_x + progress_width - 1, bar_y + 1), 2)
            
            # Efecto de brillo en el borde derecho (punto de carga) - más grande y brillante
            if progress_width > 5:
                glow_color = (255, 255, 200)  # Definir antes de usar
                glow_radius = bar_height // 2 + 2
                # Glow exterior (más suave)
                for r in range(glow_radius, glow_radius + 3):
                    alpha = 100 - (r - glow_radius) * 30
                    if alpha > 0:
                        glow_surface = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                        glow_color_alpha = (*glow_color[:3], alpha)
                        pygame.draw.circle(glow_surface, glow_color_alpha, (r, r), r)
                        screen.blit(glow_surface, 
                                  (bar_x + progress_width - r, bar_y + bar_height // 2 - r))
                
                # Glow interior (brillante)
                pygame.draw.circle(screen, glow_color, 
                                 (bar_x + progress_width, bar_y + bar_height // 2), 
                                 glow_radius)
        
        # Texto "Cargando..." con puntos animados (más grande y colorido)
        if self.font:
            dots_text = "." * self.loading_dots
            loading_text = f"Cargando{dots_text}"
            # Color más vibrante (blanco/naranja claro)
            text_color = (255, 220, 180)
            text_surface = self.font.render(loading_text, True, text_color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, bar_y + 35))
            screen.blit(text_surface, text_rect)
            
            # Porcentaje de carga (más grande y destacado)
            percent_text = f"{int(self.progress * 100)}%"
            # Color dorado brillante
            percent_color = (255, 200, 100)
            if self.epic_font:
                percent_surface = self.epic_font.render(percent_text, True, percent_color)
                percent_rect = percent_surface.get_rect(center=(SCREEN_WIDTH // 2, bar_y + 75))
                screen.blit(percent_surface, percent_rect)
        
        # Fade out overlay (cuando la carga está completa)
        if self.fade_alpha < 255:
            fade_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_overlay.set_alpha(self.fade_alpha)
            fade_overlay.fill((0, 0, 0))
            screen.blit(fade_overlay, (0, 0))
