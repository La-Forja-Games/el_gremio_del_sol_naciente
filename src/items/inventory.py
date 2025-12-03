"""
Sistema de inventario
"""

from typing import List, Optional, Dict
from src.items.item import Item


class InventorySlot:
    """Representa un slot del inventario"""
    
    def __init__(self):
        self.item: Optional[Item] = None
        self.quantity: int = 0
    
    def is_empty(self) -> bool:
        """Retorna True si el slot está vacío"""
        return self.item is None or self.quantity == 0
    
    def can_stack(self, item: Item) -> bool:
        """Verifica si se puede apilar un item en este slot"""
        if self.is_empty():
            return item.stackable
        return (self.item.id == item.id and 
                self.item.stackable and 
                self.quantity < self.item.max_stack)
    
    def add_item(self, item: Item, quantity: int = 1) -> int:
        """
        Agrega items al slot
        
        Args:
            item: Item a agregar
            quantity: Cantidad a agregar
            
        Returns:
            Cantidad que no pudo ser agregada (0 si todo se agregó)
        """
        if self.is_empty():
            self.item = item
            self.quantity = min(quantity, item.max_stack)
            return max(0, quantity - item.max_stack)
        
        if self.can_stack(item):
            space_available = self.item.max_stack - self.quantity
            to_add = min(quantity, space_available)
            self.quantity += to_add
            return quantity - to_add
        
        return quantity  # No se pudo agregar nada
    
    def remove_item(self, quantity: int = 1) -> int:
        """
        Remueve items del slot
        
        Args:
            quantity: Cantidad a remover
            
        Returns:
            Cantidad que no pudo ser removida (0 si todo se removió)
        """
        if self.is_empty():
            return quantity
        
        to_remove = min(quantity, self.quantity)
        self.quantity -= to_remove
        
        if self.quantity == 0:
            self.item = None
        
        return quantity - to_remove
    
    def clear(self):
        """Limpia el slot"""
        self.item = None
        self.quantity = 0


class Inventory:
    """Maneja el inventario del jugador"""
    
    def __init__(self, max_slots: int = 40):
        """
        Inicializa el inventario
        
        Args:
            max_slots: Número máximo de slots
        """
        self.max_slots = max_slots
        self.slots: List[InventorySlot] = [InventorySlot() for _ in range(max_slots)]
    
    def add_item(self, item: Item, quantity: int = 1) -> int:
        """
        Agrega un item al inventario
        
        Args:
            item: Item a agregar
            quantity: Cantidad a agregar
            
        Returns:
            Cantidad que no pudo ser agregada (0 si todo se agregó)
        """
        remaining = quantity
        
        # Si el item es stackable, intentar agregar a slots existentes
        if item.stackable:
            for slot in self.slots:
                if slot.can_stack(item):
                    remaining = slot.add_item(item, remaining)
                    if remaining == 0:
                        return 0
        
        # Si aún queda cantidad, buscar slots vacíos
        while remaining > 0:
            empty_slot = self._find_empty_slot()
            if empty_slot is None:
                return remaining  # Inventario lleno
            
            remaining = empty_slot.add_item(item, remaining)
        
        return 0
    
    def remove_item(self, item_id: int, quantity: int = 1) -> int:
        """
        Remueve items del inventario
        
        Args:
            item_id: ID del item a remover
            quantity: Cantidad a remover
            
        Returns:
            Cantidad que no pudo ser removida (0 si todo se removió)
        """
        remaining = quantity
        
        for slot in self.slots:
            if not slot.is_empty() and slot.item.id == item_id:
                remaining = slot.remove_item(remaining)
                if remaining == 0:
                    return 0
        
        return remaining
    
    def has_item(self, item_id: int, quantity: int = 1) -> bool:
        """
        Verifica si el inventario tiene una cantidad suficiente de un item
        
        Args:
            item_id: ID del item
            quantity: Cantidad requerida
            
        Returns:
            True si tiene suficiente cantidad
        """
        total = 0
        for slot in self.slots:
            if not slot.is_empty() and slot.item.id == item_id:
                total += slot.quantity
                if total >= quantity:
                    return True
        return False
    
    def get_item_quantity(self, item_id: int) -> int:
        """
        Retorna la cantidad total de un item en el inventario
        
        Args:
            item_id: ID del item
            
        Returns:
            Cantidad total
        """
        total = 0
        for slot in self.slots:
            if not slot.is_empty() and slot.item.id == item_id:
                total += slot.quantity
        return total
    
    def _find_empty_slot(self) -> Optional[InventorySlot]:
        """Encuentra el primer slot vacío"""
        for slot in self.slots:
            if slot.is_empty():
                return slot
        return None
    
    def get_items_by_category(self, category: str) -> List[tuple]:
        """
        Retorna todos los items de una categoría específica
        
        Args:
            category: Categoría a filtrar
            
        Returns:
            Lista de tuplas (slot_index, item, quantity)
        """
        result = []
        for i, slot in enumerate(self.slots):
            if not slot.is_empty() and slot.item.categoria == category:
                result.append((i, slot.item, slot.quantity))
        return result
    
    def to_dict(self) -> Dict:
        """Convierte el inventario a diccionario para serialización"""
        items_data = []
        for slot in self.slots:
            if not slot.is_empty():
                items_data.append({
                    "item": slot.item.to_dict(),
                    "quantity": slot.quantity
                })
        return {
            "max_slots": self.max_slots,
            "items": items_data
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Inventory':
        """
        Crea un inventario desde un diccionario
        
        Args:
            data: Diccionario con los datos del inventario
            
        Returns:
            Instancia de Inventory
        """
        from src.items.item import Item
        
        max_slots = data.get("max_slots", 40)
        inventory = Inventory(max_slots)
        
        items_data = data.get("items", [])
        for item_data in items_data:
            item = Item.from_dict(item_data["item"])
            quantity = item_data.get("quantity", 1)
            inventory.add_item(item, quantity)
        
        return inventory

