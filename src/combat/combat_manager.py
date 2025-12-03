"""
Gestor de combate - maneja el combate por turnos
"""

from typing import List, Optional, Dict
from enum import Enum
from src.entities.character import Character
from src.combat.enemy import Enemy
from src.combat.ability import Ability
from src.combat.status_effect import StatusManager, StatusEffect, StatusType


class CombatAction:
    """Representa una acción en combate"""
    
    def __init__(self, actor: Character, action_type: str, 
                 ability: Optional[Ability] = None,
                 target: Optional[Character] = None,
                 targets: Optional[List[Character]] = None):
        """
        Inicializa una acción de combate
        
        Args:
            actor: Personaje que realiza la acción
            action_type: Tipo de acción ("ability", "attack", "defend", "item", "skip")
            ability: Habilidad a usar (si action_type es "ability")
            target: Objetivo único
            targets: Lista de objetivos
        """
        self.actor = actor
        self.action_type = action_type
        self.ability = ability
        self.target = target
        self.targets = targets or ([] if target is None else [target])
        self.results = []
    
    def execute(self) -> List[Dict]:
        """
        Ejecuta la acción
        
        Returns:
            Lista de resultados
        """
        if self.action_type == "ability" and self.ability:
            return self.ability.use(self.actor, self.target, self.targets)
        elif self.action_type == "attack":
            return self._execute_attack()
        elif self.action_type == "defend":
            return self._execute_defend()
        elif self.action_type == "skip":
            return []
        return []
    
    def _execute_attack(self) -> List[Dict]:
        """Ejecuta un ataque básico"""
        results = []
        for target in self.targets:
            damage = self.actor.stats.get("ATK", 0) - target.stats.get("DEF", 0)
            damage = max(1, damage)
            target.stats["HP"] = max(0, target.stats["HP"] - damage)
            results.append({
                "target": target,
                "damage": damage,
                "heal": 0
            })
        return results
    
    def _execute_defend(self) -> List[Dict]:
        """Ejecuta una defensa"""
        # TODO: Implementar defensa (reducir daño del próximo ataque)
        return []


class CombatManager:
    """Maneja el combate por turnos"""
    
    def __init__(self):
        """Inicializa el gestor de combate"""
        self.party: List[Character] = []
        self.enemies: List[Enemy] = []
        self.turn_order: List[Character] = []
        self.current_turn = 0
        self.turn_count = 0
        
        # Estados de combate
        self.combat_active = False
        self.victory = False
        self.defeat = False
        
        # Acciones pendientes
        self.pending_actions: Dict[Character, CombatAction] = {}
    
    def start_combat(self, party: List[Character], enemies: List[Enemy]):
        """
        Inicia un combate
        
        Args:
            party: Lista de personajes aliados
            enemies: Lista de enemigos
        """
        self.party = party
        self.enemies = enemies
        self.combat_active = True
        self.victory = False
        self.defeat = False
        self.turn_count = 0
        
        # Crear orden de turnos basado en velocidad
        all_combatants = party + enemies
        self.turn_order = sorted(
            all_combatants,
            key=lambda c: c.stats.get("VEL", 0),
            reverse=True
        )
        
        self.current_turn = 0
        
        # Inicializar gestores de estado para todos
        for combatant in all_combatants:
            if not hasattr(combatant, 'status_manager'):
                combatant.status_manager = StatusManager()
    
    def get_current_actor(self) -> Optional[Character]:
        """Retorna el personaje cuyo turno es actual"""
        if self.current_turn < len(self.turn_order):
            return self.turn_order[self.current_turn]
        return None
    
    def queue_action(self, actor: Character, action: CombatAction):
        """
        Encola una acción para un personaje
        
        Args:
            actor: Personaje que realiza la acción
            action: Acción a realizar
        """
        self.pending_actions[actor] = action
    
    def execute_turn(self) -> Dict:
        """
        Ejecuta el turno actual
        
        Returns:
            Diccionario con resultados del turno
        """
        if not self.combat_active:
            return {}
        
        actor = self.get_current_actor()
        if not actor:
            return {}
        
        # Aplicar efectos de estado al inicio del turno
        if hasattr(actor, 'status_manager'):
            status_changes = actor.status_manager.apply_turn_effects()
            actor.stats["HP"] = max(0, actor.stats["HP"] - status_changes.get("damage", 0))
            actor.stats["HP"] = min(actor.max_hp, actor.stats["HP"] + status_changes.get("heal", 0))
        
        # Ejecutar acción si está en cola
        action = self.pending_actions.get(actor)
        results = {}
        if action:
            action_results = action.execute()
            results["action_results"] = action_results
            del self.pending_actions[actor]
            
            # Actualizar cooldowns de habilidades
            if action.ability:
                action.ability.update_cooldown()
        else:
            # Si no hay acción, saltar turno
            results["action_results"] = []
        
        # Avanzar turno
        self.current_turn += 1
        
        # Si se completaron todos los turnos, iniciar nueva ronda
        if self.current_turn >= len(self.turn_order):
            self.current_turn = 0
            self.turn_count += 1
            
            # Actualizar cooldowns de todas las habilidades
            for combatant in self.turn_order:
                if hasattr(combatant, 'abilities'):
                    for ability in combatant.abilities:
                        ability.update_cooldown()
        
        # Verificar condiciones de victoria/derrota
        self._check_combat_end()
        
        return results
    
    def _check_combat_end(self):
        """Verifica si el combate ha terminado"""
        # Verificar si todos los enemigos están derrotados
        alive_enemies = [e for e in self.enemies if e.stats.get("HP", 0) > 0]
        if len(alive_enemies) == 0:
            self.victory = True
            self.combat_active = False
            return
        
        # Verificar si todos los aliados están derrotados
        alive_party = [p for p in self.party if p.stats.get("HP", 0) > 0]
        if len(alive_party) == 0:
            self.defeat = True
            self.combat_active = False
            return
    
    def get_loot(self) -> List[Dict]:
        """
        Calcula el loot de los enemigos derrotados
        
        Returns:
            Lista de items obtenidos
        """
        loot = []
        for enemy in self.enemies:
            if enemy.stats.get("HP", 0) <= 0:
                # TODO: Calcular loot según loot_table del enemigo
                pass
        return loot
    
    def get_exp_reward(self) -> int:
        """Calcula la experiencia ganada"""
        total_exp = 0
        for enemy in self.enemies:
            if enemy.stats.get("HP", 0) <= 0:
                total_exp += enemy.exp_reward
        return total_exp

