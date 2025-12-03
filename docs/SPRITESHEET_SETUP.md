# Configuración de Spritesheets

## Ubicación de Sprites

Coloca los spritesheets en la carpeta `assets/sprites/`

## Spritesheet del Jugador

El spritesheet del jugador debe llamarse `player.png` y estar en `assets/sprites/player.png`

### Formato Esperado

- **Tamaño de cada sprite**: 32x32 píxeles (TILE_SIZE)
- **Layout**: Grid 4x4 (16 sprites totales)
- **Formato**: PNG con transparencia

### Layout del Spritesheet (según descripción):

```
Fila 0: [Front Idle (sword), Back Idle, Back Idle (arms out), Front Idle (arms out)]
Fila 1: [Duplicado de Fila 0]
Fila 2: [Front Idle, Front con espada fuego (izq), Back Idle, Front con espada fuego (der)]
Fila 3: [Front Idle, Front Idle, Front Walking, Front con espada fuego (der)]
```

### Uso

El sistema automáticamente:
- Detecta si existe `assets/sprites/player.png`
- Si existe, carga y usa el spritesheet
- Si no existe, usa sprites generados como fallback

## Otros Sprites

Para agregar más spritesheets:
1. Coloca el archivo en `assets/sprites/`
2. Usa `SpriteSheetLoader` para cargarlo
3. Extrae los frames necesarios con `get_sprite(x, y)` o `get_animation_frames(row, start_col, num_frames)`

