import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from datetime import datetime
from interface_graphique.departement_front import DepartementGestFrontend
from interface_graphique.agent_front import AgentGestFrontend
from interface_graphique.bareme_interrfaxe import BaremeSalarialeGestFrontend
from interface_graphique.fonction_interface import FonctionGestFrontend
from interface_graphique.affectation_interface import AffectationGestFrontend
from backend.connexion import Connexion

class GRHManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1000x700')
        self.root.title('GRH Management')
        self.conexion = Connexion()
        
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
        self.hom_indicate = tk.Label(self.options_frame, text="", bg=self.bg)
        self.hom_indicate.place(x=3, y=50, width=4, height=40)

        self.bareme_button = tk.Button(self.options_frame, text="Barème Salarial", bg=self.fontground, fg='white', command=lambda: self.on_option_selected(self.bareme_indicate, self.show_bareme_salariale_portal))
        self.bareme_button.place(x=10, y=100, width=150, height=40)
        self.bareme_indicate = tk.Label(self.options_frame, text="", bg=self.bg)
        self.bareme_indicate.place(x=3, y=100, width=4, height=40)

        self.paie_button = tk.Button(self.options_frame, text="Paie", bg=self.fontground, fg='white', command=lambda: self.on_option_selected(self.paie_indicate, self.show_paie_portal))
        self.paie_button.place(x=10, y=150, width=150, height=40)
        self.paie_indicate = tk.Label(self.options_frame, text="", bg=self.bg)
        self.paie_indicate.place(x=3, y=150, width=4, height=40)

        # Ajout des nouvelles options pour les tables
        self.affecter_button = tk.Button(self.options_frame, text="Affecter", bg=self.fontground, fg='white', command=lambda: self.on_option_selected(self.affecter_indicate, self.show_affecter_portal))
        self.affecter_button.place(x=10, y=200, width=150, height=40)
        self.affecter_indicate = tk.Label(self.options_frame, text="", bg=self.bg)
        self.affecter_indicate.place(x=3, y=200, width=4, height=40)

        self.pointer_button = tk.Button(self.options_frame, text="Pointer", bg=self.fontground, fg='white', command=lambda: self.on_option_selected(self.pointer_indicate, self.show_pointer_portal))
        self.pointer_button.place(x=10, y=250, width=150, height=40)
        self.pointer_indicate = tk.Label(self.options_frame, text="", bg=self.bg)
        self.pointer_indicate.place(x=3, y=250, width=4, height=40)

        self.performance_button = tk.Button(self.options_frame, text="Performance", bg=self.fontground, fg='white', command=lambda: self.on_option_selected(self.performance_indicate, self.show_performance_portal))
        self.performance_button.place(x=10, y=300, width=150, height=40)
        self.performance_indicate = tk.Label(self.options_frame, text="", bg=self.bg)
        self.performance_indicate.place(x=3, y=300, width=4, height=40)

        self.grh_button = tk.Button(self.options_frame, text="GRH", bg=self.fontground, fg='white', command=lambda: self.on_option_selected(self.grh_indicate, self.show_grh_portal))
        self.grh_button.place(x=10, y=350, width=150, height=40)
        self.grh_indicate = tk.Label(self.options_frame, text="", bg=self.bg)
        self.grh_indicate.place(x=3, y=350, width=4, height=40)

        # Ajout des nouvelles options pour Département et Fonction
        self.departement_button = tk.Button(self.options_frame, text="Département", bg=self.fontground, fg='white', command=lambda: self.on_option_selected(self.departement_indicate, self.show_departement_portal))
        self.departement_button.place(x=10, y=400, width=150, height=40)
        self.departement_indicate = tk.Label(self.options_frame, text="", bg=self.bg)
        self.departement_indicate.place(x=3, y=400, width=4, height=40)

        self.fonction_button = tk.Button(self.options_frame, text="Fonction", bg=self.fontground, fg='white', command=lambda: self.on_option_selected(self.fonction_indicate, self.show_fonction_portal))
        self.fonction_button.place(x=10, y=450, width=150, height=40)
        self.fonction_indicate = tk.Label(self.options_frame, text="", bg=self.bg)
        self.fonction_indicate.place(x=3, y=450, width=4, height=40)

        # Main Frame
        self.main_frame = tk.Frame(self.root, bg=self.bg)
        self.main_frame.pack(side=tk.LEFT)
        self.main_frame.pack_propagate(False)
        self.main_frame.configure(width=800, height=700)

    # Masquer tous les indicateurs
    def hide_all(self):
        self.hom_indicate.config(bg=self.bg)
        self.bareme_indicate.config(bg=self.bg)
        self.paie_indicate.config(bg=self.bg)
        self.affecter_indicate.config(bg=self.bg)
        self.pointer_indicate.config(bg=self.bg)
        self.performance_indicate.config(bg=self.bg)
        self.grh_indicate.config(bg=self.bg)
        self.departement_indicate.config(bg=self.bg)
        self.fonction_indicate.config(bg=self.bg)

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
        AgentGestFrontend(self.main_frame, self.conexion.get_curseur())
        
    # Méthode pour afficher le contenu du portail Barème salarial
    def show_bareme_salariale_portal(self):
        self.clear_main_frame()
        BaremeSalarialeGestFrontend(self.main_frame, self.conexion.get_curseur())
    # Méthode pour afficher le contenu du portail Paie
    def show_paie_portal(self):
        self.clear_main_frame()
        paie_label = tk.Label(self.main_frame, text="Portail de Paie", font=('Helvetica', 18))
        paie_label.pack(pady=20)

    # Méthode pour afficher le contenu du portail Affecter
    def show_affecter_portal(self):
        self.clear_main_frame()
        AffectationGestFrontend(self.main_frame,self.conexion.get_curseur())
    # Méthode pour afficher le contenu du portail Pointer
    def show_pointer_portal(self):
        self.clear_main_frame()
        pointer_label = tk.Label(self.main_frame, text="Portail de Pointer", font=('Helvetica', 18))
        pointer_label.pack(pady=20)

    # Méthode pour afficher le contenu du portail Performance
    def show_performance_portal(self):
        self.clear_main_frame()
        performance_label = tk.Label(self.main_frame, text="Portail de Performance", font=('Helvetica', 18))
        performance_label.pack(pady=20)

    # Méthode pour afficher le contenu du portail GRH
    def show_grh_portal(self):
        self.clear_main_frame()
        grh_label = tk.Label(self.main_frame, text="Portail de GRH", font=('Helvetica', 18))
        grh_label.pack(pady=20)

    # Méthode pour afficher le contenu du portail Département
    def show_departement_portal(self):
        self.clear_main_frame()
        DepartementGestFrontend(self.main_frame,self.conexion.get_curseur())
    # Méthode pour afficher le contenu du portail Fonction
    def show_fonction_portal(self):
        self.clear_main_frame()
        FonctionGestFrontend(self.main_frame,self.conexion.get_curseur())

    # Méthode pour effacer le contenu précédent dans main_frame
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = GRHManagementApp(root)
    root.mainloop()
