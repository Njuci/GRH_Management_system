import tkinter as tk

class GRHManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('900x700')
        self.root.resizable(False, False)
        self.root.title('GRH Management')

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

        self.femme_button = tk.Button(self.options_frame, text="Barème salariale", bg=self.fontground, fg='white', command=lambda: self.indicate(self.femme_indicate))
        self.femme_button.place(x=10, y=100, width=150, height=40)
        self.femme_indicate = tk.Label(self.options_frame, text="", bg=self.fontground)
        self.femme_indicate.place(x=3, y=100, width=4, height=40)

        self.conge_button = tk.Button(self.options_frame, text="Congé", bg=self.fontground, fg='white', command=lambda: self.indicate(self.conge_indicate))
        self.conge_button.place(x=10, y=150, width=150, height=40)
        self.conge_indicate = tk.Label(self.options_frame, text="", bg=self.fontground)
        self.conge_indicate.place(x=3, y=150, width=4, height=40)

        self.salaire_button = tk.Button(self.options_frame, text="Paie", bg=self.fontground, fg='white', command=lambda: self.indicate(self.salaire_indicate))
        self.salaire_button.place(x=10, y=200, width=150, height=40)
        self.salaire_indicate = tk.Label(self.options_frame, text="", bg=self.fontground)
        self.salaire_indicate.place(x=3, y=200, width=4, height=40)

        self.demission_button = tk.Button(self.options_frame, text="Demission", bg=self.fontground, fg='white', command=lambda: self.indicate(self.demission_indicate))
        self.demission_button.place(x=10, y=250, width=150, height=40)
        self.demission_indicate = tk.Label(self.options_frame, text="", bg=self.fontground)
        self.demission_indicate.place(x=3, y=250, width=4, height=40)

        # Main Frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side=tk.LEFT)
        self.main_frame.pack_propagate(False)
        self.main_frame.configure(width=700, height=700)

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
# 
    # Méthode pour afficher le contenu du portail agent
    def show_agent_portal(self):
        # Effacer le contenu précédent dans main_frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Ajouter des widgets spécifiques pour le portail agent
        agent_label = tk.Label(self.main_frame, text="Portail de Gestion des Agents", font=('Helvetica', 18))
        agent_label.pack(pady=20)

        # Exemple de boutons supplémentaires dans le portail agent
        agent_info_button = tk.Button(self.main_frame, text="Voir les informations des agents", font=('Helvetica', 14))
        agent_info_button.pack(pady=10)

        agent_add_button = tk.Button(self.main_frame, text="Ajouter un nouvel agent", font=('Helvetica', 14))
        agent_add_button.pack(pady=10)

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = GRHManagementApp(root)
    root.mainloop()
