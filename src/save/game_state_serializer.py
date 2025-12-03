"""
Funciones helper para serializar y deserializar el estado del juego
"""

from typing import Dict, Any
from src.entities.player import Player
from src.items.inventory import Inventory


def serialize_game_state(player: Player, inventory: Inventory, 
                         current_map_id: str, player_pos: tuple,
                         game_flags: Dict[str, bool] = None) -> Dict[str, Any]:
    """
    Serializa el estado completo del juego
    
    Args:
        player: Instancia del jugador
        inventory: Inventario del jugador
        current_map_id: ID del mapa actual
        player_pos: Posición del jugador (x, y)
        game_flags: Flags de progreso del juego
        
    Returns:
        Diccionario con todos los datos serializados
    """
    # Serializar jugador
    player_data = {
        "level": player.level,
        "exp": player.exp,
        "x": player.x,
        "y": player.y,
        "base_stats": player.base_stats,
        "current_hp": player.stats.get("HP", player.max_hp),
        "current_mp": player.stats.get("MP", player.max_mp),
        "equipment": player.equipment.to_dict()
    }
    
    # Serializar inventario
    inventory_data = inventory.to_dict()
    
    # Estado del mundo
    world_state = {
        "current_map_id": current_map_id,
        "player_pos_x": player_pos[0],
        "player_pos_y": player_pos[1],
        "game_flags": game_flags or {}
    }
    
    return {
        "player": player_data,
        "inventory": inventory_data,
        "world_state": world_state
    }


def deserialize_game_state(save_data: Dict[str, Any], resource_manager=None) -> Dict[str, Any]:
    """
    Deserializa el estado del juego desde un diccionario
    
    Args:
        save_data: Diccionario con los datos del guardado
        resource_manager: Instancia de ResourceManager
        
    Returns:
        Diccionario con los objetos reconstruidos:
        {
            "player": Player,
            "inventory": Inventory,
            "world_state": dict
        }
    """
    from src.entities.player import Player
    from src.items.inventory import Inventory
    from src.items.item import Item
    
    # Deserializar jugador
    player_data = save_data.get("player", {})
    player = Player(
        player_data.get("x", 0),
        player_data.get("y", 0),
        resource_manager=resource_manager
    )
    player.level = player_data.get("level", 1)
    player.exp = player_data.get("exp", 0)
    player.base_stats = player_data.get("base_stats", player.base_stats)
    player.stats = player.base_stats.copy()
    
    # Restaurar HP y MP actuales
    current_hp = player_data.get("current_hp", player.max_hp)
    current_mp = player_data.get("current_mp", player.max_mp)
    player.stats["HP"] = current_hp
    player.stats["MP"] = current_mp
    player.max_hp = player.base_stats["HP"]
    player.max_mp = player.base_stats["MP"]
    
    # Restaurar equipamiento
    equipment_data = player_data.get("equipment", {})
    from src.items.equipment import Equipment
    player.equipment = Equipment.from_dict(equipment_data)
    player._recalculate_stats()
    
    # Deserializar inventario
    inventory_data = save_data.get("inventory", {})
    inventory = Inventory.from_dict(inventory_data)
    
    # Estado del mundo
    world_state = save_data.get("world_state", {})
    
    return {
        "player": player,
        "inventory": inventory,
        "world_state": world_state
    }

