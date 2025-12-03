"""
Clase principal del juego - Loop principal
"""

import pygame
import sys
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, 
    STATE_MENU, STATE_EXPLORATION, STATE_PAUSE
)
from src.state_manager import StateManager
from src.resource_manager import ResourceManager
from src.states.menu_state import MenuState
from src.states.exploration_state import ExplorationState
from src.states.pause_state import PauseState


class Game:
    """Clase principal que maneja el loop del juego"""
    
    def __init__(self):
        """Inicializa Pygame y crea la ventana"""
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        self.running = True
        self.dt = 0.0  # Delta time en segundos
        
        # Inicializar sistemas
        self.resource_manager = ResourceManager()
        self.state_manager = StateManager()
        
        # Pasar referencia del juego a los estados (para acceso a resource_manager)
        self.state_manager.game = self
        
        # Registrar estados
        menu_state = MenuState(self.state_manager)
        menu_state.game = self
        self.state_manager.register_state(STATE_MENU, menu_state)
        
        exploration_state = ExplorationState(self.state_manager)
        exploration_state.game = self
        self.state_manager.register_state(STATE_EXPLORATION, exploration_state)
        
        pause_state = PauseState(self.state_manager)
        pause_state.game = self
        self.state_manager.register_state(STATE_PAUSE, pause_state)
        
        # Iniciar con el menú
        self.state_manager.change_state(STATE_MENU)
        
    def run(self):
        """Ejecuta el loop principal del juego"""
        while self.running:
            # Calcular delta time
            self.dt = self.clock.tick(FPS) / 1000.0  # Convertir a segundos
            
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    # Pasar eventos al estado actual
                    if self.state_manager.get_current_state():
                        current_state = self.state_manager._states.get(
                            self.state_manager.get_current_state()
                        )
                        if current_state:
                            current_state.handle_event(event)
            
            # Actualizar
            self.state_manager.update(self.dt)
            
            # Renderizar
            self.screen.fill((0, 0, 0))  # Limpiar pantalla
            self.state_manager.render(self.screen)
            pygame.display.flip()
        
        self.quit()
    
    def quit(self):
        """Limpia recursos y cierra el juego"""
        pygame.quit()
        sys.exit()


def main():
    """Punto de entrada principal"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

