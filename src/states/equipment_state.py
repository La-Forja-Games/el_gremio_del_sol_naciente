"""
Estado de equipamiento - UI del equipamiento
"""

import pygame
from src.state_manager import GameState
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_BLACK
)
from src.items.equipment import Equipment


class EquipmentState(GameState):
    """Estado del equipamiento"""
    
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.game = None
        self.player = None
        self.equipment = None
        
        # UI
        self.font = None
        self.title_font = None
        self.small_font = None
        
        # Navegación
        self.selected_slot = 0
        self.slot_names = ["arma", "armadura", "accesorio1", "accesorio2"]
        self.slot_labels = ["Arma", "Armadura", "Accesorio 1", "Accesorio 2"]
    
    def enter(self):
        """Inicializa el estado de equipamiento"""
        # Obtener referencia al jugador
        if self.game:
            from src.config import STATE_EXPLORATION
            exploration = self.state_manager._states.get(STATE_EXPLORATION)
            if exploration and hasattr(exploration, 'player'):
                self.player = exploration.player
                self.equipment = self.player.equipment
        
        # Fuentes
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 18)
        
        self.selected_slot = 0
    
    def handle_event(self, event):
        """Maneja eventos de entrada"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_c:
                # Cerrar equipamiento
                self.state_manager.pop_state()
                return True
            elif event.key == pygame.K_UP:
                self.selected_slot = (self.selected_slot - 1) % len(self.slot_names)
                return True
            elif event.key == pygame.K_DOWN:
                self.selected_slot = (self.selected_slot + 1) % len(self.slot_names)
                return True
            elif event.key == pygame.K_x:
                # Desequipar item seleccionado
                self._unequip_selected_slot()
                return True
        
        return False
    
    def _unequip_selected_slot(self):
        """Desequipa el item del slot seleccionado"""
        if not self.player or not self.equipment:
            return
        
        slot_name = self.slot_names[self.selected_slot]
        item = self.equipment.unequip(slot_name)
        
        if item:
            # Agregar al inventario
            self.player.inventory.add_item(item, 1)
            # Recalcular stats
            self.player._recalculate_stats()
            print(f"Desequipado: {item.nombre}")
    
    def update(self, dt):
        """Actualiza la lógica del equipamiento"""
        pass
    
    def render(self, screen):
        """Renderiza la UI del equipamiento"""
        if not self.equipment or not self.player:
            return
        
        # Fondo semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Panel principal
        panel_width = 700
        panel_height = 500
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2
        
        # Fondo del panel
        panel = pygame.Surface((panel_width, panel_height))
        panel.fill((40, 40, 40))
        pygame.draw.rect(panel, COLOR_WHITE, (0, 0, panel_width, panel_height), 2)
        screen.blit(panel, (panel_x, panel_y))
        
        # Título
        title_text = self.title_font.render("EQUIPAMIENTO", True, COLOR_WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 30))
        screen.blit(title_text, title_rect)
        
        # Slots de equipamiento
        y_offset = panel_y + 80
        for i, (slot_name, slot_label) in enumerate(zip(self.slot_names, self.slot_labels)):
            is_selected = (i == self.selected_slot)
            
            # Color de fondo
            bg_color = (80, 80, 80) if is_selected else (60, 60, 60)
            slot_rect = pygame.Rect(panel_x + 20, y_offset + i * 80, panel_width - 40, 70)
            pygame.draw.rect(screen, bg_color, slot_rect)
            if is_selected:
                pygame.draw.rect(screen, COLOR_WHITE, slot_rect, 2)
            
            # Label del slot
            label_text = self.font.render(slot_label + ":", True, COLOR_WHITE)
            screen.blit(label_text, (panel_x + 30, y_offset + i * 80 + 10))
            
            # Item equipado
            item = self.equipment.get_equipped_item(slot_name)
            if item:
                item_text = self.font.render(item.nombre, True, (150, 255, 150))
                screen.blit(item_text, (panel_x + 30, y_offset + i * 80 + 35))
                
                # Bonos de stats
                bonuses = []
                for stat, bonus in item.bonus_stats.items():
                    if bonus != 0:
                        sign = "+" if bonus > 0 else ""
                        bonuses.append(f"{stat}: {sign}{bonus}")
                
                if bonuses:
                    bonus_text = self.small_font.render(", ".join(bonuses), True, (200, 200, 100))
                    screen.blit(bonus_text, (panel_x + 30, y_offset + i * 80 + 55))
            else:
                empty_text = self.small_font.render("Vacío", True, (100, 100, 100))
                screen.blit(empty_text, (panel_x + 30, y_offset + i * 80 + 35))
        
        # Stats del personaje
        stats_x = panel_x + panel_width - 250
        stats_y = panel_y + 80
        stats_title = self.font.render("Stats Totales:", True, COLOR_WHITE)
        screen.blit(stats_title, (stats_x, stats_y))
        
        stats_y += 30
        for stat_name, stat_value in self.player.stats.items():
            stat_text = self.small_font.render(f"{stat_name}: {stat_value}", True, COLOR_WHITE)
            screen.blit(stat_text, (stats_x, stats_y))
            stats_y += 20
        
        # Instrucciones
        instructions_y = panel_y + panel_height - 40
        inst_text = self.small_font.render("X: Desequipar | ESC: Cerrar", True, (200, 200, 200))
        screen.blit(inst_text, (panel_x + 20, instructions_y))

