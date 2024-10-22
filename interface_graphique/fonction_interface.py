import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from backend.fonction_backend import Fonction
from backend.departement_backend import Departement

class FonctionGestFrontend:
    def __init__(self, parent_frame, curseur):
        self.parent_frame = parent_frame
        self.fonctions = []  # Liste pour stocker les fonctions localement
        self.departements = []  # Liste pour stocker les départements localement
        self.bg = '#FFFFFF'
        self.curseur = curseur
        self.succes_colors = '#27B795'
        self.bleck_color = '#000000'
        
        # Section des fonctions
        self.FonctionSection = tk.Frame(self.parent_frame, height=700, bg=self.bg, width=760, relief="groove")
        self.FonctionSection.place(x=10, y=20)
       
        # Formulaire de gestion des fonctions
        self.form = tk.Frame(self.FonctionSection, height=200, width=750, relief="groove", bg=self.bg)
        self.form.place(x=5, y=20)

        self.TitleForm = tk.Label(self.form, text='GESTION DES FONCTIONS', bg=self.bg, font='Arial 14', fg=self.bleck_color)
        self.TitleForm.place(x=250, y=20, height=30)

        # Champs du formulaire
        self.NomLab = tk.Label(self.form, text='Nom de la Fonction', bg='white', font='12')
        self.NomLab.place(x=60, y=70, height=30)
        self.NomEnt = tk.Entry(self.form, bg='lightblue', relief="flat", fg=self.bleck_color)
        self.NomEnt.place(x=220, y=70, width=200, height=30)

        self.DepartementLab = tk.Label(self.form, text='Département', bg='white', font='12')
        self.DepartementLab.place(x=60, y=110, height=30)
        self.DepartementCombo = ttk.Combobox(self.form, values=self.get_departements())
        self.DepartementCombo.place(x=220, y=110, width=200, height=30)

        # Boutons
        self.Ajouter_btn = tk.Button(self.FonctionSection, bg=self.succes_colors, text='AJOUTER', fg='white', relief="flat", font="Arial 9", command=self.ajouter_fonction)
        self.Ajouter_btn.place(x=200, y=180, width=100, height=30)

        self.Supprimer_btn = tk.Button(self.FonctionSection, bg='red', text='SUPPRIMER', fg='white', relief="flat", font="Arial 9", command=self.supprimer_fonction)
        self.Supprimer_btn.place(x=310, y=180, width=100, height=30)

        self.Modifier_btn = tk.Button(self.FonctionSection, bg='#4CAF50', text='MODIFIER', fg='white', relief="flat", font="Arial 9", command=self.modifier_fonction)
        self.Modifier_btn.place(x=420, y=180, width=100, height=30)

        self.Imprimer_btn = tk.Button(self.FonctionSection, bg='orange', text='IMPRIMER', fg='white', relief="flat", font="Arial 9", command=self.imprimer_fonction)
        self.Imprimer_btn.place(x=530, y=180, width=100, height=30)

        # Section du tableau
        self.TabSection = tk.Frame(self.FonctionSection, height=400, width=740, relief="groove")
        self.TabSection.place(x=0, y=220)

        # Ajout des barres de défilement
        self.scroll_x = ttk.Scrollbar(self.TabSection, orient=tk.HORIZONTAL)
        self.scroll_y = ttk.Scrollbar(self.TabSection, orient=tk.VERTICAL)

        # Tableau avec colonnes
        self.tableau = ttk.Treeview(self.TabSection, columns=('N°', 'ID', 'Nom de la Fonction', 'Département'), 
                                    show='headings', xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        # Configuration des colonnes du tableau
        self.tableau.heading('N°', text='N°')
        self.tableau.heading('ID', text='ID')
        self.tableau.heading('Nom de la Fonction', text='Nom de la Fonction')
        self.tableau.heading('Département', text='Département')

        self.tableau.column('N°', width=40, anchor='center')
        self.tableau.column('ID', width=100, anchor='center')
        self.tableau.column('Nom de la Fonction', width=200, anchor='center')
        self.tableau.column('Département', width=200, anchor='center')

        # Placement du tableau et des barres de défilement
        self.tableau.place(x=0, y=0, width=720, height=380)
        self.scroll_x.place(x=0, y=380, width=720)
        self.scroll_y.place(x=720, y=0, height=380)

        self.scroll_x.config(command=self.tableau.xview)
        self.scroll_y.config(command=self.tableau.yview)
        self.afficher()

    def get_departements(self):
        departement = Departement("")
        data = departement.get_all(self.curseur)
        self.departements = {row[1]: row[0] for row in data}  # Dictionnaire {nom: id}
        return list(self.departements.keys())

    def ajouter_fonction(self):
        # Récupérer les informations des champs
        nom_fonction = self.NomEnt.get()
        nom_departement = self.DepartementCombo.get()
        id_departement = self.departements.get(nom_departement)

        # Validation simple
        if not (nom_fonction and id_departement):
            showinfo('Erreur', 'Veuillez remplir tous les champs')
            return

        fonction = Fonction(nom_fonction, id_departement)
        if fonction.save(self.curseur):
            showinfo('Succès', 'Fonction ajoutée avec succès')
            self.afficher()
            self.clean()

    def clean(self):
        # Réinitialiser les champs
        self.NomEnt.delete(0, tk.END)
        self.DepartementCombo.set('')
        
    def afficher(self):
        fonction = Fonction("", "")
        data = fonction.get_all(self.curseur)
        
        self.tableau.delete(*self.tableau.get_children())
        cpt = 0

        for row in data:
            cpt += 1
            self.tableau.insert('', 'end', values=(cpt, row[0], row[1], row[2]))
        
        # Bind double click to get selected row data
        self.tableau.bind('<Double-Button-1>', self.get_selection)

    def get_selection(self, event):
        selected_item = self.tableau.selection()[0]
        values = self.tableau.item(selected_item, 'values')

        # Populate the form fields with the selected row's data
        self.NomEnt.delete(0, tk.END)
        self.NomEnt.insert(0, values[2])
        self.DepartementCombo.set(values[3])
   
    # Méthode pour avoir les informations des entry et returner les valeurs sous forme de liste
    def get_values(self):
        nom_fonction = self.NomEnt.get()
        nom_departement = self.DepartementCombo.get()
        id_departement = self.departements.get(nom_departement)
        return [nom_fonction, id_departement]
   
    # Méthode pour modifier une fonction
    def modifier_fonction(self):
        # Récupérer les informations des champs
        nom_fonction, id_departement = self.get_values()

        # Validation simple
        if not (nom_fonction and id_departement):
            showinfo('Erreur', 'Veuillez remplir tous les champs')
            return

        id = self.get_selected_fonction_id()
        if id is not None:
            fonction = Fonction(nom_fonction, id_departement)
            if fonction.update(self.curseur, id):
                showinfo('Succès', 'Fonction modifiée avec succès')

        # Afficher les fonctions
        self.afficher()
        self.clean()

    def get_selected_fonction_id(self):
        try:
            # Vérifie s'il y a une sélection
            selected_item = self.tableau.selection()
            
            if not selected_item:
                showinfo("Aucune sélection", "Veuillez sélectionner une ligne.")
                return None

            # Si une ligne est sélectionnée, récupérer l'ID de la fonction
            selected_item = selected_item[0]  # Prendre le premier élément sélectionné
            fonction_id = self.tableau.item(selected_item, 'values')[1]
            return fonction_id

        except IndexError:
            showinfo("Erreur", "La sélection est invalide.")
            return None

    def supprimer_fonction(self):
        id = self.get_selected_fonction_id()
        if id is not None:
            fonction = Fonction("", "")
            if fonction.delete(self.curseur, id):
                showinfo('Succès', 'Fonction supprimée avec succès')
                self.afficher()
                self.clean()

    # Méthode pour imprimer toutes les fonctions
    def imprimer_fonction(self):
        pass
