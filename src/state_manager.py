"""
Gestor de estados del juego (máquina de estados)
"""

from typing import Dict, Optional
from src.config import (
    STATE_MENU, STATE_EXPLORATION, STATE_COMBAT, 
    STATE_INVENTORY, STATE_CAMP, STATE_DIALOG, STATE_PAUSE
)


class StateManager:
    """Maneja los diferentes estados del juego"""
    
    def __init__(self):
        self._states: Dict[str, 'GameState'] = {}
        self._current_state: Optional[str] = None
        self._previous_state: Optional[str] = None
        
    def register_state(self, state_name: str, state_instance: 'GameState'):
        """
        Registra un estado en el gestor
        
        Args:
            state_name: Nombre del estado
            state_instance: Instancia de la clase GameState
        """
        self._states[state_name] = state_instance
        
    def change_state(self, new_state: str):
        """
        Cambia al nuevo estado
        
        Args:
            new_state: Nombre del estado al que cambiar
        """
        if new_state not in self._states:
            print(f"Error: Estado '{new_state}' no registrado")
            return
        
        # Salir del estado actual
        if self._current_state and self._current_state in self._states:
            self._states[self._current_state].exit()
        
        # Guardar estado anterior
        self._previous_state = self._current_state
        
        # Cambiar al nuevo estado
        self._current_state = new_state
        self._states[self._current_state].enter()
        
    def push_state(self, new_state: str):
        """
        Apila un nuevo estado (útil para pausa, inventario sobre exploración)
        
        Args:
            new_state: Nombre del estado a apilar
        """
        if new_state not in self._states:
            print(f"Error: Estado '{new_state}' no registrado")
            return
        
        if self._current_state:
            self._states[self._current_state].pause()
        
        self._previous_state = self._current_state
        self._current_state = new_state
        self._states[self._current_state].enter()
    
    def pop_state(self):
        """Vuelve al estado anterior (desapila)"""
        if not self._previous_state:
            return
        
        if self._current_state and self._current_state in self._states:
            self._states[self._current_state].exit()
        
        self._current_state = self._previous_state
        self._previous_state = None
        
        if self._current_state in self._states:
            self._states[self._current_state].resume()
    
    def get_current_state(self) -> Optional[str]:
        """Retorna el nombre del estado actual"""
        return self._current_state
    
    def update(self, dt: float):
        """
        Actualiza el estado actual
        
        Args:
            dt: Delta time (tiempo transcurrido desde el último frame)
        """
        if self._current_state and self._current_state in self._states:
            self._states[self._current_state].update(dt)
    
    def render(self, screen):
        """
        Renderiza el estado actual
        
        Args:
            screen: Superficie de Pygame donde renderizar
        """
        if self._current_state and self._current_state in self._states:
            self._states[self._current_state].render(screen)


class GameState:
    """Clase base para todos los estados del juego"""
    
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        
    def enter(self):
        """Se llama cuando se entra al estado"""
        pass
    
    def exit(self):
        """Se llama cuando se sale del estado"""
        pass
    
    def pause(self):
        """Se llama cuando se pausa el estado (otro estado se apila encima)"""
        pass
    
    def resume(self):
        """Se llama cuando se reanuda el estado (se desapila el estado superior)"""
        pass
    
    def update(self, dt: float):
        """
        Actualiza la lógica del estado
        
        Args:
            dt: Delta time
        """
        pass
    
    def render(self, screen):
        """
        Renderiza el estado
        
        Args:
            screen: Superficie de Pygame
        """
        pass
    
    def handle_event(self, event):
        """
        Maneja eventos de entrada
        
        Args:
            event: Evento de Pygame
            
        Returns:
            True si el evento fue manejado, False si no
        """
        return False

