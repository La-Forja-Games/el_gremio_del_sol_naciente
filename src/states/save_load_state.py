"""
Estado de guardado/carga - UI de guardado y carga
"""

import pygame
from src.state_manager import GameState
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, STATE_MENU, STATE_EXPLORATION
)
from src.save.save_manager import SaveManager
from src.save.game_state_serializer import serialize_game_state, deserialize_game_state


class SaveLoadState(GameState):
    """Estado de guardado/carga"""
    
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.game = None
        self.save_manager = SaveManager()
        self.is_save_mode = True  # True para guardar, False para cargar
        
        # UI
        self.font = None
        self.title_font = None
        self.small_font = None
        
        # Navegación
        self.selected_slot = 0
        self.max_slots = 10
        self.save_info = []
    
    def enter(self):
        """Inicializa el estado de guardado/carga"""
        # Fuentes
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 18)
        
        self.selected_slot = 0
        self._refresh_save_info()
    
    def set_mode(self, is_save: bool):
        """Establece el modo (guardar o cargar)"""
        self.is_save_mode = is_save
        self._refresh_save_info()
    
    def _refresh_save_info(self):
        """Actualiza la información de los slots"""
        self.save_info = []
        for slot in range(1, self.max_slots + 1):
            info = self.save_manager.get_save_info(slot)
            if info:
                self.save_info.append(info)
            else:
                self.save_info.append({"slot": slot, "save_time": None})
    
    def handle_event(self, event):
        """Maneja eventos de entrada"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Cerrar
                self.state_manager.pop_state()
                return True
            elif event.key == pygame.K_UP:
                self.selected_slot = (self.selected_slot - 1) % self.max_slots
                return True
            elif event.key == pygame.K_DOWN:
                self.selected_slot = (self.selected_slot + 1) % self.max_slots
                return True
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Guardar o cargar
                if self.is_save_mode:
                    self._save_game()
                else:
                    self._load_game()
                return True
            elif event.key == pygame.K_DELETE:
                # Eliminar guardado (solo en modo carga)
                if not self.is_save_mode:
                    self._delete_save()
                return True
        
        return False
    
    def _save_game(self):
        """Guarda el juego en el slot seleccionado"""
        # Obtener el jugador y estado actual
        from src.config import STATE_EXPLORATION
        exploration = self.state_manager._states.get(STATE_EXPLORATION)
        
        if not exploration or not hasattr(exploration, 'player'):
            print("Error: No se puede guardar, no hay partida activa")
            return
        
        player = exploration.player
        current_map_id = exploration.map_transition.get_map_id() or "unknown"
        player_pos = (player.x, player.y)
        
        # Serializar estado del juego
        save_data = serialize_game_state(
            player=player,
            inventory=player.inventory,
            current_map_id=current_map_id,
            player_pos=player_pos,
            game_flags={}  # TODO: Agregar flags de progreso
        )
        
        # Guardar
        slot_number = self.selected_slot + 1
        if self.save_manager.save_game(save_data, slot_number):
            print(f"Partida guardada en slot {slot_number}")
            self._refresh_save_info()
            # Cerrar el menú después de guardar
            self.state_manager.pop_state()
    
    def _load_game(self):
        """Carga el juego desde el slot seleccionado"""
        slot_number = self.selected_slot + 1
        save_data = self.save_manager.load_game(slot_number)
        
        if not save_data:
            print(f"No hay partida guardada en slot {slot_number}")
            return
        
        # Deserializar
        game_state = deserialize_game_state(save_data, self.game.resource_manager)
        
        # Restaurar jugador
        player = game_state["player"]
        inventory = game_state["inventory"]
        world_state = game_state["world_state"]
        
        # Actualizar estado de exploración
        from src.config import STATE_EXPLORATION
        exploration = self.state_manager._states.get(STATE_EXPLORATION)
        
        if exploration:
            exploration.player = player
            exploration.player.inventory = inventory
            
            # Cambiar de mapa si es necesario
            map_id = world_state.get("current_map_id")
            if map_id and map_id != "unknown":
                spawn_pos = exploration.map_transition.change_map(map_id, "default")
                if spawn_pos:
                    player.x = spawn_pos[0]
                    player.y = spawn_pos[1]
                    player.rect.x = int(spawn_pos[0])
                    player.rect.y = int(spawn_pos[1])
            
            # Posición del jugador
            player.x = world_state.get("player_pos_x", player.x)
            player.y = world_state.get("player_pos_y", player.y)
            player.rect.x = int(player.x)
            player.rect.y = int(player.y)
            
            # Actualizar cámara
            if exploration.camera:
                exploration.camera.update(player)
        
        print(f"Partida cargada desde slot {slot_number}")
        # Cerrar y volver a exploración
        self.state_manager.change_state(STATE_EXPLORATION)
    
    def _delete_save(self):
        """Elimina un guardado"""
        slot_number = self.selected_slot + 1
        if self.save_manager.delete_save(slot_number):
            self._refresh_save_info()
    
    def update(self, dt):
        """Actualiza la lógica"""
        pass
    
    def render(self, screen):
        """Renderiza la UI de guardado/carga"""
        # Fondo semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Panel principal
        panel_width = 600
        panel_height = 500
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2
        
        # Fondo del panel
        panel = pygame.Surface((panel_width, panel_height))
        panel.fill((40, 40, 40))
        pygame.draw.rect(panel, COLOR_WHITE, (0, 0, panel_width, panel_height), 2)
        screen.blit(panel, (panel_x, panel_y))
        
        # Título
        title_text = "GUARDAR" if self.is_save_mode else "CARGAR"
        title_surface = self.title_font.render(title_text, True, COLOR_WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 30))
        screen.blit(title_surface, title_rect)
        
        # Lista de slots
        y_offset = panel_y + 80
        for i in range(self.max_slots):
            slot_number = i + 1
            is_selected = (i == self.selected_slot)
            
            # Color de fondo
            bg_color = (80, 80, 80) if is_selected else (60, 60, 60)
            slot_rect = pygame.Rect(panel_x + 20, y_offset + i * 40, panel_width - 40, 35)
            pygame.draw.rect(screen, bg_color, slot_rect)
            if is_selected:
                pygame.draw.rect(screen, COLOR_WHITE, slot_rect, 2)
            
            # Información del slot
            slot_text = f"Slot {slot_number:02d}: "
            info = self.save_info[i] if i < len(self.save_info) else {"save_time": None}
            
            if info.get("save_time"):
                # Hay guardado
                from datetime import datetime
                try:
                    save_time = datetime.fromisoformat(info["save_time"])
                    time_str = save_time.strftime("%Y-%m-%d %H:%M")
                    slot_text += time_str
                except:
                    slot_text += "Guardado disponible"
                
                map_name = info.get("current_map", "Desconocido")
                slot_text += f" - {map_name}"
            else:
                # Vacío
                slot_text += "Vacío"
            
            text_surface = self.font.render(slot_text, True, COLOR_WHITE)
            screen.blit(text_surface, (panel_x + 30, y_offset + i * 40 + 8))
        
        # Instrucciones
        instructions_y = panel_y + panel_height - 50
        if self.is_save_mode:
            inst_text = self.small_font.render("ENTER: Guardar | ESC: Cancelar", True, (200, 200, 200))
        else:
            inst_text = self.small_font.render("ENTER: Cargar | DEL: Eliminar | ESC: Cancelar", True, (200, 200, 200))
        screen.blit(inst_text, (panel_x + 20, instructions_y))

