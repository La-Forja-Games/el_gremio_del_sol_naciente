"""
Estado del menú principal
"""

import pygame
from src.state_manager import GameState
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, STATE_EXPLORATION


class MenuState(GameState):
    """Menú principal del juego"""
    
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = None
        self.title_font = None
        self.selected_option = 0
        self.options = ["Nueva Partida", "Cargar Partida", "Opciones", "Salir"]
        self.game = None  # Referencia al juego (se asigna desde Game)
        self.background = None  # Imagen de fondo
        
    def enter(self):
        """Inicializa el estado del menú"""
        # Cargar fuentes épicas
        from src.utils.font_helper import get_epic_font
        self.font = get_epic_font(36, bold=True)
        self.title_font = get_epic_font(72, bold=True)
        
        # Cargar imagen de fondo
        if self.game and self.game.resource_manager:
            self.background = self.game.resource_manager.load_image("ui/main_menu_bg.png", use_alpha=False)
            # Escalar la imagen al tamaño de la pantalla si es necesario
            if self.background:
                from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
                bg_width = self.background.get_width()
                bg_height = self.background.get_height()
                # Solo escalar si el tamaño es diferente
                if bg_width != SCREEN_WIDTH or bg_height != SCREEN_HEIGHT:
                    self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
                print(f"[OK] Fondo del menú cargado: {bg_width}x{bg_height}")
            else:
                print("[ADVERTENCIA] No se pudo cargar el fondo del menú")
        
    def update(self, dt):
        """Actualiza la lógica del menú"""
        pass
    
    def handle_event(self, event):
        """Maneja eventos de entrada"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._select_option()
        return True
    
    def _select_option(self):
        """Ejecuta la opción seleccionada"""
        if self.selected_option == 0:  # Nueva Partida
            # Iniciar nueva partida (ir a exploración)
            self.state_manager.change_state(STATE_EXPLORATION)
        elif self.selected_option == 1:  # Cargar Partida
            # Abrir menú de carga
            save_load = self.state_manager._states.get("save_load")
            if save_load:
                save_load.set_mode(False)  # Modo cargar
                self.state_manager.push_state("save_load")
        elif self.selected_option == 2:  # Opciones
            # TODO: Mostrar menú de opciones
            print("Opciones - Por implementar")
        elif self.selected_option == 3:  # Salir
            pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def render(self, screen):
        """Renderiza el menú con assets RPG"""
        # Fondo (imagen o color sólido)
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            # Fallback: fondo negro si no hay imagen
            from src.config import COLOR_BLACK
            screen.fill(COLOR_BLACK)
        
        # Título con mejor contraste
        from src.config import COLOR_BLACK, COLOR_WHITE
        # Usar color blanco para mejor contraste con el fondo
        title_color = COLOR_WHITE
        
        # Sombra del título para mejor legibilidad
        title_shadow = self.title_font.render("El Gremio del Sol Naciente", True, (0, 0, 0))
        title_text = self.title_font.render("El Gremio del Sol Naciente", True, title_color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2 + 2, 152))
        screen.blit(title_shadow, title_rect)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)
        
        # Opciones del menú con mejor estilo
        y_offset = 320
        button_width = 400
        button_height = 50
        
        for i, option in enumerate(self.options):
            # Color según selección
            if i == self.selected_option:
                # Opción seleccionada: color destacado
                text_color = (255, 215, 0)  # Dorado
                bg_color = (100, 100, 100, 180)  # Fondo semi-transparente
            else:
                # Opción no seleccionada
                text_color = COLOR_WHITE
                bg_color = (50, 50, 50, 120)
            
            # Fondo del botón (rectángulo semi-transparente)
            button_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - button_width // 2,
                y_offset + i * 70 - button_height // 2,
                button_width,
                button_height
            )
            button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
            button_surface.fill(bg_color)
            screen.blit(button_surface, button_rect)
            
            # Texto del botón
            text = self.font.render(option, True, text_color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 70))
            screen.blit(text, text_rect)
            
            # Indicador de selección (flecha o símbolo)
            if i == self.selected_option:
                # Dibujar flecha o símbolo de selección
                arrow_points = [
                    (SCREEN_WIDTH // 2 - button_width // 2 + 20, y_offset + i * 70),
                    (SCREEN_WIDTH // 2 - button_width // 2 + 10, y_offset + i * 70 - 8),
                    (SCREEN_WIDTH // 2 - button_width // 2 + 10, y_offset + i * 70 + 8)
                ]
                pygame.draw.polygon(screen, text_color, arrow_points)

