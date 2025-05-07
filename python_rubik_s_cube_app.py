# Diamo vita al nostro artificio come il sapiente alchimista che raccoglie gli ingredienti per la Grande Opera
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from rubiks_cube_model import RubiksCube
from rubiks_cube_3d import RubiksCube3D

# La classe principale, come la corte di un nobile signore che governa il reame dell'applicazione
class RubiksCubeGUI:
    # Come l'architetto che pone la prima pietra di una cattedrale
    def __init__(self, root):
        # La radice, come il tronco da cui si diramano tutti i rami dell'albero
        self.root = root
        # Le dimensioni della finestra, come le proporzioni del tempio di Salomone
        self.root.geometry("600x250")
        # Il titolo, come l'iscrizione sul frontone della porta infernale scardinata descritta dal sommo poeta
        self.root.title("3D Rubik's Cube Solver")
        # Il colore di sfondo, come il cielo sereno che accoglie l'opera
        self.root.configure(bg='#f0f0f0')
        # Prepariamo l'aspetto, come il sarto che cuce le vesti per una cerimonia e che strizza l'occhio per meglio vedere la cruna dell'ago o come le Parche, o Moire, che personificano il destino, gestendo il filo della vita di ciascuno di noi
        self.setup_theme()
        # Creiamo l'interfaccia, come il mastro vetraio che compone una vetrata
        self.create_interface()
        # Il cubo tridimensionale, come l'anima che dà vita al corpo
        self.cube_3d = RubiksCube3D(root)

    # Come l'artista Francesco Guardi che sceglie i colori per il suo affresco
    def setup_theme(self):
        # Tentiamo di applicare uno stile elegante, come chi cerca stoffe pregiate
        try:
            # Lo stile, come la livrea che distingue i nobili dai plebei
            self.style = ThemedStyle(self.root)
            # Impostiamo il tema, come il tono di una composizione musicale
            self.style.set_theme("clam")
        # Se fallisce, ripieghiamo su una soluzione più semplice, come il viandante che trova riparo in una capanna
        except Exception:
            self.style = ttk.Style(self.root)
        # Configuriamo i bottoni, come il sarto che adorna gli abiti con ricami e bordure
        self.style.configure('Custom.TButton', padding=(10, 5), font=('Segoe UI', 10))
        # Configuriamo le etichette, come lo scriba che sceglie la pergamena e l'inchiostro
        self.style.configure('Custom.TLabel', background='#f0f0f0', foreground='black', font=('Segoe UI', 10))

    # Come il mastro costruttore che erige le mura e dispone le stanze del palazzo
    def create_interface(self):
        # Il telaio principale, come le fondamenta su cui poggia l'intero edificio
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        # Il telaio dei controlli, come la sala del trono dove si prendono le decisioni
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(expand=True, fill='both', pady=5)
        # Il bottone di reset, come la fontana che purifica e rinnova
        self.reset_button = ttk.Button(controls_frame, text="Reset", style='Custom.TButton', command=self.reset_cube)
        self.reset_button.pack(side='left', padx=5)
        # Il bottone di chiusura, come il portale che segna il confine tra il dentro e il fuori
        self.close_button = ttk.Button(controls_frame, text="Chiudi", style='Custom.TButton', command=self.close_program)
        self.close_button.pack(side='left', padx=5)

    # Come il tramonto che pone fine al giorno
    def close_program(self):
        # Distruggiamo la finestra, come il tempo che tutto consuma, ovvero come Crono che divora i suoi figli
        self.root.destroy()

    # Come il diluvio che purifica il mondo per ricominciare da capo, dopo la comparsa di un arcobaleno, simbolo del patto di pacificazione stabilito tra Dio e i credenti
    def reset_cube(self):
        # Disabilitiamo i pulsanti di comando, come il saggio che impone il silenzio prima di un rito
        self.disable_all_buttons()
        # Resettiamo il cubo, come il ritorno all'età dell'oro
        self.cube_3d.reset_cube()
        # Dopo un breve tempo, come la paziente attesa del contadino che, appoggiato alla sua zappa, ammira il campo costellato di lucciole all'imbrunire
        self.root.after(50, self.enable_buttons)

    # Come il signore che vieta l'accesso al castello durante un assedio
    def disable_all_buttons(self):
        # Disabilitiamo il pulsante di comando di reset, come una porta sbarrata
        self.reset_button.config(state=tk.DISABLED)
        # Disabilitiamo il pulsante di comando di chiusura, come un ponte levatoio sollevato
        self.close_button.config(state=tk.DISABLED)

    # Come il signore che riapre le porte del castello dopo che il pericolo è passato
    def enable_buttons(self):
        # Riabilitiamo il pulsante di comando di reset, come una porta che si schiude, come gli occhi pesanti di morte di Piramo che si schiusero quando riapparve Tisbe al suo cospetto
        self.reset_button.config(state=tk.NORMAL)
        # Riabilitiamo il pulsante di comando di chiusura, come un ponte levatoio che si abbassa
        self.close_button.config(state=tk.NORMAL)

# Come il rito che dà inizio alla cerimonia
if __name__ == "__main__":
    # Creiamo la radice, come il seme da cui germoglierà l'albero
    root = tk.Tk()
    # Creiamo l'applicazione, come l'anima che dà vita al corpo dopo essere stata soffiata direttamente da Dio
    app = RubiksCubeGUI(root)
    # Avviamo il ciclo principale, come il tempo che scorre eternamente
    root.mainloop()

