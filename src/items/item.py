"""
Clase base para items
"""

import json
import os
from typing import Dict, List, Optional, Any
from src.config import DATA_DIR


class Item:
    """Representa un item en el juego"""
    
    def __init__(self, item_id: int, item_data: Dict = None):
        """
        Inicializa un item
        
        Args:
            item_id: ID único del item
            item_data: Diccionario con los datos del item (si no se proporciona, se carga desde JSON)
        """
        self.id = item_id
        
        if item_data:
            self._load_from_dict(item_data)
        else:
            self._load_from_json(item_id)
    
    def _load_from_dict(self, data: Dict):
        """Carga los datos del item desde un diccionario"""
        self.nombre = data.get("nombre", "Item Desconocido")
        self.descripcion = data.get("descripcion", "")
        self.categoria = data.get("categoria", "Misc")
        self.stackable = data.get("stackable", False)
        self.max_stack = data.get("max_stack", 1)
        self.precio = data.get("precio", 0)
        self.efecto = data.get("efecto", [])
        
        # Atributos específicos por tipo
        self.tipo_arma = data.get("tipo_arma", None)
        self.bonus_stats = data.get("bonus_stats", {})
        
        # Sprite path (opcional)
        self.sprite_path = data.get("sprite_path", None)
    
    def _load_from_json(self, item_id: int):
        """Carga los datos del item desde el archivo JSON"""
        try:
            items_file = os.path.join(DATA_DIR, "items", "items_base.json")
            with open(items_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Buscar el item por ID
            for item_data in data.get("items", []):
                if item_data.get("id") == item_id:
                    self._load_from_dict(item_data)
                    return
            
            # Si no se encuentra, usar valores por defecto
            print(f"Advertencia: Item {item_id} no encontrado en JSON")
            self._load_from_dict({})
            
        except Exception as e:
            print(f"Error cargando item {item_id}: {e}")
            self._load_from_dict({})
    
    def is_consumible(self) -> bool:
        """Retorna True si el item es consumible"""
        return self.categoria == "Consumible"
    
    def is_equipable(self) -> bool:
        """Retorna True si el item es equipable"""
        return self.categoria in ["Arma", "Armadura", "Accesorio"]
    
    def is_material(self) -> bool:
        """Retorna True si el item es un material"""
        return self.categoria == "Material"
    
    def get_stat_bonus(self, stat_name: str) -> int:
        """
        Retorna el bonus de un stat específico
        
        Args:
            stat_name: Nombre del stat (ej: "ATK", "DEF")
            
        Returns:
            Valor del bonus (0 si no existe)
        """
        return self.bonus_stats.get(stat_name, 0)
    
    def to_dict(self) -> Dict:
        """Convierte el item a diccionario para serialización"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "categoria": self.categoria,
            "stackable": self.stackable,
            "max_stack": self.max_stack,
            "precio": self.precio,
            "efecto": self.efecto,
            "tipo_arma": self.tipo_arma,
            "bonus_stats": self.bonus_stats,
            "sprite_path": self.sprite_path
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Item':
        """
        Crea un item desde un diccionario
        
        Args:
            data: Diccionario con los datos del item
            
        Returns:
            Instancia de Item
        """
        item_id = data.get("id", 0)
        return Item(item_id, data)

