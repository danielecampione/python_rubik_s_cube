#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cubo di Rubik 3D - Visualizzazione
Implementazione completa da zero con VPython
"""

import vpython as vp
import math
import threading
import time
from rubiks_cube_model import RubiksCubeModel

# I colori primigeni, come le quattro qualità elementari della fisica antica
SOLVED_COLORS = {
    'up': "white",     # Bianco come la purezza del cielo empireo
    'down': "yellow",  # Giallo come l'oro degli alchimisti
    'front': "blue",   # Azzurro come il manto della Vergine
    'back': "green",   # Verde come i prati di primavera
    'right': "red",    # Rosso come il fuoco trasformatore
    'left': "orange"   # Arancio come il sole al tramonto
}

# La traduzione dei colori in numeri, come il sapiente che riduce le qualità sensibili a proporzioni matematiche
VPYTHON_COLORS = {
    "white": vp.vector(1, 1, 1),      # Bianco, somma di tutti i colori, come la luce divina
    "yellow": vp.vector(1, 0.9, 0),   # Giallo, colore dell'intelletto e della saggezza
    "blue": vp.vector(0, 0.4, 1),     # Azzurro, colore del cielo e dell'infinito
    "green": vp.vector(0, 0.8, 0.2),  # Verde, colore della natura e della vita
    "red": vp.vector(1, 0.1, 0),      # Rosso, colore della passione e del sangue
    "orange": vp.vector(1, 0.4, 0)    # Arancio, colore del calore e dell'energia
}

# Mappatura lettere del modello -> nomi colori
LETTER_TO_COLOR = {
    'W': 'white',
    'Y': 'yellow', 
    'B': 'blue',
    'G': 'green',
    'R': 'red',
    'O': 'orange'
}

class RubiksCube3D:
    def __init__(self):
        """Inizializza il cubo 3D"""
        # Modello logico
        self.model = RubiksCubeModel()
        
        # Stato animazione
        self.is_animating = False
        self.animation_callback = None
        
        # Parametri grafici
        self.cube_size = 0.9
        self.sticker_size = 0.8
        self.gap = 0.05
        
        # Colori delle facce
        self.colors = {
            'W': VPYTHON_COLORS["white"],
            'Y': VPYTHON_COLORS["yellow"],
            'B': VPYTHON_COLORS["blue"],
            'G': VPYTHON_COLORS["green"],
            'R': VPYTHON_COLORS["red"],
            'O': VPYTHON_COLORS["orange"]
        }
        
        # Sistema di posizioni logiche per tracciare le trasformazioni
        # Simile al sistema ThreeJS con currentPosition
        self.logical_positions = {}
        
        # Inizializza la scena 3D
        self.setup_scene()
        self.create_cube()
        self.update_colors()
    
    def setup_scene(self):
        """Configura la scena 3D"""
        # Crea la scena VPython
        self.scene = vp.canvas(
            title="Cubo di Rubik 3D",
            width=800,
            height=600,
            background=vp.color.gray(0.95)  # Sfondo molto più chiaro
        )
        
        # Le luci, come i luminari che Dio pose nel firmamento per rischiarare la terra
        vp.distant_light(direction=vp.vector(1,2,1), color=vp.color.gray(0.9))
        vp.distant_light(direction=vp.vector(-1,-2,-0.5), color=vp.color.gray(0.7))
        vp.distant_light(direction=vp.vector(0,1,0), color=vp.color.gray(0.5))
        # La luce ambiente, come l'etere che tutto permea
        self.scene.ambient = vp.color.gray(0.3)
        
        # Posiziona la camera per una vista ottimale
        self.scene.camera.pos = vp.vector(6, 4, 6)
        self.scene.camera.axis = vp.vector(-6, -4, -6)
        self.scene.up = vp.vector(0, 1, 0)
    
    def create_cube(self):
        """Crea la struttura 3D del cubo"""
        self.cubies = {}  # Cubetti individuali
        self.stickers = {}  # Sticker colorati
        self.logical_positions = {}  # Reset delle posizioni logiche
        
        # Crea i 27 cubetti (3x3x3)
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    # Posizione del cubetto
                    pos = vp.vector(
                        (x - 1) * (self.cube_size + self.gap),
                        (y - 1) * (self.cube_size + self.gap),
                        (z - 1) * (self.cube_size + self.gap)
                    )
                    
                    # Crea il cubetto base (nero)
                    cubie = vp.box(
                        pos=pos,
                        size=vp.vector(self.cube_size, self.cube_size, self.cube_size),
                        color=vp.color.gray(0.2),
                        ambient=0.2,
                        diffuse=0.7,
                        specular=0.8,
                        shininess=1.0,
                        emissive=vp.color.gray(0.05)
                    )
                    self.cubies[(x, y, z)] = cubie
                    
                    # Inizializza la posizione logica (simile a ThreeJS currentPosition)
                    self.logical_positions[(x, y, z)] = {'x': x, 'y': y, 'z': z}
                    
                    # Crea gli sticker sulle facce esterne
                    self.create_stickers(x, y, z, pos)
    
    def create_stickers(self, x, y, z, pos):
        """Crea gli sticker colorati per un cubetto"""
        sticker_thickness = 0.02
        offset = (self.cube_size + sticker_thickness) / 2
        
        # Sticker sulla faccia superiore (y = 2)
        if y == 2:
            color_letter = self.model.faces['up'][x][z]
            current_color = LETTER_TO_COLOR[color_letter]
            sticker = vp.box(
                pos=pos + vp.vector(0, offset, 0),
                size=vp.vector(self.sticker_size, sticker_thickness, self.sticker_size),
                color=VPYTHON_COLORS[current_color],
                shininess=0.5
            )
            self.stickers[('up', x, z)] = sticker
        
        # Sticker sulla faccia inferiore (y = 0)
        if y == 0:
            color_letter = self.model.faces['down'][x][z]
            current_color = LETTER_TO_COLOR[color_letter]
            sticker = vp.box(
                pos=pos + vp.vector(0, -offset, 0),
                size=vp.vector(self.sticker_size, sticker_thickness, self.sticker_size),
                color=VPYTHON_COLORS[current_color],
                shininess=0.5
            )
            self.stickers[('down', x, z)] = sticker
        
        # Sticker sulla faccia frontale (z = 2)
        if z == 2:
            color_letter = self.model.faces['front'][x][y]
            current_color = LETTER_TO_COLOR[color_letter]
            sticker = vp.box(
                pos=pos + vp.vector(0, 0, offset),
                size=vp.vector(self.sticker_size, self.sticker_size, sticker_thickness),
                color=VPYTHON_COLORS[current_color],
                shininess=0.5
            )
            self.stickers[('front', x, y)] = sticker
        
        # Sticker sulla faccia posteriore (z = 0)
        if z == 0:
            color_letter = self.model.faces['back'][x][y]
            current_color = LETTER_TO_COLOR[color_letter]
            sticker = vp.box(
                pos=pos + vp.vector(0, 0, -offset),
                size=vp.vector(self.sticker_size, self.sticker_size, sticker_thickness),
                color=VPYTHON_COLORS[current_color],
                shininess=0.5
            )
            self.stickers[('back', x, y)] = sticker
        
        # Sticker sulla faccia destra (x = 2)
        if x == 2:
            color_letter = self.model.faces['right'][z][y]
            current_color = LETTER_TO_COLOR[color_letter]
            sticker = vp.box(
                pos=pos + vp.vector(offset, 0, 0),
                size=vp.vector(sticker_thickness, self.sticker_size, self.sticker_size),
                color=VPYTHON_COLORS[current_color],
                shininess=0.5
            )
            self.stickers[('right', z, y)] = sticker
        
        # Sticker sulla faccia sinistra (x = 0)
        if x == 0:
            color_letter = self.model.faces['left'][z][y]
            current_color = LETTER_TO_COLOR[color_letter]
            sticker = vp.box(
                pos=pos + vp.vector(-offset, 0, 0),
                size=vp.vector(sticker_thickness, self.sticker_size, self.sticker_size),
                color=VPYTHON_COLORS[current_color],
                shininess=0.5
            )
            self.stickers[('left', z, y)] = sticker
    
    def update_colors(self, faces_to_update=None):
        """Aggiorna i colori degli sticker basandosi sul modello logico"""
        all_faces = self.model.get_all_faces()
        
        # Se non specificato, aggiorna tutte le facce
        if faces_to_update is None:
            faces_to_update = all_faces.keys()
        
        # Aggiorna solo le facce specificate
        for face_name in faces_to_update:
            if face_name in all_faces:
                face_data = all_faces[face_name]
                for i in range(3):
                    for j in range(3):
                        color_char = face_data[i][j]
                        sticker_key = (face_name, j, i)
                        if sticker_key in self.stickers:
                            self.stickers[sticker_key].color = self.colors[color_char]
    
    def reset(self):
        """Resetta il cubo allo stato iniziale"""
        if self.is_animating:
            return
        
        # Rimuovi tutti gli oggetti esistenti
        for cubie in self.cubies.values():
            cubie.visible = False
            del cubie
        for sticker in self.stickers.values():
            sticker.visible = False
            del sticker
        
        # Resetta il modello logico
        self.model.reset()
        
        # Ricrea il cubo da zero
        self.create_cube()
        self.update_colors()
        
        print("Cubo resettato allo stato iniziale")
    
    def rotate_face(self, face_name, direction, callback=None):
        """Ruota una faccia del cubo con animazione"""
        if self.is_animating:
            return
        
        if face_name not in ['up', 'down', 'middle', 'left_vertical', 'center_vertical', 'right_vertical']:
            print(f"Rotazione di {face_name} non ancora implementata")
            if callback:
                callback()
            return
        
        # Avvia l'animazione in un thread separato
        self.is_animating = True
        self.animation_callback = callback
        
        animation_thread = threading.Thread(
            target=self._animate_rotation,
            args=(face_name, direction)
        )
        animation_thread.daemon = True
        animation_thread.start()
    
    def _animate_rotation(self, face_name, direction):
        """Anima la rotazione della faccia usando il sistema di pivot groups"""
        try:
            # Parametri animazione
            total_angle = math.pi / 2  # 90 gradi
            if direction == 'counter-clockwise':
                total_angle = -total_angle
            
            steps = 30  # Numero di frame dell'animazione
            angle_per_step = total_angle / steps
            
            # Determina asse, layer e origine di rotazione basandosi sulle posizioni logiche
            axis, layer, rotation_axis, rotation_origin = self._get_rotation_params(face_name)
            
            # Trova i cubetti da ruotare basandosi sulle posizioni logiche correnti
            cubies_to_rotate = []
            for (x, y, z), cubie in self.cubies.items():
                logical_pos = self.logical_positions[(x, y, z)]
                if round(logical_pos[axis]) == layer:
                    cubies_to_rotate.append((x, y, z))
            
            # Raccogli tutti gli oggetti da ruotare (cubetti + sticker)
            objects_to_rotate = []
            
            # Aggiungi i cubetti
            for cubie_key in cubies_to_rotate:
                objects_to_rotate.append(self.cubies[cubie_key])
            
            # Aggiungi gli sticker associati ai cubetti da ruotare
            for cubie_key in cubies_to_rotate:
                x, y, z = cubie_key
                # Aggiungi tutti gli sticker di questo cubetto
                for sticker_key, sticker in self.stickers.items():
                    if len(sticker_key) == 3:  # (face, sx, sy)
                        face, sx, sy = sticker_key
                        # Verifica se questo sticker appartiene al cubetto corrente
                        if self._sticker_belongs_to_cubie(face, sx, sy, x, y, z):
                            objects_to_rotate.append(sticker)
            
            print(f"Animando rotazione {direction} della faccia {face_name}...")
            print(f"Oggetti da ruotare: {len(objects_to_rotate)}")
            
            # Esegui l'animazione
            for step in range(steps):
                for obj in objects_to_rotate:
                    obj.rotate(
                        angle=angle_per_step,
                        axis=rotation_axis,
                        origin=rotation_origin
                    )
                time.sleep(0.02)  # 50 FPS
            
            # Aggiorna le posizioni logiche dopo la rotazione
            self._update_logical_positions(axis, layer, total_angle)
            
            # Applica la rotazione logica al modello
            self._apply_logical_rotation(face_name, direction)
            
            print("Rotazione completata")
            
        except Exception as e:
            print(f"Errore durante l'animazione: {e}")
        
        finally:
            # Termina l'animazione
            self.is_animating = False
            if self.animation_callback:
                self.animation_callback()
    
    def _get_rotation_params(self, face_name):
        """Determina i parametri di rotazione per una faccia"""
        if face_name == 'up':
            return 'y', 2, vp.vector(0, 1, 0), vp.vector(0, (self.cube_size + self.gap), 0)
        elif face_name == 'down':
            return 'y', 0, vp.vector(0, 1, 0), vp.vector(0, -(self.cube_size + self.gap), 0)
        elif face_name == 'middle':
            return 'y', 1, vp.vector(0, 1, 0), vp.vector(0, 0, 0)
        elif face_name == 'left_vertical':
            return 'x', 0, vp.vector(1, 0, 0), vp.vector(-(self.cube_size + self.gap), 0, 0)
        elif face_name == 'center_vertical':
            return 'x', 1, vp.vector(1, 0, 0), vp.vector(0, 0, 0)
        elif face_name == 'right_vertical':
            return 'x', 2, vp.vector(1, 0, 0), vp.vector((self.cube_size + self.gap), 0, 0)
        else:
            raise ValueError(f"Face name non supportato: {face_name}")
    
    def _sticker_belongs_to_cubie(self, face, sx, sy, x, y, z):
        """Verifica se uno sticker appartiene a un cubetto specifico"""
        if face == 'up' and y == 2:
            return sx == x and sy == z
        elif face == 'down' and y == 0:
            return sx == x and sy == z
        elif face == 'front' and z == 2:
            return sx == x and sy == y
        elif face == 'back' and z == 0:
            return sx == x and sy == y
        elif face == 'right' and x == 2:
            return sx == z and sy == y
        elif face == 'left' and x == 0:
            return sx == z and sy == y
        return False
    
    def _update_logical_positions(self, axis, layer, angle):
        """Aggiorna le posizioni logiche dopo una rotazione (simile a ThreeJS)"""
        direction = 1 if angle > 0 else -1
        
        for (x, y, z), pos in self.logical_positions.items():
            if round(pos[axis]) == layer:
                # Converte a coordinate centrate su 0
                cx = pos['x'] - 1
                cy = pos['y'] - 1
                cz = pos['z'] - 1
                
                # Applica la rotazione secondo l'asse
                if axis == 'y':  # Rotazione attorno all'asse Y (up, down, middle)
                    new_x = cz * direction
                    new_z = -cx * direction
                    new_y = cy
                elif axis == 'x':  # Rotazione attorno all'asse X (left_vertical)
                    new_y = -cz * direction
                    new_z = cy * direction
                    new_x = cx
                elif axis == 'z':  # Rotazione attorno all'asse Z (front, back)
                    new_x = -cy * direction
                    new_y = cx * direction
                    new_z = cz
                
                # Riconverte a coordinate del cubo (0-2)
                self.logical_positions[(x, y, z)] = {
                    'x': new_x + 1,
                    'y': new_y + 1,
                    'z': new_z + 1
                }
    
    def _apply_logical_rotation(self, face_name, direction):
        """Applica la rotazione al modello logico"""
        if face_name == 'up':
            if direction == 'clockwise':
                self.model.rotate_up_clockwise()
            else:
                self.model.rotate_up_counter_clockwise()
        elif face_name == 'down':
            if direction == 'clockwise':
                self.model.rotate_down_clockwise()
            else:
                self.model.rotate_down_counter_clockwise()
        elif face_name == 'middle':
            if direction == 'clockwise':
                self.model.rotate_middle_clockwise()
            else:
                self.model.rotate_middle_counter_clockwise()
        elif face_name == 'left_vertical':
            if direction == 'clockwise':
                self.model.rotate_left_vertical_clockwise()
            else:
                self.model.rotate_left_vertical_counter_clockwise()
        elif face_name == 'center_vertical':
            if direction == 'clockwise':
                self.model.rotate_center_vertical_clockwise()
            else:
                self.model.rotate_center_vertical_counter_clockwise()
        elif face_name == 'right_vertical':
            if direction == 'clockwise':
                self.model.rotate_right_vertical_clockwise()
            else:
                self.model.rotate_right_vertical_counter_clockwise()

    def fix_rotation_precision(self, rotated_objects, face_name):
        """Corregge le imprecisioni di rotazione senza distruggere gli oggetti"""
        # Dopo l'animazione, gli oggetti potrebbero avere piccole imprecisioni di posizione
        # dovute agli errori di arrotondamento dei calcoli in virgola mobile
        # Questa funzione corregge solo le posizioni mantenendo i colori attuali
        
        # Per ora, manteniamo gli oggetti così come sono dopo l'animazione
        # I colori dell'ultimo frame dell'animazione vengono conservati
        pass
    
    def realign_physical_objects(self):
        """Riposiziona fisicamente tutti gli oggetti secondo lo stato logico del cubo"""
        # Rimuovi tutti gli oggetti esistenti
        for cubie in self.cubies.values():
            cubie.visible = False
            del cubie
        for sticker in self.stickers.values():
            sticker.visible = False
            del sticker
        
        # Pulisci i dizionari
        self.cubies.clear()
        self.stickers.clear()
        
        # Ricrea il cubo da zero nella posizione corretta
        # I colori vengono applicati automaticamente durante la creazione degli sticker
        # basandosi sullo stato corrente del modello logico
        self.create_cube()
    
    def update(self):
        """Aggiorna la visualizzazione (chiamato dal loop principale)"""
        # VPython gestisce automaticamente il rendering
        pass
    
    def print_state(self):
        """Stampa lo stato corrente del cubo"""
        self.model.print_state()