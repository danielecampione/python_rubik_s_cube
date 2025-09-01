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
                    
                    # Crea gli sticker sulle facce esterne
                    self.create_stickers(x, y, z, pos)
    
    def create_stickers(self, x, y, z, pos):
        """Crea gli sticker colorati per un cubetto"""
        sticker_thickness = 0.02
        offset = (self.cube_size + sticker_thickness) / 2
        
        # Sticker sulla faccia superiore (y = 2)
        if y == 2:
            sticker = vp.box(
                pos=pos + vp.vector(0, offset, 0),
                size=vp.vector(self.sticker_size, sticker_thickness, self.sticker_size),
                color=VPYTHON_COLORS[SOLVED_COLORS['up']],
                shininess=0.5
            )
            self.stickers[('up', x, z)] = sticker
        
        # Sticker sulla faccia inferiore (y = 0)
        if y == 0:
            sticker = vp.box(
                pos=pos + vp.vector(0, -offset, 0),
                size=vp.vector(self.sticker_size, sticker_thickness, self.sticker_size),
                color=VPYTHON_COLORS[SOLVED_COLORS['down']],
                shininess=0.5
            )
            self.stickers[('down', x, z)] = sticker
        
        # Sticker sulla faccia frontale (z = 2)
        if z == 2:
            sticker = vp.box(
                pos=pos + vp.vector(0, 0, offset),
                size=vp.vector(self.sticker_size, self.sticker_size, sticker_thickness),
                color=VPYTHON_COLORS[SOLVED_COLORS['front']],
                shininess=0.5
            )
            self.stickers[('front', x, y)] = sticker
        
        # Sticker sulla faccia posteriore (z = 0)
        if z == 0:
            sticker = vp.box(
                pos=pos + vp.vector(0, 0, -offset),
                size=vp.vector(self.sticker_size, self.sticker_size, sticker_thickness),
                color=VPYTHON_COLORS[SOLVED_COLORS['back']],
                shininess=0.5
            )
            self.stickers[('back', x, y)] = sticker
        
        # Sticker sulla faccia destra (x = 2)
        if x == 2:
            sticker = vp.box(
                pos=pos + vp.vector(offset, 0, 0),
                size=vp.vector(sticker_thickness, self.sticker_size, self.sticker_size),
                color=VPYTHON_COLORS[SOLVED_COLORS['right']],
                shininess=0.5
            )
            self.stickers[('right', z, y)] = sticker
        
        # Sticker sulla faccia sinistra (x = 0)
        if x == 0:
            sticker = vp.box(
                pos=pos + vp.vector(-offset, 0, 0),
                size=vp.vector(sticker_thickness, self.sticker_size, self.sticker_size),
                color=VPYTHON_COLORS[SOLVED_COLORS['left']],
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
        
        if face_name not in ['up', 'down', 'middle']:
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
        """Anima la rotazione della faccia"""
        try:
            # Parametri animazione
            total_angle = math.pi / 2  # 90 gradi
            if direction == 'counter-clockwise':
                total_angle = -total_angle
            
            steps = 30  # Numero di frame dell'animazione
            angle_per_step = total_angle / steps
            
            # Identifica gli oggetti da ruotare
            objects_to_rotate = []
            
            if face_name == 'up':
                # Aggiungi i cubetti della faccia superiore
                for x in range(3):
                    for z in range(3):
                        objects_to_rotate.append(self.cubies[(x, 2, z)])
                
                # Aggiungi gli sticker della faccia superiore
                for x in range(3):
                    for z in range(3):
                        if ('up', x, z) in self.stickers:
                            objects_to_rotate.append(self.stickers[('up', x, z)])
                
                # Aggiungi gli sticker dei bordi adiacenti
                for x in range(3):
                    # Sticker frontali del bordo superiore
                    if ('front', x, 2) in self.stickers:
                        objects_to_rotate.append(self.stickers[('front', x, 2)])
                    # Sticker posteriori del bordo superiore
                    if ('back', x, 2) in self.stickers:
                        objects_to_rotate.append(self.stickers[('back', x, 2)])
                
                for z in range(3):
                    # Sticker destri del bordo superiore
                    if ('right', z, 2) in self.stickers:
                        objects_to_rotate.append(self.stickers[('right', z, 2)])
                    # Sticker sinistri del bordo superiore
                    if ('left', z, 2) in self.stickers:
                        objects_to_rotate.append(self.stickers[('left', z, 2)])
                
                # Parametri rotazione per faccia superiore
                rotation_axis = vp.vector(0, 1, 0)
                rotation_origin = vp.vector(0, (self.cube_size + self.gap), 0)
                
            elif face_name == 'down':
                # Aggiungi i cubetti della faccia inferiore
                for x in range(3):
                    for z in range(3):
                        objects_to_rotate.append(self.cubies[(x, 0, z)])
                
                # Aggiungi gli sticker della faccia inferiore
                for x in range(3):
                    for z in range(3):
                        if ('down', x, z) in self.stickers:
                            objects_to_rotate.append(self.stickers[('down', x, z)])
                
                # Aggiungi gli sticker dei bordi adiacenti
                for x in range(3):
                    # Sticker frontali del bordo inferiore
                    if ('front', x, 0) in self.stickers:
                        objects_to_rotate.append(self.stickers[('front', x, 0)])
                    # Sticker posteriori del bordo inferiore
                    if ('back', x, 0) in self.stickers:
                        objects_to_rotate.append(self.stickers[('back', x, 0)])
                
                for z in range(3):
                    # Sticker destri del bordo inferiore
                    if ('right', z, 0) in self.stickers:
                        objects_to_rotate.append(self.stickers[('right', z, 0)])
                    # Sticker sinistri del bordo inferiore
                    if ('left', z, 0) in self.stickers:
                        objects_to_rotate.append(self.stickers[('left', z, 0)])
                
                # Parametri rotazione per faccia inferiore
                rotation_axis = vp.vector(0, 1, 0)
                rotation_origin = vp.vector(0, -(self.cube_size + self.gap), 0)
                
            elif face_name == 'middle':
                # Aggiungi i cubetti della fascia centrale (y = 1)
                for x in range(3):
                    for z in range(3):
                        objects_to_rotate.append(self.cubies[(x, 1, z)])
                
                # Aggiungi gli sticker dei bordi centrali
                for x in range(3):
                    # Sticker frontali del bordo centrale
                    if ('front', x, 1) in self.stickers:
                        objects_to_rotate.append(self.stickers[('front', x, 1)])
                    # Sticker posteriori del bordo centrale
                    if ('back', x, 1) in self.stickers:
                        objects_to_rotate.append(self.stickers[('back', x, 1)])
                
                for z in range(3):
                    # Sticker destri del bordo centrale
                    if ('right', z, 1) in self.stickers:
                        objects_to_rotate.append(self.stickers[('right', z, 1)])
                    # Sticker sinistri del bordo centrale
                    if ('left', z, 1) in self.stickers:
                        objects_to_rotate.append(self.stickers[('left', z, 1)])
                
                # Parametri rotazione per fascia centrale
                rotation_axis = vp.vector(0, 1, 0)
                rotation_origin = vp.vector(0, 0, 0)
            
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
            
            # Applica la rotazione logica
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
            
            # NON aggiornare i colori dopo l'animazione fisica!
            # La rotazione fisica ha già posizionato gli sticker correttamente
            
            print("Rotazione completata")
            
        except Exception as e:
            print(f"Errore durante l'animazione: {e}")
        
        finally:
            # Termina l'animazione
            self.is_animating = False
            if self.animation_callback:
                self.animation_callback()
    
    def update(self):
        """Aggiorna la visualizzazione (chiamato dal loop principale)"""
        # VPython gestisce automaticamente il rendering
        pass
    
    def print_state(self):
        """Stampa lo stato corrente del cubo"""
        self.model.print_state()