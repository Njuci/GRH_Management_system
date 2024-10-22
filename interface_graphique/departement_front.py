import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from backend.departement_backend import Departement

class DepartementGestFrontend:
    def __init__(self, parent_frame, curseur):
        self.parent_frame = parent_frame
        self.departements = []  # Liste pour stocker les départements localement
        self.bg = '#FFFFFF'
        self.curseur = curseur
        self.succes_colors = '#27B795'
        self.bleck_color = '#000000'
        
        # Section des départements
        self.DepartementSection = tk.Frame(self.parent_frame, height=700, bg=self.bg, width=760, relief="groove")
        self.DepartementSection.place(x=10, y=20)
       
        # Formulaire de gestion des départements
        self.form = tk.Frame(self.DepartementSection, height=200, width=750, relief="groove", bg=self.bg)
        self.form.place(x=5, y=20)

        self.TitleForm = tk.Label(self.form, text='GESTION DES DEPARTEMENTS', bg=self.bg, font='Arial 14', fg=self.bleck_color)
        self.TitleForm.place(x=250, y=20, height=30)

        # Champs du formulaire
        self.NomLab = tk.Label(self.form, text='Nom du Département', bg='white', font='12')
        self.NomLab.place(x=60, y=70, height=30)
        self.NomEnt = tk.Entry(self.form, bg='lightblue', relief="flat", fg=self.bleck_color)
        self.NomEnt.place(x=220, y=70, width=200, height=30)

        # Boutons
        self.Ajouter_btn = tk.Button(self.DepartementSection, bg=self.succes_colors, text='AJOUTER', fg='white', relief="flat", font="Arial 9", command=self.ajouter_departement)
        self.Ajouter_btn.place(x=200, y=150, width=100, height=30)

        self.Supprimer_btn = tk.Button(self.DepartementSection, bg='red', text='SUPPRIMER', fg='white', relief="flat", font="Arial 9", command=self.supprimer_departement)
        self.Supprimer_btn.place(x=310, y=150, width=100, height=30)

        self.Modifier_btn = tk.Button(self.DepartementSection, bg='#4CAF50', text='MODIFIER', fg='white', relief="flat", font="Arial 9", command=self.modifier_departement)
        self.Modifier_btn.place(x=420, y=150, width=100, height=30)

        self.Imprimer_btn = tk.Button(self.DepartementSection, bg='orange', text='IMPRIMER', fg='white', relief="flat", font="Arial 9", command=self.imprimer_departement)
        self.Imprimer_btn.place(x=530, y=150, width=100, height=30)

        # Section du tableau
        self.TabSection = tk.Frame(self.DepartementSection, height=400, width=740, relief="groove")
        self.TabSection.place(x=0, y=200)

        # Ajout des barres de défilement
        self.scroll_x = ttk.Scrollbar(self.TabSection, orient=tk.HORIZONTAL)
        self.scroll_y = ttk.Scrollbar(self.TabSection, orient=tk.VERTICAL)

        # Tableau avec colonnes
        self.tableau = ttk.Treeview(self.TabSection, columns=('N°', 'ID', 'Nom du Département'), 
                                    show='headings', xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        # Configuration des colonnes du tableau
        self.tableau.heading('N°', text='N°')
        self.tableau.heading('ID', text='ID')
        self.tableau.heading('Nom du Département', text='Nom du Département')

        self.tableau.column('N°', width=40, anchor='center')
        self.tableau.column('ID', width=100, anchor='center')
        self.tableau.column('Nom du Département', width=200, anchor='center')

        # Placement du tableau et des barres de défilement
        self.tableau.place(x=0, y=0, width=720, height=380)
        self.scroll_x.place(x=0, y=380, width=720)
        self.scroll_y.place(x=720, y=0, height=380)

        self.scroll_x.config(command=self.tableau.xview)
        self.scroll_y.config(command=self.tableau.yview)
        self.afficher()

    def ajouter_departement(self):
        # Récupérer les informations des champs
        nom_depart = self.NomEnt.get()

        # Validation simple
        if not nom_depart:
            showinfo('Erreur', 'Veuillez remplir tous les champs')
            return

        departement = Departement(nom_depart)
        if departement.save(self.curseur):
            showinfo('Succès', 'Département ajouté avec succès')
            self.afficher()
            self.clean()

    def clean(self):
        # Réinitialiser les champs
        self.NomEnt.delete(0, tk.END)
        
    def afficher(self):
        departement = Departement("")
        data = departement.get_all(self.curseur)
        
        self.tableau.delete(*self.tableau.get_children())
        cpt = 0

        for row in data:
            cpt += 1
            self.tableau.insert('', 'end', values=(cpt, row[0], row[1]))
        
        # Bind double click to get selected row data
        self.tableau.bind('<Double-Button-1>', self.get_selection)

    def get_selection(self, event):
        selected_item = self.tableau.selection()[0]
        values = self.tableau.item(selected_item, 'values')

        # Populate the form fields with the selected row's data
        self.NomEnt.delete(0, tk.END)
        self.NomEnt.insert(0, values[2])
   
    # Méthode pour avoir les informations des entry et returner les valeurs sous forme de liste
    def get_values(self):
        nom_depart = self.NomEnt.get()
        return [nom_depart]
   
    # Méthode pour modifier un département
    def modifier_departement(self):
        # Récupérer les informations des champs
        nom_depart = self.get_values()[0]

        # Validation simple
        if not nom_depart:
            showinfo('Erreur', 'Veuillez remplir tous les champs')
            return

        id = self.get_selected_departement_id()
        if id is not None:
            departement = Departement(nom_depart)
            if departement.update(self.curseur, id):
                showinfo('Succès', 'Département modifié avec succès')

        # Afficher les départements
        self.afficher()
        self.clean()

    def get_selected_departement_id(self):
        try:
            # Vérifie s'il y a une sélection
            selected_item = self.tableau.selection()
            
            if not selected_item:
                showinfo("Aucune sélection", "Veuillez sélectionner une ligne.")
                return None

            # Si une ligne est sélectionnée, récupérer l'ID du département
            selected_item = selected_item[0]  # Prendre le premier élément sélectionné
            departement_id = self.tableau.item(selected_item, 'values')[1]
            return departement_id

        except IndexError:
            showinfo("Erreur", "La sélection est invalide.")
            return None

    def supprimer_departement(self):
        id = self.get_selected_departement_id()
        if id is not None:
            departement = Departement("")
            if departement.delete(self.curseur, id):
                showinfo('Succès', 'Département supprimé avec succès')
                self.afficher()
                self.clean()

    # Méthode pour imprimer tous les départements
    def imprimer_departement(self):
        pass

# Exemple d'utilisation
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestion des Départements")
    root.geometry("800x800")
    
    # Connexion à la base de données
    import mysql.connector
    conn = mysql.connector.connect(user='votre_utilisateur', password='votre_mot_de_passe', host='localhost', database='votre_base_de_donnees')
    curseur = conn.cursor()

    app = DepartementGestFrontend(root, curseur)
    root.mainloop()

    # Fermeture de la connexion
    curseur.close()
    conn.close()