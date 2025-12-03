"""
Estado de pausa
"""

import pygame
from src.state_manager import GameState
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, STATE_MENU, STATE_INVENTORY


class PauseState(GameState):
    """Menú de pausa"""
    
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = None
        self.title_font = None
        self.selected_option = 0
        self.options = ["Continuar", "Inventario", "Equipamiento", "Guardar", "Cargar", "Menú Principal"]
        self.game = None  # Referencia al juego (se asigna desde Game)
        self.background = None  # Fondo del menú secundario
        
    def enter(self):
        """Inicializa el estado de pausa"""
        from src.utils.font_helper import get_epic_font
        self.font = get_epic_font(36, bold=True)
        self.title_font = get_epic_font(48, bold=True)
        self.selected_option = 0
        
        # Cargar fondo de menú secundario
        if self.game and self.game.resource_manager:
            self.background = self.game.resource_manager.load_image("ui/secondary_menu_bg.png", use_alpha=False)
            if self.background:
                from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
                bg_width = self.background.get_width()
                bg_height = self.background.get_height()
                if bg_width != SCREEN_WIDTH or bg_height != SCREEN_HEIGHT:
                    self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
                print(f"[OK] Fondo de menú secundario cargado: {bg_width}x{bg_height}")
    
    def handle_event(self, event):
        """Maneja eventos de entrada"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Continuar
                self.state_manager.pop_state()
                return True
            elif event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                return True
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                return True
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._select_option()
                return True
        return False
    
    def _select_option(self):
        """Ejecuta la opción seleccionada"""
        if self.selected_option == 0:  # Continuar
            self.state_manager.pop_state()
        elif self.selected_option == 1:  # Inventario
            self.state_manager.push_state(STATE_INVENTORY)
        elif self.selected_option == 2:  # Equipamiento
            self.state_manager.push_state("equipment")
        elif self.selected_option == 3:  # Guardar
            save_load = self.state_manager._states.get("save_load")
            if save_load:
                save_load.set_mode(True)  # Modo guardar
                self.state_manager.push_state("save_load")
        elif self.selected_option == 4:  # Cargar
            save_load = self.state_manager._states.get("save_load")
            if save_load:
                save_load.set_mode(False)  # Modo cargar
                self.state_manager.push_state("save_load")
        elif self.selected_option == 5:  # Menú Principal
            # Volver al menú principal (cambiar estado directamente)
            self.state_manager.change_state(STATE_MENU)
    
    def update(self, dt):
        """Actualiza la lógica de pausa"""
        pass
    
    def render(self, screen):
        """Renderiza el menú de pausa con efecto de fuego"""
        # Fondo del menú secundario
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            # Fallback: fondo semi-transparente
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
        
        # Panel oscuro semi-transparente para mejor legibilidad
        panel_width = 500
        panel_height = 450
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = 150
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 200))  # Negro semi-transparente
        screen.blit(panel, (panel_x, panel_y))
        
        # Título con efecto de fuego oscuro
        title_text = "PAUSA"
        title_surface = self._render_fire_text(self.title_font, title_text)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(title_surface, title_rect)
        
        # Opciones con efecto de fuego
        y_offset = 280
        button_width = 400
        button_height = 50
        
        for i, option in enumerate(self.options):
            # Color según selección
            if i == self.selected_option:
                # Opción seleccionada: fuego más intenso
                text_surface = self._render_fire_text(self.font, option, intensity=1.0)
                bg_color = (100, 50, 0, 220)  # Fondo naranja oscuro más opaco
            else:
                # Opción no seleccionada: fuego más suave
                text_surface = self._render_fire_text(self.font, option, intensity=0.7)
                bg_color = (50, 25, 0, 150)  # Fondo marrón oscuro más opaco
            
            # Fondo del botón (más opaco para mejor legibilidad)
            button_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - button_width // 2,
                y_offset + i * 55 - button_height // 2,
                button_width,
                button_height
            )
            button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
            button_surface.fill(bg_color)
            screen.blit(button_surface, button_rect)
            
            # Borde del botón para mejor definición
            if i == self.selected_option:
                pygame.draw.rect(screen, (255, 150, 50), button_rect, 2)
            else:
                pygame.draw.rect(screen, (100, 50, 0), button_rect, 1)
            
            # Texto del botón con efecto de fuego
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 55))
            screen.blit(text_surface, text_rect)
            
            # Indicador de selección (flecha con color de fuego)
            if i == self.selected_option:
                arrow_points = [
                    (SCREEN_WIDTH // 2 - button_width // 2 + 20, y_offset + i * 55),
                    (SCREEN_WIDTH // 2 - button_width // 2 + 10, y_offset + i * 55 - 8),
                    (SCREEN_WIDTH // 2 - button_width // 2 + 10, y_offset + i * 55 + 8)
                ]
                fire_color = (255, 150, 50)  # Color de fuego oscuro
                pygame.draw.polygon(screen, fire_color, arrow_points)
    
    def _render_fire_text(self, font, text, intensity=1.0):
        """
        Renderiza texto con efecto de fuego oscuro (mismo que el menú principal)
        
        Args:
            font: Fuente de pygame
            text: Texto a renderizar
            intensity: Intensidad del efecto (0.0 a 1.0)
            
        Returns:
            Superficie con el texto renderizado con efecto de fuego
        """
        # Colores de fuego oscuro (de más claro a más oscuro)
        fire_colors = [
            (255, 150, 50),   # Naranja dorado (centro - más oscuro)
            (255, 120, 30),   # Naranja oscuro
            (220, 80, 20),    # Naranja rojizo oscuro
            (180, 50, 10),    # Rojo naranja oscuro
            (150, 40, 5),     # Rojo oscuro
            (120, 30, 0),     # Rojo muy oscuro
            (80, 20, 0),      # Rojo casi negro (bordes)
        ]
        
        # Ajustar intensidad
        fire_colors = [tuple(int(c * intensity) for c in color) for color in fire_colors]
        
        # Crear superficie base con el texto en el color más oscuro (para sombra)
        base_text = font.render(text, True, fire_colors[-1])
        text_surface = pygame.Surface(base_text.get_size(), pygame.SRCALPHA)
        
        # Renderizar múltiples capas del texto con diferentes colores y offsets
        # para crear efecto de gradiente/fuego
        num_layers = len(fire_colors)
        for i, color in enumerate(fire_colors):
            # Offset para crear efecto de profundidad
            offset_x = int((num_layers - i) * 0.5)
            offset_y = int((num_layers - i) * 0.3)
            
            # Renderizar texto con este color
            layer_text = font.render(text, True, color)
            
            # Aplicar alpha según la capa (más transparente en los bordes)
            alpha = int(255 * (1.0 - i * 0.15))
            if alpha > 0:
                layer_text.set_alpha(alpha)
                text_surface.blit(layer_text, (offset_x, offset_y))
        
        # Capa final con el color más brillante en el centro
        center_text = font.render(text, True, fire_colors[0])
        center_rect = center_text.get_rect(center=(text_surface.get_width() // 2, 
                                                    text_surface.get_height() // 2))
        text_surface.blit(center_text, center_rect)
        
        return text_surface

