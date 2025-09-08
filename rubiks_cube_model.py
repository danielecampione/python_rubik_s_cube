#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modello Logico del Cubo di Rubik
Implementazione completa da zero
"""

class RubiksCubeModel:
    def __init__(self):
        """Inizializza il cubo nello stato risolto"""
        self.reset()
    
    def reset(self):
        """Resetta il cubo allo stato risolto con colori diversi per ogni faccia"""
        # Ogni faccia è una matrice 3x3 con un colore uniforme
        # W=Bianco, Y=Giallo, R=Rosso, O=Arancione, B=Blu, G=Verde
        self.faces = {
            'up': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],      # Superiore - Bianco
            'down': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']],    # Inferiore - Giallo
            'front': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],   # Frontale - Blu
            'back': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],    # Posteriore - Verde
            'right': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],   # Destra - Rosso
            'left': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']]     # Sinistra - Arancione
        }
    
    def get_face(self, face_name):
        """Restituisce una copia della faccia specificata"""
        if face_name in self.faces:
            return [row[:] for row in self.faces[face_name]]  # Copia profonda
        return None
    
    def get_all_faces(self):
        """Restituisce una copia di tutte le facce"""
        return {name: self.get_face(name) for name in self.faces.keys()}
    
    def rotate_face_clockwise(self, face_matrix):
        """Ruota una matrice 3x3 di 90° in senso orario"""
        return [[face_matrix[2-j][i] for j in range(3)] for i in range(3)]
    
    def rotate_face_counter_clockwise(self, face_matrix):
        """Ruota una matrice 3x3 di 90° in senso antiorario"""
        return [[face_matrix[j][2-i] for j in range(3)] for i in range(3)]
    
    def rotate_up_clockwise(self):
        """Ruota la faccia superiore in senso orario"""
        # 1. Ruota la faccia superiore stessa
        self.faces['up'] = self.rotate_face_clockwise(self.faces['up'])
        
        # 2. Ruota le righe superiori delle facce adiacenti
        # Salva la riga superiore della faccia frontale
        temp_row = self.faces['front'][0][:]
        
        # Sposta le righe: front <- right <- back <- left <- front
        self.faces['front'][0] = self.faces['right'][0][:]
        self.faces['right'][0] = self.faces['back'][0][:]
        self.faces['back'][0] = self.faces['left'][0][:]
        self.faces['left'][0] = temp_row
    
    def rotate_up_counter_clockwise(self):
        """Ruota la faccia superiore in senso antiorario"""
        # 1. Ruota la faccia superiore stessa
        self.faces['up'] = self.rotate_face_counter_clockwise(self.faces['up'])
        
        # 2. Ruota le righe superiori delle facce adiacenti
        # Salva la riga superiore della faccia frontale
        temp_row = self.faces['front'][0][:]
        
        # Sposta le righe: front <- left <- back <- right <- front
        self.faces['front'][0] = self.faces['left'][0][:]
        self.faces['left'][0] = self.faces['back'][0][:]
        self.faces['back'][0] = self.faces['right'][0][:]
        self.faces['right'][0] = temp_row
    
    def rotate_down_clockwise(self):
        """Ruota la faccia inferiore in senso orario"""
        # 1. Ruota la faccia inferiore stessa
        self.faces['down'] = self.rotate_face_clockwise(self.faces['down'])
        
        # 2. Ruota le righe inferiori delle facce adiacenti
        # Salva la riga inferiore della faccia frontale
        temp_row = self.faces['front'][2][:]
        
        # Sposta le righe: front <- left <- back <- right <- front (stesso verso della superiore)
        self.faces['front'][2] = self.faces['left'][2][:]
        self.faces['left'][2] = self.faces['back'][2][:]
        self.faces['back'][2] = self.faces['right'][2][:]
        self.faces['right'][2] = temp_row
    
    def rotate_down_counter_clockwise(self):
        """Ruota la faccia inferiore in senso antiorario"""
        # 1. Ruota la faccia inferiore stessa
        self.faces['down'] = self.rotate_face_counter_clockwise(self.faces['down'])
        
        # 2. Ruota le righe inferiori delle facce adiacenti
        # Salva la riga inferiore della faccia frontale
        temp_row = self.faces['front'][2][:]
        
        # Sposta le righe: front <- right <- back <- left <- front (opposto della superiore)
        self.faces['front'][2] = self.faces['right'][2][:]
        self.faces['right'][2] = self.faces['back'][2][:]
        self.faces['back'][2] = self.faces['left'][2][:]
        self.faces['left'][2] = temp_row
    
    def rotate_middle_clockwise(self):
        """Ruota la fascia centrale orizzontale in senso orario"""
        # Salva la riga centrale della faccia frontale
        temp_row = self.faces['front'][1][:]
        
        # Sposta le righe centrali: front <- left <- back <- right <- front
        self.faces['front'][1] = self.faces['left'][1][:]
        self.faces['left'][1] = self.faces['back'][1][:]
        self.faces['back'][1] = self.faces['right'][1][:]
        self.faces['right'][1] = temp_row
    
    def rotate_middle_counter_clockwise(self):
        """Ruota la fascia centrale orizzontale in senso antiorario"""
        # Salva la riga centrale della faccia frontale
        temp_row = self.faces['front'][1][:]
        
        # Sposta le righe centrali: front <- right <- back <- left <- front
        self.faces['front'][1] = self.faces['right'][1][:]
        self.faces['right'][1] = self.faces['back'][1][:]
        self.faces['back'][1] = self.faces['left'][1][:]
        self.faces['left'][1] = temp_row
    
    def rotate_left_vertical_clockwise(self):
        """Ruota la fascia verticale sinistra in senso orario (vista da sinistra)"""
        # 1. Ruota la faccia sinistra stessa
        self.faces['left'] = self.rotate_face_clockwise(self.faces['left'])
        
        # 2. Ruota le colonne sinistre delle facce adiacenti
        # Salva la colonna sinistra della faccia superiore
        temp_col = [self.faces['up'][i][0] for i in range(3)]
        
        # Sposta le colonne: up <- back <- down <- front <- up
        # Nota: la faccia back è vista da dietro, quindi le colonne sono invertite
        for i in range(3):
            self.faces['up'][i][0] = self.faces['front'][i][0]
            self.faces['front'][i][0] = self.faces['down'][i][0]
            self.faces['down'][i][0] = self.faces['back'][2-i][2]  # Colonna destra di back (invertita)
            self.faces['back'][2-i][2] = temp_col[i]
    
    def rotate_left_vertical_counter_clockwise(self):
        """Ruota la fascia verticale sinistra in senso antiorario (vista da sinistra)"""
        # 1. Ruota la faccia sinistra stessa
        self.faces['left'] = self.rotate_face_counter_clockwise(self.faces['left'])
        
        # 2. Ruota le colonne sinistre delle facce adiacenti
        # Salva la colonna sinistra della faccia superiore
        temp_col = [self.faces['up'][i][0] for i in range(3)]
        
        # Sposta le colonne: up <- back <- down <- front <- up (direzione opposta)
        for i in range(3):
            self.faces['up'][i][0] = self.faces['back'][2-i][2]  # Colonna destra di back (invertita)
            self.faces['back'][2-i][2] = self.faces['down'][i][0]
            self.faces['down'][i][0] = self.faces['front'][i][0]
            self.faces['front'][i][0] = temp_col[i]
    
    def rotate_center_vertical_clockwise(self):
        """Ruota la fascia verticale centrale in senso orario (vista da sinistra)"""
        # Salva la colonna centrale della faccia superiore
        temp_col = [self.faces['up'][i][1] for i in range(3)]
        
        # Sposta le colonne centrali: up <- front <- down <- back <- up
        for i in range(3):
            self.faces['up'][i][1] = self.faces['front'][i][1]
            self.faces['front'][i][1] = self.faces['down'][i][1]
            self.faces['down'][i][1] = self.faces['back'][2-i][1]  # Colonna centrale di back (invertita)
            self.faces['back'][2-i][1] = temp_col[i]
    
    def rotate_center_vertical_counter_clockwise(self):
        """Ruota la fascia verticale centrale in senso antiorario (vista da sinistra)"""
        # Salva la colonna centrale della faccia superiore
        temp_col = [self.faces['up'][i][1] for i in range(3)]
        
        # Sposta le colonne centrali: up <- back <- down <- front <- up (direzione opposta)
        for i in range(3):
            self.faces['up'][i][1] = self.faces['back'][2-i][1]  # Colonna centrale di back (invertita)
            self.faces['back'][2-i][1] = self.faces['down'][i][1]
            self.faces['down'][i][1] = self.faces['front'][i][1]
            self.faces['front'][i][1] = temp_col[i]
    
    def rotate_right_vertical_clockwise(self):
        """Ruota la fascia verticale destra in senso orario (vista da sinistra)"""
        # 1. Ruota la faccia destra stessa
        self.faces['right'] = self.rotate_face_clockwise(self.faces['right'])
        
        # 2. Ruota le colonne destre delle facce adiacenti
        # Salva la colonna destra della faccia superiore
        temp_col = [self.faces['up'][i][2] for i in range(3)]
        
        # Sposta le colonne: up <- front <- down <- back <- up
        for i in range(3):
            self.faces['up'][i][2] = self.faces['front'][i][2]
            self.faces['front'][i][2] = self.faces['down'][i][2]
            self.faces['down'][i][2] = self.faces['back'][2-i][0]  # Colonna sinistra di back (invertita)
            self.faces['back'][2-i][0] = temp_col[i]
    
    def rotate_right_vertical_counter_clockwise(self):
        """Ruota la fascia verticale destra in senso antiorario (vista da sinistra)"""
        # 1. Ruota la faccia destra stessa
        self.faces['right'] = self.rotate_face_counter_clockwise(self.faces['right'])
        
        # 2. Ruota le colonne destre delle facce adiacenti
        # Salva la colonna destra della faccia superiore
        temp_col = [self.faces['up'][i][2] for i in range(3)]
        
        # Sposta le colonne: up <- back <- down <- front <- up (direzione opposta)
        for i in range(3):
            self.faces['up'][i][2] = self.faces['back'][2-i][0]  # Colonna sinistra di back (invertita)
            self.faces['back'][2-i][0] = self.faces['down'][i][2]
            self.faces['down'][i][2] = self.faces['front'][i][2]
            self.faces['front'][i][2] = temp_col[i]
    
    def is_solved(self):
        """Controlla se il cubo è risolto (ogni faccia ha un colore uniforme)"""
        for face_name, face in self.faces.items():
            first_color = face[0][0]
            for row in face:
                for color in row:
                    if color != first_color:
                        return False
        return True
    
    def print_state(self):
        """Stampa lo stato corrente del cubo per debug"""
        print("\n=== STATO CUBO DI RUBIK ===")
        for face_name, face in self.faces.items():
            print(f"{face_name.upper()}:")
            for row in face:
                print(f"  {' '.join(row)}")
        print("=========================\n")
    
    def get_face_colors(self):
        """Restituisce i colori centrali di ogni faccia (per identificazione)"""
        return {
            face_name: face[1][1]  # Colore centrale
            for face_name, face in self.faces.items()
        }