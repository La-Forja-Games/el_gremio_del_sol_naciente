# El Gremio del Sol Naciente

Un RPG de vista superior desarrollado con Python y Pygame, inspirado en los clásicos *Zelda* y *Pokémon*.

## 📖 Descripción

El juego sigue las aventuras de un grupo de exploradores en un continente recién descubierto. Los jugadores deben explorar múltiples biomas, gestionar recursos en el campamento base, y desarrollar habilidades profundas para cada miembro del gremio.

## 🎮 Características

- **Sistema de Combate por Turnos** con posicionamiento táctico
- **Múltiples Biomas** (Bosques, Desiertos, Montañas Nevadas)
- **Sistema de Gestión de Recursos** para el campamento base
- **Árbol de Habilidades Profundo** para cada personaje
- **5 Actos** con mecánicas únicas por región
- **Sistema de Crafting** y mejoras del campamento

## 🚀 Instalación

### Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd el_gremio_del_sol_naciente
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
```

3. Activar el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

5. Verificar la instalación (opcional):
```bash
python check_setup.py
```

## 🎯 Ejecución

```bash
python main.py
```

El juego iniciará con el menú principal. Usa las flechas ↑↓ para navegar y Enter para seleccionar.

## 📁 Estructura del Proyecto

```
el_gremio_del_sol_naciente/
├── src/                    # Código fuente principal
│   ├── game.py            # Loop principal del juego
│   ├── config.py          # Configuración global
│   ├── state_manager.py   # Gestor de estados
│   ├── resource_manager.py # Gestor de recursos
│   ├── camera.py          # Sistema de cámara
│   └── states/            # Estados del juego
│       └── menu_state.py  # Estado del menú
├── assets/                # Recursos gráficos y de audio
│   ├── sprites/          # Spritesheets de personajes
│   ├── tilesets/         # Tilesets para mapas
│   ├── ui/               # Elementos de interfaz
│   └── audio/            # Música y efectos
├── data/                 # Datos del juego (JSON)
│   ├── items/            # Definiciones de objetos
│   ├── characters/       # Stats y habilidades
│   ├── enemies/          # Stats de enemigos
│   ├── dialogs/          # Diálogos
│   ├── quests/           # Misiones
│   └── maps/             # Archivos .tmx de Tiled
├── saves/                # Partidas guardadas
├── tests/                # Tests unitarios
├── main.py               # Punto de entrada
├── requirements.txt      # Dependencias
└── README.md             # Este archivo
```

## 🛠️ Desarrollo

### Fases de Desarrollo

El proyecto está organizado en fases:

- **Fase 0**: ✅ Configuración inicial y arquitectura (COMPLETADA)
- **Fase 1**: Motor base y sistemas fundamentales
- **Fase 2**: Sistemas de datos y persistencia
- **Fase 3**: Combate por turnos
- **Fase 4**: Interfaz de usuario (UI)
- **Fase 5**: Sistemas de progresión y contenido
- **Fase 6**: Campamento base y crafting
- **Fase 7**: Mecánicas específicas por acto
- **Fase 8**: Contenido y assets
- **Fase 9**: Implementación de la historia
- **Fase 10**: Pulido y optimización

### Herramientas Recomendadas

- **Tiled Map Editor**: Para diseñar mapas
- **Aseprite** o **GIMP**: Para crear sprites pixel art
- **Audacity**: Para editar audio

## 📝 Licencia

[Especificar licencia]

## 👥 Créditos

Desarrollado siguiendo el plan de desarrollo detallado del proyecto.
