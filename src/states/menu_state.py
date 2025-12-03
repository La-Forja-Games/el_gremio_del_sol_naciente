"""
Estado del menú principal
"""

import pygame
from src.state_manager import GameState
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, STATE_EXPLORATION


class MenuState(GameState):
    """Menú principal del juego"""
    
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = None
        self.title_font = None
        self.selected_option = 0
        self.options = ["Nueva Partida", "Cargar Partida", "Opciones", "Salir"]
        self.game = None  # Referencia al juego (se asigna desde Game)
        
    def enter(self):
        """Inicializa el estado del menú"""
        # Cargar fuentes (usar fuente por defecto por ahora)
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        
    def update(self, dt):
        """Actualiza la lógica del menú"""
        pass
    
    def handle_event(self, event):
        """Maneja eventos de entrada"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._select_option()
        return True
    
    def _select_option(self):
        """Ejecuta la opción seleccionada"""
        if self.selected_option == 0:  # Nueva Partida
            # Iniciar nueva partida (ir a exploración)
            self.state_manager.change_state(STATE_EXPLORATION)
        elif self.selected_option == 1:  # Cargar Partida
            # Abrir menú de carga
            save_load = self.state_manager._states.get("save_load")
            if save_load:
                save_load.set_mode(False)  # Modo cargar
                self.state_manager.push_state("save_load")
        elif self.selected_option == 2:  # Opciones
            # TODO: Mostrar menú de opciones
            print("Opciones - Por implementar")
        elif self.selected_option == 3:  # Salir
            pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def render(self, screen):
        """Renderiza el menú"""
        # Título
        title_text = self.title_font.render("El Gremio del Sol Naciente", True, COLOR_WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)
        
        # Opciones del menú
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

