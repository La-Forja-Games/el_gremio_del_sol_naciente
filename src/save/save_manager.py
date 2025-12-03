"""
Sistema de guardado y carga
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
from src.config import SAVES_DIR


class SaveManager:
    """Maneja el guardado y carga de partidas"""
    
    def __init__(self):
        """Inicializa el gestor de guardados"""
        # Asegurar que la carpeta de guardados existe
        os.makedirs(SAVES_DIR, exist_ok=True)
    
    def save_game(self, save_data: Dict[str, Any], slot: int = 1) -> bool:
        """
        Guarda el juego en un slot
        
        Args:
            save_data: Diccionario con todos los datos del juego
            slot: Número de slot (1-10)
            
        Returns:
            True si se guardó correctamente, False si hubo error
        """
        try:
            # Agregar metadata
            save_data["metadata"] = {
                "save_time": datetime.now().isoformat(),
                "version": "0.1.0"
            }
            
            # Guardar en archivo
            save_path = os.path.join(SAVES_DIR, f"save_{slot:02d}.json")
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            print(f"Partida guardada en slot {slot}")
            return True
            
        except Exception as e:
            print(f"Error guardando partida: {e}")
            return False
    
    def load_game(self, slot: int = 1) -> Optional[Dict[str, Any]]:
        """
        Carga una partida desde un slot
        
        Args:
            slot: Número de slot (1-10)
            
        Returns:
            Diccionario con los datos del juego, o None si hay error
        """
        try:
            save_path = os.path.join(SAVES_DIR, f"save_{slot:02d}.json")
            
            if not os.path.exists(save_path):
                print(f"No hay partida guardada en slot {slot}")
                return None
            
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            print(f"Partida cargada desde slot {slot}")
            return save_data
            
        except Exception as e:
            print(f"Error cargando partida: {e}")
            return None
    
    def get_save_info(self, slot: int = 1) -> Optional[Dict[str, Any]]:
        """
        Obtiene información de un slot de guardado sin cargar todo
        
        Args:
            slot: Número de slot
            
        Returns:
            Diccionario con información del guardado, o None si no existe
        """
        try:
            save_path = os.path.join(SAVES_DIR, f"save_{slot:02d}.json")
            
            if not os.path.exists(save_path):
                return None
            
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            metadata = save_data.get("metadata", {})
            return {
                "slot": slot,
                "save_time": metadata.get("save_time", "Desconocido"),
                "version": metadata.get("version", "Desconocido"),
                "current_map": save_data.get("world_state", {}).get("current_map_id", "Desconocido")
            }
            
        except Exception as e:
            print(f"Error obteniendo info del slot {slot}: {e}")
            return None
    
    def list_saves(self) -> list:
        """
        Lista todos los slots de guardado disponibles
        
        Returns:
            Lista de diccionarios con información de cada slot
        """
        saves = []
        for slot in range(1, 11):  # Slots 1-10
            info = self.get_save_info(slot)
            if info:
                saves.append(info)
        return saves
    
    def delete_save(self, slot: int) -> bool:
        """
        Elimina un guardado
        
        Args:
            slot: Número de slot a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        try:
            save_path = os.path.join(SAVES_DIR, f"save_{slot:02d}.json")
            if os.path.exists(save_path):
                os.remove(save_path)
                print(f"Guardado del slot {slot} eliminado")
                return True
            return False
        except Exception as e:
            print(f"Error eliminando guardado: {e}")
            return False

