"""
Estado de inventario - UI del inventario
"""

import pygame
from src.state_manager import GameState
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_BLACK,
    STATE_EXPLORATION
)
from src.items.item import Item


class InventoryState(GameState):
    """Estado del inventario"""
    
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.game = None
        self.player = None
        self.inventory = None
        
        # UI
        self.font = None
        self.title_font = None
        self.small_font = None
        
        # Navegación
        self.selected_slot = 0
        self.scroll_offset = 0
        self.slots_per_page = 10
        
        # Filtros
        self.current_filter = "Todos"
        self.filters = ["Todos", "Consumibles", "Materiales", "Armas", "Armaduras"]
        self.filter_index = 0
    
    def enter(self):
        """Inicializa el estado de inventario"""
        # Obtener referencia al jugador
        if self.game:
            # Buscar el estado de exploración para obtener el jugador
            exploration = self.state_manager._states.get(STATE_EXPLORATION)
            if exploration and hasattr(exploration, 'player'):
                self.player = exploration.player
                self.inventory = self.player.inventory
        
        # Fuentes
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 18)
        
        self.selected_slot = 0
        self.scroll_offset = 0
    
    def handle_event(self, event):
        """Maneja eventos de entrada"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                # Cerrar inventario
                self.state_manager.pop_state()
                return True
            elif event.key == pygame.K_UP:
                if self.selected_slot > 0:
                    self.selected_slot -= 1
                    # Ajustar scroll
                    if self.selected_slot < self.scroll_offset:
                        self.scroll_offset = self.selected_slot
                return True
            elif event.key == pygame.K_DOWN:
                max_slots = self._get_filtered_slots_count()
                if self.selected_slot < max_slots - 1:
                    self.selected_slot += 1
                    # Ajustar scroll
                    if self.selected_slot >= self.scroll_offset + self.slots_per_page:
                        self.scroll_offset = self.selected_slot - self.slots_per_page + 1
                return True
            elif event.key == pygame.K_LEFT:
                # Cambiar filtro
                self.filter_index = (self.filter_index - 1) % len(self.filters)
                self.current_filter = self.filters[self.filter_index]
                self.selected_slot = 0
                self.scroll_offset = 0
                return True
            elif event.key == pygame.K_RIGHT:
                # Cambiar filtro
                self.filter_index = (self.filter_index + 1) % len(self.filters)
                self.current_filter = self.filters[self.filter_index]
                self.selected_slot = 0
                self.scroll_offset = 0
                return True
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Usar item seleccionado
                self._use_selected_item()
                return True
            elif event.key == pygame.K_e:
                # Equipar item (si es equipable)
                self._equip_selected_item()
                return True
            elif event.key == pygame.K_x:
                # Tirar item
                self._drop_selected_item()
                return True
        
        return False
    
    def _get_filtered_slots(self):
        """Retorna los slots filtrados según la categoría actual"""
        if not self.inventory:
            return []
        
        if self.current_filter == "Todos":
            return [(i, slot) for i, slot in enumerate(self.inventory.slots) if not slot.is_empty()]
        else:
            category_map = {
                "Consumibles": "Consumible",
                "Materiales": "Material",
                "Armas": "Arma",
                "Armaduras": "Armadura"
            }
            category = category_map.get(self.current_filter, "Todos")
            return [(i, slot) for i, slot in enumerate(self.inventory.slots) 
                   if not slot.is_empty() and slot.item.categoria == category]
    
    def _get_filtered_slots_count(self):
        """Retorna el número de slots filtrados"""
        return len(self._get_filtered_slots())
    
    def _use_selected_item(self):
        """Usa el item seleccionado"""
        filtered_slots = self._get_filtered_slots()
        if self.selected_slot < len(filtered_slots):
            slot_index, slot = filtered_slots[self.selected_slot]
            if slot.item and slot.item.is_consumible():
                # TODO: Aplicar efectos del consumible
                print(f"Usando {slot.item.nombre}")
                # Por ahora solo remover 1
                slot.remove_item(1)
    
    def _equip_selected_item(self):
        """Equipa el item seleccionado"""
        if not self.player:
            return
        
        filtered_slots = self._get_filtered_slots()
        if self.selected_slot < len(filtered_slots):
            slot_index, slot = filtered_slots[self.selected_slot]
            if slot.item and slot.item.is_equipable():
                previous_item = self.player.equip_item(slot.item)
                # Remover el item del inventario
                slot.remove_item(1)
                # Si había un item anterior, agregarlo al inventario
                if previous_item:
                    self.inventory.add_item(previous_item, 1)
                print(f"Equipado: {slot.item.nombre}")
    
    def _drop_selected_item(self):
        """Tira el item seleccionado"""
        filtered_slots = self._get_filtered_slots()
        if self.selected_slot < len(filtered_slots):
            slot_index, slot = filtered_slots[self.selected_slot]
            if slot.item:
                # Remover 1 del stack
                slot.remove_item(1)
                print(f"Tirado: {slot.item.nombre}")
    
    def update(self, dt):
        """Actualiza la lógica del inventario"""
        pass
    
    def render(self, screen):
        """Renderiza la UI del inventario"""
        if not self.inventory:
            return
        
        # Fondo semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Panel principal
        panel_width = 800
        panel_height = 600
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2
        
        # Fondo del panel
        panel = pygame.Surface((panel_width, panel_height))
        panel.fill((40, 40, 40))
        pygame.draw.rect(panel, COLOR_WHITE, (0, 0, panel_width, panel_height), 2)
        screen.blit(panel, (panel_x, panel_y))
        
        # Título
        title_text = self.title_font.render("INVENTARIO", True, COLOR_WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 30))
        screen.blit(title_text, title_rect)
        
        # Filtro actual
        filter_text = self.font.render(f"Filtro: {self.current_filter} (← →)", True, COLOR_WHITE)
        screen.blit(filter_text, (panel_x + 20, panel_y + 70))
        
        # Lista de items
        filtered_slots = self._get_filtered_slots()
        start_index = self.scroll_offset
        end_index = min(start_index + self.slots_per_page, len(filtered_slots))
        
        y_offset = panel_y + 110
        for i in range(start_index, end_index):
            if i >= len(filtered_slots):
                break
            
            slot_index, slot = filtered_slots[i]
            is_selected = (i == self.selected_slot)
            
            # Color de fondo
            bg_color = (80, 80, 80) if is_selected else (60, 60, 60)
            item_rect = pygame.Rect(panel_x + 20, y_offset + (i - start_index) * 45, 
                                   panel_width - 40, 40)
            pygame.draw.rect(screen, bg_color, item_rect)
            if is_selected:
                pygame.draw.rect(screen, COLOR_WHITE, item_rect, 2)
            
            # Nombre del item
            if slot.item:
                item_name = slot.item.nombre
                if slot.quantity > 1:
                    item_name += f" x{slot.quantity}"
                name_text = self.font.render(item_name, True, COLOR_WHITE)
                screen.blit(name_text, (panel_x + 30, y_offset + (i - start_index) * 45 + 8))
                
                # Descripción (pequeña)
                desc_text = self.small_font.render(slot.item.descripcion[:50], True, (150, 150, 150))
                screen.blit(desc_text, (panel_x + 30, y_offset + (i - start_index) * 45 + 25))
        
        # Instrucciones
        instructions_y = panel_y + panel_height - 80
        instructions = [
            "ENTER: Usar | E: Equipar | X: Tirar | ESC: Cerrar"
        ]
        for instruction in instructions:
            inst_text = self.small_font.render(instruction, True, (200, 200, 200))
            screen.blit(inst_text, (panel_x + 20, instructions_y))
            instructions_y += 20

