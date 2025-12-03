"""
Script para crear map_01.tmx - Un pueblo completo con caminos sinuosos, 
dos asentamientos, bosques, rocas y agua
"""

import os
import math
from pathlib import Path

def create_village_map():
    """Crea un mapa de pueblo completo estilo isométrico"""
    
    # Configuración del mapa
    map_width = 80
    map_height = 80
    tile_size = 32
    
    # Rutas
    base_dir = Path(__file__).parent
    maps_dir = base_dir / "data" / "maps"
    maps_dir.mkdir(parents=True, exist_ok=True)
    
    # Generar datos CSV para Background (todo grass - tile 1)
    background_data = []
    for y in range(map_height):
        row = []
        for x in range(map_width):
            row.append("1")  # Tile 1 = base_grass
        background_data.append(",".join(row))
    background_csv = "\n".join(background_data) + "\n"
    
    # Generar datos CSV para Terrain (caminos, casas, agua, etc.)
    terrain_data = []
    
    # Asentamiento 1: Superior izquierda (meseta rocosa)
    settlement1_x = 8
    settlement1_y = 8
    settlement1_size = 12
    
    # Asentamiento 2: Inferior izquierda (costero)
    settlement2_x = 10
    settlement2_y = map_height - 18
    settlement2_size = 10
    
    # Casa del abuelo (en el asentamiento 1, más grande)
    grandpa_house_x = settlement1_x + 2
    grandpa_house_y = settlement1_y + 2
    grandpa_house_w = 6
    grandpa_house_h = 5
    
    for y in range(map_height):
        row = []
        for x in range(map_width):
            tile_gid = "0"  # Vacío por defecto
            
            # AGUA Y PLAYA (esquina inferior izquierda)
            if x < 15 and y > map_height - 20:
                # Agua (usar tile oscuro o especial si existe)
                if x < 8 and y > map_height - 12:
                    tile_gid = "0"  # Agua (se puede agregar tileset de agua después)
                # Playa (arena)
                elif x < 12 and y > map_height - 15:
                    # Usar tile de piso claro para playa
                    tile_gid = "1182"  # Tile de piso claro
            
            # BOSQUES (bordes del mapa)
            elif x < 5 or x >= map_width - 5 or y < 5 or y >= map_height - 5:
                # Bosque denso (usar tiles de árboles en la capa de objetos)
                pass  # Los árboles van en la capa de objetos
            
            # ASENTAMIENTO 1: Superior izquierda (meseta rocosa)
            elif settlement1_x <= x < settlement1_x + settlement1_size and settlement1_y <= y < settlement1_y + settlement1_size:
                # Casa del abuelo (más grande)
                if grandpa_house_x <= x < grandpa_house_x + grandpa_house_w and grandpa_house_y <= y < grandpa_house_y + grandpa_house_h:
                    if x == grandpa_house_x or x == grandpa_house_x + grandpa_house_w - 1 or y == grandpa_house_y or y == grandpa_house_y + grandpa_house_h - 1:
                        tile_gid = "1225"  # Pared
                    else:
                        tile_gid = "1226"  # Techo/interior
                # Casa 2 (asentamiento 1)
                elif settlement1_x + 6 <= x < settlement1_x + 11 and settlement1_y + 1 <= y < settlement1_y + 5:
                    if x == settlement1_x + 6 or x == settlement1_x + 10 or y == settlement1_y + 1 or y == settlement1_y + 4:
                        tile_gid = "1225"
                    else:
                        tile_gid = "1226"
                # Casa 3 (asentamiento 1)
                elif settlement1_x + 1 <= x < settlement1_x + 6 and settlement1_y + 7 <= y < settlement1_y + 11:
                    if x == settlement1_x + 1 or x == settlement1_x + 5 or y == settlement1_y + 7 or y == settlement1_y + 10:
                        tile_gid = "1225"
                    else:
                        tile_gid = "1226"
                # Casa 4 (asentamiento 1 - torre)
                elif settlement1_x + 9 <= x < settlement1_x + 12 and settlement1_y + 7 <= y < settlement1_y + 11:
                    if x == settlement1_x + 9 or x == settlement1_x + 11 or y == settlement1_y + 7 or y == settlement1_y + 10:
                        tile_gid = "1225"
                    else:
                        tile_gid = "1226"
                # Rocas en la meseta
                elif (x + y) % 7 == 0:
                    tile_gid = "1026"  # Tile de roca (legacy_Tiles)
            
            # ASENTAMIENTO 2: Inferior izquierda (costero)
            elif settlement2_x <= x < settlement2_x + settlement2_size and settlement2_y <= y < settlement2_y + settlement2_size:
                # Casa 1 (asentamiento 2)
                if settlement2_x + 1 <= x < settlement2_x + 6 and settlement2_y + 1 <= y < settlement2_y + 5:
                    if x == settlement2_x + 1 or x == settlement2_x + 5 or y == settlement2_y + 1 or y == settlement2_y + 4:
                        tile_gid = "1225"
                    else:
                        tile_gid = "1226"
                # Casa 2 (asentamiento 2 - con domo)
                elif settlement2_x + 6 <= x < settlement2_x + 11 and settlement2_y + 2 <= y < settlement2_y + 6:
                    if x == settlement2_x + 6 or x == settlement2_x + 10 or y == settlement2_y + 2 or y == settlement2_y + 5:
                        tile_gid = "1225"
                    else:
                        tile_gid = "1226"
                # Casa 3 (asentamiento 2)
                elif settlement2_x + 2 <= x < settlement2_x + 7 and settlement2_y + 7 <= y < settlement2_y + 11:
                    if x == settlement2_x + 2 or x == settlement2_x + 6 or y == settlement2_y + 7 or y == settlement2_y + 10:
                        tile_gid = "1225"
                    else:
                        tile_gid = "1226"
            
            # CAMINOS SINUOSOS (conectando asentamientos)
            # Camino desde asentamiento 1 hacia el centro
            path1_points = []
            for t in range(0, 50):
                px = int(settlement1_x + settlement1_size // 2 + t * 0.8 + math.sin(t * 0.2) * 2)
                py = int(settlement1_y + settlement1_size // 2 + t * 0.6 + math.cos(t * 0.15) * 1.5)
                if 0 <= px < map_width and 0 <= py < map_height:
                    path1_points.append((px, py))
            
            # Camino desde asentamiento 2 hacia el centro
            path2_points = []
            for t in range(0, 40):
                px = int(settlement2_x + settlement2_size // 2 + t * 0.7 + math.sin(t * 0.25) * 2.5)
                py = int(settlement2_y - t * 0.8 + math.cos(t * 0.2) * 1.8)
                if 0 <= px < map_width and 0 <= py < map_height:
                    path2_points.append((px, py))
            
            # Camino central (conectando los dos caminos)
            center_x = map_width // 2
            center_y = map_height // 2
            path_center_points = []
            for t in range(0, 30):
                px = int(center_x - 15 + t + math.sin(t * 0.3) * 3)
                py = int(center_y - 10 + t * 0.5 + math.cos(t * 0.25) * 2)
                if 0 <= px < map_width and 0 <= py < map_height:
                    path_center_points.append((px, py))
            
            # Aplicar caminos (3 tiles de ancho)
            all_path_points = set()
            for path_points in [path1_points, path2_points, path_center_points]:
                for px, py in path_points:
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            nx, ny = px + dx, py + dy
                            if 0 <= nx < map_width and 0 <= ny < map_height:
                                all_path_points.add((nx, ny))
            
            if (x, y) in all_path_points:
                tile_gid = "1181"  # Camino de piedra
            
            # ROCAS DISPERSAS (formaciones rocosas)
            # Rocas grandes en el lado derecho
            if map_width - 15 <= x < map_width - 5 and 10 <= y < map_height - 10:
                if (x + y * 2) % 8 < 2:
                    tile_gid = "1026"  # Roca
            
            # Rocas pequeñas dispersas
            elif 15 < x < map_width - 15 and 15 < y < map_height - 15:
                if (x * 3 + y * 5) % 23 == 0 and tile_gid == "0":
                    tile_gid = "1027"  # Roca pequeña
            
            row.append(tile_gid)
        terrain_data.append(",".join(row))
    terrain_csv = "\n".join(terrain_data) + "\n"
    
    # Capa de objetos (árboles, vegetación)
    objects_data = []
    for y in range(map_height):
        row = []
        for x in range(map_width):
            tile_gid = "0"
            
            # BOSQUES DENSOS (bordes)
            if x < 8 or x >= map_width - 8 or y < 8 or y >= map_height - 8:
                # Árboles densos en los bordes
                if (x + y) % 3 == 0:
                    tile_gid = "1381"  # Árbol
                elif (x + y) % 5 == 0:
                    tile_gid = "1382"  # Variante de árbol
            
            # VEGETACIÓN DISPERSA (entre caminos y casas)
            else:
                # Verificar que no esté en camino o casa
                is_road = False
                is_house = False
                
                # Verificar caminos
                settlement1_center = (settlement1_x + settlement1_size // 2, settlement1_y + settlement1_size // 2)
                settlement2_center = (settlement2_x + settlement2_size // 2, settlement2_y + settlement2_size // 2)
                center = (map_width // 2, map_height // 2)
                
                # Distancia a caminos principales
                dist_to_path1 = abs(x - settlement1_center[0]) + abs(y - settlement1_center[1])
                dist_to_path2 = abs(x - settlement2_center[0]) + abs(y - settlement2_center[1])
                dist_to_center = abs(x - center[0]) + abs(y - center[1])
                
                if dist_to_path1 < 3 or dist_to_path2 < 3 or dist_to_center < 5:
                    is_road = True
                
                # Verificar casas
                houses = [
                    (grandpa_house_x, grandpa_house_y, grandpa_house_w, grandpa_house_h),
                    (settlement1_x + 6, settlement1_y + 1, 5, 4),
                    (settlement1_x + 1, settlement1_y + 7, 5, 4),
                    (settlement1_x + 9, settlement1_y + 7, 3, 4),
                    (settlement2_x + 1, settlement2_y + 1, 5, 4),
                    (settlement2_x + 6, settlement2_y + 2, 5, 4),
                    (settlement2_x + 2, settlement2_y + 7, 5, 4),
                ]
                
                for hx, hy, hw, hh in houses:
                    if hx <= x < hx + hw and hy <= y < hy + hh:
                        is_house = True
                        break
                
                # Colocar árboles/bushes dispersos
                if not is_road and not is_house:
                    if (x * 7 + y * 11) % 17 == 0:
                        tile_gid = "1381"  # Árbol
                    elif (x * 5 + y * 9) % 21 == 0:
                        tile_gid = "1383"  # Bush/vegetación
            
            row.append(tile_gid)
        objects_data.append(",".join(row))
    objects_csv = "\n".join(objects_data) + "\n"
    
    # Punto de spawn (frente a la casa del abuelo)
    spawn_x = (grandpa_house_x + grandpa_house_w // 2) * tile_size - 16
    spawn_y = (grandpa_house_y + grandpa_house_h) * tile_size - 16
    
    # Colisiones (paredes de todas las casas)
    collision_objects = []
    collision_id = 1
    
    # Casa del abuelo
    collision_objects.append(f'  <object id="{collision_id}" name="house_grandpa_wall_1" x="{grandpa_house_x * tile_size}" y="{grandpa_house_y * tile_size}" width="{grandpa_house_w * tile_size}" height="{tile_size}"/>')
    collision_id += 1
    collision_objects.append(f'  <object id="{collision_id}" name="house_grandpa_wall_2" x="{grandpa_house_x * tile_size}" y="{grandpa_house_y * tile_size}" width="{tile_size}" height="{grandpa_house_h * tile_size}"/>')
    collision_id += 1
    collision_objects.append(f'  <object id="{collision_id}" name="house_grandpa_wall_3" x="{(grandpa_house_x + grandpa_house_w - 1) * tile_size}" y="{grandpa_house_y * tile_size}" width="{tile_size}" height="{grandpa_house_h * tile_size}"/>')
    collision_id += 1
    collision_objects.append(f'  <object id="{collision_id}" name="house_grandpa_wall_4" x="{grandpa_house_x * tile_size}" y="{(grandpa_house_y + grandpa_house_h - 1) * tile_size}" width="{grandpa_house_w * tile_size}" height="{tile_size}"/>')
    collision_id += 1
    
    # Agregar colisiones para otras casas
    other_houses = [
        (settlement1_x + 6, settlement1_y + 1, 5, 4, "house1"),
        (settlement1_x + 1, settlement1_y + 7, 5, 4, "house2"),
        (settlement1_x + 9, settlement1_y + 7, 3, 4, "house3"),
        (settlement2_x + 1, settlement2_y + 1, 5, 4, "house4"),
        (settlement2_x + 6, settlement2_y + 2, 5, 4, "house5"),
        (settlement2_x + 2, settlement2_y + 7, 5, 4, "house6"),
    ]
    
    for hx, hy, hw, hh, name in other_houses:
        collision_objects.append(f'  <object id="{collision_id}" name="{name}_wall_1" x="{hx * tile_size}" y="{hy * tile_size}" width="{hw * tile_size}" height="{tile_size}"/>')
        collision_id += 1
        collision_objects.append(f'  <object id="{collision_id}" name="{name}_wall_2" x="{hx * tile_size}" y="{hy * tile_size}" width="{tile_size}" height="{hh * tile_size}"/>')
        collision_id += 1
        collision_objects.append(f'  <object id="{collision_id}" name="{name}_wall_3" x="{(hx + hw - 1) * tile_size}" y="{hy * tile_size}" width="{tile_size}" height="{hh * tile_size}"/>')
        collision_id += 1
        collision_objects.append(f'  <object id="{collision_id}" name="{name}_wall_4" x="{hx * tile_size}" y="{(hy + hh - 1) * tile_size}" width="{hw * tile_size}" height="{tile_size}"/>')
        collision_id += 1
    
    collision_xml = "\n".join(collision_objects)
    
    # Plantilla XML del mapa
    map_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<map version="1.10" tiledversion="1.10.2" orientation="orthogonal" renderorder="right-down" width="{map_width}" height="{map_height}" tilewidth="{tile_size}" tileheight="{tile_size}" infinite="0" nextlayerid="6" nextobjectid="{collision_id + 1}">
 <tileset firstgid="1" name="base_grass" tilewidth="{tile_size}" tileheight="{tile_size}" tilecount="1024" columns="32">
  <image source="../../assets/tilesets/base_grass.png" width="1024" height="1024"/>
 </tileset>
 <tileset firstgid="1025" name="legacy_Tiles" tilewidth="{tile_size}" tileheight="{tile_size}" tilecount="156" columns="13">
  <image source="../../assets/tilesets/legacy_Tiles.png" width="416" height="384"/>
 </tileset>
 <tileset firstgid="1181" name="walls_floor" tilewidth="{tile_size}" tileheight="{tile_size}" tilecount="44" columns="5">
  <image source="../../assets/tilesets/walls_floor.png" width="160" height="288"/>
 </tileset>
 <tileset firstgid="1225" name="legacy_Buildings" tilewidth="{tile_size}" tileheight="{tile_size}" tilecount="156" columns="13">
  <image source="../../assets/tilesets/legacy_Buildings.png" width="416" height="384"/>
 </tileset>
 <tileset firstgid="1381" name="legacy_Tree-Assets" tilewidth="{tile_size}" tileheight="{tile_size}" tilecount="131" columns="11">
  <image source="../../assets/tilesets/legacy_Tree-Assets.png" width="352" height="384"/>
 </tileset>
 <layer id="1" name="Background" width="{map_width}" height="{map_height}">
  <data encoding="csv">
{background_csv}</data>
 </layer>
 <layer id="2" name="Terrain" width="{map_width}" height="{map_height}">
  <data encoding="csv">
{terrain_csv}</data>
 </layer>
 <layer id="3" name="Objects" width="{map_width}" height="{map_height}">
  <data encoding="csv">
{objects_csv}</data>
 </layer>
 <objectgroup id="4" name="Collision">
{collision_xml}
 </objectgroup>
 <objectgroup id="5" name="Events">
  <object id="{collision_id + 1}" name="spawn_default" x="{spawn_x}" y="{spawn_y}" width="32" height="32">
   <properties>
    <property name="type" value="spawn"/>
   </properties>
  </object>
 </objectgroup>
</map>'''
    
    # Escribir archivo
    map_file = maps_dir / "map_01.tmx"
    with open(map_file, 'w', encoding='utf-8') as f:
        f.write(map_xml)
    
    print(f"[OK] Mapa de pueblo completo creado: {map_file}")
    print(f"  Tamaño: {map_width}x{map_height} tiles")
    print(f"  Tamaño en píxeles: {map_width * tile_size}x{map_height * tile_size}")
    print(f"  Asentamiento 1 (meseta): {settlement1_size}x{settlement1_size} tiles con 4 casas")
    print(f"  Asentamiento 2 (costero): {settlement2_size}x{settlement2_size} tiles con 3 casas")
    print(f"  Casa del abuelo: {grandpa_house_w}x{grandpa_house_h} tiles (asentamiento 1)")
    print(f"  Caminos: sinuosos conectando asentamientos")
    print(f"  Bosques: densos en los bordes")
    print(f"  Rocas: formaciones grandes y pequeñas")
    print(f"  Agua/Playa: esquina inferior izquierda")
    print(f"  Punto de spawn: frente a la casa del abuelo")
    return True

if __name__ == "__main__":
    create_village_map()
