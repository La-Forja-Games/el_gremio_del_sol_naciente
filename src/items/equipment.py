"""
Sistema de equipamiento
"""

from typing import Dict, Optional
from src.items.item import Item


class Equipment:
    """Maneja el equipamiento del personaje"""
    
    def __init__(self):
        """Inicializa el equipamiento"""
        self.slots: Dict[str, Optional[Item]] = {
            "arma": None,
            "armadura": None,
            "accesorio1": None,
            "accesorio2": None
        }
    
    def equip(self, item: Item) -> Optional[Item]:
        """
        Equipa un item
        
        Args:
            item: Item a equipar
            
        Returns:
            Item previamente equipado (si había uno), o None
        """
        if not item.is_equipable():
            return None
        
        slot_name = self._get_slot_for_item(item)
        if slot_name is None:
            return None
        
        # Guardar el item anterior
        previous_item = self.slots[slot_name]
        
        # Equipar el nuevo item
        self.slots[slot_name] = item
        
        return previous_item
    
    def unequip(self, slot_name: str) -> Optional[Item]:
        """
        Desequipa un item de un slot
        
        Args:
            slot_name: Nombre del slot ("arma", "armadura", etc.)
            
        Returns:
            Item desequipado, o None si el slot estaba vacío
        """
        if slot_name not in self.slots:
            return None
        
        item = self.slots[slot_name]
        self.slots[slot_name] = None
        return item
    
    def get_equipped_item(self, slot_name: str) -> Optional[Item]:
        """
        Retorna el item equipado en un slot
        
        Args:
            slot_name: Nombre del slot
            
        Returns:
            Item equipado, o None
        """
        return self.slots.get(slot_name)
    
    def get_stat_bonuses(self) -> Dict[str, int]:
        """
        Calcula todos los bonos de stats del equipamiento
        
        Returns:
            Diccionario con los bonos de cada stat
        """
        bonuses = {
            "HP": 0,
            "MP": 0,
            "ATK": 0,
            "DEF": 0,
            "VEL": 0,
            "MAG": 0
        }
        
        for item in self.slots.values():
            if item:
                for stat_name, bonus_value in item.bonus_stats.items():
                    if stat_name in bonuses:
                        bonuses[stat_name] += bonus_value
        
        return bonuses
    
    def _get_slot_for_item(self, item: Item) -> Optional[str]:
        """
        Determina en qué slot debe ir un item
        
        Args:
            item: Item a equipar
            
        Returns:
            Nombre del slot, o None si no es equipable
        """
        if item.categoria == "Arma":
            return "arma"
        elif item.categoria == "Armadura":
            return "armadura"
        elif item.categoria == "Accesorio":
            # Buscar un slot de accesorio vacío
            if self.slots["accesorio1"] is None:
                return "accesorio1"
            elif self.slots["accesorio2"] is None:
                return "accesorio2"
            else:
                # Si ambos están ocupados, reemplazar el primero
                return "accesorio1"
        
        return None
    
    def to_dict(self) -> Dict:
        """Convierte el equipamiento a diccionario para serialización"""
        equipment_data = {}
        for slot_name, item in self.slots.items():
            if item:
                equipment_data[slot_name] = item.to_dict()
            else:
                equipment_data[slot_name] = None
        return equipment_data
    
    @staticmethod
    def from_dict(data: Dict) -> 'Equipment':
        """
        Crea un equipamiento desde un diccionario
        
        Args:
            data: Diccionario con los datos del equipamiento
            
        Returns:
            Instancia de Equipment
        """
        from src.items.item import Item
        
        equipment = Equipment()
        
        for slot_name, item_data in data.items():
            if item_data:
                item = Item.from_dict(item_data)
                equipment.slots[slot_name] = item
            else:
                equipment.slots[slot_name] = None
        
        return equipment

