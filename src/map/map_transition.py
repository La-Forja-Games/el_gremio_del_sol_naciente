"""
Sistema de transiciones entre mapas
"""

from typing import Optional, Dict, Tuple
from src.map.map_manager import MapManager


class MapTransition:
    """Maneja las transiciones entre mapas"""
    
    def __init__(self, map_manager: MapManager):
        """
        Inicializa el sistema de transiciones
        
        Args:
            map_manager: Instancia de MapManager
        """
        self.map_manager = map_manager
        self.current_map_id: Optional[str] = None
        self.spawn_points: Dict[str, Tuple[float, float]] = {}
    
    def change_map(self, map_id: str, spawn_point_id: str = "default"):
        """
        Cambia al mapa especificado
        
        Args:
            map_id: ID del mapa (nombre del archivo .tmx)
            spawn_point_id: ID del punto de spawn en el nuevo mapa
            
        Returns:
            Tupla (x, y) con la posición de spawn, o None si hay error
        """
        # Cargar el nuevo mapa
        self.map_manager.load_map(map_id)
        self.current_map_id = map_id
        
        # Buscar punto de spawn
        spawn_point = self._find_spawn_point(spawn_point_id)
        
        if spawn_point:
            return spawn_point
        else:
            # Si no hay spawn point, usar el centro del mapa
            map_width = self.map_manager.get_map_width()
            map_height = self.map_manager.get_map_height()
            return (map_width // 2, map_height // 2)
    
    def _find_spawn_point(self, spawn_point_id: str) -> Optional[Tuple[float, float]]:
        """
        Busca un punto de spawn en el mapa actual
        
        Args:
            spawn_point_id: ID del punto de spawn
            
        Returns:
            Tupla (x, y) con la posición, o None si no se encuentra
        """
        if not self.map_manager.event_layer:
            return None
        
        # Buscar objeto de spawn en la capa de eventos
        for obj in self.map_manager.event_layer:
            if obj.name == f"spawn_{spawn_point_id}" or obj.name == spawn_point_id:
                return (obj.x, obj.y)
        
        # Buscar objeto "spawn" genérico
        for obj in self.map_manager.event_layer:
            if obj.name == "spawn" or obj.name == "default":
                return (obj.x, obj.y)
        
        return None
    
    def get_map_id(self) -> Optional[str]:
        """Retorna el ID del mapa actual"""
        return self.current_map_id

