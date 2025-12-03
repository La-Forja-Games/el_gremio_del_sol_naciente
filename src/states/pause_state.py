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
        self.selected_option = 0
        self.options = ["Continuar", "Inventario", "Equipamiento", "Guardar", "Cargar", "Menú Principal"]
        self.game = None  # Referencia al juego (se asigna desde Game)
        self.ui_panel = None  # Panel UI para el menú de pausa
        
    def enter(self):
        """Inicializa el estado de pausa"""
        from src.utils.font_helper import get_epic_font
        self.font = get_epic_font(36, bold=True)
        self.selected_option = 0
        
        # Cargar UI panel usando RPG Asset Library
        if self.game and self.game.asset_lib:
            self.ui_panel = self.game.asset_lib.get_ui_element("Base-01")
    
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
        """Renderiza el menú de pausa con assets RPG"""
        from src.utils.font_helper import get_epic_font
        
        # Fondo semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Panel UI de fondo (si está disponible)
        if self.ui_panel:
            panel_width = 500
            panel_height = 450
            panel_scaled = pygame.transform.scale(self.ui_panel, (panel_width, panel_height))
            panel_rect = panel_scaled.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(panel_scaled, panel_rect)
        
        # Título con sombra
        title_font = get_epic_font(48, bold=True)
        title_shadow = title_font.render("PAUSA", True, (0, 0, 0))
        title_text = title_font.render("PAUSA", True, COLOR_WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2 + 2, 202))
        screen.blit(title_shadow, title_rect)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(title_text, title_rect)
        
        # Opciones con mejor estilo
        y_offset = 280
        button_width = 350
        button_height = 45
        
        for i, option in enumerate(self.options):
            # Color según selección
            if i == self.selected_option:
                text_color = (255, 215, 0)  # Dorado
                bg_color = (100, 100, 100, 180)
            else:
                text_color = COLOR_WHITE
                bg_color = (50, 50, 50, 120)
            
            # Fondo del botón
            button_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - button_width // 2,
                y_offset + i * 55 - button_height // 2,
                button_width,
                button_height
            )
            button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
            button_surface.fill(bg_color)
            screen.blit(button_surface, button_rect)
            
            # Texto del botón
            text = self.font.render(option, True, text_color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 55))
            screen.blit(text, text_rect)
            
            # Indicador de selección (flecha)
            if i == self.selected_option:
                arrow_points = [
                    (SCREEN_WIDTH // 2 - button_width // 2 + 20, y_offset + i * 55),
                    (SCREEN_WIDTH // 2 - button_width // 2 + 10, y_offset + i * 55 - 8),
                    (SCREEN_WIDTH // 2 - button_width // 2 + 10, y_offset + i * 55 + 8)
                ]
                pygame.draw.polygon(screen, text_color, arrow_points)

