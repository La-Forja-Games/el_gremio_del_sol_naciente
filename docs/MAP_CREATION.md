# Guía para Crear Mapas con Tiled

## Requisitos

1. **Tiled Map Editor**: Descarga desde [mapeditor.org](https://www.mapeditor.org/)
2. **Tilesets**: Necesitarás tilesets en formato de imagen (PNG) para crear los mapas

## Estructura de Capas Recomendada

Cada mapa debe tener las siguientes capas (en este orden):

### 1. Capas de Tiles (Tile Layers)

- **Background**: Fondo del mapa (césped, tierra, etc.)
- **Terrain**: Terreno principal (caminos, estructuras)
- **Objects**: Objetos decorativos (árboles, rocas, etc.)
- **Foreground**: Elementos que van delante del jugador (opcional)

### 2. Capas de Objetos (Object Layers)

- **Collision**: Objetos rectangulares que marcan zonas de colisión
- **Events**: Objetos que activan eventos (cambios de mapa, diálogos, etc.)

## Configuración del Mapa

1. **Tamaño del Tile**: 32x32 píxeles (configurado en `src/config.py`)
2. **Formato**: Guardar como `.tmx` (formato XML de Tiled)
3. **Ubicación**: Guardar en `data/maps/`

## Crear un Mapa de Prueba

### Paso 1: Crear el Mapa

1. Abre Tiled
2. File → New → New Map
3. Configura:
   - **Orientation**: Orthogonal
   - **Tile layer format**: CSV
   - **Tile size**: 32 x 32
   - **Map size**: 50 x 50 tiles (o el tamaño que prefieras)

### Paso 2: Agregar Tilesets

1. File → Add External Tileset
2. Selecciona tu archivo de tileset (PNG)
3. Configura el tamaño de tile (32x32)

### Paso 3: Crear Capas

1. **Capa de Fondo**:
   - Crea una capa de tiles llamada "Background"
   - Dibuja el fondo del mapa

2. **Capa de Colisión**:
   - Crea una capa de objetos llamada "Collision"
   - Dibuja rectángulos donde no debe pasar el jugador
   - Los objetos deben tener el nombre "collision" o estar en una capa llamada "Collision"

3. **Capa de Eventos**:
   - Crea una capa de objetos llamada "Events"
   - Agrega objetos para puntos de spawn:
     - Nombre: "spawn" o "spawn_default"
     - Posición: Donde aparecerá el jugador

### Paso 4: Guardar

1. File → Save As
2. Guarda en `data/maps/test_map.tmx`

## Ejemplo de Uso en el Código

```python
# En exploration_state.py
self.map_manager.load_map("test_map.tmx")
```

## Notas Importantes

- Los nombres de las capas son case-insensitive
- Las capas de colisión y eventos deben ser **Object Layers**, no Tile Layers
- Los objetos de spawn deben tener un nombre que comience con "spawn_"
- El sistema busca automáticamente objetos con nombre "spawn" o "default" si no se especifica un spawn point

