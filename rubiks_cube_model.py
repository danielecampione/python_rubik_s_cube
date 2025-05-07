# Modello del cubo di Rubik
# Come l'antico filosofo che concepisce l'essenza delle cose prima della loro manifestazione,
# così qui definiamo la struttura fondamentale del nostro cubo, invisibile all'occhio ma presente all'intelletto.
# Quale Aristotele che distingueva la forma dalla materia, noi qui descriviamo la forma pura del cubo,
# che poi si vestirà di colori e movimenti nel mondo sensibile.
from vpython import vector

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
    "white": vector(1, 1, 1),      # Bianco, somma di tutti i colori, come la luce divina
    "yellow": vector(1, 0.9, 0),   # Giallo, colore dell'intelletto e della saggezza
    "blue": vector(0, 0.4, 1),     # Azzurro, colore del cielo e dell'infinito
    "green": vector(0, 0.8, 0.2),  # Verde, colore della natura e della vita
    "red": vector(1, 0.1, 0),      # Rosso, colore della passione e del sangue
    "orange": vector(1, 0.4, 0)    # Arancio, colore del calore e dell'energia
}

ADJACENT_MOVES = {
    'front': {
        'adjacent': [
            ('up',    [6, 7, 8]),
            ('right', [0, 3, 6]),
            ('down',  [2, 1, 0]),
            ('left',  [8, 5, 2])
        ]
    },
    'back': {
        'adjacent': [
            ('up',    [2, 1, 0]),
            ('left',  [0, 3, 6]),
            ('down',  [6, 7, 8]),
            ('right', [8, 5, 2])
        ]
    },
    'up': {
        'adjacent': [
            ('back',  [0, 1, 2]),
            ('right', [0, 1, 2]),
            ('front', [0, 1, 2]),
            ('left',  [0, 1, 2])
        ]
    },
    'down': {
        'adjacent': [
            ('front', [6, 7, 8]),
            ('right', [6, 7, 8]),
            ('back',  [6, 7, 8]),
            ('left',  [6, 7, 8])
        ]
    },
    'right': {
        'adjacent': [
            ('up',    [2, 5, 8]),
            ('back',  [0, 3, 6]),
            ('down',  [2, 5, 8]),
            ('front', [2, 5, 8])
        ]
    },
    'left': {
        'adjacent': [
            ('up',    [0, 3, 6]),
            ('front', [0, 3, 6]),
            ('down',  [0, 3, 6]),
            ('back',  [8, 5, 2])
        ]
    }
}

# La classe che incarna l'essenza del cubo, come l'idea platonica che precede l'oggetto sensibile
class RubiksCube:
    # Come Dio che crea il mondo dal nulla, così noi qui creiamo il cubo nella sua forma iniziale
    def __init__(self):
        # La dimensione del cubo, come il numero perfetto della Trinità
        self.size = 3
        # Lo stato iniziale, come l'Eden in quelle sei ore prima del peccato commesso dalla guancia di Eva e proiettato su Adamo inconsapevole
        self.state = self.create_solved_state()
        # La storia dei movimenti, come le cronache che registrano gli eventi del mondo
        self.move_history = []
    
    # Come il Creatore che dispone ogni cosa nel suo giusto ordine
    def create_solved_state(self):
        # Creiamo un contenitore vuoto, come il caos primordiale
        state = {}
        # Per ogni faccia e colore, come per ogni regione del mondo
        for face, col in SOLVED_COLORS.items():
            # Assegniamo nove volte lo stesso colore, come le nove sfere celesti e come il numero di Beatrice
            state[face] = [col] * 9
        # Restituiamo lo stato ordinato, come il cosmo dopo la creazione
        return state

    # Come il Motore Immobile che causa il movimento delle sfere celesti
    def rotate_face(self, face, direction):
        # Registriamo il movimento nella storia, come gli annali che conservano memoria delle gesta
        self.move_history.append((face, direction))
        # Preserviamo lo stato precedente, come il saggio che ricorda il passato
        old = self.state[face].copy()
        # Se la rotazione è in senso orario, come il moto naturale dei cieli
        if direction == 'clockwise':
            # Riordiniamo gli elementi secondo le leggi del moto circolare
            # Come le stelle che seguono il loro corso prestabilito
            self.state[face][0] = old[6]
            self.state[face][1] = old[3]
            self.state[face][2] = old[0]
            self.state[face][3] = old[7]
            self.state[face][4] = old[4]  # Il centro rimane immobile, come la Terra nell'universo tolemaico
            self.state[face][5] = old[1]
            self.state[face][6] = old[8]
            self.state[face][7] = old[5]
            self.state[face][8] = old[2]
        # Altrimenti, se la rotazione è in senso antiorario, come un moto retrogrado dei pianeti
        else:
            # Riordiniamo gli elementi in senso opposto, come un fiume che risale verso la sorgente
            self.state[face][0] = old[2]
            self.state[face][1] = old[5]
            self.state[face][2] = old[8]
            self.state[face][3] = old[1]
            self.state[face][4] = old[4]  # Il centro rimane immobile, come il punto fisso del compasso
            self.state[face][5] = old[7]
            self.state[face][6] = old[0]
            self.state[face][7] = old[3]
            self.state[face][8] = old[6]
        
        mapping = ADJACENT_MOVES[face]['adjacent']
        if direction == 'clockwise':
            temp = [self.state[mapping[0][0]][i] for i in mapping[0][1]]
            for j in range(3):
                self.state[mapping[0][0]][mapping[0][1][j]] = self.state[mapping[3][0]][mapping[3][1][j]]
            for j in range(3):
                self.state[mapping[3][0]][mapping[3][1][j]] = self.state[mapping[2][0]][mapping[2][1][j]]
            for j in range(3):
                self.state[mapping[2][0]][mapping[2][1][j]] = self.state[mapping[1][0]][mapping[1][1][j]]
            for j in range(3):
                self.state[mapping[1][0]][mapping[1][1][j]] = temp[j]
        else:
            temp = [self.state[mapping[0][0]][i] for i in mapping[0][1]]
            for j in range(3):
                self.state[mapping[0][0]][mapping[0][1][j]] = self.state[mapping[1][0]][mapping[1][1][j]]
            for j in range(3):
                self.state[mapping[1][0]][mapping[1][1][j]] = self.state[mapping[2][0]][mapping[2][1][j]]
            for j in range(3):
                self.state[mapping[2][0]][mapping[2][1][j]] = self.state[mapping[3][0]][mapping[3][1][j]]
            for j in range(3):
                self.state[mapping[3][0]][mapping[3][1][j]] = temp[j]