#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cubo di Rubik 3D - Applicazione Principale
Implementazione completa da zero con rotazione faccia superiore
"""

import tkinter as tk
from tkinter import ttk
from rubiks_cube_3d import RubiksCube3D

class RubiksCubeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cubo di Rubik 3D")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Inizializza il cubo 3D
        self.cube_3d = RubiksCube3D()
        
        # Stato dell'applicazione
        self.is_animating = False
        
        # Crea l'interfaccia utente
        self.create_interface()
        
        # Avvia il loop di aggiornamento
        self.update_loop()
    
    def create_interface(self):
        """Crea l'interfaccia utente"""
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titolo
        title_label = ttk.Label(main_frame, text="Cubo di Rubik 3D", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Sezione rotazioni faccia superiore
        rotation_up_frame = ttk.LabelFrame(main_frame, text="Rotazione Faccia Superiore", padding="10")
        rotation_up_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Pulsanti rotazione superiore
        self.btn_up_clockwise = ttk.Button(rotation_up_frame, text="Ruota Orario", 
                                          command=self.rotate_up_clockwise)
        self.btn_up_clockwise.grid(row=0, column=0, padx=(0, 10))
        
        self.btn_up_counter_clockwise = ttk.Button(rotation_up_frame, text="Ruota Antiorario", 
                                                  command=self.rotate_up_counter_clockwise)
        self.btn_up_counter_clockwise.grid(row=0, column=1)
        
        # Sezione rotazioni fascia centrale
        rotation_middle_frame = ttk.LabelFrame(main_frame, text="Rotazione Fascia Centrale", padding="10")
        rotation_middle_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Pulsanti rotazione centrale
        self.btn_middle_clockwise = ttk.Button(rotation_middle_frame, text="Ruota Orario", 
                                              command=self.rotate_middle_clockwise)
        self.btn_middle_clockwise.grid(row=0, column=0, padx=(0, 10))
        
        self.btn_middle_counter_clockwise = ttk.Button(rotation_middle_frame, text="Ruota Antiorario", 
                                                      command=self.rotate_middle_counter_clockwise)
        self.btn_middle_counter_clockwise.grid(row=0, column=1)
        
        # Sezione rotazioni faccia inferiore
        rotation_down_frame = ttk.LabelFrame(main_frame, text="Rotazione Faccia Inferiore", padding="10")
        rotation_down_frame.grid(row=3, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Pulsanti rotazione inferiore
        self.btn_down_clockwise = ttk.Button(rotation_down_frame, text="Ruota Orario", 
                                            command=self.rotate_down_clockwise)
        self.btn_down_clockwise.grid(row=0, column=0, padx=(0, 10))
        
        self.btn_down_counter_clockwise = ttk.Button(rotation_down_frame, text="Ruota Antiorario", 
                                                    command=self.rotate_down_counter_clockwise)
        self.btn_down_counter_clockwise.grid(row=0, column=1)
        
        # Sezione rotazione verticale sinistra
        rotation_left_vertical_frame = ttk.LabelFrame(main_frame, text="Rotazione Verticale Sinistra", padding="10")
        rotation_left_vertical_frame.grid(row=4, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Pulsanti rotazione verticale sinistra
        self.btn_left_vertical_clockwise = ttk.Button(rotation_left_vertical_frame, text="Ruota Orario", 
                                                     command=self.rotate_left_vertical_clockwise)
        self.btn_left_vertical_clockwise.grid(row=0, column=0, padx=(0, 10))
        
        self.btn_left_vertical_counter_clockwise = ttk.Button(rotation_left_vertical_frame, text="Ruota Antiorario", 
                                                             command=self.rotate_left_vertical_counter_clockwise)
        self.btn_left_vertical_counter_clockwise.grid(row=0, column=1)
        
        # Sezione controlli
        control_frame = ttk.LabelFrame(main_frame, text="Controlli", padding="10")
        control_frame.grid(row=5, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Pulsante reset
        self.btn_reset = ttk.Button(control_frame, text="Reset Cubo", 
                                   command=self.reset_cube)
        self.btn_reset.grid(row=0, column=0, padx=(0, 10))
        
        # Pulsante chiudi
        self.btn_close = ttk.Button(control_frame, text="Chiudi", 
                                   command=self.close_app)
        self.btn_close.grid(row=0, column=1)
        
        # Label di stato
        self.status_label = ttk.Label(main_frame, text="Pronto", 
                                     foreground="green", font=('Arial', 10))
        self.status_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))
    
    def rotate_up_clockwise(self):
        """Ruota la faccia superiore in senso orario"""
        if self.is_animating:
            return
        
        self.set_animating(True)
        self.status_label.config(text="Rotazione superiore oraria in corso...", foreground="orange")
        self.cube_3d.rotate_face('up', 'clockwise', self.on_rotation_complete)
    
    def rotate_up_counter_clockwise(self):
        """Ruota la faccia superiore in senso antiorario"""
        if self.is_animating:
            return
        
        self.set_animating(True)
        self.status_label.config(text="Rotazione superiore antioraria in corso...", foreground="orange")
        self.cube_3d.rotate_face('up', 'counter-clockwise', self.on_rotation_complete)
    
    def rotate_down_clockwise(self):
        """Ruota la faccia inferiore in senso orario"""
        if self.is_animating:
            return
        
        self.set_animating(True)
        self.status_label.config(text="Rotazione inferiore oraria in corso...", foreground="orange")
        self.cube_3d.rotate_face('down', 'clockwise', self.on_rotation_complete)
    
    def rotate_down_counter_clockwise(self):
        """Ruota la faccia inferiore in senso antiorario"""
        if self.is_animating:
            return
        
        self.set_animating(True)
        self.status_label.config(text="Rotazione inferiore antioraria in corso...", foreground="orange")
        self.cube_3d.rotate_face('down', 'counter-clockwise', self.on_rotation_complete)
    
    def rotate_middle_clockwise(self):
        """Ruota la fascia centrale in senso orario"""
        if self.is_animating:
            return
        
        self.set_animating(True)
        self.status_label.config(text="Rotazione centrale oraria in corso...", foreground="orange")
        self.cube_3d.rotate_face('middle', 'clockwise', self.on_rotation_complete)
    
    def rotate_middle_counter_clockwise(self):
        """Ruota la fascia centrale in senso antiorario"""
        if self.is_animating:
            return
        
        self.set_animating(True)
        self.status_label.config(text="Rotazione centrale antioraria in corso...", foreground="orange")
        self.cube_3d.rotate_face('middle', 'counter-clockwise', self.on_rotation_complete)
    
    def rotate_left_vertical_clockwise(self):
        """Ruota la fascia verticale sinistra in senso orario"""
        if self.is_animating:
            return
        
        self.set_animating(True)
        self.status_label.config(text="Rotazione verticale sinistra oraria in corso...", foreground="orange")
        self.cube_3d.rotate_face('left_vertical', 'clockwise', self.on_rotation_complete)
    
    def rotate_left_vertical_counter_clockwise(self):
        """Ruota la fascia verticale sinistra in senso antiorario"""
        if self.is_animating:
            return
        
        self.set_animating(True)
        self.status_label.config(text="Rotazione verticale sinistra antioraria in corso...", foreground="orange")
        self.cube_3d.rotate_face('left_vertical', 'counter-clockwise', self.on_rotation_complete)
    
    def reset_cube(self):
        """Resetta il cubo allo stato iniziale"""
        if self.is_animating:
            return
        
        self.cube_3d.reset()
        self.status_label.config(text="Cubo resettato", foreground="blue")
        self.root.after(2000, lambda: self.status_label.config(text="Pronto", foreground="green"))
    
    def close_app(self):
        """Chiude l'applicazione"""
        self.root.quit()
        self.root.destroy()
    
    def on_rotation_complete(self):
        """Callback chiamato al completamento di una rotazione"""
        self.set_animating(False)
        self.status_label.config(text="Rotazione completata", foreground="blue")
        self.root.after(2000, lambda: self.status_label.config(text="Pronto", foreground="green"))
    
    def set_animating(self, animating):
        """Imposta lo stato di animazione e abilita/disabilita i pulsanti"""
        self.is_animating = animating
        state = 'disabled' if animating else 'normal'
        
        self.btn_up_clockwise.config(state=state)
        self.btn_up_counter_clockwise.config(state=state)
        self.btn_middle_clockwise.config(state=state)
        self.btn_middle_counter_clockwise.config(state=state)
        self.btn_down_clockwise.config(state=state)
        self.btn_down_counter_clockwise.config(state=state)
        self.btn_reset.config(state=state)
    
    def update_loop(self):
        """Loop di aggiornamento dell'applicazione"""
        # Aggiorna il cubo 3D
        if hasattr(self.cube_3d, 'update'):
            self.cube_3d.update()
        
        # Programma il prossimo aggiornamento
        self.root.after(16, self.update_loop)  # ~60 FPS

def main():
    """Funzione principale"""
    root = tk.Tk()
    app = RubiksCubeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

