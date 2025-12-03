"""
Estado de combate - UI y lógica de combate
"""

import pygame
from src.state_manager import GameState
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_BLACK,
    COLOR_RED, COLOR_GREEN, COLOR_BLUE, STATE_EXPLORATION
)
from src.combat.combat_manager import CombatManager, CombatAction
from src.combat.enemy import Enemy
from src.combat.ability import Ability
from src.combat.status_effect import StatusManager


class CombatState(GameState):
    """Estado de combate por turnos"""
    
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.game = None
        self.combat_manager = CombatManager()
        
        # UI
        self.font = None
        self.title_font = None
        self.small_font = None
        
        # Navegación
        self.selected_action = 0
        self.selected_target = 0
        self.action_menu_open = False
        self.target_selection = False
        
        # Acciones disponibles
        self.available_actions = ["Ataque", "Habilidad", "Defender", "Item", "Huir"]
        self.current_abilities = []
        
        # Partículas para efectos de combate
        from src.utils.particles import ParticleSystem
        self.particles = ParticleSystem()
    
    def enter(self):
        """Inicializa el estado de combate"""
        # Fuentes
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 18)
        
        # Obtener jugador y crear combate de prueba
        from src.config import STATE_EXPLORATION
        exploration = self.state_manager._states.get(STATE_EXPLORATION)
        
        if exploration and hasattr(exploration, 'player'):
            player = exploration.player
            
            # Inicializar status manager si no existe
            if not hasattr(player, 'status_manager'):
                player.status_manager = StatusManager()
            
            # Crear enemigo de prueba
            enemy = Enemy(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2, 
                         enemy_id=1001, resource_manager=self.game.resource_manager if self.game else None)
            
            # Inicializar status manager del enemigo
            if not hasattr(enemy, 'status_manager'):
                enemy.status_manager = StatusManager()
            
            # Iniciar combate
            self.combat_manager.start_combat([player], [enemy])
        
        self.selected_action = 0
        self.action_menu_open = False
        self.target_selection = False
    
    def handle_event(self, event):
        """Maneja eventos de entrada"""
        if event.type == pygame.KEYDOWN:
            current_actor = self.combat_manager.get_current_actor()
            
            # Solo permitir input si es el turno del jugador
            if current_actor not in self.combat_manager.party:
                # Turno del enemigo - ejecutar automáticamente
                self._execute_enemy_turn()
                return True
            
            if self.target_selection:
                # Selección de objetivo
                if event.key == pygame.K_UP:
                    self.selected_target = (self.selected_target - 1) % len(self.combat_manager.enemies)
                    return True
                elif event.key == pygame.K_DOWN:
                    self.selected_target = (self.selected_target + 1) % len(self.combat_manager.enemies)
                    return True
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Confirmar objetivo
                    self._execute_action_with_target()
                    return True
                elif event.key == pygame.K_ESCAPE:
                    # Cancelar selección
                    self.target_selection = False
                    return True
            elif self.action_menu_open:
                # Menú de acciones
                if event.key == pygame.K_UP:
                    self.selected_action = (self.selected_action - 1) % len(self.available_actions)
                    return True
                elif event.key == pygame.K_DOWN:
                    self.selected_action = (self.selected_action + 1) % len(self.available_actions)
                    return True
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self._select_action()
                    return True
                elif event.key == pygame.K_ESCAPE:
                    self.action_menu_open = False
                    return True
            else:
                # Menú principal de combate
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.action_menu_open = True
                    return True
        
        return False
    
    def _select_action(self):
        """Selecciona una acción del menú"""
        action_name = self.available_actions[self.selected_action]
        
        if action_name == "Ataque":
            self.target_selection = True
            self.action_menu_open = False
        elif action_name == "Habilidad":
            # TODO: Mostrar lista de habilidades
            self.target_selection = True
            self.action_menu_open = False
        elif action_name == "Defender":
            self._execute_defend()
        elif action_name == "Item":
            # TODO: Abrir inventario de combate
            pass
        elif action_name == "Huir":
            # TODO: Intentar huir
            self._try_escape()
    
    def _execute_action_with_target(self):
        """Ejecuta la acción seleccionada con el objetivo"""
        current_actor = self.combat_manager.get_current_actor()
        target = self.combat_manager.enemies[self.selected_target]
        
        action = CombatAction(current_actor, "attack", target=target)
        self.combat_manager.queue_action(current_actor, action)
        
        # Efecto visual de ataque
        self.particles.add_explosion(
            target.rect.centerx if hasattr(target, 'rect') else SCREEN_WIDTH - 100,
            target.rect.centery if hasattr(target, 'rect') else SCREEN_HEIGHT // 2,
            (255, 100, 0),
            15
        )
        
        self.target_selection = False
        self.action_menu_open = False
        
        # Ejecutar turno
        results = self.combat_manager.execute_turn()
        
        # Efectos visuales según resultados
        if results.get("action_results"):
            for result in results["action_results"]:
                if result.get("damage", 0) > 0:
                    target = result.get("target")
                    if target:
                        x = target.rect.centerx if hasattr(target, 'rect') else SCREEN_WIDTH - 100
                        y = target.rect.centery if hasattr(target, 'rect') else SCREEN_HEIGHT // 2
                        self.particles.add_damage_effect(x, y)
                if result.get("heal", 0) > 0:
                    target = result.get("target")
                    if target:
                        x = target.rect.centerx if hasattr(target, 'rect') else SCREEN_WIDTH - 100
                        y = target.rect.centery if hasattr(target, 'rect') else SCREEN_HEIGHT // 2
                        self.particles.add_heal_effect(x, y)
    
    def _execute_defend(self):
        """Ejecuta acción de defender"""
        current_actor = self.combat_manager.get_current_actor()
        action = CombatAction(current_actor, "defend")
        self.combat_manager.queue_action(current_actor, action)
        self.action_menu_open = False
        self.combat_manager.execute_turn()
    
    def _execute_enemy_turn(self):
        """Ejecuta el turno de un enemigo (AI básica)"""
        current_actor = self.combat_manager.get_current_actor()
        
        if current_actor in self.combat_manager.enemies:
            # AI simple: atacar al primer aliado vivo
            target = None
            for party_member in self.combat_manager.party:
                if party_member.stats.get("HP", 0) > 0:
                    target = party_member
                    break
            
            if target:
                action = CombatAction(current_actor, "attack", target=target)
                self.combat_manager.queue_action(current_actor, action)
                self.combat_manager.execute_turn()
    
    def _try_escape(self):
        """Intenta huir del combate"""
        # TODO: Implementar probabilidad de huida
        # Por ahora, simplemente terminar el combate
        self.combat_manager.combat_active = False
        self.state_manager.change_state(STATE_EXPLORATION)
    
    def update(self, dt):
        """Actualiza la lógica de combate"""
        # Actualizar partículas
        self.particles.update(dt)
        
        # Verificar si el combate terminó
        if not self.combat_manager.combat_active:
            if self.combat_manager.victory:
                # TODO: Mostrar pantalla de victoria y recompensas
                print("¡Victoria!")
                # Volver a exploración después de un momento
                self.state_manager.change_state(STATE_EXPLORATION)
            elif self.combat_manager.defeat:
                # TODO: Mostrar pantalla de derrota
                print("Derrota...")
                self.state_manager.change_state(STATE_EXPLORATION)
    
    def render(self, screen):
        """Renderiza la UI de combate"""
        # Fondo
        screen.fill((20, 20, 40))
        
        # Título
        title_text = self.title_font.render("COMBATE", True, COLOR_WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - 80, 20))
        
        # Renderizar personajes
        party_x = 100
        party_y = SCREEN_HEIGHT // 2 - 100
        
        for i, member in enumerate(self.combat_manager.party):
            self._render_character(screen, member, party_x, party_y + i * 120, is_ally=True)
        
        # Renderizar enemigos
        enemy_x = SCREEN_WIDTH - 200
        enemy_y = SCREEN_HEIGHT // 2 - 100
        
        for i, enemy in enumerate(self.combat_manager.enemies):
            self._render_character(screen, enemy, enemy_x, enemy_y + i * 120, is_ally=False)
        
        # UI de acciones
        if self.action_menu_open:
            self._render_action_menu(screen)
        elif self.target_selection:
            self._render_target_selection(screen)
        else:
            self._render_combat_hud(screen)
        
        # Renderizar partículas
        self.particles.render(screen)
        
        # Indicador de turno
        current_actor = self.combat_manager.get_current_actor()
        if current_actor:
            turn_text = self.font.render(f"Turno: {current_actor.nombre if hasattr(current_actor, 'nombre') else 'Jugador'}", 
                                       True, COLOR_WHITE)
            screen.blit(turn_text, (10, SCREEN_HEIGHT - 100))
            
            # Resaltar personaje activo
            if current_actor in self.combat_manager.party:
                idx = self.combat_manager.party.index(current_actor)
                highlight_x = 80
                highlight_y = SCREEN_HEIGHT // 2 - 100 + idx * 120
                highlight_rect = pygame.Rect(highlight_x - 10, highlight_y - 10, 180, 100)
                pygame.draw.rect(screen, (255, 255, 0), highlight_rect, 3)
    
    def _render_character(self, screen, character, x, y, is_ally=True):
        """Renderiza un personaje en combate"""
        # Barra de HP
        hp = character.stats.get("HP", 0)
        max_hp = character.max_hp
        hp_percent = hp / max_hp if max_hp > 0 else 0
        
        bar_width = 150
        bar_height = 20
        
        # Fondo de la barra
        bg_rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(screen, (50, 50, 50), bg_rect)
        
        # Barra de HP
        hp_rect = pygame.Rect(x, y, int(bar_width * hp_percent), bar_height)
        color = COLOR_GREEN if is_ally else COLOR_RED
        pygame.draw.rect(screen, color, hp_rect)
        pygame.draw.rect(screen, COLOR_WHITE, bg_rect, 2)
        
        # Texto HP
        hp_text = self.small_font.render(f"HP: {hp}/{max_hp}", True, COLOR_WHITE)
        screen.blit(hp_text, (x, y + 25))
        
        # Nombre
        name = character.nombre if hasattr(character, 'nombre') else "Jugador"
        name_text = self.small_font.render(name, True, COLOR_WHITE)
        screen.blit(name_text, (x, y - 20))
        
        # MP (si tiene)
        mp = character.stats.get("MP", 0)
        max_mp = character.max_mp
        if max_mp > 0:
            mp_text = self.small_font.render(f"MP: {mp}/{max_mp}", True, COLOR_BLUE)
            screen.blit(mp_text, (x, y + 45))
    
    def _render_action_menu(self, screen):
        """Renderiza el menú de acciones"""
        menu_x = 50
        menu_y = SCREEN_HEIGHT - 200
        menu_width = 200
        menu_height = len(self.available_actions) * 40 + 20
        
        # Fondo del menú
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(screen, (40, 40, 40), menu_rect)
        pygame.draw.rect(screen, COLOR_WHITE, menu_rect, 2)
        
        # Título
        title_text = self.font.render("Acciones:", True, COLOR_WHITE)
        screen.blit(title_text, (menu_x + 10, menu_y + 5))
        
        # Opciones
        for i, action in enumerate(self.available_actions):
            y_pos = menu_y + 35 + i * 40
            color = COLOR_WHITE if i == self.selected_action else (150, 150, 150)
            
            action_text = self.font.render(action, True, color)
            screen.blit(action_text, (menu_x + 20, y_pos))
            
            if i == self.selected_action:
                pygame.draw.circle(screen, COLOR_WHITE, (menu_x + 10, y_pos + 12), 5)
    
    def _render_target_selection(self, screen):
        """Renderiza la selección de objetivo"""
        instruction_text = self.font.render("Selecciona objetivo:", True, COLOR_WHITE)
        screen.blit(instruction_text, (50, SCREEN_HEIGHT - 150))
        
        # Resaltar objetivo seleccionado
        if self.selected_target < len(self.combat_manager.enemies):
            enemy = self.combat_manager.enemies[self.selected_target]
            # Dibujar marco alrededor del enemigo seleccionado
            highlight_x = SCREEN_WIDTH - 220
            highlight_y = SCREEN_HEIGHT // 2 - 100 + self.selected_target * 120
            highlight_rect = pygame.Rect(highlight_x - 10, highlight_y - 10, 180, 100)
            pygame.draw.rect(screen, COLOR_WHITE, highlight_rect, 3)
    
    def _render_combat_hud(self, screen):
        """Renderiza el HUD básico de combate"""
        instruction_text = self.small_font.render("ENTER: Abrir menú de acciones", True, (200, 200, 200))
        screen.blit(instruction_text, (10, SCREEN_HEIGHT - 50))

