import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from datetime import datetime
from interface_graphique.agent_front import AgentGestFrontend
from backend.connexion import Connexion
class GRHManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1000x700')
        #self.root.resizable(False, False)
        self.root.title('GRH Management')
        self.conexion=Connexion()

        # Couleurs
        self.fontground = '#27B795'
        self.bg = '#FFFFFF'

        # Créer les frames et les widgets
        self.create_widgets()

        # Sélectionner l'option "Agent" par défaut
        self.indicate(self.hom_indicate)
        self.show_agent_portal()  # Afficher le portail agent par défaut

    def create_widgets(self):
        # Frame des options
        self.options_frame = tk.Frame(self.root, bg=self.bg)
        self.options_frame.pack(side=tk.LEFT)
        self.options_frame.pack_propagate(False)
        self.options_frame.configure(width=200, height=700)

        # Boutons et indicateurs pour chaque option
        self.hom_button = tk.Button(self.options_frame, text="Agent", bg=self.fontground, fg='white', command=lambda: self.on_option_selected(self.hom_indicate, self.show_agent_portal))
        self.hom_button.place(x=10, y=50, width=150, height=40)
        self.hom_indicate = tk.Label(self.options_frame, text="", bg=self.fontground)
        self.hom_indicate.place(x=3, y=50, width=4, height=40)

        self.femme_button = tk.Button(self.options_frame, text="Barème salariale", bg=self.fontground, fg='white', command=lambda: self.on_option_selected(self.femme_indicate, self.show_bareme_salariale_portal))
        self.femme_button.place(x=10, y=100, width=150, height=40)
        self.femme_indicate = tk.Label(self.options_frame, text="", bg=self.fontground)
        self.femme_indicate.place(x=3, y=100, width=4, height=40)

        self.conge_button = tk.Button(self.options_frame, text="Congé", bg=self.fontground, fg='white', command=lambda: self.on_option_selected(self.conge_indicate, self.show_conge_portal))
        self.conge_button.place(x=10, y=150, width=150, height=40)
        self.conge_indicate = tk.Label(self.options_frame, text="", bg=self.fontground)
        self.conge_indicate.place(x=3, y=150, width=4, height=40)

        self.salaire_button = tk.Button(self.options_frame, text="Paie", bg=self.fontground, fg='white', command=lambda: self.on_option_selected(self.salaire_indicate, self.show_paie_portal))
        self.salaire_button.place(x=10, y=200, width=150, height=40)
        self.salaire_indicate = tk.Label(self.options_frame, text="", bg=self.fontground)
        self.salaire_indicate.place(x=3, y=200, width=4, height=40)

        self.demission_button = tk.Button(self.options_frame, text="Démission", bg=self.fontground, fg='white', command=lambda: self.on_option_selected(self.demission_indicate, self.show_demission_portal))
        self.demission_button.place(x=10, y=250, width=150, height=40)
        self.demission_indicate = tk.Label(self.options_frame, text="", bg=self.fontground)
        self.demission_indicate.place(x=3, y=250, width=4, height=40)

        # Main Frame
        self.main_frame = tk.Frame(self.root, bg=self.bg)
        self.main_frame.pack(side=tk.LEFT)
        self.main_frame.pack_propagate(False)
        self.main_frame.configure(width=800, height=700)

    # Masquer tous les indicateurs
    def hide_all(self):
        self.hom_indicate.config(bg=self.bg)
        self.femme_indicate.config(bg=self.bg)
        self.conge_indicate.config(bg=self.bg)
        self.salaire_indicate.config(bg=self.bg)
        self.demission_indicate.config(bg=self.bg)

    # Indiquer l'option sélectionnée et appeler la fonction correspondante
    def on_option_selected(self, label, show_portal_func):
        self.indicate(label)
        show_portal_func()

    # Indiquer l'option sélectionnée
    def indicate(self, label):
        self.hide_all()
        label.config(bg=self.fontground)

    # Méthode pour afficher le contenu du portail agent
    def show_agent_portal(self):
        self.clear_main_frame()
        AgentGestFrontend(self.main_frame,self.conexion.get_curseur())
        
    # Méthode pour afficher le contenu du portail Barème salariale
    def show_bareme_salariale_portal(self):
        self.clear_main_frame()
        bareme_label = tk.Label(self.main_frame, text="Portail de Barème Salariale", font=('Helvetica', 18))
        bareme_label.pack(pady=20)

    # Méthode pour afficher le contenu du portail Congé
    def show_conge_portal(self):
        self.clear_main_frame()
        conge_label = tk.Label(self.main_frame, text="Portail de Congé", font=('Helvetica', 18))
        conge_label.pack(pady=20)

    # Méthode pour afficher le contenu du portail Paie
    def show_paie_portal(self):
        self.clear_main_frame()
        paie_label = tk.Label(self.main_frame, text="Portail de Paie", font=('Helvetica', 18))
        paie_label.pack(pady=20)

    # Méthode pour afficher le contenu du portail Démission
    def show_demission_portal(self):
        self.clear_main_frame()
        demission_label = tk.Label(self.main_frame, text="Portail de Démission", font=('Helvetica', 18))
        demission_label.pack(pady=20)

    # Méthode pour effacer le contenu précédent dans main_frame
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = GRHManagementApp(root)
    root.mainloop()



