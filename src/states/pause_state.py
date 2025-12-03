"""
Estado de pausa
"""

import pygame
from src.state_manager import GameState
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, STATE_MENU


class PauseState(GameState):
    """Menú de pausa"""
    
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = None
        self.selected_option = 0
        self.options = ["Continuar", "Inventario", "Opciones", "Menú Principal"]
        self.game = None  # Referencia al juego (se asigna desde Game)
        
    def enter(self):
        """Inicializa el estado de pausa"""
        self.font = pygame.font.Font(None, 36)
        self.selected_option = 0
    
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
            # TODO: Abrir inventario
            print("Inventario - Por implementar")
        elif self.selected_option == 2:  # Opciones
            # TODO: Abrir opciones
            print("Opciones - Por implementar")
        elif self.selected_option == 3:  # Menú Principal
            # Volver al menú principal (cambiar estado directamente)
            self.state_manager.change_state(STATE_MENU)
    
    def update(self, dt):
        """Actualiza la lógica de pausa"""
        pass
    
    def render(self, screen):
        """Renderiza el menú de pausa"""
        # Fondo semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Título
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("PAUSA", True, COLOR_WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(title_text, title_rect)
        
        # Opciones
        y_offset = 300
        for i, option in enumerate(self.options):
            color = COLOR_WHITE if i == self.selected_option else (150, 150, 150)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 60))
            screen.blit(text, text_rect)
            
            # Indicador de selección
            if i == self.selected_option:
                pygame.draw.circle(screen, COLOR_WHITE,
                                 (SCREEN_WIDTH // 2 - 100, y_offset + i * 60), 5)

