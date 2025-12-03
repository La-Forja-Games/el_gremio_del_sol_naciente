"""
Sistema de habilidades
"""

from typing import Dict, List, Optional
from enum import Enum


class ElementType(Enum):
    """Tipos elementales"""
    FIRE = "Fuego"
    EARTH = "Tierra"
    WATER = "Agua"
    ICE = "Hielo"
    PHYSICAL = "Físico"
    NONE = "Ninguno"


class Ability:
    """Representa una habilidad"""
    
    def __init__(self, ability_id: int, name: str, ability_data: Dict = None):
        """
        Inicializa una habilidad
        
        Args:
            ability_id: ID único de la habilidad
            name: Nombre de la habilidad
            ability_data: Datos de la habilidad
        """
        self.id = ability_id
        self.name = name
        
        if ability_data:
            self._load_from_dict(ability_data)
        else:
            self._load_defaults()
    
    def _load_from_dict(self, data: Dict):
        """Carga datos desde un diccionario"""
        self.descripcion = data.get("descripcion", "")
        self.costo_mp = data.get("costo_mp", 0)
        self.cooldown = data.get("cooldown", 0)
        self.cooldown_remaining = 0
        
        # Tipo de habilidad
        self.tipo = data.get("tipo", "ataque")  # ataque, soporte, defensa
        
        # Elemento
        elemento_str = data.get("elemento", "Ninguno")
        try:
            self.elemento = ElementType[elemento_str.upper()]
        except:
            self.elemento = ElementType.NONE
        
        # Daño/cura
        self.damage = data.get("damage", 0)
        self.heal = data.get("heal", 0)
        self.damage_type = data.get("damage_type", "fisico")  # fisico, magico
        
        # Área de efecto
        self.area_of_effect = data.get("area_of_effect", False)
        self.target_all = data.get("target_all", False)
        
        # Efectos adicionales
        self.status_effects = data.get("status_effects", [])
        self.stat_buffs = data.get("stat_buffs", {})
        
        # Requisitos
        self.required_level = data.get("required_level", 1)
        self.required_position = data.get("required_position", None)  # vanguardia, medio, retaguardia
    
    def _load_defaults(self):
        """Carga valores por defecto"""
        self.descripcion = ""
        self.costo_mp = 0
        self.cooldown = 0
        self.cooldown_remaining = 0
        self.tipo = "ataque"
        self.elemento = ElementType.NONE
        self.damage = 0
        self.heal = 0
        self.damage_type = "fisico"
        self.area_of_effect = False
        self.target_all = False
        self.status_effects = []
        self.stat_buffs = {}
        self.required_level = 1
        self.required_position = None
    
    def can_use(self, character) -> tuple[bool, str]:
        """
        Verifica si la habilidad puede ser usada
        
        Args:
            character: Personaje que intenta usar la habilidad
            
        Returns:
            Tupla (puede_usar, razon)
        """
        # Verificar MP
        if character.stats.get("MP", 0) < self.costo_mp:
            return (False, "MP insuficiente")
        
        # Verificar cooldown
        if self.cooldown_remaining > 0:
            return (False, f"En cooldown ({self.cooldown_remaining} turnos)")
        
        # Verificar nivel
        if character.level < self.required_level:
            return (False, "Nivel insuficiente")
        
        return (True, "")
    
    def use(self, caster, target=None, targets: List = None):
        """
        Usa la habilidad
        
        Args:
            caster: Personaje que usa la habilidad
            target: Objetivo único (opcional)
            targets: Lista de objetivos (opcional)
        """
        # Consumir MP
        caster.stats["MP"] = max(0, caster.stats["MP"] - self.costo_mp)
        
        # Establecer cooldown
        self.cooldown_remaining = self.cooldown
        
        # Determinar objetivos
        if targets:
            actual_targets = targets
        elif target:
            actual_targets = [target]
        elif self.target_all:
            # TODO: Obtener todos los objetivos válidos
            actual_targets = []
        else:
            actual_targets = []
        
        # Aplicar efectos
        results = []
        for tgt in actual_targets:
            result = self._apply_to_target(caster, tgt)
            results.append(result)
        
        return results
    
    def _apply_to_target(self, caster, target) -> Dict:
        """
        Aplica la habilidad a un objetivo
        
        Args:
            caster: Personaje que usa la habilidad
            target: Objetivo
            
        Returns:
            Diccionario con el resultado
        """
        result = {
            "target": target,
            "damage": 0,
            "heal": 0,
            "status_effects": []
        }
        
        # Calcular daño
        if self.damage > 0:
            base_damage = self.damage
            
            # Aplicar stats del caster
            if self.damage_type == "fisico":
                base_damage += caster.stats.get("ATK", 0)
            else:  # mágico
                base_damage += caster.stats.get("MAG", 0)
            
            # Aplicar defensa del objetivo
            if self.damage_type == "fisico":
                defense = target.stats.get("DEF", 0)
            else:
                defense = target.stats.get("MAG", 0)  # Resistencia mágica
            
            damage = max(1, base_damage - defense)
            result["damage"] = damage
            target.stats["HP"] = max(0, target.stats["HP"] - damage)
        
        # Calcular curación
        if self.heal > 0:
            heal_amount = self.heal + caster.stats.get("MAG", 0)
            result["heal"] = heal_amount
            target.stats["HP"] = min(target.max_hp, target.stats["HP"] + heal_amount)
        
        # Aplicar efectos de estado
        for status_effect_data in self.status_effects:
            # TODO: Crear StatusEffect desde los datos
            pass
        
        return result
    
    def update_cooldown(self):
        """Actualiza el cooldown (llamar al final de cada turno)"""
        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= 1
    
    def to_dict(self) -> Dict:
        """Serializa la habilidad"""
        return {
            "id": self.id,
            "name": self.name,
            "descripcion": self.descripcion,
            "costo_mp": self.costo_mp,
            "cooldown": self.cooldown,
            "tipo": self.tipo,
            "elemento": self.elemento.value,
            "damage": self.damage,
            "heal": self.heal,
            "damage_type": self.damage_type,
            "area_of_effect": self.area_of_effect,
            "target_all": self.target_all,
            "status_effects": self.status_effects,
            "stat_buffs": self.stat_buffs,
            "required_level": self.required_level,
            "required_position": self.required_position
        }

