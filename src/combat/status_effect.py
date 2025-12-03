"""
Sistema de estados (buffs/debuffs)
"""

from typing import Dict, Optional
from enum import Enum


class StatusType(Enum):
    """Tipos de estados"""
    BUFF = "buff"
    DEBUFF = "debuff"
    DOT = "dot"  # Damage over time
    HOT = "hot"  # Heal over time


class StatusEffect:
    """Representa un efecto de estado"""
    
    def __init__(self, name: str, status_type: StatusType, duration: int, 
                 effect_data: Dict = None):
        """
        Inicializa un efecto de estado
        
        Args:
            name: Nombre del efecto
            status_type: Tipo de estado
            duration: Duración en turnos
            effect_data: Datos del efecto (stats modificados, daño, etc.)
        """
        self.name = name
        self.status_type = status_type
        self.duration = duration
        self.turns_remaining = duration
        self.effect_data = effect_data or {}
        
        # Modificadores de stats
        self.stat_modifiers = self.effect_data.get("stat_modifiers", {})
        
        # Daño/cura por turno
        self.damage_per_turn = self.effect_data.get("damage_per_turn", 0)
        self.heal_per_turn = self.effect_data.get("heal_per_turn", 0)
    
    def apply_turn(self) -> Dict[str, int]:
        """
        Aplica el efecto por un turno
        
        Returns:
            Diccionario con cambios (damage, heal)
        """
        self.turns_remaining -= 1
        
        return {
            "damage": self.damage_per_turn,
            "heal": self.heal_per_turn
        }
    
    def is_expired(self) -> bool:
        """Retorna True si el efecto ha expirado"""
        return self.turns_remaining <= 0
    
    def get_stat_modifiers(self) -> Dict[str, int]:
        """Retorna los modificadores de stats"""
        return self.stat_modifiers.copy()
    
    def to_dict(self) -> Dict:
        """Serializa el efecto de estado"""
        return {
            "name": self.name,
            "status_type": self.status_type.value,
            "duration": self.duration,
            "turns_remaining": self.turns_remaining,
            "effect_data": self.effect_data
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'StatusEffect':
        """Deserializa un efecto de estado"""
        status_type = StatusType(data["status_type"])
        return StatusEffect(
            data["name"],
            status_type,
            data["duration"],
            data.get("effect_data", {})
        )


class StatusManager:
    """Maneja los estados de un personaje"""
    
    def __init__(self):
        """Inicializa el gestor de estados"""
        self.effects: list[StatusEffect] = []
    
    def add_effect(self, effect: StatusEffect):
        """
        Agrega un efecto de estado
        
        Args:
            effect: Efecto a agregar
        """
        # Si ya existe un efecto del mismo tipo, reemplazarlo
        self.remove_effect(effect.name)
        self.effects.append(effect)
    
    def remove_effect(self, effect_name: str):
        """
        Remueve un efecto de estado
        
        Args:
            effect_name: Nombre del efecto a remover
        """
        self.effects = [e for e in self.effects if e.name != effect_name]
    
    def apply_turn_effects(self) -> Dict[str, int]:
        """
        Aplica todos los efectos por un turno
        
        Returns:
            Diccionario con cambios totales (damage, heal)
        """
        total_damage = 0
        total_heal = 0
        
        effects_to_remove = []
        
        for effect in self.effects:
            changes = effect.apply_turn()
            total_damage += changes.get("damage", 0)
            total_heal += changes.get("heal", 0)
            
            if effect.is_expired():
                effects_to_remove.append(effect)
        
        # Remover efectos expirados
        for effect in effects_to_remove:
            self.effects.remove(effect)
        
        return {
            "damage": total_damage,
            "heal": total_heal
        }
    
    def get_stat_modifiers(self) -> Dict[str, int]:
        """
        Calcula todos los modificadores de stats
        
        Returns:
            Diccionario con modificadores totales
        """
        modifiers = {}
        for effect in self.effects:
            effect_modifiers = effect.get_stat_modifiers()
            for stat, value in effect_modifiers.items():
                modifiers[stat] = modifiers.get(stat, 0) + value
        return modifiers
    
    def get_effects_by_type(self, status_type: StatusType) -> list[StatusEffect]:
        """Retorna todos los efectos de un tipo específico"""
        return [e for e in self.effects if e.status_type == status_type]
    
    def clear_all(self):
        """Limpia todos los efectos"""
        self.effects.clear()
    
    def has_effect(self, effect_name: str) -> bool:
        """Verifica si tiene un efecto específico"""
        return any(e.name == effect_name for e in self.effects)

