"""
Sistema elemental - efectividad y sinergias
"""

from typing import Dict, Optional
from src.combat.ability import ElementType


class ElementalSystem:
    """Maneja las relaciones elementales"""
    
    # Tabla de efectividad (multiplicador de daño)
    EFFECTIVENESS_TABLE: Dict[ElementType, Dict[ElementType, float]] = {
        ElementType.FIRE: {
            ElementType.ICE: 2.0,      # Fuego es fuerte contra Hielo
            ElementType.EARTH: 0.5,    # Fuego es débil contra Tierra
            ElementType.WATER: 0.5,    # Fuego es débil contra Agua
            ElementType.FIRE: 0.5,     # Mismo elemento reduce daño
            ElementType.PHYSICAL: 1.0, # Neutral
            ElementType.NONE: 1.0
        },
        ElementType.WATER: {
            ElementType.FIRE: 2.0,     # Agua es fuerte contra Fuego
            ElementType.EARTH: 0.5,   # Agua es débil contra Tierra
            ElementType.ICE: 0.5,     # Agua es débil contra Hielo
            ElementType.WATER: 0.5,
            ElementType.PHYSICAL: 1.0,
            ElementType.NONE: 1.0
        },
        ElementType.EARTH: {
            ElementType.WATER: 2.0,   # Tierra es fuerte contra Agua
            ElementType.ICE: 0.5,     # Tierra es débil contra Hielo
            ElementType.FIRE: 1.5,    # Tierra resiste Fuego
            ElementType.EARTH: 0.5,
            ElementType.PHYSICAL: 1.0,
            ElementType.NONE: 1.0
        },
        ElementType.ICE: {
            ElementType.EARTH: 2.0,   # Hielo es fuerte contra Tierra
            ElementType.FIRE: 0.5,    # Hielo es débil contra Fuego
            ElementType.WATER: 1.5,   # Hielo congela Agua
            ElementType.ICE: 0.5,
            ElementType.PHYSICAL: 1.0,
            ElementType.NONE: 1.0
        },
        ElementType.PHYSICAL: {
            ElementType.FIRE: 1.0,
            ElementType.WATER: 1.0,
            ElementType.EARTH: 1.0,
            ElementType.ICE: 1.0,
            ElementType.PHYSICAL: 1.0,
            ElementType.NONE: 1.0
        },
        ElementType.NONE: {
            ElementType.FIRE: 1.0,
            ElementType.WATER: 1.0,
            ElementType.EARTH: 1.0,
            ElementType.ICE: 1.0,
            ElementType.PHYSICAL: 1.0,
            ElementType.NONE: 1.0
        }
    }
    
    @staticmethod
    def get_effectiveness(attack_element: ElementType, 
                         defense_element: ElementType) -> float:
        """
        Calcula la efectividad de un ataque elemental
        
        Args:
            attack_element: Elemento del ataque
            defense_element: Elemento de la defensa
            
        Returns:
            Multiplicador de daño (2.0 = super efectivo, 0.5 = no muy efectivo)
        """
        return ElementalSystem.EFFECTIVENESS_TABLE.get(
            attack_element, {}
        ).get(defense_element, 1.0)
    
    @staticmethod
    def calculate_elemental_damage(base_damage: float,
                                   attack_element: ElementType,
                                   defense_element: ElementType) -> float:
        """
        Calcula el daño elemental final
        
        Args:
            base_damage: Daño base
            attack_element: Elemento del ataque
            defense_element: Elemento de la defensa
            
        Returns:
            Daño final con multiplicador elemental
        """
        effectiveness = ElementalSystem.get_effectiveness(
            attack_element, defense_element
        )
        return base_damage * effectiveness
    
    @staticmethod
    def get_effectiveness_text(effectiveness: float) -> str:
        """
        Retorna texto descriptivo de la efectividad
        
        Args:
            effectiveness: Multiplicador de efectividad
            
        Returns:
            Texto descriptivo
        """
        if effectiveness >= 2.0:
            return "¡Super efectivo!"
        elif effectiveness >= 1.5:
            return "Muy efectivo"
        elif effectiveness <= 0.5:
            return "No muy efectivo"
        else:
            return "Efectivo"

