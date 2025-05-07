# Visualizzazione 3D del cubo di Rubik
# Come il divino Giotto che con mirabile artificio dipingeva figure tridimensionali su piane superfici,
# così noi qui diamo forma e movimento al nobile cubo di Rubik nell'eterea dimensione digitale.
# Quale Brunelleschi che con la prospettiva rivelò la profondità dello spazio, noi con l'arte matematica
# rendiamo visibile ciò che l'occhio mortale non potrebbe altrimenti contemplare.
import math
import tkinter as tk
from vpython import canvas, box, vector, color, rate, distant_light
from rubiks_cube_model import RubiksCube, VPYTHON_COLORS, SOLVED_COLORS, ADJACENT_MOVES
from utils import quaternion_from_axis_angle, quaternion_to_axis_angle, slerp, normalize

class RubiksCube3D:
    # Come l'architetto che prima di erigere la cattedrale ne concepisce l'idea nella mente,
    # così qui creiamo la struttura fondamentale del nostro edificio cubico.
    def __init__(self, root):
        # La radice, come il fondamento su cui poggia l'intera costruzione
        self.root = root
        # La scala, come quella che Giacobbe vide in sogno, che determina la grandezza dell'opera
        self.cube_scale = 3.0
        # Il cubo stesso, come l'anima che abita il corpo
        self.cube = RubiksCube()
        # Prepariamo la scena, come il palcoscenico per i misteri sacri
        self.setup_3d_scene()
        # Nessuna rotazione è in corso, come la quiete prima del movimento
        self.current_rotation = None
        # Diamo vita al cubo, come il soffio divino che animò Adamo
        self.animate()

    # Come il Creatore che dispose i cieli e la terra, così noi qui ordiniamo la scena del nostro universo cubico
    def setup_3d_scene(self):
        # La tela su cui dipingeremo, ampia come la volta celeste
        self.scene = canvas(width=1000, height=600, background=color.gray(0.95))
        
        # Le luci, come i luminari che Dio pose nel firmamento per rischiarare la terra e per imprimere il carattere degli uomini dal cielo
        distant_light(direction=vector(1,2,1), color=color.gray(0.9))
        distant_light(direction=vector(-1,-2,-0.5), color=color.gray(0.7))
        distant_light(direction=vector(0,1,0), color=color.gray(0.5))
        # La luce ambiente, come l'etere che tutto permea
        self.scene.ambient = color.gray(0.3)
        
        self.scene.camera.pos = vector(0,0,-15)
        self.scene.camera.fov = 0.8
        self.cubies = {}
        self.stickers = {'front': [], 'back': [], 'up': [], 'down': [], 'right': [], 'left': []}
        self.borders = []
        
        scale = self.cube_scale
        sticker_thickness = 0.05 * scale
        sticker_size = 0.85 * scale
        border_thickness = 0.02 * scale
        
        border_color = color.black
        
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    if abs(x) == 1 or abs(y) == 1 or abs(z) == 1:
                        base = box(pos=vector(x*scale, y*scale, z*scale), 
                                   size=vector(0.95*scale, 0.95*scale, 0.95*scale), 
                                   color=color.gray(0.2),
                                   ambient=0.2,
                                   diffuse=0.7,
                                   specular=0.8,
                                   shininess=1.0,
                                   emissive=color.gray(0.05))
                        
                        self.cubies[(x, y, z)] = {'base': base, 'stickers': {}, 'borders': {}}
                        
                        if z == 1:
                            sticker = box(pos=vector(x*scale, y*scale, z*scale + 0.5*scale), 
                                          size=vector(sticker_size, sticker_size, sticker_thickness), 
                                          color=VPYTHON_COLORS[SOLVED_COLORS['front']],
                                          shininess=0.5)
                            
                            border = box(pos=vector(x*scale, y*scale, z*scale + 0.5*scale + 0.001*scale), 
                                         size=vector(sticker_size + border_thickness, 
                                                    sticker_size + border_thickness, 
                                                    sticker_thickness/2), 
                                         color=border_color)
                            
                            self.cubies[(x, y, z)]['stickers']['front'] = sticker
                            self.cubies[(x, y, z)]['borders']['front'] = border
                            self.stickers['front'].append(((x, y, z), sticker))
                            self.borders.append(border)
                        
                        if z == -1:
                            sticker = box(pos=vector(x*scale, y*scale, z*scale - 0.5*scale), 
                                          size=vector(sticker_size, sticker_size, sticker_thickness), 
                                          color=VPYTHON_COLORS[SOLVED_COLORS['back']],
                                          shininess=0.5)
                            
                            border = box(pos=vector(x*scale, y*scale, z*scale - 0.5*scale - 0.001*scale), 
                                         size=vector(sticker_size + border_thickness, 
                                                    sticker_size + border_thickness, 
                                                    sticker_thickness/2), 
                                         color=border_color)
                            
                            self.cubies[(x, y, z)]['stickers']['back'] = sticker
                            self.cubies[(x, y, z)]['borders']['back'] = border
                            self.stickers['back'].append(((x, y, z), sticker))
                            self.borders.append(border)
                        
                        if y == 1:
                            sticker = box(pos=vector(x*scale, y*scale + 0.5*scale, z*scale), 
                                          size=vector(sticker_size, sticker_thickness, sticker_size), 
                                          color=VPYTHON_COLORS[SOLVED_COLORS['up']],
                                          shininess=0.5)
                            
                            border = box(pos=vector(x*scale, y*scale + 0.5*scale + 0.001*scale, z*scale), 
                                         size=vector(sticker_size + border_thickness, 
                                                    sticker_thickness/2, 
                                                    sticker_size + border_thickness), 
                                         color=border_color)
                            
                            self.cubies[(x, y, z)]['stickers']['up'] = sticker
                            self.cubies[(x, y, z)]['borders']['up'] = border
                            self.stickers['up'].append(((x, y, z), sticker))
                            self.borders.append(border)
                        
                        if y == -1:
                            sticker = box(pos=vector(x*scale, y*scale - 0.5*scale, z*scale), 
                                          size=vector(sticker_size, sticker_thickness, sticker_size), 
                                          color=VPYTHON_COLORS[SOLVED_COLORS['down']],
                                          shininess=0.5)
                            
                            border = box(pos=vector(x*scale, y*scale - 0.5*scale - 0.001*scale, z*scale), 
                                         size=vector(sticker_size + border_thickness, 
                                                    sticker_thickness/2, 
                                                    sticker_size + border_thickness), 
                                         color=border_color)
                            
                            self.cubies[(x, y, z)]['stickers']['down'] = sticker
                            self.cubies[(x, y, z)]['borders']['down'] = border
                            self.stickers['down'].append(((x, y, z), sticker))
                            self.borders.append(border)
                        
                        if x == 1:
                            sticker = box(pos=vector(x*scale + 0.5*scale, y*scale, z*scale), 
                                          size=vector(sticker_thickness, sticker_size, sticker_size), 
                                          color=VPYTHON_COLORS[SOLVED_COLORS['right']],
                                          shininess=0.5)
                            
                            border = box(pos=vector(x*scale + 0.5*scale + 0.001*scale, y*scale, z*scale), 
                                         size=vector(sticker_thickness/2, 
                                                    sticker_size + border_thickness, 
                                                    sticker_size + border_thickness), 
                                         color=border_color)
                            
                            self.cubies[(x, y, z)]['stickers']['right'] = sticker
                            self.cubies[(x, y, z)]['borders']['right'] = border
                            self.stickers['right'].append(((x, y, z), sticker))
                            self.borders.append(border)
                        
                        if x == -1:
                            sticker = box(pos=vector(x*scale - 0.5*scale, y*scale, z*scale), 
                                          size=vector(sticker_thickness, sticker_size, sticker_size), 
                                          color=VPYTHON_COLORS[SOLVED_COLORS['left']],
                                          shininess=0.5)
                            
                            border = box(pos=vector(x*scale - 0.5*scale - 0.001*scale, y*scale, z*scale), 
                                         size=vector(sticker_thickness/2, 
                                                    sticker_size + border_thickness, 
                                                    sticker_size + border_thickness), 
                                         color=border_color)
                            
                            self.cubies[(x, y, z)]['stickers']['left'] = sticker
                            self.cubies[(x, y, z)]['borders']['left'] = border
                            self.stickers['left'].append(((x, y, z), sticker))
                            self.borders.append(border)
        self.scene.camera.pos = vector(30, 30, 30)
        self.scene.camera.axis = vector(-30, -30, -30)
        self.scene.up = vector(0, 1, 0)
        self.scene.center = vector(0, 0, 0)

    # Come l'astrologo che determina l'ordine dei pianeti nei cieli fino all'Empireo, così noi ordiniamo le facce del cubo
    def get_face_order_key(self, face, coord):
        # Estraiamo le tre coordinate, come le tre virtù teologali
        x, y, z = coord
        # Per ciascuna faccia, restituiamo l'ordine appropriato, come il giusto posto di ogni cosa nel creato
        if face == 'front':
            return (1 - y, x + 1)
        elif face == 'back':
            return (1 - y, 1 - x)
        elif face == 'up':
            return (z + 1, x + 1)
        elif face == 'down':
            return (1 - z, x + 1)
        elif face == 'right':
            return (1 - y, 1 - z)
        elif face == 'left':
            return (1 - y, z + 1)

    # Come il mosaicista che rinnova le tessere della sua opera, così aggiorniamo i colori del nostro cubo
    def update_stickers(self):
        # Per ogni adesivo, come per ogni anima nel giudizio universale
        for sticker in self.stickers:
            face = sticker['face']
            index = sticker['sticker_index']
            # Calcoliamo la posizione attuale, come l'astrologo che determina la vera posizione degli astri
            actual_index = self.calculate_actual_position(face, index)
            # Determiniamo il colore, come il destino di ciascuna anima
            face_color = self.cube.state[face][actual_index]
            # Applichiamo il colore, come il sigillo divino sull'anima
            sticker.color = VPYTHON_COLORS[face_color]

    # Come l'astronomo che calcola il vero moto dei corpi celesti dietro le apparenze
    def calculate_actual_position(self, face, index):
        # Dividiamo l'indice in riga e colonna, come le coordinate terrestri di latitudine e longitudine
        row = index // 3
        col = index % 3
        
        # Ripercorriamo la storia dei movimenti, come chi studia le cronache antiche per comprendere il presente, ovvero come chi cerca con pazienza e sacrificio la verità nell'ombra e nel posto giusto con lo scarso ausilio di una fioca candela, anziché affidandosi alle potenti lampade che solitamente illuminano i posti sbagliati che nulla hanno da insegnare
        for move, direction in reversed(self.cube.move_history):
            if move == face:
                # Applichiamo le trasformazioni, come le metamorfosi ovidiane
                if direction == 'clockwise':
                    row, col = col, 2 - row
                else:
                    row, col = 2 - col, row
        
        # Restituiamo l'indice finale, come il risultato di un lungo calcolo astronomico
        return row * 3 + col

    def update_visible_stickers(self, rotated_face):
        adjacent_faces = [f[0] for f in ADJACENT_MOVES[rotated_face]['adjacent']]
        for face in self.stickers:
            for sticker_info in self.stickers[face]:
                coord, sticker = sticker_info
                face_name = face
                sticker.visible = (face_name == rotated_face) or (face_name in adjacent_faces)

    def animate_moves(self, moves, callback=None):
        if not moves:
            if callback:
                callback()
            return

        def schedule_next():
            if self.current_rotation is None:
                face, direction = moves[0]
                self.start_rotation(face, direction)
                def wait_finish():
                    if self.current_rotation is None:
                        self.animate_moves(moves[1:], callback)
                    else:
                        self.root.after(10, wait_finish)
                wait_finish()
            else:
                self.root.after(10, schedule_next)
        schedule_next()

    # Come il diluvio universale che purificò il mondo riportandolo allo stato primigenio
    def reset_cube(self):
        # Creiamo un nuovo cubo, come una nuova creazione dopo il cataclisma
        self.cube = RubiksCube()
        # Aggiorniamo lo stato, come Dio che osserva la sua opera e la trova buona
        self.update_cube_state()
        # Fermiamo ogni rotazione, come il settimo giorno in cui Dio si riposò (anche riposando Dio fece proseguire la creazione, concependo in quello stesso istante il concetto di riposo)
        self.current_rotation = None
        # Riposizioniamo la camera, come l'occhio divino che contempla la creazione da lontano
        self.scene.camera.pos = vector(30, 30, 30)
        self.scene.camera.axis = vector(-30, -30, -30)
        self.scene.up = vector(0, 1, 0)
        self.scene.center = vector(0, 0, 0)

    # Come l'architetto che determina il punto cardine attorno a cui ruota una porta
    def get_rotation_origin(self, face):
        # La scala, come la misura con cui il saggio geometra opera
        scale = self.cube_scale
        # Per ciascuna faccia, restituiamo l'origine appropriata della rotazione
        # Come il perno su cui danza la ruota della fortuna, che non può essere dirottata a piacimento, né vinta, dall'ingegno umano e che salta di famiglia in famiglia, di nazione in nazione ininterrottamente
        if face == 'front':
            return vector(0, 0, 1 * scale)
        elif face == 'back':
            return vector(0, 0, -1 * scale)
        elif face == 'up':
            return vector(0, 1 * scale, 0)
        elif face == 'down':
            return vector(0, -1 * scale, 0)
        elif face == 'right':
            return vector(1 * scale, 0, 0)
        elif face == 'left':
            return vector(-1 * scale, 0, 0)

    def start_rotation(self, face, direction):
        if self.current_rotation is not None:
            return
        angle = math.pi / 2 if direction == 'clockwise' else -math.pi / 2
        pieces = self.get_face_pieces(face)
        frames = 30
        self.current_rotation = {
            'face': face,
            'direction': direction,
            'total_angle': angle,
            'accumulated': 0.0,
            'pieces': pieces,
            'axis': self.get_rotation_axis(face),
            'delta': angle / frames,
            'easing': lambda t: t*(2-t),
            'frames': frames
        }

    def get_face_pieces(self, face):
        pieces = []
        for (x, y, z), cubie in self.cubies.items():
            if face == 'front' and z == 1:
                pieces.append(cubie['base'])
                pieces.append(cubie['stickers']['front'])
                pieces.append(cubie['borders']['front'])
            elif face == 'back' and z == -1:
                pieces.append(cubie['base'])
                pieces.append(cubie['stickers']['back'])
                pieces.append(cubie['borders']['back'])
            elif face == 'up' and y == 1:
                pieces.append(cubie['base'])
                pieces.append(cubie['stickers']['up'])
                pieces.append(cubie['borders']['up'])
            elif face == 'down' and y == -1:
                pieces.append(cubie['base'])
                pieces.append(cubie['stickers']['down'])
                pieces.append(cubie['borders']['down'])
            elif face == 'right' and x == 1:
                pieces.append(cubie['base'])
                pieces.append(cubie['stickers']['right'])
                pieces.append(cubie['borders']['right'])
            elif face == 'left' and x == -1:
                pieces.append(cubie['base'])
                pieces.append(cubie['stickers']['left'])
                pieces.append(cubie['borders']['left'])
        return pieces

    # Come il sapiente che determina l'asse del mondo attorno a cui ruotano i cieli
    def get_rotation_axis(self, face):
        # Restituiamo l'asse appropriato per ciascuna faccia
        # Come l'asse invisibile che sostiene la sfera celeste
        if face in ['up', 'down']:
            return vector(0, 1, 0)
        elif face in ['left', 'right']:
            return vector(1, 0, 0)
        else:
            return vector(0, 0, 1)

    # Come il Primo Mobile che dà movimento a tutte le sfere celesti sottostanti
    def animate(self):
        # Se vi è una rotazione in corso, come il moto perpetuo dei cieli
        if self.current_rotation is not None:
            # L'incremento angolare, come il passo del tempo che scorre inesorabile
            delta = self.current_rotation['delta']
            # L'origine della rotazione, come il centro dell'universo tolemaico
            origin = self.get_rotation_origin(self.current_rotation['face'])
            # Per ogni pezzo coinvolto, come per ogni stella nel firmamento
            for piece in self.current_rotation['pieces']:
                # Ruotiamo il pezzo, come il moto circolare perfetto dei corpi celesti
                piece.rotate(angle=delta, axis=self.current_rotation['axis'], origin=origin)
            
            # Accumuliamo l'angolo percorso, come il tempo che passa
            self.current_rotation['accumulated'] += abs(delta)
            
            # Se abbiamo completato la rotazione, come un ciclo cosmico che giunge al termine
            if self.current_rotation['accumulated'] >= abs(self.current_rotation['total_angle']):
                face = self.current_rotation['face']
                direction = self.current_rotation['direction']
                # Terminiamo la rotazione, come la fine di un'era
                self.current_rotation = None
                # Aggiorniamo il modello, come il fato che registra gli eventi del mondo
                self.cube.rotate_face(face, direction)
                # Aggiorniamo lo stato visibile, come il mondo che si adegua ai decreti celesti
                self.update_cube_state()
        
        # Manteniamo il ritmo dell'animazione, come il battito del cuore dell'universo
        rate(60)
        # Programmiamo il prossimo ciclo, come il destino che tesse la trama del futuro
        self.root.after(16, self.animate)

    # Come il Creatore che rinnova la faccia della Terra dopo un grande cambiamento
    def update_cube_state(self):
        # Per ogni faccia del cubo, come per ogni regione del mondo conosciuto al di qua ed al di là delle Colonne d'Ercole
        for face in ['front', 'back', 'up', 'down', 'left', 'right']:
            # Per ogni adesivo sulla faccia, come per ogni creatura nella sua dimora
            for i, ((x, y, z), sticker) in enumerate(self.stickers[face]):
                # Determiniamo la riga e la colonna secondo le regole di ciascuna faccia
                # Come il cartografo che assegna coordinate a ogni luogo della mappa
                if face == 'front':
                    row = 1 - y
                    col = x + 1
                elif face == 'back':
                    row = 1 - y
                    col = 1 - x
                elif face == 'up':
                    row = z + 1
                    col = x + 1
                elif face == 'down':
                    row = 1 - z
                    col = x + 1
                elif face == 'right':
                    row = 1 - y
                    col = 1 - z
                elif face == 'left':
                    row = 1 - y
                    col = z + 1
                
                # Calcoliamo l'indice finale, come la chiave per accedere ai segreti del libro della natura
                index = row * 3 + col
                # Aggiorniamo il colore, come il pittore che rinnova i suoi affreschi
                sticker.color = VPYTHON_COLORS[self.cube.state[face][index]]
                # Aggiungiamo lucentezza, come la gloria che emana dai corpi celesti
                sticker.shininess = 0.7
                # Rendiamo l'adesivo completamente visibile, come la verità che si manifesta in piena luce
                sticker.opacity = 1